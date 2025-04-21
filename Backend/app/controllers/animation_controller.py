import os
import logging
import traceback
from ..services.manim_service import save_manim_code
from ..services.video_service import create_video
from ..services.voice_service import create_voiceover
from ..langgraph.workflow import AnimationWorkflow

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_animation(prompt):
    """
    Create an educational animation from a user prompt.
    
    Args:
        prompt (str): User prompt describing the animation
        
    Returns:
        dict: Animation details including video path, script, etc.
    """
    try:
        logger.info(f"Creating animation for prompt: {prompt}")
        
        # Check if we're using AI workflow
        use_ai_workflow = os.environ.get("USE_AI_WORKFLOW", "true").lower() in ["true", "1", "yes"]
        
        if use_ai_workflow:
            # Use LangGraph workflow
            try:
                workflow = AnimationWorkflow()
                result = workflow.run(prompt)
                
                manim_code = result.get("manim_code", "")
                script = result.get("script", "")
            except Exception as e:
                logger.error(f"Error in AI workflow: {e}")
                logger.error(traceback.format_exc())
                # Fallback to simple template
                manim_code = f"# Failed to generate code, using template\nfrom manim import *\n\nclass EducationalScene(Scene):\n    def construct(self):\n        title = Text(\"{prompt}\").scale(0.8)\n        title.to_edge(UP)\n        self.play(Write(title))\n        self.wait(2)"
                script = f"Here is an explanation about {prompt}"
        else:
            # Use direct template approach
            from ..services.manim_service import generate_manim_code
            manim_code = generate_manim_code(prompt)
            script = f"Here is an explanation about {prompt}"
            
        # Create video from code
        try:
            video_path = create_video(manim_code)
            if not video_path or not os.path.exists(video_path):
                raise FileNotFoundError("Failed to generate video file")
        except Exception as e:
            logger.error(f"Error creating video: {e}")
            logger.error(traceback.format_exc())
            raise Exception(f"Failed to generate video: {str(e)}")
            
        # Create voiceover from script
        try:
            audio_path = create_voiceover(script)
        except Exception as e:
            logger.error(f"Error creating voiceover: {e}")
            logger.error(traceback.format_exc())
            audio_path = None
            
        return {
            "video_path": video_path,
            "audio_path": audio_path,
            "script": script,
            "prompt": prompt
        }
        
    except Exception as e:
        logger.error(f"Error creating animation: {e}")
        logger.error(traceback.format_exc())
        raise Exception(f"Failed to create animation: {str(e)}")
    finally:
        logger.info("Animation creation process completed.")
        