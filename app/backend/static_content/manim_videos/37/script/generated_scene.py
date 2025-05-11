from manim import *
import numpy as np

class ManimScene(Scene):
    def construct(self):
        # Scene 1: The Request - Confused Robot
        robo = VGroup(
            Circle(radius=1, color=BLUE),  # Head
            Rectangle(width=1.5, height=2, color=BLUE, stroke_width=2).shift(DOWN * 1.5),  # Body
            Line(start=LEFT, end=RIGHT, color=BLUE).shift(DOWN * 0.5),  # Arms
            Line(start=DOWN + LEFT, end=DOWN + RIGHT, color=BLUE).shift(DOWN * 2.5)  # Legs
        )
        self.play(FadeIn(robo, run_time=2))

        num_question_marks = 5
        question_marks = VGroup()
        for i in range(num_question_marks):
            q = Text("?", font_size=24, color=YELLOW)
            q.move_to(robo.get_center() + np.array([np.random.uniform(-1, 1), np.random.uniform(1, 2), 0]))
            question_marks.add(q)
        self.play(Create(question_marks), run_time=1)

        # Define ValueTrackers for the question marks' movement
        y_offsets = [ValueTracker(np.random.uniform(0.1, 0.3)) for _ in range(num_question_marks)]

        def update_question_marks(group):
            for i, q in enumerate(group):
                q.move_to(robo.get_center() + np.array([
                    np.random.uniform(-1, 1) * 0.75,  # Reduced horizontal movement
                    1.5 + np.sin(self.time + i) * y_offsets[i].get_value(), #Smoother bobbing
                    0
                ]))

        question_marks.add_updater(update_question_marks)
        self.add(question_marks)


        tablet = Rectangle(width=2, height=3, color=WHITE).shift(RIGHT * 2)
        text_input = Text("jııj", font_size=36, color=BLACK).move_to(tablet.get_center())
        self.play(Create(tablet), Create(text_input), run_time=2)

        self.wait(3)
        self.play(FadeOut(question_marks), run_time=1)

        # Scene 2: Image Data Arrives - Base64 Stream
        self.play(tablet.animate.scale(3).move_to(ORIGIN),
                  text_input.animate.move_to(UP*3), run_time=2) #Zoom in tablet

        base64_header = Text("data:image/png;base64,", font_size=24, color=GREEN)
        base64_text = Text("".join([chr(np.random.randint(97, 123)) for _ in range(500)]),
                              font_size=12, color=WHITE, font="monospace")

        base64_group = VGroup(base64_header, base64_text).arrange(DOWN, aligned_edge=LEFT).move_to(ORIGIN)
        base64_text.shift(DOWN)

        code_background = Rectangle(width=7, height=5, color=BLACK, fill_opacity=1).move_to(ORIGIN)
        self.add(code_background)
        self.play(Write(base64_group), run_time=2)
        self.add(base64_group)

        self.play(base64_group.animate.shift(UP * 5), run_time=5, rate_func=linear)
        self.wait(1)

        surrounding_rect = SurroundingRectangle(base64_header, color=YELLOW, buff=0.1)
        self.play(Create(surrounding_rect), run_time=3)
        self.wait(2)
        self.play(FadeOut(surrounding_rect), run_time=1)

        # Scene 3: Inability to Process - Brain Freeze
        self.play(tablet.animate.scale(1/3).move_to(RIGHT * 2),
                  base64_group.animate.move_to(text_input.get_center()))
        self.remove(base64_group, code_background)
        self.add(text_input)

        smoke = VGroup()
        num_particles = 50
        SMOKE_Y_LIMIT = 3

        def random_color():
            r, g, b = np.random.uniform(0.3, 0.7, size=3)
            return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

        # Pre-calculate random shifts for all smoke particles
        shifts = [np.array([np.random.uniform(-0.1, 0.1), np.random.uniform(0, 0.2), 0]) for _ in range(num_particles)]

        for i in range(num_particles):
            dot = Dot(color=random_color(), radius=0.05)
            dot.move_to(robo.get_center() + UP)
            smoke.add(dot)

        def update_smoke(group, dt):
            for i, dot in enumerate(group):
                dot.shift(shifts[i])
                if dot.get_y() > SMOKE_Y_LIMIT:
                    dot.move_to(robo.get_center() + UP)

        smoke.add_updater(update_smoke)
        self.add(smoke)

        error_message = Text("ERROR", color=RED, font_size=48).shift(UP * 2)
        self.play(FadeIn(error_message), run_time=0.5)

        error_message.add_updater(lambda mob, dt: mob.become(Text("ERROR", color=RED, font_size=48).shift(UP * 2).set_opacity(0.2 if self.time % 0.5 > 0.25 else 1)))
        self.add(error_message)

        self.play(robo.animate.shift(np.array([0.1, 0.05, 0])).shift(np.array([-0.1, -0.05, 0])).repeat(3))
        self.wait(2)

        # Scene 4: Limitation Explained - Apology
        self.play(FadeOut(smoke), FadeOut(error_message), run_time=2)
        speech_bubble = VGroup(
            Polygon([LEFT, UP, RIGHT, DOWN], color=WHITE),
            Text("I cannot do what you're asking.", color=BLACK, font_size=24).move_to(DOWN*0.1)
        ).scale(0.7).next_to(robo, RIGHT)
        self.play(Create(speech_bubble), robo.animate.shift(DOWN*0.2), run_time=2) #Sad Robo

        self.wait(4)
        self.play(FadeOut(robo), FadeOut(speech_bubble), FadeOut(tablet), run_time=1)


        # Scene 5: Data Transfer Issue - Roadblock
        road = Line(start=LEFT * 5, end=RIGHT * 5, color=GRAY).shift(DOWN * 2)
        self.play(Create(road), run_time=2)

        sign = VGroup(
            Rectangle(width=2, height=1, color=WHITE),
            Text("BASE64 ONLY", color=BLACK, font_size=24)
        ).arrange(DOWN).shift(UP * 0.5 + LEFT * 3)
        self.play(Create(sign), run_time=1)

        truck = VGroup(
            Rectangle(width=1, height=0.5, color=BLUE),  # Body
            Circle(radius=0.2, color=BLACK).shift(DOWN * 0.5 + LEFT * 0.5),  # Wheel 1
            Circle(radius=0.2, color=BLACK).shift(DOWN * 0.5 + RIGHT * 0.5),  # Wheel 2
            Rectangle(width=0.4, height=0.3, color=GREEN).move_to(truck.get_center()+UP*0.2) # Image data
        ).scale(0.7).shift(LEFT * 5 + DOWN*1.5)

        self.play(Create(truck), run_time=3)

        roadblock = VGroup(
            Rectangle(width=0.2, height=1, color=RED).shift(RIGHT * 1.5 + DOWN * 1),
            Rectangle(width=0.2, height=1, color=RED).shift(RIGHT * 1.7 + DOWN * 1),
            Rectangle(width=0.2, height=1, color=RED).shift(RIGHT * 1.9 + DOWN * 1)
        ).shift(DOWN*0.5)
        self.play(Create(roadblock), run_time=2)

        self.wait(2)