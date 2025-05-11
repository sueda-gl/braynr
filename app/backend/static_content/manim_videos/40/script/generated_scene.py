from manim import *

class ManimScene(Scene):
    def construct(self):
        # Call each phase of the animation one by one
        self.intro_ocr()
        self.image_capture()
        self.image_preprocessing()
        self.text_recognition()
        self.post_processing()
        self.applications_digitization()
        self.enhanced_archiving_access()
        self.search_editing_capabilities()
    
    def intro_ocr(self):
        # Display "OCR" text and fade in multiple rectangular boxes to represent documents
        ocr_text = Text("OCR", font_size=72, weight=BOLD, color=YELLOW)
        documents = VGroup(
            RectangularBoxesFader(2, 3, WHITE, UP * 0.5 + LEFT * 1),
            RectangularBoxesFader(2, 3, WHITE, UP * 0.5 + RIGHT * 1),
            RectangularBoxesFader(2, 3, WHITE, DOWN * 0.5 + LEFT * 1),
            RectangularBoxesFader(2, 3, WHITE, DOWN * 0.5 + RIGHT),
        )
        self.play(FadeIn(ocr_text), rate_func=smooth, run_time=1)
        self.play(Create(documents), rate_func=smooth, run_time=2)
        self.wait(1)
        self.play(FadeOut(ocr_text), FadeOut(documents))
        
    def image_capture(self):
        # Animate scanner and camera capturing images
        scanner = self.create_scan_animation("Scanner", scale_factor=1)
        phone = self.create_scan_animation("Camera", scale_factor=0.5)
        phone.next_to(scanner, RIGHT, buff=1)
        self.play(scanner, rate_func=smooth, run_time=2.5)
        self.play(phone, rate_func=smooth, run_time=2.5)
        self.wait(1)

    def image_preprocessing(self):
        # Display image and sliders to represent pre-processing adjustments
        image = Rectangle(height=3.5, width=2, fill_color=GRAY, fill_opacity=0.5)
        sliders = VGroup(
            Line(start=LEFT * 0.5, end=RIGHT * 0.5, color=WHITE).shift(LEFT * 0.5),
            Line(start=LEFT * 0.5, end=RIGHT * 0.5, color=WHITE).shift(RIGHT * 0.5)
        )
        sliders.next_to(image, DOWN, buff=0.5)
        self.play(FadeIn(image), Create(sliders), rate_func=smooth, run_time=2.5)
        self.wait(2)

    def text_recognition(self):
        # Show recognized text popping up next to the original
        text = Text("Recognized Text", font_size=24)
        side_window = RoundedRectangle(width=3.5, height=2.5, color=BLUE)
        side_window.next_to(text, RIGHT, buff=1)
        self.play(Write(text), Create(side_window), rate_func=smooth, run_time=3)
        self.wait(2)

    def post_processing(self):
        # Display interface elements for text correction
        correction_interface = VGroup(
            Line(LEFT, RIGHT, color=GREEN),
            Polygon(UP, DOWN, LEFT, color=GREEN),
            Rectangle(width=2, height=1, color=GREEN)
        ).arrange(DOWN, buff=0.25)
        self.play(Create(correction_interface), rate_func=smooth, run_time=2.5)
        self.wait(2)

    def applications_digitization(self):
        # Represent digitization by showing books and a cloud object
        library_books = VGroup(
            Rectangle(width=2, height=3, color=RED).shift(LEFT),
            Rectangle(width=2, height=3, color=RED).shift(RIGHT)
        )
        try:
            cloud = SVGMobject("Cloud").scale(0.75)
            self.play(Create(library_books), Create(cloud), rate_func=smooth, run_time=3)
        except FileNotFoundError:
            print("Cloud SVG file not found.")
        self.wait(2)

    def enhanced_archiving_access(self):
        # Display archival interface representation
        archive_interface = VGroup(
            Rectangle(width=4, height=2, color=BLUE),
            Line(start=UP, end=DOWN, color=BLUE)
        )
        self.play(Create(archive_interface), rate_func=smooth, run_time=2.5)
        self.wait(2)

    def search_editing_capabilities(self):
        # Highlight search and editing capabilities with an interface
        search_interface = VGroup(
            Rectangle(width=4, height=1, color=ORANGE),
            Line(start=LEFT, end=RIGHT, color=ORANGE)
        )
        editing_area = Rectangle(width=4, height=2.5, color=ORANGE, fill_opacity=0.3)
        editing_area.next_to(search_interface, DOWN, buff=0.25)
        self.play(Create(search_interface), Create(editing_area), rate_func=smooth, run_time=3)
        self.wait(2)

def RectangularBoxesFader(num_boxes, box_height, color_fill, shift_amount):
    # Create a series of faded rectangular boxes
    if num_boxes < 0:
        raise ValueError("Number of boxes must be non-negative")
    boxes = []
    for i in range(num_boxes):
        rect = Rectangle(height=box_height, width=0.5, color=color_fill, fill_color=color_fill, fill_opacity=0.5)
        rect.shift(shift_amount + RIGHT * i)
        boxes.append(rect)
    return VGroup(*boxes)

def create_scan_animation(name, scale_factor):
    # Return a scale animation for scanning
    return ScaleInPlace(Text(name, font_size=24), scale_factor)