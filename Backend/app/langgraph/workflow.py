import os
import logging
from typing import TypedDict, Optional, Dict, Any
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the state schema
class WorkflowState(TypedDict):
    prompt: str
    plan: Optional[str]
    scene_plan: Optional[str]
    manim_code: Optional[str]
    script: Optional[str]

class AnimationWorkflow:
    """
    LangGraph workflow for educational animation generation.
    """
    
    def __init__(self, groq_api_key=None):
        """
        Initialize the animation workflow.
        
        Args:
            groq_api_key (str, optional): Groq API key.
                If not provided, will be taken from environment variables.
        """
        self.groq_api_key = groq_api_key or os.environ.get("GROQ_API_KEY")
        self.llm = ChatGroq(
            model="llama3-70b-8192",  # Groq model format doesn't need the "groq/" prefix
            temperature=0.7,
            groq_api_key=self.groq_api_key  # Use groq_api_key parameter instead of api_key
        )
        # Create a chain that parses the output to string
        self.output_parser = StrOutputParser()
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """
        Build the LangGraph workflow.
        
        Returns:
            StateGraph: The workflow graph
        """
        # Define nodes and edges in the graph
        graph = StateGraph(WorkflowState)
        
        # Add nodes for each step in the animation generation process
        graph.add_node("director", self._director_node)
        graph.add_node("scene_planner", self._scene_planner_node)
        graph.add_node("code_generator", self._code_generator_node)
        graph.add_node("script_writer", self._script_writer_node)
        
        # Define the workflow edges
        graph.add_edge("director", "scene_planner")
        graph.add_edge("scene_planner", "code_generator")
        graph.add_edge("code_generator", "script_writer")
        graph.add_edge("script_writer", END)
        
        # Set the entry point
        graph.set_entry_point("director")
        
        # Compile the graph
        return graph.compile()
    
    def _director_node(self, state: WorkflowState) -> WorkflowState:
        """
        Director node: Understands the user's prompt and creates a high-level plan.
        
        Args:
            state (WorkflowState): Current workflow state
            
        Returns:
            WorkflowState: Updated workflow state
        """
        prompt = PromptTemplate.from_template(
            """You are a Director for educational animations.
            
            Given the following user prompt, create a high-level plan for an educational animation.
            Focus on clarity, educational value, and visual appeal.
            
            User prompt: {prompt}
            
            Provide a plan with:
            1. Animation title
            2. Key concepts to visualize
            3. Visual style suggestions
            4. Educational objectives
            """
        )
        
        # Use modern syntax: prompt | llm | parser
        chain = prompt | self.llm | self.output_parser
        plan = chain.invoke({"prompt": state["prompt"]})
        
        logger.info("Director has created a high-level plan")
        
        return {"prompt": state["prompt"], "plan": plan}
    
    def _scene_planner_node(self, state: WorkflowState) -> WorkflowState:
        """
        Scene planner node: Plans individual scenes for the animation.
        
        Args:
            state (WorkflowState): Current workflow state
            
        Returns:
            WorkflowState: Updated workflow state with scene plan
        """
        prompt = PromptTemplate.from_template(
            """You are a Scene Planner for educational animations.
            
            Given the high-level plan, create a detailed scene breakdown.
            
            High-level plan:
            {plan}
            
            For each scene, provide:
            1. Scene duration (in seconds)
            2. Visual elements to include
            3. Transitions between scenes
            4. Mathematical concepts or formulas to display
            
            Create 3-5 scenes that would work well in an educational animation.
            """
        )
        
        # Use modern syntax with proper parsing
        chain = prompt | self.llm | self.output_parser
        scene_plan = chain.invoke({"plan": state["plan"]})
        
        logger.info("Scene Planner has created a scene breakdown")
        
        return {**state, "scene_plan": scene_plan}
    
    def _code_generator_node(self, state: WorkflowState) -> WorkflowState:
        """
        Code generator node: Creates Manim code for each scene.
        
        Args:
            state (WorkflowState): Current workflow state
            
        Returns:
            WorkflowState: Updated workflow state with generated code
        """
        prompt = PromptTemplate.from_template(
            """You are a Manim Code Generator for educational animations.
            
            Given the scene plan below, write Python code using the Manim library to create each scene.
            Follow best practices for code organization and readability.
            
            Scene plan:
            {scene_plan}
            
            Original prompt:
            {prompt}
            
            Generate complete, runnable Manim code for this animation:
            """
        )
        
        # Use modern syntax with proper parsing
        chain = prompt | self.llm | self.output_parser
        manim_code = chain.invoke({
            "scene_plan": state["scene_plan"], 
            "prompt": state["prompt"]
        })
        
        logger.info("Code Generator has created Manim code")
        
        return {**state, "manim_code": manim_code}
    
    def _script_writer_node(self, state: WorkflowState) -> WorkflowState:
        """
        Script writer node: Creates a voiceover script for the animation.
        
        Args:
            state (WorkflowState): Current workflow state
            
        Returns:
            WorkflowState: Updated workflow state with script
        """
        prompt = PromptTemplate.from_template(
            """You are a Script Writer for educational animations.
            
            Given the scene plan below, write a voiceover script that matches the animation timing.
            
            Scene plan:
            {scene_plan}
            
            Original prompt:
            {prompt}
            
            Write a clear, engaging script suitable for a narrator:
            """
        )
        
        # Use modern syntax with proper parsing
        chain = prompt | self.llm | self.output_parser
        script = chain.invoke({
            "scene_plan": state["scene_plan"], 
            "prompt": state["prompt"]
        })
        
        logger.info("Script Writer has created a voiceover script")
        
        return {**state, "script": script}
    
    def run(self, prompt: str) -> Dict[str, Any]:
        """
        Run the workflow with a user prompt.
        
        Args:
            prompt (str): User prompt for animation generation
            
        Returns:
            dict: Final workflow state with all generated content
        """
        logger.info(f"Starting animation workflow for prompt: {prompt}")
        
        # Initialize the workflow state
        initial_state: WorkflowState = {"prompt": prompt}
        
        # Execute the workflow
        result = self.graph.invoke(initial_state)
        
        logger.info("Animation workflow completed successfully")
        return result