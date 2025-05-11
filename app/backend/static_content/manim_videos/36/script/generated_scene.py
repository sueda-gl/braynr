from manim import *
import numpy as np

class ManimScene(Scene):
    def construct(self):
        # Intro (2 seconds)
        title = Text("Image Processing Explained")
        self.play(FadeIn(title, rate_functions=smooth))
        self.wait(2)
        self.play(FadeOut(title, rate_functions=smooth))

        # Scene 1: The Upload (5 seconds)
        hand = Text("🖐️")  # Simple hand representation
        image_icon = Square(side_length=1, color=BLUE)
        landscape_lines = [
            Line(start=image_icon.get_center() + 0.2 * LEFT + 0.2 * UP, end=image_icon.get_center() + 0.2 * RIGHT + 0.2 * UP, color=GREEN),
            Line(start=image_icon.get_center() + 0.2 * LEFT, end=image_icon.get_center() + 0.2 * RIGHT, color=GREEN),
            Line(start=image_icon.get_center() + 0.2 * LEFT + 0.2 * DOWN, end=image_icon.get_center() + 0.2 * RIGHT + 0.2 * DOWN, color=BLUE),
        ]
        image_group = VGroup(image_icon, *landscape_lines)

        progress_bar = Rectangle(width=2, height=0.2, color=BLUE).shift(DOWN * 1.5)
        progress_fill = Rectangle(width=0, height=0.2, color=BLUE).move_to(progress_bar.get_left()).align_to(progress_bar, LEFT)

        error_symbol = Triangle(color=RED, fill_opacity=1).scale(0.5)
        error_symbol_exclamation = Text("!", color=WHITE).scale(1.2).move_to(error_symbol.get_center())
        error_group = VGroup(error_symbol, error_symbol_exclamation)

        fail_text = Text("Image Processing Failed", color=RED).scale(0.7).shift(UP*1.5)

        self.play(hand.animate.move_to(image_group.get_center()+2*RIGHT+2*UP, rate_functions=smooth))
        self.play(hand.animate.move_to(image_group.get_center(), rate_functions=smooth), Create(image_group, rate_functions=smooth))

        self.play(Create(progress_bar, rate_functions=smooth))
        self.play(progress_fill.animate.stretch_to_right(progress_bar.get_right()*0.8, rate_functions=smooth), run_time=1)
        self.wait(1)
        self.play(Transform(progress_bar, error_group, rate_functions=smooth), FadeOut(progress_fill, rate_functions=smooth))
        # Use Transform to subtly scale image_group instead of shifting
        self.play(Transform(image_group, image_group.copy().scale(0.95)), FadeIn(fail_text, rate_functions=smooth), run_time=0.5)
        self.play(Transform(image_group, image_group.copy().scale(1/0.95)), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(image_group, progress_bar, fail_text, hand, rate_functions=smooth))

        # Scene 2: System's Perspective (7 seconds)
        module1 = RoundedRectangle(corner_radius=0.2, width=2, height=1, color=BLUE).shift(LEFT*3)
        module2 = RoundedRectangle(corner_radius=0.2, width=2, height=1, color=BLUE).shift(RIGHT*3)
        module1_text = Text("Image Processing Module", color=WHITE).scale(0.4).move_to(module1.get_center())
        # Use StreamLines for better data flow visualization
        stream_lines = StreamLines(
            start_points=LEFT*5 + np.random.normal(0, 0.2, size=(20, 3)),
            vector_field=lambda p: module1.get_center() - p,
            color=YELLOW
        )
        stream_lines2 = StreamLines(
            start_points=module1.get_right() + np.random.normal(0, 0.2, size=(20, 3)),
            vector_field=lambda p: module2.get_center() - p,
            color=YELLOW
        )
        red_x = Tex("X", color=RED).scale(3).move_to(module1.get_center())

        code_snippet = Text("Some code here\nwith an error", color=WHITE, font_size = 18).move_to(module1.get_center()+2*DOWN) # Increased font_size

        self.play(Create(module1, rate_functions=smooth), Create(module2, rate_functions=smooth))
        self.play(Write(module1_text, rate_functions=smooth))
        self.play(Create(stream_lines, rate_functions=smooth))
        self.play(stream_lines.animate.become(stream_lines2), run_time = 1)
        self.play(FadeIn(red_x, rate_functions=smooth), FadeIn(code_snippet, rate_functions=smooth))
        self.wait(1)
        self.play(module1.animate.set_color(RED), rate_functions=smooth)
        self.play(FadeOut(module1, module2, module1_text, stream_lines2, red_x, code_snippet, rate_functions=smooth))

        # Common elements for Scenes 3 and 4
        def create_chat_elements():
            chat_bg = Rectangle(width=8, height=5, color=GRAY, fill_opacity=0.2)
            ai_avatar = Circle(radius=0.5, color=TEAL, fill_opacity=1).shift(LEFT * 3)
            robot_head = Rectangle(width = 0.3, height = 0.3, color = WHITE).move_to(ai_avatar.get_center()+0.1*UP)
            robot_eye1 = Circle(radius = 0.05, color = BLACK).move_to(robot_head.get_center()+0.1*LEFT+0.05*UP)
            robot_eye2 = Circle(radius = 0.05, color = BLACK).move_to(robot_head.get_center()+0.1*RIGHT+0.05*UP)
            robot_mouth = Line(start = robot_head.get_center() + 0.1 * DOWN + 0.1 * LEFT, end = robot_head.get_center() + 0.1*DOWN + 0.1*RIGHT)
            return chat_bg, ai_avatar, robot_head, robot_eye1, robot_eye2, robot_mouth
        
        # Scene 3: Request for Description (6 seconds)
        chat_bg, ai_avatar, robot_head, robot_eye1, robot_eye2, robot_mouth = create_chat_elements()
        ai_bubble = RoundedRectangle(corner_radius=0.3, width=4, height=1, color=WHITE, fill_opacity=1).next_to(ai_avatar, RIGHT)
        ai_message = Text("I couldn't process the image.\nCan you describe what it is?", color=BLACK, font_size=18).move_to(ai_bubble.get_center())
        input_field = Rectangle(width=6, height=0.5, color=WHITE, fill_opacity=1).shift(DOWN * 2)
        cursor = Line(start=input_field.get_left() + 0.2 * RIGHT, end=input_field.get_left() + 0.2 * RIGHT + UP * 0.3, color=BLACK).move_to(input_field.get_left()+0.2*RIGHT).align_to(input_field.get_left()+0.2*RIGHT, LEFT)

        self.play(Create(chat_bg, rate_functions=smooth))
        self.play(Create(ai_avatar, rate_functions=smooth), Create(robot_head, rate_functions=smooth), Create(robot_eye1, rate_functions=smooth), Create(robot_eye2, rate_functions=smooth), Create(robot_mouth, rate_functions=smooth))
        self.play(Create(ai_bubble, rate_functions=smooth), Write(ai_message, rate_functions=smooth))
        self.play(Create(input_field, rate_functions=smooth), Create(cursor, rate_functions=smooth))
        self.play(cursor.animate.shift(0.1*RIGHT, rate_functions=there_and_back), run_time = 0.5)
        self.play(cursor.animate.shift(-0.1*RIGHT, rate_functions=there_and_back), run_time = 0.5)
        self.wait(2)
        self.play(FadeOut(chat_bg, ai_avatar, ai_bubble, ai_message, input_field, cursor, robot_head, robot_eye1, robot_eye2, robot_mouth, rate_functions=smooth))

        # Scene 4: Offer to Explain (7 seconds)
        chat_bg, ai_avatar, robot_head, robot_eye1, robot_eye2, robot_mouth = create_chat_elements()

        thinking_bubble = Circle(radius=0.3, color=BLUE, fill_opacity=0.5).next_to(ai_avatar, UP)
        dots = [Dot(color=WHITE).move_to(thinking_bubble.get_center()+0.1*LEFT), Dot(color=WHITE).move_to(thinking_bubble.get_center()), Dot(color=WHITE).move_to(thinking_bubble.get_center()+0.1*RIGHT)]
        ai_bubble2 = RoundedRectangle(corner_radius=0.3, width=5, height=1, color=WHITE, fill_opacity=1).next_to(ai_avatar, RIGHT)
        ai_message2 = Text("If you tell me what the image is about,\nI can still explain it to you.", color=BLACK, font_size=18).move_to(ai_bubble2.get_center())
        # Directly create the concept_word Text object
        concept_word = Text("concept", color=YELLOW, font_size=18).move_to(ai_message2.get_center() + 0.2*DOWN)
        check_mark = Tex(r"\checkmark", color=GREEN).next_to(ai_bubble2, RIGHT)


        self.play(Create(chat_bg, rate_functions=smooth))
        self.play(Create(ai_avatar, rate_functions=smooth), Create(robot_head, rate_functions=smooth), Create(robot_eye1, rate_functions=smooth), Create(robot_eye2, rate_functions=smooth), Create(robot_mouth, rate_functions=smooth))
        self.play(Create(thinking_bubble, rate_functions=smooth))
        self.play(*[Create(dot, rate_functions=smooth) for dot in dots])
        self.wait(1)

        self.play(Create(ai_bubble2, rate_functions=smooth), Write(ai_message2, rate_functions=smooth))
        self.play(Create(concept_word, rate_functions=smooth)) # Directly create it

        self.play(*[FadeOut(dot, rate_functions=smooth) for dot in dots])
        self.play(FadeOut(thinking_bubble, rate_functions=smooth))
        self.play(Create(check_mark, rate_functions=smooth))
        self.wait(2)
        self.play(FadeOut(chat_bg, ai_avatar, ai_bubble2, ai_message2, check_mark, concept_word, robot_head, robot_eye1, robot_eye2, robot_mouth, rate_functions=smooth))


        # Outro (3 seconds)
        outro_text = Text("Learn more about AI!", color=BLUE)
        website_text = Text("www.example.com", color=GRAY, font_size=24).next_to(outro_text, DOWN) #Ensured Valid URL

        self.play(FadeIn(outro_text, rate_functions=smooth), FadeIn(website_text, rate_functions=smooth))
        self.wait(2)
        self.play(FadeOut(outro_text, website_text, rate_functions=smooth)) # Explicit fadeout

        self.play(FadeOut(*self.mobjects, rate_functions=smooth))