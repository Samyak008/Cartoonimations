from manim import *

class BasicEducationalScene(Scene):
    """
    A template for basic educational animations.
    This class can be extended for creating more complex animations.
    """
    
    def __init__(self, title_text="Educational Animation", **kwargs):
        super().__init__(**kwargs)
        self.title_text = title_text
    
    def construct(self):
        # Display the title
        self.show_title()
        
        # Placeholder for main content
        self.create_content()
        
        # End scene
        self.end_scene()
    
    def show_title(self):
        """Display the title of the animation."""
        title = Text(self.title_text).scale(0.8)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
    
    def create_content(self):
        """
        Create the main content of the animation.
        Override this method in subclasses.
        """
        # Default implementation: show a circle
        circle = Circle()
        self.play(Create(circle))
        self.wait(1)
        
        # Add some text
        text = Text("Override create_content() method").scale(0.5)
        text.next_to(circle, DOWN)
        self.play(FadeIn(text))
        self.wait(1)
    
    def end_scene(self):
        """End the scene with a conclusion."""
        conclusion = Text("Thank you for watching!").scale(0.7)
        conclusion.to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(2)