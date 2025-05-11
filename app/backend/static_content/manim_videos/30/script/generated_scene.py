from manim import *

class ExplainingComplexTopic(Scene):
    def construct(self):
        """
        A scene explaining the process of understanding and explaining a complex topic.
        It includes scenes representing lack of information, inability to explain,
        the moment of clarity, and finally, a successful explanation.
        """

        # --- Initial Objects (declared outside scenes for reusability) ---
        desk = Rectangle(width=6, height=3, color=GRAY).shift(LEFT * 5)
        laptop_screen = Rectangle(width=3, height=2, color=BLACK).shift(desk.get_center() + UP * 1)
        white_document = Rectangle(width=2.8, height=1.8, color=WHITE).move_to(laptop_screen.get_center())
        sarah = Circle(radius=0.5, color=BLUE) # Sarah's initial definition without position
        sarah.rotate(PI)  # Facing away initially

        # --- Scene 1: The Blank Page (Lack of Information) ---
        self.play(Create(desk), run_time=1)

        sarah.move_to(desk.get_center() + DOWN * 0.5) # Position Sarah in scene 1
        self.play(FadeIn(sarah), run_time=1.5)  # Use FadeIn instead of Create
        self.play(sarah.animate.rotate(-PI)) # Face forward

        self.play(GrowFromCenter(laptop_screen), run_time=0.75)
        self.play(Write(white_document), run_time=1)

        # Representing Sarah's confusion with eyebrows
        brow = Line(start=sarah.get_center() + UP * 0.7 + LEFT * 0.2, end=sarah.get_center() + UP * 0.7 + LEFT * 0.4, color=BLACK)
        brow2 = Line(start=sarah.get_center() + UP * 0.7 + RIGHT * 0.2, end=sarah.get_center() + UP * 0.7 + RIGHT * 0.4, color=BLACK)
        self.play(Create(brow), Create(brow2), run_time=0.5)

        # Question mark to symbolize confusion
        question_mark = Text("?", font_size=48, color=YELLOW).shift(sarah.get_center() + UP * 2)
        self.play(FadeIn(question_mark), run_time=1)
        self.play(question_mark.animate.scale(1.1), run_time=0.5)
        self.play(question_mark.animate.scale(0.9), run_time=0.5)
        self.wait(1)

        # Fade out objects in scene 1
        self.play(FadeOut(question_mark, brow, brow2))

        # Zoom out and transition to white
        self.play(
            ZoomedOut(desk, zoom_factor=0.5),
            FadeOut(sarah, laptop_screen, white_document), # Fade out all at once
            run_time=0.5
        )
        self.play(FadeToColor(VGroup(desk), WHITE), run_time = 0.5)
        self.wait(0.5)

        # --- Scene 2: Mumbled Explanation (Inability to Explain) ---
        speech_bubble = white_document.copy().scale(0.3).move_to(LEFT * 4 + UP * 2)
        self.play(Transform(white_document, speech_bubble), run_time=0.75)

        sarah.move_to(LEFT * 3 + DOWN * 1) # Move Sarah to scene 2's position
        friend = Circle(radius=0.5, color=GREEN).shift(RIGHT * 3 + DOWN * 1)

        self.play(FadeIn(sarah), Create(friend), run_time=1) # Use FadeIn for Sarah

        # Create symbols for jumbled explanation
        symbols = VGroup(*[
            Tex(s, font_size=24) for s in ["α", "β", "∫", "∑", "?", "x=y+z"]
        ]).arrange(DOWN, buff=0.2).move_to(LEFT * 3 + UP * 2)

        # Simplified speech bubble creation
        speech_bubbles = VGroup()
        for i, symbol in enumerate(symbols):
            speech_bubble_i = SpeechBubble().scale(0.5).move_to(sarah.get_center() + UP * 1.5 + LEFT * 0.5 * (i % 2))
            speech_bubble_i.add(symbol.move_to(speech_bubble_i.get_center()))
            speech_bubbles.add(speech_bubble_i)
        self.play(Create(speech_bubbles), run_time = 2)

        # Confused eyebrows for the friend
        confused_brow = Line(start=friend.get_center() + UP * 0.7 + LEFT * 0.2, end=friend.get_center() + UP * 0.7 + LEFT * 0.4, color=BLACK)
        confused_brow2 = Line(start=friend.get_center() + UP * 0.7 + RIGHT * 0.2, end=friend.get_center() + UP * 0.7 + RIGHT * 0.4, color=BLACK)
        self.play(Create(confused_brow), Create(confused_brow2), run_time=0.5)

        # Question marks above the friend's head, adjusted for better placement
        friend_question_marks = VGroup(*[
            Text("?", font_size=24, color=YELLOW).shift(friend.get_center() + UP * 1.5 + LEFT * 0.75 + RIGHT * 0.75 * i)
            for i in range(3)
        ])
        self.play(FadeIn(friend_question_marks), run_time=1)
        self.wait(0.5)

        # Fade out multiple objects at once
        self.play(FadeOut(*speech_bubbles, confused_brow, confused_brow2, friend_question_marks), run_time = 0.75)

        # --- Scene 3: The Lightbulb Moment (Requirement for a Clear Hint) ---
        # Sarah remains in the same position as the previous scene
        self.play(FadeIn(sarah), run_time=0.5) # FadeIn Sarah

        # Desk, laptop_screen, and white_document are already created, so just fade them in
        self.play(
            Create(desk),
            GrowFromCenter(laptop_screen),
            Write(white_document),
            run_time = 0.75
        )

        # Lightbulb moment
        lightbulb = Circle(radius=0.5, color=YELLOW).shift(sarah.get_center() + UP * 2)
        self.play(GrowFromCenter(lightbulb), run_time=1)

        # Displaying a clear definition
        definition = Text("Definition:\nA clear and concise\nexplanation.", font_size=24).move_to(laptop_screen.get_center())
        definition_box = SurroundingRectangle(definition, color=BLUE)
        self.play(Create(definition_box), Write(definition), run_time=2)

        # Magnifying glass to emphasize the definition
        magnifying_glass = Circle(radius=0.3, color=WHITE, fill_opacity=0.2).shift(LEFT * 1.5 + UP * 0.5).move_to(definition.get_center() + LEFT * 2)
        handle = Rectangle(width=0.1, height=0.5, color=WHITE).move_to(magnifying_glass.get_center() + DOWN * 0.5)
        self.play(magnifying_glass.animate.shift(RIGHT * 4), Create(handle), run_time=1.5)

        self.play(FadeOut(lightbulb), run_time = 0.5)

        # --- Scene 4: Clear Explanation (Success!) ---
        # Sarah and friend remain in the same positions as before
        friend.move_to(RIGHT * 3 + DOWN * 1)
        self.play(FadeIn(sarah, friend), run_time = 1)

        # Whiteboard for visual explanation
        whiteboard = Rectangle(width=4, height=3, color=WHITE).shift(LEFT * 1 + UP * 0.5)
        self.play(Create(whiteboard), run_time=0.5)

        # Dynamic diagram creation (example: a simple concept map)
        node1 = Circle(radius=0.2, color=BLUE).shift(LEFT * 1 + UP * 1.5)
        node2 = Circle(radius=0.2, color=BLUE).shift(LEFT * 1 + DOWN * 0.5)
        arrow = Arrow(start=LEFT * 1 + UP * 1.3, end=LEFT * 1 + DOWN * 0.3)
        label1 = Text("Concept A", font_size=18).next_to(node1, UP)
        label2 = Text("Concept B", font_size=18).next_to(node2, DOWN)

        diagram = VGroup(node1, node2, arrow, label1, label2)
        self.play(Create(diagram), run_time=2)

        # Checkmark to indicate understanding
        checkmark = Tex(r"\checkmark", color=GREEN, font_size=48).shift(friend.get_center() + UP * 1.5)
        self.play(FadeIn(checkmark), run_time = 1)
        self.wait(0.5)
        self.play(FadeOut(checkmark), run_time = 0.25)

        # Zoom out and fade to black
        self.play(
            ZoomedOut(whiteboard, zoom_factor=1.5), # Reduced zoom factor
            run_time = 1.5
        )
        self.play(FadeToColor(VGroup(whiteboard), BLACK))
        self.wait(0.5)