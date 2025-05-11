from manim import *

IMAGE_DIR = "./"  # Current directory.
config.media_dir = IMAGE_DIR

class SVGMobject(SVGMobject):
    def __init__(self, file_name, **kwargs):
        kwargs["file_name"] = file_name
        super().__init__(**kwargs)

class ImageMobject(ImageMobject):
    def __init__(self, image_name, **kwargs):
        kwargs["image_name"] = image_name
        super().__init__(**kwargs)

class ImageProcessorExplanation(Scene):
    def construct(self):
        self.scene1()
        self.scene2()
        self.scene3()
        self.scene4()
        self.scene5()

    def scene1(self):
        """Scene 1: The Image Processor"""
        image_processor_title = Text("The Image Processor").to_edge(UP)
        self.play(Write(image_processor_title))

        computer = RoundedRectangle(corner_radius=0.5, height=3, width=4, color=GRAY, fill_opacity=0.2)
        eye_icon = SVGMobject("assets/eye_icon.svg").scale(0.5).move_to(computer.get_center())
        input_port = Rectangle(height=0.5, width=0.3, color=BLUE, fill_opacity=0.8).next_to(computer, RIGHT, buff=0.1)
        computer_group = VGroup(computer, eye_icon, input_port).move_to(ORIGIN)
        computer_group.set_z_index(1)

        cat_image = ImageMobject("assets/cat.png").scale(0.5).to_edge(LEFT, buff=1)

        self.play(Create(computer_group))
        self.play(FadeIn(cat_image))

        self.wait(1)

        self.play(cat_image.animate.shift(RIGHT * 3.5).scale(0.5).set_rate_functions(smooth), run_time=2)
        self.play(cat_image.animate.scale(0.1).move_to(input_port.get_center()), FadeOut(input_port), run_time=1)

        self.wait(2)

        self.play(FadeOut(cat_image))
        self.play(
            computer_group.animate.scale(1.5).move_to(ORIGIN),
            image_processor_title.animate.move_to(UP*2),
            run_time=1.5
        )
        self.wait(0.5)

        self.image_processor_title = image_processor_title #Save title for next scene
        self.computer_group = computer_group

    def scene2(self):
        """Scene 2: Processing Power"""
        image_processor_title = Text("Processing Power").to_edge(UP)
        self.play(Transform(self.image_processor_title, image_processor_title), run_time=0.5)
        self.camera.frame.save_state() #Save camera location

        self.play(self.computer_group.animate.scale(0.4), run_time = 0.5) #Zoom in Effect
        self.play(self.computer_group.animate.shift(LEFT*3), run_time = 0.5)
        self.remove(self.computer_group)

        internal_cat = ImageMobject("assets/cat.png").scale(0.75).shift(LEFT*3)
        self.play(FadeIn(internal_cat))
        
        edge_group = self.highlight_feature(internal_cat, "ear", YELLOW, "Edge Detection")
        self.play(Create(edge_group[0]), Write(edge_group[1])) #Create highlight, Write text
        self.wait(0.75)
        self.play(FadeOut(edge_group))

        eye_group = self.highlight_feature(internal_cat, "eye", GREEN, "Eye Shape")
        self.play(Create(eye_group[0]), Write(eye_group[1]))
        self.wait(0.75)
        self.play(FadeOut(eye_group))

        fur_color_group = self.highlight_feature(internal_cat, "cat", "#F0E68C", "Fur Color", buffer = 1, is_color = True)
        self.play(Write(fur_color_group[1]))
        self.wait(0.75)
        self.play(FadeOut(fur_color_group[1]))
        self.wait(0.75)

        processing_lines = VGroup(*[Line(start=np.array([x, y, 0]), end=np.array([x+0.5, y, 0]), color=BLUE, stroke_width = 2) for x in np.arange(-5, 5, 0.5) for y in np.arange(-3, 3, 0.5)])
        self.play(Create(processing_lines, lag_ratio = 0.1), run_time=3)
        self.play(FadeOut(processing_lines), FadeOut(internal_cat)) #Clean up
        self.internal_cat = internal_cat #Save for scene 3

        self.image_processor_title = image_processor_title
    
    def highlight_feature(self, image, feature_tex, color, text, buffer=0.1, font_size=20, is_color = False):
        """Highlights a feature of an image with a surrounding shape and label."""
        if is_color:
            label = Text(f"Color: {color}", font_size=font_size, color = color).next_to(image, DOWN)
            highlight = image #No actual highlighting
        else:
            part = image.get_part_by_tex(feature_tex)
            if feature_tex == "eye":
                highlight = Circle(color=color, stroke_width=3).surround(part, buffer=buffer)
            else:
                highlight = Rectangle(color=color, stroke_width=3).surround(part, buffer=buffer)
            label = Text(text, font_size=font_size).next_to(highlight, UP)

        return VGroup(highlight, label)

    def scene3(self):
        """Scene 3: Processing Failure"""
        image_processor_title = Text("Processing Failure").to_edge(UP)
        self.play(Transform(self.image_processor_title, image_processor_title), run_time=0.5)
        internal_cat = self.internal_cat #Restore cat

        error_cat = internal_cat.copy()
        self.add(error_cat)
        self.wait(0.5)

        self.play(error_cat.animate.shift(np.array([0.1,0.1,0])).shift(np.array([-0.2,-0.2,0])).shift(np.array([0.1,0.1,0])).shift(np.array([-0.2,-0.2,0])), run_time = 1) #glitch

        loading = VGroup(*[Dot(radius=0.05, color = BLUE).shift(RIGHT*np.cos(angle)).shift(UP*np.sin(angle)) for angle in np.arange(0, 2*PI, PI/4)]).scale(0.5)
        loading.add_updater(lambda obj, dt: obj.rotate(PI/4 * dt)) #Continuously rotate
        self.play(Create(loading))
        self.wait(1.5)
        self.play(FadeOut(loading))
        loading.clear_updaters() #Remove updaters

        error_message = Rectangle(height=2, width=4, color=WHITE, fill_opacity=1).set_z_index(2)
        error_text = Text("Unable to process image.", color=RED).move_to(error_message.get_center())
        error_code = Text("Error 403", color=RED, font_size=24).next_to(error_text, DOWN)
        error_group = VGroup(error_message, error_text, error_code)

        self.play(Create(error_message))
        self.play(Write(error_text))
        self.play(Write(error_code))
        self.wait(2)
        self.play(FadeOut(error_cat))

        self.wait(1)
        self.play(FadeOut(error_group), run_time=2)
        self.image_processor_title = image_processor_title

    def scene4(self):
        """Scene 4: The Access Key"""
        image_processor_title = Text("The Access Key").to_edge(UP)
        self.play(Transform(self.image_processor_title, image_processor_title), run_time=0.5)

        computer = RoundedRectangle(corner_radius=0.5, height=3, width=4, color=GRAY, fill_opacity=0.2)
        eye_icon = SVGMobject("assets/eye_icon.svg").scale(0.5).move_to(computer.get_center())
        input_port = Rectangle(height=0.5, width=0.3, color=BLUE, fill_opacity=0.8).next_to(computer, RIGHT, buff=0.1)
        computer_group = VGroup(computer, eye_icon, input_port).move_to(ORIGIN)

        self.play(FadeIn(computer_group))
        self.wait(0.5)

        padlock = SVGMobject("assets/padlock.svg", color=GOLD).scale(0.75).move_to(input_port.get_center()).set_z_index(10)
        self.play(Create(padlock))

        hand = SVGMobject("assets/hand.svg").scale(0.75).to_edge(RIGHT, buff=1).shift(DOWN*0.5)
        key = SVGMobject("assets/key.svg", color=GOLD).scale(0.3).next_to(hand, LEFT)
        key.set_z_index(11) #Ensure key is above hand
        self.play(FadeIn(hand), FadeIn(key))

        self.wait(2)
        self.image_processor_title = image_processor_title
        self.padlock = padlock
        self.key = key
        self.hand = hand
        self.computer_group = computer_group

    def scene5(self):
        """Scene 5: Unlocking the Potential"""
        image_processor_title = Text("Unlocking the Potential").to_edge(UP)
        self.play(Transform(self.image_processor_title, image_processor_title), run_time=0.5)
        self.play(self.hand.animate.move_to(self.computer_group[2].get_center()+LEFT*0.5), self.key.animate.move_to(self.computer_group[2].get_center()+LEFT*0.3).scale(1.2), run_time=0.75)
        self.wait(0.25)
        self.play(FadeOut(self.padlock), Rotate(self.key, angle = PI), run_time = 0.5)
        self.play(FadeOut(self.key), FadeOut(self.hand), run_time = 0.5)

        cat_image = ImageMobject("assets/cat.png").scale(0.5).to_edge(LEFT, buff=1)
        self.play(FadeIn(cat_image))
        self.play(cat_image.animate.shift(RIGHT * 3.5).scale(0.5), run_time=2)
        self.play(cat_image.animate.scale(0.1).move_to(self.computer_group[2].get_center()), run_time=1)

        self.play(FadeOut(self.computer_group), FadeOut(cat_image))

        internal_cat = ImageMobject("assets/cat.png").scale(0.75).shift(LEFT*3)
        self.add(internal_cat)

        edge_group = self.highlight_feature(internal_cat, "ear", YELLOW, "Edge Detection")
        self.play(Create(edge_group[0]), Write(edge_group[1]))
        self.wait(0.75)
        self.play(FadeOut(edge_group))

        eye_group = self.highlight_feature(internal_cat, "eye", GREEN, "Eye Shape")
        self.play(Create(eye_group[0]), Write(eye_group[1]))
        self.wait(0.75)
        self.play(FadeOut(eye_group))

        fur_color_group = self.highlight_feature(internal_cat, "cat", "#F0E68C", "Fur Color", buffer = 1, is_color = True)
        self.play(Write(fur_color_group[1]))
        self.wait(0.75)
        self.play(FadeOut(fur_color_group[1]))

        analysis_text = Text("Cat detected. Confidence: 98%", color=GREEN).to_edge(DOWN)
        self.play(Write(analysis_text))

        self.wait(3)
        self.play(FadeOut(analysis_text), FadeOut(internal_cat))

        self.wait(1)
        self.play(FadeOut(self.image_processor_title))
        self.wait(1)
        self.play(FadeOut(self.camera.background_color))
        self.wait(1)