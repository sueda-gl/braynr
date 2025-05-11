from google.adk.agents import SequentialAgent, LlmAgent
from google.adk.models.lite_llm import LiteLlm
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# if not GOOGLE_API_KEY:
#     raise ValueError("GOOGLE_API_KEY environment variable not found. Please add it to your .env file.")

# Get OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not found. Please add it to your .env file.")

# --- 1. Define Sub-Agents for Each Pipeline Stage ---

# Clear Explanation Agent
clear_explanation_agent = LlmAgent(
    name="ClearExplanationAgent",
    model=LiteLlm(model="openai/gpt-4o"),
    instruction="""
Du bist ein hilfreicher Erklärer von technischen und abstrakten Konzepten.
Der Benutzer hat ein Bild bereitgestellt (was zum Thema führt: {topic}).
Er hat möglicherweise auch eine spezifische Aufforderung gegeben: {user_prompt}.

Basierend auf dem Thema aus dem Bild und geleitet von der Aufforderung des Benutzers (falls vorhanden), gib eine klare und prägnante Erklärung ab, die für ein allgemeines Publikum geeignet ist.
Wenn die user_prompt leer ist oder nicht eindeutig auf die Verfeinerung der Erklärung des Themas anwendbar ist, konzentriere dich primär auf das Thema.
Vermeide Fachbegriffe, es sei denn, sie sind notwendig, und erkläre Begriffe, wenn sie verwendet werden.
Gib nur die Erklärung aus.
""",
    description="Generates clear explanations of topics, guided by user prompts.",
    output_key='explanation'
    # input_keys parameter is not supported and was causing the Pydantic error
    # The agent automatically infers input keys from the placeholders in the instruction template.
)

# Concept Separator Agent
concept_separator_agent = LlmAgent(
    name="ConceptSeparatorAgent",
    model=LiteLlm(model="openai/gpt-4o"),
    instruction="""
You are an expert at identifying key components of explanations.
Take the {explanation} and break it down into a list of its fundamental concepts.
Output only the list of concepts as bullet points.
""",
    description="Breaks down explanations into key concepts.",
    output_key='concepts',
)

# Storyboard Creator Agent
storyboard_creator_agent = LlmAgent(
    name="StoryboardCreatorAgent",
    model=LiteLlm(model="openai/gpt-4o"),
    instruction="""
You are a storyboard planner.
Given a list of concepts: {concepts}, create an ordered storyboard with visual scenes and brief captions to teach each concept clearly.
Structure it as a list of steps with short titles and descriptions.
""",
    description="Creates a storyboard from a list of concepts.",
    output_key='storyboard',
)

# Storyboard Enhancer Agent
storyboard_enhancer_agent = LlmAgent(
    name="StoryboardEnhancerAgent",
    model=LiteLlm(model="openai/gpt-4o"),
    instruction="""
You are a visual storyteller.
Enhance the provided storyboard: {storyboard} by adding narration, transitions, and visual suggestions for each step. You have to clearly state 
which objects are going to appear, how they move and interact and how long they stay on the screen.
Keep it suitable for an animated explainer using Manim.
""",
    description="Improves the storyboard with narration and visuals.",
    output_key='enhanced_storyboard',
)

