import os
import logging
from ..services.manim_service import generate_manim_code, save_manim_code
from ..services.video_service import create_video
from ..services.voice_service import create_voiceover
from ..langgraph.workflow import AnimationWorkflow

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_animation(prompt):
    """
    Create an educational animation from a prompt.
    
    Args:
        prompt (str): User prompt describing the desired animation
        
    Returns:
        dict: Information about the generated animation, including file paths
    """
    logger.info(f"Creating animation for prompt: {prompt}")
    
    try:
        # Check if we should use the AI workflow (for more advanced animations)
        use_ai_workflow = os.environ.get("USE_AI_WORKFLOW", "false").lower() == "true"
        
        if use_ai_workflow:
            # Use LangGraph workflow for advanced animation generation
            workflow = AnimationWorkflow()
            workflow_result = workflow.run(prompt)
            
            # Extract results from workflow
            manim_code = workflow_result["manim_code"]
            script = workflow_result["script"]
            
            # Save the generated code to a file
            code_file = save_manim_code(manim_code)
            
            # Generate the video from the code
            video_path = create_video(manim_code)
            
            # Generate the voiceover from the script
            audio_path = create_voiceover(script)
        else:
            # Use the simple approach for basic animations
            # Step 1: Generate Manim code from the prompt
            manim_code = generate_manim_code(prompt)
            
            # Step 2: Create video from the Manim code
            video_path = create_video(manim_code)
            
            # Step 3: Generate voiceover for the animation
            audio_path = create_voiceover(prompt)
        
        # For now, we're just returning the paths without combining audio and video
        return {
            "status": "success",
            "video_path": video_path,
            "audio_path": audio_path,
            "message": "Animation created successfully"
        }
    except Exception as e:
        logger.error(f"Error creating animation: {str(e)}")
        raise