from manim import *
import sys
import os

# Add the parent directory to the path to import from templates
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from templates.basic_scene import BasicEducationalScene

class MathGenerator:
    """
    Generator for mathematical animations.
    This class provides utility methods for creating common mathematical visualizations.
    """
    
    @staticmethod
    def create_graph_scene(title, function_str, x_range=(-5, 5, 1), y_range=(-5, 5, 1)):
        """
        Create a scene with a graph of the given function.
        
        Args:
            title (str): Title of the animation
            function_str (str): String representation of the function to graph
            x_range (tuple): Range for x-axis (min, max, step)
            y_range (tuple): Range for y-axis (min, max, step)
            
        Returns:
            str: Python code for the scene
        """
        # Convert function_str to a lambda expression safely
        # In a production environment, you'd want more safety checks here
        safe_function_str = function_str.replace("^", "**")
        
        code = f"""
from manim import *
import sys
import os

# Add the parent directory to the path to import from templates
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from templates.basic_scene import BasicEducationalScene

class GraphScene(BasicEducationalScene):
    def __init__(self, **kwargs):
        super().__init__(title_text="{title}", **kwargs)
        
    def create_content(self):
        # Create axes
        axes = Axes(
            x_range={x_range},
            y_range={y_range},
            axis_config={{"color": BLUE}},
            x_axis_config={{"numbers_to_include": range({x_range[0]}, {x_range[1]}+1)}},
            y_axis_config={{"numbers_to_include": range({y_range[0]}, {y_range[1]}+1)}},
        )
        
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        
        # Create the graph
        graph = axes.plot(lambda x: {safe_function_str}, color=YELLOW)
        graph_label = MathTex(r"f(x) = {function_str}").next_to(graph, UP)
        
        # Show the elements
        self.play(Create(axes), Write(axes_labels))
        self.wait(1)
        self.play(Create(graph), Write(graph_label))
        self.wait(2)
        
        # Optional: highlight a point on the graph
        dot = Dot().move_to(axes.c2p(1, {safe_function_str.replace('x', '1')}))
        self.play(FadeIn(dot))
        self.wait(1)
        
        # Add explanation
        explanation = Text(f"This is the graph of f(x) = {function_str}", font_size=24)
        explanation.to_edge(DOWN)
        self.play(Write(explanation))
        self.wait(2)

# For direct execution of this file
if __name__ == "__main__":
    scene = GraphScene()
    scene.render()
"""
        return code
    
    @staticmethod
    def create_geometry_scene(title, shape_type="circle", params=None):
        """
        Create a scene demonstrating geometric concepts.
        
        Args:
            title (str): Title of the animation
            shape_type (str): Type of shape to demonstrate (circle, square, triangle)
            params (dict): Parameters for the shape
            
        Returns:
            str: Python code for the scene
        """
        if params is None:
            params = {}
            
        # Default parameters
        radius = params.get("radius", 2)
        side_length = params.get("side_length", 3)
        
        shape_code = ""
        explanation_text = ""
        
        if shape_type.lower() == "circle":
            shape_code = f"""
            # Create a circle
            circle = Circle(radius={radius})
            circle.set_fill(BLUE, opacity=0.5)
            
            # Show radius
            radius_line = Line(ORIGIN, circle.point_at_angle(0))
            radius_label = MathTex("r = {radius}").next_to(radius_line, DOWN)
            
            # Calculate and show area
            area = {3.14159} * {radius}**2
            area_text = MathTex(r"\\text{{Area}} = \\pi r^2 = {area:.2f}")
            area_text.to_edge(DOWN)
            
            # Show the elements
            self.play(Create(circle))
            self.wait(1)
            self.play(Create(radius_line), Write(radius_label))
            self.wait(1)
            self.play(Write(area_text))
            """
            explanation_text = f"This animation demonstrates a circle with radius {radius}."
            
        elif shape_type.lower() == "square":
            shape_code = f"""
            # Create a square
            square = Square(side_length={side_length})
            square.set_fill(GREEN, opacity=0.5)
            
            # Show side length
            side = Line(square.get_corner(DOWN+LEFT), square.get_corner(DOWN+RIGHT))
            side_label = MathTex("s = {side_length}").next_to(side, DOWN)
            
            # Calculate and show area
            area = {side_length}**2
            area_text = MathTex(r"\\text{{Area}} = s^2 = {area}")
            area_text.to_edge(DOWN)
            
            # Show the elements
            self.play(Create(square))
            self.wait(1)
            self.play(Create(side), Write(side_label))
            self.wait(1)
            self.play(Write(area_text))
            """
            explanation_text = f"This animation demonstrates a square with side length {side_length}."
        
        elif shape_type.lower() == "triangle":
            shape_code = f"""
            # Create an equilateral triangle
            triangle = Triangle().scale({side_length}/2)
            triangle.set_fill(RED, opacity=0.5)
            
            # Show side length
            side = Line(triangle.get_vertices()[0], triangle.get_vertices()[1])
            side_label = MathTex("s = {side_length}").next_to(side, DOWN)
            
            # Calculate and show area (for equilateral triangle)
            area = ({side_length}**2 * 3**0.5) / 4
            area_text = MathTex(r"\\text{{Area}} = \\frac{{\\sqrt{{3}}s^2}}{{4}} = {area:.2f}")
            area_text.to_edge(DOWN)
            
            # Show the elements
            self.play(Create(triangle))
            self.wait(1)
            self.play(Create(side), Write(side_label))
            self.wait(1)
            self.play(Write(area_text))
            """
            explanation_text = f"This animation demonstrates an equilateral triangle with side length {side_length}."
        
        code = f"""
from manim import *
import sys
import os

# Add the parent directory to the path to import from templates
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from templates.basic_scene import BasicEducationalScene

class GeometryScene(BasicEducationalScene):
    def __init__(self, **kwargs):
        super().__init__(title_text="{title}", **kwargs)
        
    def create_content(self):
        {shape_code}
        
        # Additional explanation
        explanation = Text("{explanation_text}", font_size=24)
        explanation.to_edge(UP, buff=1.5)
        self.play(Write(explanation))
        self.wait(2)

# For direct execution of this file
if __name__ == "__main__":
    scene = GeometryScene()
    scene.render()
"""
        return code