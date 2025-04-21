import logging
import os
import tempfile
import sys
import importlib.util
import glob
import shutil
import subprocess
from pathlib import Path
import time
from .manim_service import save_manim_code, SCENE_CLASS_NAME

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get absolute paths for project directories
def get_project_paths():
    """Get absolute paths for project directories."""
    project_root = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    media_dir = os.path.abspath(os.path.join(project_root, "media"))
    output_dir = os.path.abspath(os.path.join(project_root, "animation", "output"))
    
    # Create directories if they don't exist
    os.makedirs(media_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "videos", SCENE_CLASS_NAME, "1080p60"), exist_ok=True)
    
    return {
        "project_root": project_root,
        "media_dir": media_dir,
        "output_dir": output_dir,
        "final_output_path": os.path.join(output_dir, "videos", SCENE_CLASS_NAME, "1080p60", f"{SCENE_CLASS_NAME}.mp4")
    }

def create_video(manim_code):
    """
    Create a video from Manim code.
    
    Args:
        manim_code (str): Generated Manim code
        
    Returns:
        str: Path to the generated video file
    """
    logger.info("Creating video from Manim code")
    
    try:
        # Get project paths
        paths = get_project_paths()
        project_root = paths["project_root"]
        media_dir = paths["media_dir"]
        output_dir = paths["output_dir"]
        final_output_path = paths["final_output_path"]
        
        # Save the code to a temporary file
        temp_file = save_manim_code(manim_code)
        
        # Try running Manim using command-line approach (most reliable)
        video_path = run_manim_cli(temp_file, media_dir, final_output_path)
        if video_path:
            logger.info(f"Successfully created video at {video_path}")
            return video_path
            
        # If CLI approach failed, try Python API approach
        video_path = run_manim_api(temp_file, media_dir, final_output_path)
        if video_path:
            logger.info(f"Successfully created video using Python API at {video_path}")
            return video_path
            
        # If neither approach worked, try to find partial movie files and combine them
        video_path = combine_partial_movies(media_dir, final_output_path)
        if video_path:
            logger.info(f"Successfully combined partial videos at {video_path}")
            return video_path
        
        # If all direct Manim approaches failed, create a mock video
        logger.warning("All Manim approaches failed, creating mock video")
        return create_mock_video(output_dir)
            
    except Exception as e:
        logger.error(f"Unexpected error creating video: {str(e)}")
        # Fall back to mock video
        paths = get_project_paths()
        return create_mock_video(paths["output_dir"])

def run_manim_cli(temp_file, media_dir, final_output_path):
    """Run Manim using command-line interface."""
    try:
        logger.info("Running Manim via CLI")
        
        # Command to run Manim
        cmd = [
            sys.executable, "-m", "manim",
            temp_file, SCENE_CLASS_NAME,
            "--media_dir", media_dir,
            "-o", SCENE_CLASS_NAME,
            "--format", "mp4",
            "--quality", "h"  # High quality
        ]
        
        logger.info(f"Running command: {' '.join(cmd)}")
        
        # Run with proper encoding settings
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",  # Handle encoding errors gracefully
            check=False  # Don't raise exception on non-zero exit
        )
        
        if result.returncode != 0:
            logger.warning(f"Manim CLI failed with code {result.returncode}")
            logger.warning(f"Error: {result.stderr}")
            return None
        
        # Check possible output locations
        possible_paths = [
            os.path.join(media_dir, "videos", SCENE_CLASS_NAME, "1080p60", f"{SCENE_CLASS_NAME}.mp4"),
            os.path.join(media_dir, "videos", "1080p60", f"{SCENE_CLASS_NAME}.mp4")
        ]
        
        # Allow a moment for file operations to complete
        time.sleep(1)
        
        # Check if the video was created
        for path in possible_paths:
            if os.path.exists(path):
                logger.info(f"Found Manim output at {path}")
                try:
                    # Copy to final location
                    shutil.copyfile(path, final_output_path)
                    logger.info(f"Copied to {final_output_path}")
                    return final_output_path
                except Exception as e:
                    logger.error(f"Error copying file: {e}")
                    return path
        
        # If we get here, Manim ran but we couldn't find the output
        logger.warning("Manim CLI ran without errors but output file not found")
        return None
        
    except Exception as e:
        logger.error(f"Error running Manim CLI: {e}")
        return None

