import logging
import os
import tempfile
import ast
import re
import textwrap

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a constant for the scene class name to ensure consistency
SCENE_CLASS_NAME = "EducationalScene"

def generate_manim_code(prompt):
    """Generate Manim code from a user prompt using the Groq API."""
    logger.info(f"Generating Manim code for prompt: {prompt}")
    
    try:
        # Import required libraries
        from langchain_core.prompts import PromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        from langchain_groq import ChatGroq
        import os
        import traceback
        
        # Get API key from environment
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            logger.error("GROQ_API_KEY not found in environment variables")
            return get_fallback_template(title=prompt)
        
        # Create Groq LLM instance with llama3-70b model
        llm = ChatGroq(
            api_key=api_key,
            model="llama3-70b-8192",
            temperature=0.2  # Lower temperature for more predictable code
        )
        output_parser = StrOutputParser()
        
        # Create an enhanced prompt template for Manim code generation with examples
        prompt_template = PromptTemplate.from_template(
        """
    You are a Manim animation code generator. 
    Your ONLY output must be a single, complete, and syntactically valid Python script for Manim, with:
    - Only one class: EducationalScene(Scene)
    - All code inside def construct(self)
    - No markdown, no explanations, no comments outside the code, no extra text.
    - No blank lines at the start or end.
    - Do not use triple backticks or any markdown formatting.

    If you are unsure, output nothing.

    Example:
    from manim import *

    class EducationalScene(Scene):
        def construct(self):
            title = Text("Gravity In Action").scale(0.8).to_edge(UP)
            self.play(Write(title))
            # ... more animation ...

    Now, generate code for: {prompt}

    Remember: Output ONLY valid Python code for Manim. No explanations, no markdown, no comments outside the code.
    """
        )
        # Run the chain
        chain = prompt_template | llm | output_parser
        manim_code = chain.invoke({"prompt": prompt})
        
        # Additional validation to catch obvious issues
        if manim_code and "EducationalScene" in manim_code and "def construct" in manim_code:
            # Very basic validation that code looks reasonable
            try:
                ast.parse(manim_code)
                logger.info("Successfully generated syntactically valid Manim code")
                return manim_code
            except SyntaxError as e:
                logger.warning(f"Generated code has syntax errors: {e}")
                # Log code with line numbers for debugging
                for idx, line in enumerate(manim_code.splitlines(), 1):
                    logger.warning(f"{idx:03d}: {line}")
                # Try sanitization
                try:
                    sanitized_code = sanitize_manim_code(manim_code)
                    ast.parse(sanitized_code)
                    logger.info("Successfully fixed Manim code syntax issues")
                    return sanitized_code
                except Exception as e2:
                    logger.error(f"Could not fix code syntax: {e2}")
                    for idx, line in enumerate(sanitized_code.splitlines(), 1):
                        logger.error(f"{idx:03d}: {line}")
        else:
            logger.warning("LLM generated incomplete or invalid code")
    except Exception as e:
        logger.error(f"Error generating Manim code with Groq: {e}")
        logger.error(traceback.format_exc())
    
    # Fallback to template if LLM fails
    logger.warning("Using fallback template for Manim code")
    return get_fallback_template(title=prompt)

def sanitize_manim_code(code):
    """
    Aggressively sanitize LLM output to extract only valid Python Manim code.
    """
    import re

    # Remove markdown code fences and any non-code lines at the start/end
    code = re.sub(r"^```[a-zA-Z]*\n?", "", code)
    code = re.sub(r"\n```$", "", code)
    code = code.strip()
    match = re.search(
        r"(from manim import \*.*?)(class EducationalScene\(Scene\):.*?)(?:(?:class )|$)",
        code,
        re.DOTALL,
    )
    if match:
        code = match.group(1) + "\n" + match.group(2)
    return code

    # Remove any lines before the first 'from manim import' or 'class'
    lines = code.splitlines()
    start = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("from manim import") or line.strip().startswith("class "):
            start = i
            break
    lines = lines[start:]

    # Remove any trailing non-code lines
    end = len(lines)
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() == "" or lines[i].strip().startswith("#"):
            continue
        if (
            lines[i].strip().startswith("def ")
            or lines[i].strip().startswith("class ")
            or lines[i].strip().startswith("from ")
            or lines[i].strip().startswith("import ")
            or "=" in lines[i]
            or lines[i].strip().endswith(":")
        ):
            end = i + 1
            break
    lines = lines[:end]

    # Remove any markdown, explanations, or comments outside code
    code = "\n".join(line for line in lines if not line.strip().startswith("```"))
    code = re.sub(r"^#.*$", "", code, flags=re.MULTILINE)
    code = code.strip()

    # Ensure required import and class structure
    if "from manim import" not in code:
        code = "from manim import *\n\n" + code
    if "class EducationalScene" not in code:
        code += "\n\nclass EducationalScene(Scene):\n    def construct(self):\n        self.wait(1)\n"

    return code
 
def get_fallback_template(title="Educational Topic", animation_code=None):
    """
    Return a fallback Manim template that's guaranteed to work.
    Args:
        title (str): The title to display in the animation.
        animation_code (str, optional): Custom animation code to insert in the construct method.
    Returns:
        str: Fallback Manim code
    """
    logger.info(f"Using fallback {SCENE_CLASS_NAME} template with title: {title}")
    # Default animation if none provided
    default_animation = """
        # Simple animation
        circle = Circle()
        self.play(Create(circle))
    """
    animation_body = animation_code if animation_code else default_animation

    return f"""
from manim import *

class {SCENE_CLASS_NAME}(Scene):
    def construct(self):
        # Title
        title = Text("{title}").scale(0.8)
        title.to_edge(UP)
        self.play(Write(title))
{animation_body}
        # Wait at the end
        self.wait(2)
    """

def save_manim_code(code, filename=None):
    """
    Save generated Manim code to a Python file.
    
    Args:
        code (str): Manim code to save
        filename (str, optional): Filename to save to. If None, creates a temporary file.
        
    Returns:
        str: Path to the saved file
    """
    # Create a consistent temporary file path if not provided
    if not filename:
        temp_dir = tempfile.gettempdir()
        filename = os.path.abspath(os.path.join(temp_dir, "animation_scene.py"))
    
    # Sanitize the code before saving
    sanitized_code = sanitize_manim_code(code)
    
    try:
        # Use UTF-8 encoding for all file operations
        with open(filename, "w", encoding="utf-8") as f:
            f.write(sanitized_code)
        logger.info(f"Saved Manim code to {filename}")
    except Exception as e:
        logger.error(f"Error saving Manim code: {e}")
        # Fallback with error handling for encoding issues
        try:
            # Try with replacement strategy for problematic characters
            with open(filename, "w", encoding="utf-8", errors="replace") as f:
                f.write(sanitized_code)
            logger.info(f"Saved Manim code with character replacement at {filename}")
        except Exception as e2:
            logger.error(f"Critical error saving code: {e2}")
            # Last resort: save the fallback template
            with open(filename, "w", encoding="utf-8", errors="ignore") as f:
                f.write(get_fallback_template())
            logger.warning(f"Saved fallback template to {filename}")
    
    return filename