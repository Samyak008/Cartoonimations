import logging
import os
from gtts import gTTS
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_voiceover(text, language='en', output_path=None):
    """
    Create a voiceover audio file from text using Google Text-to-Speech.
    
    Args:
        text (str): The text to convert to speech
        language (str, optional): Language for the speech. Defaults to 'en'.
        output_path (str, optional): Path to save the audio file. 
                                     If None, saves to animation/output directory.
    
    Returns:
        str: Path to the generated audio file
    """
    logger.info(f"Creating voiceover for text: {text[:50]}...")
    
    try:
        # Create the TTS object
        tts = gTTS(text=text, lang=language, slow=False)
        
        # Determine output path if not provided
        if not output_path:
            # Create output directory in the animation folder
            output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                     "animation", "output", "audio")
            os.makedirs(output_dir, exist_ok=True)
            
            # Create a temporary filename
            temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False, dir=output_dir)
            output_path = temp_file.name
            temp_file.close()
        
        # Save the audio file
        tts.save(output_path)
        logger.info(f"Voiceover created successfully at {output_path}")
        
        return output_path
    
    except Exception as e:
        logger.error(f"Error creating voiceover: {str(e)}")
        raise