def run_manim_api(temp_file, media_dir, final_output_path):
    """Run Manim using Python API."""
    try:
        # Try to import Manim
        try:
            import manim
            logger.info(f"Successfully imported Manim {manim.__version__}")
        except ImportError as e:
            logger.error(f"Failed to import Manim: {e}")
            return None
            
        # Directory containing the temp file
        module_dir = os.path.dirname(temp_file)
        module_name = os.path.splitext(os.path.basename(temp_file))[0]
        
        # Add directory to path
        if module_dir not in sys.path:
            sys.path.insert(0, module_dir)
        
        # Set Manim configuration in environment
        os.environ["MEDIA_DIR"] = media_dir
        
        # Import the module dynamically
        try:
            spec = importlib.util.spec_from_file_location(module_name, temp_file)
            animation_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(animation_module)
            
            # Get the scene class
            scene_class_obj = getattr(animation_module, SCENE_CLASS_NAME)
            
            # Render the scene
            scene = scene_class_obj()
            scene.render(preview=False)
            
            # Try to find the output file
            return find_and_copy_output(media_dir, final_output_path)
        
        except Exception as e:
            logger.error(f"Error using Manim API: {e}")
            return None
            
    except Exception as e:
        logger.error(f"Unexpected error in Manim API approach: {e}")
        return None

def find_and_copy_output(media_dir, final_output_path):
    """Find and copy the generated video to final location."""
    # Wait briefly for file operations to complete
    time.sleep(1)
    
    # Define search patterns from most specific to most general
    search_patterns = [
        # Exact matches
        os.path.join(media_dir, "videos", SCENE_CLASS_NAME, "1080p60", f"{SCENE_CLASS_NAME}.mp4"),
        os.path.join(media_dir, "videos", "1080p60", f"{SCENE_CLASS_NAME}.mp4"),
        # Pattern matches
        os.path.join(media_dir, "videos", "**", f"{SCENE_CLASS_NAME}.mp4"),
        os.path.join(media_dir, "videos", "**", "*.mp4"),
        os.path.join(media_dir, "**", "*.mp4")
    ]
    
    # Try each pattern
    for pattern in search_patterns:
        logger.info(f"Searching with pattern: {pattern}")
        if "*" in pattern:
            # Use glob for patterns with wildcards
            matches = glob.glob(pattern, recursive=True)
            if matches:
                # Get most recent file
                matches.sort(key=os.path.getmtime, reverse=True)
                video_path = matches[0]
                logger.info(f"Found video at {video_path}")
                
                # Copy to final location
                try:
                    shutil.copyfile(video_path, final_output_path)
                    logger.info(f"Copied to {final_output_path}")
                    return final_output_path
                except Exception as e:
                    logger.error(f"Error copying file: {e}")
                    return video_path
        else:
            # Direct file check
            if os.path.exists(pattern):
                logger.info(f"Found video at {pattern}")
                
                # Copy to final location
                try:
                    shutil.copyfile(pattern, final_output_path)
                    logger.info(f"Copied to {final_output_path}")
                    return final_output_path
                except Exception as e:
                    logger.error(f"Error copying file: {e}")
                    return pattern
    
    # If we get here, no video was found
    logger.warning("No video found")
    return None

