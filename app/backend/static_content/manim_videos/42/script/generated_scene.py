from manim import *

class ManimScene(Scene):
    def construct(self):
        self.introduction_to_ocr()
        self.ocr_conversion()
        self.text_editing_simplified()
        self.image_analysis()
        self.document_digitization()
        self.various_applications()
        self.enhanced_copy_and_edit()
        self.essential_technological_advancement()

    def introduction_to_ocr(self):
        # Create book page and digital screen representations
        book_page = RoundedRectangle(corner_radius=0.1, width=3, height=4, color=BLUE).shift(LEFT * 3)
        digital_screen = RoundedRectangle(corner_radius=0.1, width=3, height=4, color=GREEN).shift(RIGHT * 3)
        self.play(Create(book_page), Create(digital_screen))
        
        # Narration below illustrating OCR's purpose
        narration = Text("Discover OCR, bridging printed text and digital formats.", font_size=24).to_edge(DOWN)
        arrow = Arrow(start=LEFT*2, end=RIGHT*2, color=WHITE, buff=0.2)
        self.play(FadeIn(narration))
        self.play(Create(arrow), run_time=5, rate_func=smooth)
        self.play(AnimationGroup(FadeOut(narration), FadeOut(book_page), FadeOut(digital_screen), FadeOut(arrow)))

    def ocr_conversion(self):
        # Illustrate OCR converting notes into digital text
        notes = Rectangle(width=2, height=3, color=YELLOW).shift(LEFT * 3)
        smartphone = RoundedRectangle(corner_radius=0.2, width=2, height=4, color=BLACK).shift(RIGHT * 3)
        self.play(Create(notes), Create(smartphone))
        
        arrow = Arrow(start=LEFT*2, end=RIGHT*2, color=WHITE, buff=0.2)
        digital_text = Text("Digital Text", font_size=24).next_to(smartphone, UP)
        self.play(Create(arrow), Write(digital_text), rate_func=smooth, run_time=6)
        self.play(AnimationGroup(FadeOut(notes), FadeOut(smartphone), FadeOut(arrow), FadeOut(digital_text)))

    def text_editing_simplified(self):
        # Show transition from paper to editable text on screen
        paper = Rectangle(width=2, height=3, color=BLUE).shift(LEFT * 3)
        computer_screen = RoundedRectangle(corner_radius=0.1, width=3, height=4, color=GREEN).shift(RIGHT * 3)
        self.play(Create(paper), Create(computer_screen))

        text = Text("Editable Text", font_size=24).move_to(computer_screen.get_center())
        self.play(text.animate.move_to(computer_screen.get_center()), rate_func=smooth, run_time=6)
        self.play(AnimationGroup(FadeOut(paper), FadeOut(computer_screen), FadeOut(text)))

    def image_analysis(self):
        # Animate image to text analysis with letter recognition
        image = Rectangle(width=3, height=2, color=ORANGE).shift(LEFT * 3)
        self.play(Create(image))

        letters = VGroup(*[Text(letter, font_size=24) for letter in "TEXT"])
        letters.arrange(RIGHT, buff=0.2).move_to(image.get_center())
        self.play(LaggedStart(*[FadeIn(letter) for letter in letters], lag_ratio=0.5), run_time=7)
        self.play(AnimationGroup(FadeOut(image), *[FadeOut(letter) for letter in letters]))

    def document_digitization(self):
        # Transform stack of papers into a USB drive
        papers = VGroup(*[Rectangle(width=2.5, height=0.1, color=WHITE).shift(UP * i * 0.1) for i in range(10)])
        usb_drive = RoundedRectangle(corner_radius=0.1, width=1, height=0.5, color=GOLD)
        self.play(Create(papers), papers.animate.arrange(DOWN, buff=0.05).scale(0.5).move_to(usb_drive.get_center()), run_time=5)
        self.play(AnimationGroup(FadeOut(papers), FadeIn(usb_drive)))

    def various_applications(self):
        # Display OCR applications across different devices
        scanner = Rectangle(width=2, height=1, color=BLUE)
        smartphone = RoundedRectangle(corner_radius=0.3, width=1, height=2, color=RED)
        translation_app = RoundedRectangle(corner_radius=0.3, width=1, height=1, color=GREEN)

        self.play(FadeIn(scanner), scanner.animate.shift(LEFT * 3))
        self.play(FadeIn(smartphone), smartphone.animate.shift(LEFT))
        self.play(FadeIn(translation_app), translation_app.animate.shift(RIGHT), run_time=7)
        self.play(AnimationGroup(FadeOut(scanner), FadeOut(smartphone), FadeOut(translation_app)))

    def enhanced_copy_and_edit(self):
        # Highlight and copy text from one document to another
        document = Rectangle(width=3, height=4, color=GREY).shift(LEFT * 3)
        new_doc = Rectangle(width=3, height=4, color=GREY).shift(RIGHT * 3)
        self.play(Create(document), Create(new_doc))

        copy_text = Text("Text Highlighted", font_size=24).move_to(document.get_center())
        self.play(Write(copy_text), run_time=6)
        self.play(copy_text.animate.move_to(new_doc.get_top() + DOWN), rate_func=smooth)
        self.play(AnimationGroup(FadeOut(copy_text), FadeOut(document), FadeOut(new_doc)))

    def essential_technological_advancement(self):
        # Timeline visualizing technological advancement in text
        typewriter = Rectangle(width=3, height=2, color=PURPLE).shift(LEFT * 3)
        computer = Rectangle(width=3, height=2, color=PURPLE).shift(RIGHT * 3)
        self.play(Create(typewriter), Create(computer))

        timeline = Line(start=LEFT * 2, end=RIGHT * 2, color=WHITE)
        self.play(Create(timeline))
        
        dates = [Text(year, font_size=18) for year in ["1900", "2000", "2023"]]
        for i, date in enumerate(dates):
            self.play(Write(date.next_to(timeline, DOWN, buff=0.1).shift(i * RIGHT * 2 - LEFT * 2)))

        morph_arrow = Arrow(start=LEFT, end=RIGHT, color=YELLOW, buff=0.1)
        self.play(Create(morph_arrow), run_time=8)
        self.play(AnimationGroup(FadeOut(typewriter), FadeOut(computer), FadeOut(timeline), FadeOut(morph_arrow), *[FadeOut(date) for date in dates]))