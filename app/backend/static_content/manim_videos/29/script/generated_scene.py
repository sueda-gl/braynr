from manim import *

class ImageProcessingExplanation(Scene):
    def construct(self):
        # Overall color palette
        bg_color = WHITE
        text_color = BLACK
        accent_color = RED
        ai_color = BLUE
        screen_color = WHITE

        # Intro (2 seconds)
        logo = Square(side_length=2, color=accent_color, fill_opacity=0.5).shift(UP * 0.5) # Placeholder logo
        logo_text = Text("Image Processor", color=text_color).scale(0.6).next_to(logo, DOWN)
        self.play(FadeIn(logo, logo_text))
        self.wait(2)
        self.play(FadeOut(logo, logo_text))

        # Scene 1: The Glitch (8 seconds)
        screen = Rectangle(width=6, height=4, color=screen_color, fill_opacity=1).to_edge(LEFT)
        placeholder_image = Square(side_length=2, color=text_color, fill_opacity=0.8).move_to(screen.get_center())
        self.play(Create(screen))
        self.play(Create(placeholder_image))
        self.wait(0.5)
        self.play(FadeOut(placeholder_image)) # Fade out the placeholder image

        # Distort the image
        num_pixels = 50
        pixels = []
        for i in range(num_pixels):
            x = screen.get_center()[0] + np.random.uniform(-2, 2)
            y = screen.get_center()[1] + np.random.uniform(-1.5, 1.5)
            pixel = Square(side_length=0.2, color=random_color(), fill_opacity=1).move_to([x, y, 0])
            pixels.append(pixel)

        self.play(*[TransformFromCopy(placeholder_image, pixel) for pixel in pixels], run_time=2)

        error_messages = [
            Text("Image Corrupted", color=accent_color, font="monospace").scale(0.4).move_to(screen.get_center() + UP * 0.5),
            Text("Processing Error", color=accent_color, font="monospace").scale(0.4).move_to(screen.get_center() + DOWN * 0.5),
        ]
        self.play(FadeIn(error_messages[0]), Flash(error_messages[0]), run_time = 0.5)
        self.play(FadeIn(error_messages[1]), Flash(error_messages[1]), run_time = 0.5)
        self.wait(1)
        error_icon = Triangle(color=accent_color).scale(0.3).to_corner(UR).set_fill(color=accent_color, opacity=0.8)
        exclamation = Tex("!", color=screen_color).scale(0.7).move_to(error_icon.get_center())

        self.play(Create(error_icon), Write(exclamation))
        self.play(error_icon.animate.scale(1.1).set_opacity(0.5).set_fill(color=accent_color).set_color(accent_color),
                    exclamation.animate.scale(1.1), run_time = 1, rate_func=there_and_back)
        self.wait(1)
        distorted_image = Group(*pixels)
        self.distorted_image = distorted_image
        self.error_icon = Group(error_icon, exclamation)
        self.screen = screen

        # Scene 2: The Blind AI (8 seconds)
        self.ai_face = self.create_ai_face()
        question_marks = [Tex("?", color=text_color).scale(0.8).move_to(self.ai_face.get_center() + UP * 1.2 + LEFT * 0.5),
                          Tex("?", color=text_color).scale(0.8).move_to(self.ai_face.get_center() + UP * 0.8 + RIGHT * 0.5),
                          Tex("?", color=text_color).scale(0.8).move_to(self.ai_face.get_center() + DOWN * 0.3)]
        self.play(
            FadeOut(self.error_icon),
            FadeOut(error_messages[0]),
            FadeOut(error_messages[1]),
            self.distorted_image.animate.scale(0.5).to_edge(RIGHT).set_opacity(0.5),
            self.screen.animate.scale(0.5).to_edge(RIGHT).set_opacity(0.5)
        )
        self.play(Create(self.ai_face))

        self.play(*[Write(qm) for qm in question_marks])

        self.wait(2)
        big_question_mark = Tex("?", color=text_color).scale(2).move_to(self.ai_face.get_center() + UP * 1.5)
        self.play(*[Transform(qm.copy(), big_question_mark) for qm in question_marks])
        self.wait(2)
        self.big_question_mark = big_question_mark

        # Scene 3: Seeking Clarity (10 seconds)
        text_box = Rectangle(width=4, height=2, color=screen_color, fill_opacity=1).next_to(self.ai_face, RIGHT)
        cursor = Line(start=text_box.get_center() + LEFT * 1.9, end=text_box.get_center() + LEFT * 1.9 + UP * 0.1, color=text_color)
        self.play(Create(text_box))
        self.play(Create(cursor))
        # Improved cursor animation with vertical bobbing
        self.play(
            cursor.animate.shift(RIGHT * 0.1).set_opacity(0).shift(DOWN * 0.05).set_opacity(1).shift(UP * 0.05).repeat(3),
            run_time = 1
        )

        description = "The image was of a cat sitting on a red couch."
        description_text = Text(description, color=text_color, font_size=20).move_to(text_box.get_center())

        self.play(Write(description_text), run_time=5)  # Animate typing effect

        self.play(text_box.animate.set_color(GREEN), description_text.animate.set_color(GREEN), run_time = 1)
        self.wait(1)
        self.play(
            text_box.animate.scale(0.6).to_edge(UP).shift(LEFT * 1.5),
            description_text.animate.scale(0.6).to_edge(UP).shift(LEFT * 1.5)
        )

        # Scene 4: The Explanation (10 seconds)
        happy_ai_face = self.create_ai_face(happy=True)
        eye = next(mob for mob in self.ai_face if type(mob) == Circle and mob.radius == 0.3)
        pupil = next(mob for mob in self.ai_face if type(mob) == Circle and mob.radius == 0.1)
        happy_eye = next(mob for mob in happy_ai_face if type(mob) == Circle and mob.radius == 0.3)
        happy_pupil = next(mob for mob in happy_ai_face if type(mob) == Circle and mob.radius == 0.1)
        smile = next(mob for mob in happy_ai_face if type(mob) == Arc)
        self.play(
            Transform(eye, happy_eye),
            Transform(pupil, happy_pupil),
            Create(smile),
            FadeOut(self.big_question_mark)

        )

        explanation_text_box = Rectangle(width=4, height=2, color=screen_color, fill_opacity=1).next_to(self.ai_face, DOWN)
        explanation = "Based on the description, the image likely contained a domestic cat resting on a red couch."
        explanation_text = Text(explanation, color=text_color, font_size=20).move_to(explanation_text_box.get_center())

        self.play(Create(explanation_text_box))
        self.play(Write(explanation_text), run_time=5)
        self.wait(1)
        cat_image = ImageMobject("cat_on_couch.png").scale(0.3).next_to(explanation_text_box, RIGHT) # Replace "cat_on_couch.png" with a real image path
        try:
            self.play(FadeIn(cat_image))
        except Exception as e:
            print("Error loading cat image:", e)
            cat_image = Square(side_length=0.5, color=text_color).next_to(explanation_text_box, RIGHT)
            self.play(Create(cat_image))
        self.wait(2)

        # Outro (2 seconds)
        self.play(
            FadeOut(self.ai_face),
            FadeOut(self.distorted_image),
            FadeOut(self.screen),
            FadeOut(text_box),
            FadeOut(description_text),
            FadeOut(explanation_text_box),
            FadeOut(explanation_text),
            FadeOut(cat_image),
            #FadeOut(eye),
            #FadeOut(pupil),
            #FadeOut(smile),
        )

        logo = Square(side_length=2, color=accent_color, fill_opacity=0.5).shift(UP * 0.5) # Placeholder logo
        logo_text = Text("Image Processor", color=text_color).scale(0.6).next_to(logo, DOWN)
        outro_text = Text("Clear Communication Matters.", color=text_color).scale(0.5).next_to(logo_text, DOWN)
        self.play(FadeIn(logo, logo_text, outro_text))
        self.wait(2)

    def create_ai_face(self, color=BLUE, eye_color=WHITE, pupil_color=BLACK, happy=False):
        ai_avatar = Circle(radius=1, color=color, fill_opacity=0.7).to_edge(LEFT)
        eye = Circle(radius=0.3, color=eye_color, fill_opacity=1).move_to(ai_avatar.get_center())
        pupil = Circle(radius=0.1, color=pupil_color, fill_opacity=1).move_to(eye.get_center() + RIGHT * 0.1)
        if happy:
            smile = Arc(radius=0.4, start_angle=PI/8, angle=-PI/4, color=pupil_color).move_to(ai_avatar.get_center() + DOWN * 0.3)
            return Group(ai_avatar, eye, pupil, smile)
        return Group(ai_avatar, eye, pupil)


def random_color():
    return Color(rgb=[np.random.uniform(0, 1), np.random.uniform(0, 1), np.random.uniform(0, 1)])

# To render the animation, you can use the following command in the terminal:
# manim -pql your_file_name.py ImageProcessingExplanation