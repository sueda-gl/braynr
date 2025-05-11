
from manim import *

class TextExtractionExplanation(Scene):
    def construct(self):
        # --- Scene 1: Initial Image Load - Processing Icon ---
        self.next_section(name="Scene 1: Initial Image Load - Processing Icon")
        
        # Hand and Tablet (Illustrative elements)
        hand = VectorizedPoint(LEFT * 4 + DOWN * 2)  # Placeholder for hand graphic
        tablet = Rectangle(width=3, height=5).shift(RIGHT * 4)
        tablet.set_fill(color=GRAY, opacity=0.8)
        tablet.set_stroke(color=WHITE, width=2)

        self.play(Create(hand), Create(tablet), run_time=1)
        self.wait(0.5)

        # Image (Placeholder - Replace with actual image loading)
        image = Rectangle(width=2.5, height=4).shift(RIGHT * 4) # Placeholder for image
        image.set_fill(color=BLUE_E, opacity=1)
        self.play(FadeIn(image, shift=UP), run_time=2)
        self.wait(0.5)

        # Loading Icon (Dashed circle to indicate processing)
        loading_circle = DashedVMobject(Circle(radius=0.7).shift(RIGHT * 4), num_dashes=30)
        loading_circle.set_color(color=GRAY).set_opacity(0.5)

        self.play(Create(loading_circle))
        self.play(Rotate(loading_circle, angle=2*PI, about_point=loading_circle.get_center()), rate_func=linear, run_time=2,  loop=True)
        self.wait(2) # Keep spinning for a bit

        self.play(FadeOut(loading_circle, run_time=0.6)) #Fading out loading circle

        # --- Scene 2: Processing Failure - Error Symbol ---
        self.next_section(name="Scene 2: Processing Failure - Error Symbol")

        # Error Symbol (A red 'X' mark)
        error_x = Cross(scale=2).shift(RIGHT * 4)
        error_x.set_color(RED)

        # Display error Symbol
        self.play(Create(error_x), run_time =0.5)
        self.play(Wiggle(error_x)) # Add wobble to emphasize the error

        self.wait(1)

        # --- Scene 3: Text Extraction Failed Message ---
        self.next_section(name="Scene 3: Text Extraction Failed Message")

        # Panel (A rounded rectangle for the message box)
        panel = RoundedRectangle(width=6, height=2, corner_radius=0.3).to_edge(DOWN)
        panel.set_fill(color=BLACK, opacity=0.7)
        panel.set_stroke(color=WHITE, width=1)

        # Message Text
        text_failed = MarkupText("Text extraction failed.\nUnable to process the image.", color=WHITE).scale(0.6).move_to(panel.get_center())

        self.play(Create(panel))
        self.play(Write(text_failed), run_time=2)

        self.wait(1)
        self.play(panel.animate.shift(UP * 2), text_failed.animate.shift(UP * 2), run_time=1)
        self.wait(0.5)

        # --- Scene 4: Request for Manual Input ---
        self.next_section(name="Scene 4: Request for Manual Input")

        # Text Box (Where the user will input the text)
        text_box = Rectangle(width=4, height=1, color=WHITE).shift(DOWN * 2)
        text_box.set_fill(color=BLACK, opacity=0.3)
        # Prompt Text (Instructions for the user)
        prompt_text = MarkupText("Please provide the text from the image here:", color=WHITE).scale(0.5).move_to(text_box.get_center() + UP*0.7)
        # Cursor (Blinking cursor in the text box)
        cursor = Line(start=text_box.get_center() + LEFT * 1.9, end=text_box.get_center() + LEFT * 1.9 + UP*0.01, color=WHITE)
        cursor.add_updater(lambda c: c.set_opacity(np.sin(self.time * 5) + 1))

        self.play(Create(text_box))
        self.play(Write(prompt_text), Create(cursor), run_time=2)
        self.wait(1)

        # --- Scene 5: Offer to Explain - Question Mark ---
        self.next_section(name="Scene 5: Offer to Explain - Question Mark")

        # Speech Bubble (To contain the question mark)
        speech_bubble = SVGMobject("speech_bubble.svg") # Use a pre-existing speech bubble SVG file for demonstration purposes
        speech_bubble.scale(0.5).shift(RIGHT * 2 + UP * 0.5)
        # Question Mark
        question_mark = Tex("?").scale(2).move_to(speech_bubble.get_center())
        question_mark.set_color(WHITE)
        
        # ValueTracker for Question Mark Bounce Animation
        bounce_tracker = ValueTracker(0)

        # Animation for Question Mark Bounce
        def bounce(mob):
            alpha = bounce_tracker.get_value()
            initial_pos = mob.get_center()
            vertical_shift = np.sin(alpha * PI) * 0.2  # Adjust amplitude and frequency as needed
            mob.move_to(initial_pos + UP * vertical_shift)

        question_mark.add_updater(bounce)

        # Offer Text
        offer_text = MarkupText("Once you provide the text, I can offer an explanation.", color=WHITE).scale(0.4).move_to(text_box.get_center() + DOWN * 1)

        self.play(Create(speech_bubble), Create(question_mark))
        self.play(Write(offer_text), run_time=2)
        self.play(bounce_tracker.animate.set_value(1), run_time=2, rate_func=there_and_back) # Loop the bounce animation

        self.wait(2)

        # Loop back to Scene 4 (Request for Manual Input)
        self.play(FadeOut(speech_bubble), FadeOut(question_mark), FadeOut(offer_text), run_time=1)
        question_mark.remove_updater(bounce) # Remove the updater to prevent errors
        self.play(FadeIn(text_box), FadeIn(prompt_text), FadeIn(cursor), run_time=1)
        self.wait(1)