# Code Generator Agent
code_generator_agent = LlmAgent(
    name="CodeGeneratorAgent",
    model=LiteLlm(model="openai/gpt-4o"),
    instruction='''
You are an expert Manim animation code generator, creating scripts for Manim Community v0.18.0 or newer.
Given an enhanced storyboard: {enhanced_storyboard}, write a complete Python script to visualize the content.
Output *only* the raw Python code, enclosed in triple backticks: ```python ... ```

**CRITICAL REQUIREMENTS FOR THE GENERATED MANIM SCRIPT:**

1.  **START WITH:** The script MUST begin *exactly* with `from manim import *`. Standard Python imports like `import numpy as np` are allowed if needed.

2.  **NO EXTERNAL ASSETS OR LATEX/TEX (EXTREMELY IMPORTANT):**
    *   ABSOLUTELY DO NOT USE `SVGMobject`.
    *   ABSOLUTELY DO NOT USE `ImageMobject`.
    *   ABSOLUTELY DO NOT USE `Tex()`, `MathTex()`, or ANY LaTeX-based text objects.
    *   Use ONLY `Text()` objects for ALL text in the animation.
    *   For mathematical symbols and equations, use simple Unicode in Text objects (e.g., `Text("x²")`, `Text("Σ")`, `Text("det(A)")`, `Text("|A|")`, etc.)
    *   All visuals MUST be created using ONLY Manim's built-in shapes (e.g., `Circle`, `Square`, `Rectangle`, `RoundedRectangle`, `Line`, `Polygon`, `Dot`, `Arrow`, `Triangle`) and Manim's `Text` objects only.
    *   Do NOT reference any external files (e.g., `.svg`, `.png`, `.jpg`, `.mp3`, `.wav`).
    *   Do NOT use `self.add_sound()` or any other sound-related functions.

3.  **COLORS:**
    *   Use Manim's predefined color constants (e.g., `RED`, `BLUE`, `GREEN`, `WHITE`, `BLACK`) or hexadecimal color strings (e.g., `color='#FFC0CB'`).
    *   If a function like `def random_color():` is used, it MUST return a valid Manim color format (preferably a hex string like `f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"` if r,g,b are 0-1 floats from np.random.uniform, or Manim color constants).
    *   AVOID `Color(...)` unless `from manim.utils.color import Color` is also included and used correctly as `Color(...)`.

4.  **RECTANGLES AND POLYGONS:**
    *   For a simple rectangle, use `Rectangle(width=W, height=H, color=C)`. The `Rectangle` class DOES NOT accept a `corner_radius` argument.
    *   For a rectangle with rounded corners, you MUST use `RoundedRectangle(corner_radius=0.2, width=3, height=1, color=BLUE)`.
    *   When creating a `Polygon` with multiple vertices, pass each vertex (which can be a Manim vector like `LEFT`, `UP`, or an explicit coordinate like `np.array([1,1,0])` or `[1,1,0]`) as a separate argument to `Polygon`. 
        CORRECT: `my_poly = Polygon(LEFT, UP, RIGHT, color=BLUE)` 
        CORRECT: `my_poly = Polygon([-1,-1,0], [1,-1,0], [1,1,0], [-1,1,0], color=GREEN)`
        INCORRECT (DO NOT DO THIS): `my_poly = Polygon([LEFT, UP, RIGHT, DOWN], color=BLUE)` (i.e., do not pass a list of vectors/points as the *first single* argument if you intend them to be separate vertices).

5.  **RATE FUNCTIONS (e.g., `smooth`, `linear`):**
    *   If you want to apply a rate function to an animation, it MUST be passed as the `rate_func` keyword argument to the `self.play()` method itself.
    *   CORRECT USAGE: `self.play(FadeIn(my_object), Create(another_object), rate_func=smooth, run_time=2)`
    *   INCORRECT USAGE (DO NOT DO THIS): `self.play(FadeIn(my_object, rate_func=smooth))` or `self.play(Create(my_object, rate_functions=linear))`.

6.  **SCENE CLASS:**
    *   Define one main scene class that inherits from `Scene`. Consistently name this class `ManimScene` (e.g., `class ManimScene(Scene):`). The backend service will use this name.
    *   The `construct(self)` method of this scene should NOT call `super().construct()` if it directly inherits from `manim.Scene`.

7.  **VALID MANIM API:** Ensure all Manim classes and functions used are standard parts of the Manim Community library (v0.18+) and are used with correct arguments. Do not use non-existent animation classes or pass invalid keyword arguments.

8.  **CONCISENESS:** The animation should be relatively simple and render quickly for testing (suitable for Manim's `-ql` flag).

9.  **HELPER FUNCTIONS:** If you define helper functions outside the main scene class:
    *   They must be called directly by their name (e.g., `result = my_helper_function(args)`), NOT using `self.` 
    *   INCORRECT USAGE (DO NOT DO THIS): `self.my_helper_function(args)` for a function that is defined globally.
    *   If you want to call the function with `self.`, then define it as a method INSIDE the scene class.
    *   Be consistent: either define all helper functions as class methods, or all as global functions.

10. **CAMERA MANIPULATION (2D SCENES):**
    *   For camera actions like zooming or panning in a 2D `Scene`, manipulate `self.camera.frame`.
    *   Use the `.animate` syntax for these camera frame animations. For example:
        *   To zoom out (make things appear smaller): `self.play(self.camera.frame.animate.scale(1.2))`
        *   To zoom in (make things appear larger): `self.play(self.camera.frame.animate.scale(0.8))`
        *   To pan/move the camera's view: `self.play(self.camera.frame.animate.move_to(SOME_MOBJECT_OR_POINT))`
    *   Avoid unusual or direct manipulations of `self.camera` object itself unless it's a well-established Manim pattern for a specific effect.

11. **PYTHON FUNCTION CALLS & ANIMATION SEQUENCES:**
    *   Remember Python's function call syntax: once a keyword argument is used, all subsequent arguments must also be keyword arguments.
    *   For `self.play()` with multiple animations and settings, use one of these patterns:
        *   **CORRECT:** `self.play(animation1, animation2, run_time=1, rate_func=linear)`
        *   **CORRECT:** For sequential animations, use separate `self.play()` calls:
            ```python
            self.play(animation1, run_time=0.5)
            self.play(animation2, run_time=0.5)
            ```
        *   **CORRECT:** For complex sequences, use `Succession` or `LaggedStart`:
            ```python
            self.play(Succession(animation1, animation2), run_time=2)
            ```
        *   **INCORRECT:** Do NOT mix keyword and positional arguments like this:
            ```python
            self.play(animation1, run_time=0.5, animation2)  # SyntaxError!
            ```

Remember to output *only* the Python code block.
''',
    description="Generates asset-free Manim code with strict rules for shapes, colors, rate functions, and no external files.",
    output_key='generated_code',
)


