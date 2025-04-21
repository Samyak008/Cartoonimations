import logging
import os
import tempfile
import ast
import re
import textwrap

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_manim_code(prompt):
    """
    Generate Manim code from a user prompt.
    
    In Phase 1, this is a simple template-based approach.
    In Phase 3, this will be replaced with LLM-generated code.
    
    Args:
        prompt (str): User prompt describing the desired animation
        
    Returns:
        str: Generated Manim code
    """
    logger.info(f"Generating Manim code for prompt: {prompt}")
    
    # For Phase 1, we'll use a simple template
    # This will be replaced with an LLM call in Phase 3
    
    # Simple example: create a scene with a title and a circle
    title = prompt.replace("'", "\\'")
    
    code = f"""
from manim import *

class EducationalScene(Scene):
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
    # Remove any markdown code blocks and language specifiers
    code = re.sub(r'^```(?:python|manim)?\n', '', code)
    code = re.sub(r'\n```$', '', code)
    
    # Remove any descriptive text at the beginning or end that isn't Python code
    lines = code.split('\n')
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
        # Skip empty lines
        if not stripped:
            continue
        # If this looks like a descriptive comment not a code comment, exclude it
        if not stripped.startswith('#') and not stripped.startswith('import') and not stripped.startswith('class') and not stripped.startswith('def') and not stripped.startswith('if') and '=' not in stripped and stripped[-1] != ':':
            if any(keyword in stripped.lower() for keyword in ['note', 'create', 'place', 'need', 'file']):
                last_code_line = i - 1
            else:
                break
                
    # Extract just the Python code portion
    code_lines = lines[first_code_line:last_code_line+1]
    
    # Skip any lines that are describing Manim requirements
    code_lines = [line for line in code_lines if not any(x in line.lower() for x in ['you\'ll need', 'place them', 'same directory'])]
    
    # Replace image references with dummy implementations
    clean_lines = []
    for line in code_lines:
        if "ImageMobject" in line:
            # Get the indentation
            indent = len(line) - len(line.lstrip())
            # Create a Circle instead of an ImageMobject
            clean_lines.append(' ' * indent + line.strip().split('=')[0] + '= Circle(color=RED)')
        elif "add_sound" in line:
            # Skip sound-related lines
            continue
        else:
            clean_lines.append(line)
    
    # Reconstruct the code
    clean_code = '\n'.join(clean_lines)
    
    # Make sure the Scene class name is consistent
    clean_code = re.sub(r'class\s+(\w+)\s*\(\s*Scene\s*\)', 'class EducationalScene(Scene)', clean_code)
    
    # Ensure the code has the minimum required imports
    if 'from manim import' not in clean_code:
        clean_code = 'from manim import *\n\n' + clean_code
    
    # If there's no class definition at all, create a minimal one
    if 'class EducationalScene' not in clean_code:
        clean_code += '\n\nclass EducationalScene(Scene):\n    def construct(self):\n        self.wait(1)\n'
    
    # Try to validate the Python syntax
    try:
        ast.parse(clean_code)
        logger.info("Manim code validation successful")
    except SyntaxError as e:
        logger.warning(f"Syntax error in generated code: {e}")
        # Create a minimal valid scene as fallback
        clean_code = """
from manim import *

class EducationalScene(Scene):
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
        formula = MathTex("a^2 + b^2 = c^2")
        formula.next_to(triangle, DOWN * 2)
        self.play(Write(formula))
        
        # Wait at the end
        self.wait(2)
        """
        logger.info("Using fallback Pythagorean theorem animation template")
    
    return clean_code

def save_manim_code(code, filename=None):
    """
    Save generated Manim code to a Python file.
    
    Args:
        code (str): Manim code to save
        filename (str, optional): Filename to save to. If None, creates a temporary file.
        
    Returns:
        str: Path to the saved file
    """
    if not filename:
        temp_dir = tempfile.gettempdir()
        filename = os.path.join(temp_dir, "animation_scene.py")
    
    # Sanitize the code before saving
    sanitized_code = sanitize_manim_code(code)
        
    try:
        # Use UTF-8 encoding to handle special characters like Greek symbols
        with open(filename, "w", encoding="utf-8") as f:
            f.write(sanitized_code)
        logger.info(f"Saved Manim code to {filename}")
    except Exception as e:
        logger.error(f"Error saving Manim code: {e}")
        # Fallback: If there are still encoding issues, strip or replace problematic characters
        logger.info("Attempting to save with problematic characters replaced")
        with open(filename, "w", encoding="utf-8", errors="replace") as f:
            f.write(sanitized_code)
        
    return filename