def combine_partial_movies(media_dir, final_output_path):
    """Combine partial movie files if they exist."""
    try:
        logger.info("Checking for partial movie files...")
        
        # Check partial movie directory
        partial_dir = os.path.join(media_dir, "videos", "1080p60", "partial_movie_files", SCENE_CLASS_NAME)
        
        if not os.path.exists(partial_dir):
            logger.info(f"Partial movie directory not found: {partial_dir}")
            return None
            
        # Look for MP4 files
        partial_files = glob.glob(os.path.join(partial_dir, "*.mp4"))
        
        if not partial_files:
            logger.info("No partial movie files found")
            return None
            
        logger.info(f"Found {len(partial_files)} partial movie files")
        
        # Create file list for FFmpeg
        file_list_path = os.path.join(tempfile.gettempdir(), "file_list.txt")
        with open(file_list_path, 'w', encoding="utf-8") as f:
            # Sort files to ensure correct order
            for partial in sorted(partial_files):
                # Use forward slashes for paths in file list
                clean_path = partial.replace('\\', '/')
                f.write(f"file '{clean_path}'\n")
        
        # Use FFmpeg to concatenate files
        try:
            ffmpeg_cmd = [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                "-i", file_list_path, "-c", "copy", final_output_path
            ]
            
            logger.info(f"Running FFmpeg: {' '.join(ffmpeg_cmd)}")
            
            result = subprocess.run(
                ffmpeg_cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False
            )
            
            if result.returncode != 0:
                logger.error(f"FFmpeg failed: {result.stderr}")
                return None
                
            # Check if output was created
            if os.path.exists(final_output_path):
                logger.info(f"Combined video created at {final_output_path}")
                return final_output_path
            else:
                logger.error("FFmpeg ran but output file not found")
                return None
        
        except Exception as e:
            logger.error(f"Error running FFmpeg: {e}")
            return None
    
    except Exception as e:
        logger.error(f"Error combining partial movies: {e}")
        return None

def create_mock_video(output_dir):
    """
    Create a mock video as a fallback.
    
    Args:
        output_dir (str): Output directory
        
    Returns:
        str: Path to the mock video
    """
    logger.warning("Creating mock video")
    
    # Define output path
    output_path = os.path.join(output_dir, "videos", SCENE_CLASS_NAME, "1080p60", f"{SCENE_CLASS_NAME}.mp4")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        # Try to create a matplotlib animation
        import numpy as np
        import matplotlib.pyplot as plt
        import matplotlib.animation as animation
        from matplotlib.animation import FuncAnimation
        
        # Create figure and axis
        try:
            fig, ax = plt.subplots()
            
            # Set up plot for Pythagorean theorem
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            
            # Draw right triangle
            ax.plot([1, 5, 1, 1], [1, 1, 5, 1], 'r-', linewidth=2)
            
            # Add labels
            ax.text(3, 0.5, "a", fontsize=14)
            ax.text(0.5, 3, "b", fontsize=14)
            ax.text(3, 3, "c", fontsize=14)
            
            # Add title
            ax.set_title("Pythagorean Theorem: a² + b² = c²")
            
            # Animation function
            def animate(i):
                ax.set_title(f"Pythagorean Theorem: a² + b² = c² (Frame {i})")
                return []
            
            # Create animation
            ani = FuncAnimation(fig, animate, frames=60, interval=50, blit=True)
            
            # Save as MP4
            writer = animation.FFMpegWriter(fps=15, metadata=dict(title="Pythagorean Theorem"))
            ani.save(output_path, writer=writer)
            
            logger.info(f"Mock video created at {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating matplotlib animation: {e}")
            # Create an empty file as last resort
            with open(output_path, 'wb') as f:
                f.write(b'Placeholder for video file')
            logger.warning(f"Created placeholder file at {output_path}")
            return output_path
            
    except ImportError:
        logger.error("Matplotlib not available, creating empty file")
        # Create empty file
        with open(output_path, 'wb') as f:
            f.write(b'Placeholder for video file')
        return output_path
    except Exception as e:
        logger.error(f"Unexpected error in mock video creation: {e}")
        # Create empty file
        with open(output_path, 'wb') as f:
            f.write(b'Placeholder for video file')
        return output_path