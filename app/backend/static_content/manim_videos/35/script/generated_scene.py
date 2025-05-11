from manim import *
import numpy as np

class DataUnderstandingScene(Scene):
    def construct(self):
        # Scene 1: Initial Processing Attempt (0:00 - 0:04)
        screen = Rectangle(width=6, height=4, color=BLUE, stroke_width=3, corner_radius=0.5)
        self.play(Create(screen), run_time=1)

        pixels = []
        for i in range(1000):
            x = np.random.uniform(-screen.width/2 + 0.1, screen.width/2 - 0.1)
            y = np.random.uniform(-screen.height/2 + 0.1, screen.height/2 - 0.1)
            color = "#{:02x}{:02x}{:02x}".format(np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
            pixel = Dot(point=[x, y, 0], color=color, radius=0.02)
            pixels.append(pixel)

        self.play(*[Create(p) for p in pixels], run_time=2)

        processing_text = Text("Processing...", font_size=24, color=WHITE).move_to(screen.get_bottom() + DOWN * 0.5)
        loading_dots = VGroup(*[Dot(radius=0.05) for _ in range(3)]).arrange(RIGHT).next_to(processing_text, RIGHT, buff=0.2)
        self.play(Write(processing_text), Create(loading_dots))

        # Loading bar simulation
        loading_bar = Rectangle(width=0, height=0.1, color=GREEN).move_to(screen.get_bottom() + DOWN * 0.8)
        self.play(Create(loading_bar))
        self.play(loading_bar.animate.set(width=screen.width * 0.3), run_time=1) # Increase loading bar slightly

        self.play(loading_dots[0].animate.set_opacity(0.2), run_time=0.3)
        self.play(loading_dots[1].animate.set_opacity(0.2), run_time=0.3)
        self.play(loading_dots[2].animate.set_opacity(0.2), run_time=0.3)
        self.play(loading_dots[0].animate.set_opacity(1), run_time=0.3)
        self.play(loading_dots[1].animate.set_opacity(1), run_time=0.3)
        self.play(loading_dots[2].animate.set_opacity(1), run_time=0.3)

        self.wait(1)
        self.play(FadeOut(screen, *pixels, processing_text, loading_dots, loading_bar), run_time=1)

        # Scene 2: Error Encountered (0:04 - 0:08)
        blurred_pixels = []
        for p in pixels:
           blurred_pixels.append(Dot(point=p.get_center(), color=p.get_color(), radius=0.02, opacity=0.3))
        self.add(*blurred_pixels)
        self.bring_to_back(*blurred_pixels)

        error_box = Rectangle(width=4, height=2, color=RED, fill_opacity=0.8).move_to(processing_text.get_center())
        error_text = Text("Unable to decode image", font_size=24, color=WHITE).move_to(error_box.get_center())
        warning_icon = Triangle(color=YELLOW).scale(0.2).move_to(error_box.get_left() + LEFT * 0.5)
        exclamation = Tex("!", color=BLACK).scale(1.5).move_to(warning_icon.get_center())
        warning_icon.add(exclamation)

        self.play(Transform(processing_text, error_box), Write(error_text), Create(warning_icon), run_time=0.5) # Smoother transition


        self.wait(2)
        self.play(
            FadeOut(error_box, error_text, warning_icon, *blurred_pixels),
            self.camera.frame.animate.scale(0.5),
            run_time=1
        )

        # Scene 3: Lack of Meaningful Content (0:08 - 0:12)
        self.camera.background_color = WHITE
        self.clear()
        self.camera.frame.scale(1)
        
        speck = Dot(color=BLUE, radius=0.01).move_to(ORIGIN)
        self.play(Create(speck))
        self.wait(1)

        magnifying_glass = Circle(radius=0.5, color=GRAY, stroke_width=2)
        handle = Line(start=magnifying_glass.get_bottom(), end=magnifying_glass.get_bottom() + DOWN + RIGHT * 0.5, color=GRAY, stroke_width=2)
        magnifying_glass_group = VGroup(magnifying_glass, handle)
        magnifying_glass_group.move_to(speck.get_center() + UP * 2)  # Start above the speck
        self.play(Create(magnifying_glass_group))
        self.play(magnifying_glass_group.animate.move_to(speck.get_center()), run_time=0.5) # Move towards speck

        self.wait(0.5)
        self.play(FadeOut(magnifying_glass_group), self.camera.frame.animate.scale(2), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(speck), run_time=0.5)

        # Scene 4: Absence of Understandable Information (Text) (0:12 - 0:16)
        text_box = Rectangle(width=3, height=1, color=BLUE, fill_opacity=0.2)
        self.play(Create(text_box))

        jkjg_text = Text("", font_size=48, color=BLACK).move_to(text_box.get_center())
        self.play(Write(jkjg_text), run_time=0.2) #Initial write, it will be updated
        for i, char in enumerate("jkjg"):
            new_text = Text(jkjg_text.text + char, font_size=48, color=BLACK).move_to(text_box.get_center())
            self.play(Transform(jkjg_text, new_text), jkjg_text.animate.scale(1.1).set_color(RED), run_time=0.3) # Emphasis on each letter
            self.play(jkjg_text.animate.scale(1).set_color(BLACK), run_time = 0.1) #Return to original

        self.wait(1)
        self.play(
            self.camera.frame.animate.scale(0.7).rotate(0.1 * PI),
            run_time=1
        )

        # Scene 5: The Question Mark (0:16 - 0:22)
        self.clear()
        self.camera.background_color = BLACK
        question_mark = Tex("?", font_size=144, color=WHITE)

        # Create a blurred background by creating small, faded squares
        num_squares = 200
        x_coords = np.random.uniform(-FRAME_WIDTH / 2, FRAME_WIDTH / 2, num_squares)
        y_coords = np.random.uniform(-FRAME_HEIGHT / 2, FRAME_HEIGHT / 2, num_squares)
        sizes = np.random.uniform(0.1, 0.3, num_squares)
        background_squares = VGroup(*[
            Square(side_length=sizes[i], fill_color=BLUE, fill_opacity=0.1, stroke_width=0).move_to([x_coords[i], y_coords[i], 0])
            for i in range(num_squares)
        ])

        self.add(background_squares)
        self.play(Create(question_mark), run_time=1)
        self.play(question_mark.animate.scale(1.05).set_color(YELLOW), run_time = 1) #Pulsating glow animation
        self.play(question_mark.animate.scale(1).set_color(WHITE), run_time = 1)
        self.wait(2)
        self.play(FadeOut(question_mark, background_squares), run_time=1)
        self.wait(0.5)