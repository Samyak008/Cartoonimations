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
    """
    Generate Manim code from a user prompt.
    
    Args:
        prompt (str): User prompt describing the desired animation
        
    Returns:
        str: Generated Manim code
    """
    logger.info(f"Generating Manim code for prompt: {prompt}")
    
    # Escape single quotes in the prompt
    title = prompt.replace("'", "\\'")
    
    # Use the standardized scene class name
    code = f"""
from manim import *

class {SCENE_CLASS_NAME}(Scene):
    def construct(self):
        # Title
        title = Text("{title}").scale(0.8)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Simple animation
        circle = Circle()
        self.play(Create(circle))
        
        # Wait at the end
        self.wait(2)
    """
    
    logger.info("Manim code generated successfully")
    return code

def sanitize_manim_code(code):
    """
    Sanitize and validate Manim code to ensure it will run properly.
    
    Args:
        code (str): Manim code to sanitize
        
    Returns:
        str: Sanitized Manim code
    """
    # Remove markdown code block syntax
    code = re.sub(r'^```(?:python|manim)?\s*', '', code)
    code = re.sub(r'\s*```$', '', code)
    
    # Remove any descriptive text at the beginning or end
    lines = code.splitlines()
    
    # Find the start and end of actual Python code
    first_code_line = 0
    last_code_line = len(lines) - 1
    
    # Find first line that looks like Python code
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('from ') or stripped.startswith('import ') or stripped.startswith('class '):
            first_code_line = i
            break
            
    # Find last line of Python code (before any descriptive comments)
    for i in range(len(lines) - 1, -1, -1):
        stripped = lines[i].strip()
        if not stripped:  # Skip empty lines
            continue
        # Check if this is a descriptive comment rather than code
        if not stripped.startswith('#') and not (
            stripped.startswith('import') or 
            stripped.startswith('class') or 
            stripped.startswith('def') or 
            stripped.startswith('if') or 
            '=' in stripped or 
            stripped.endswith(':')
        ):
            if any(keyword in stripped.lower() for keyword in ['note', 'create', 'place', 'need', 'file']):
                last_code_line = i - 1
            else:
                break
    
    # Extract only the Python code
    code_lines = lines[first_code_line:last_code_line+1]
    
    # Remove any lines that reference external resources
    code_lines = [line for line in code_lines if not any(x in line.lower() for x in [
        'you\'ll need', 'place them', 'same directory', 'create the', 'download'
    ])]
    
    # Replace unsupported elements with safe alternatives
    clean_lines = []
    for line in code_lines:
        if "ImageMobject" in line:
            # Replace image references with shapes
            indent = len(line) - len(line.lstrip())
            var_name = line.strip().split('=')[0].strip()
            clean_lines.append(f"{' ' * indent}{var_name} = Circle(color=RED)")
        elif "add_sound" in line or "play_sound" in line:
            # Skip sound-related lines
            continue
        else:
            clean_lines.append(line)
    
    # Reconstruct the code
    clean_code = '\n'.join(clean_lines)
    
    # Ensure the scene class name is standardized
    clean_code = re.sub(r'class\s+\w+\s*\(\s*Scene\s*\)', f'class {SCENE_CLASS_NAME}(Scene)', clean_code)
    
    # Add required imports if missing
    if 'from manim import' not in clean_code:
        clean_code = 'from manim import *\n\n' + clean_code
    
    # Add minimum scene structure if missing
    if f'class {SCENE_CLASS_NAME}' not in clean_code:
        clean_code += f'\n\nclass {SCENE_CLASS_NAME}(Scene):\n    def construct(self):\n        self.wait(1)\n'
    
    # Validate the Python syntax
    try:
        ast.parse(clean_code)
        logger.info("Manim code validation successful")
    except SyntaxError as e:
        logger.warning(f"Syntax error in generated code: {e}")
        # Use a reliable fallback template
        clean_code = get_fallback_template()
    
    return clean_code

def get_fallback_template():
    """
    Return a fallback Manim template that's guaranteed to work.
    
    Returns:
        str: Fallback Manim code
    """
    logger.info(f"Using fallback {SCENE_CLASS_NAME} template")
    return f"""
from manim import *

class {SCENE_CLASS_NAME}(Scene):
    def construct(self):
        # Title
        title = Text("Pythagorean Theorem").scale(0.8)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create a right triangle
        triangle = Polygon(
            ORIGIN, 
            RIGHT * 3, 
            UP * 4, 
            color=WHITE
        )
        self.play(Create(triangle))
        
        # Label the sides
        a_label = Text("a", font_size=24).next_to(triangle, DOWN)
        b_label = Text("b", font_size=24).next_to(triangle, RIGHT)
        c_label = Text("c", font_size=24).next_to(
            triangle.get_center() + UP * 0.5 + RIGHT * 0.5
        )
        
        self.play(Write(a_label), Write(b_label), Write(c_label))
        
        # Show the formula
        formula = MathTex(r"a^2 + b^2 = c^2")
        formula.next_to(triangle, DOWN * 2)
        self.play(Write(formula))
        
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