# Code Reviewer Agent
# Takes the code generated by the previous agent (read from state) and provides feedback.
code_reviewer_agent = LlmAgent(
    name="CodeReviewerAgent",
    model=LiteLlm(model="openai/gpt-4o"),
    instruction="""You are an expert Python Code Reviewer. 
    Your task is to provide constructive feedback on the provided code.

    **Code to Review:**
    ```python
    {generated_code}
    ```

**Review Criteria:**
1.  **Correctness:** Does the code work as intended? Are there logic errors?
2.  **Readability:** Is the code clear and easy to understand? Follows PEP 8 style guidelines?
3.  **Efficiency:** Is the code reasonably efficient? Any obvious performance bottlenecks?
4.  **Edge Cases:** Does the code handle potential edge cases or invalid inputs gracefully?
5.  **Best Practices:** Does the code follow common Python best practices?

**Output:**
Provide your feedback as a concise, bulleted list. Focus on the most important points for improvement.
If the code is excellent and requires no changes, simply state: "No major issues found."
Output *only* the review comments or the "No major issues" statement.
""",
    description="Reviews code and provides feedback.",
    output_key="review_comments",
)


# Code Refactorer Agent
# Takes the original code and the review comments (read from state) and refactors the code.
code_refactorer_agent = LlmAgent(
    name="CodeRefactorerAgent",
    model=LiteLlm(model="openai/gpt-4o"),
    instruction="""You are a Python Code Refactoring AI.
Your goal is to improve the given Python code based on the provided review comments.

  **Original Code:**
  ```python
  {generated_code}
  ```

  **Review Comments:**
  {review_comments}

**Task:**
Carefully apply the suggestions from the review comments to refactor the original code.
If the review comments state "No major issues found," return the original code unchanged.
Ensure the final code is complete, functional, and includes necessary imports and docstrings.

**Output:**
Output *only* the final, refactored Python code block, enclosed in triple backticks (```python ... ```). 
Do not add any other text before or after the code block.
""",
    description="Refactors code based on review comments.",
    output_key="refactored_code",
)


# --- 2. Create the Sequential Orchestration Agent ---

root_agent = SequentialAgent(
    name="root_agent",  # Must be named root_agent for ADK compatibility
    description="Executes a pipeline to generate a Manim animation from a concept.",
    #     instruction="""
    # Follow these steps in order to generate a Manim video from a user-supplied concept:
    # 1. Generate a clear explanation of the topic.
    # 2. Break the explanation into distinct concepts.
    # 3. Create a storyboard to teach those concepts.
    # 4. Enhance the storyboard with narration and visual ideas.
    # 5. Generate Manim code to animate the storyboard.
    # """,
    sub_agents=[
        clear_explanation_agent,
        concept_separator_agent,
        storyboard_creator_agent,
        storyboard_enhancer_agent,
        code_generator_agent,
        code_reviewer_agent,
        code_refactorer_agent
    ],
)
