from manim import *

class ManimScene(Scene):
    # Constants for shared styling
    FONT_SIZE_LARGE = 64
    FONT_SIZE_MEDIUM = 36
    FONT_SIZE_SMALL = 28
    FONT_SIZE_EXTRA_SMALL = 24
    COLOR_BLUE = BLUE
    COLOR_RED = RED
    COLOR_GREEN = GREEN
    COLOR_BLACK = BLACK
    COLOR_WHITE = WHITE
    COLOR_YELLOW = YELLOW
    COLOR_GRAY = GRAY

    def construct(self):
        # Scene 1: Introduction to OCR
        ocr_text = Text("OCR", font_size=self.FONT_SIZE_LARGE).to_edge(UP)
        magnifying_glass = Circle(radius=0.5, color=self.COLOR_BLUE).shift(LEFT)
        digital_world = Text("Digital World", font_size=self.FONT_SIZE_MEDIUM).next_to(magnifying_glass, RIGHT)
        self.play(FadeIn(ocr_text), GrowFromCenter(magnifying_glass))
        self.wait(1)
        self.play(magnifying_glass.animate.scale(1.2), FadeIn(digital_world))
        self.wait(3)

        # Scene 2: Optische Zeichenerkennung
        english_text = Text("Optical Character Recognition", font_size=self.FONT_SIZE_SMALL).to_edge(UP)
        german_text = Text("Optische Zeichenerkennung", font_size=self.FONT_SIZE_SMALL).to_edge(UP)
        union_jack = Rectangle(width=3, height=2, color=self.COLOR_RED).shift(DOWN * 1.5)
        german_flag = Rectangle(width=3, height=2, color=self.COLOR_BLACK).shift(DOWN * 1.5)
        self.play(FadeOut(magnifying_glass, ocr_text, digital_world))
        self.play(FadeIn(english_text), Create(union_jack))
        self.wait(1)
        self.play(Transform(english_text, german_text), Transform(union_jack, german_flag))
        self.wait(3)

        # Scene 3: Text Recognition Process
        handwritten_notes = VGroup(*[Text("Note", font_size=self.FONT_SIZE_EXTRA_SMALL).shift(UP * i) for i in range(-2, 3)])
        printed_pages = VGroup(*[Text("Page", font_size=self.FONT_SIZE_EXTRA_SMALL).shift(DOWN * i + RIGHT * 3) for i in range(-2, 3)])
        self.play(FadeOut(english_text, german_text, union_jack, german_flag))
        self.play(FadeIn(handwritten_notes, printed_pages))
        self.wait(1)
        binary_text = Text("1010101010", font_size=self.FONT_SIZE_SMALL).scale(1.5).to_edge(UP)
        self.play(
            handwritten_notes.animate.shift(UP * 6).set_opacity(0),
            printed_pages.animate.shift(DOWN * 6).set_opacity(0),
            FadeIn(binary_text),
            run_time=2
        )
        self.wait(2)

        # Scene 4: Conversion to Machine-Readable Text
        non_editable_text = Text("Non-editable Text", font_size=self.FONT_SIZE_EXTRA_SMALL, color=self.COLOR_RED).to_edge(LEFT)
        editable_document = Text("Editable Document", font_size=self.FONT_SIZE_EXTRA_SMALL, color=self.COLOR_GREEN).to_edge(RIGHT)
        self.play(FadeOut(binary_text))
        self.play(FadeIn(non_editable_text))
        self.wait(1)
        self.play(Transform(non_editable_text, editable_document, rate_func=smooth))
        self.wait(2)

        # Scene 5: Digital Accessibility from Scanned Documents
        paper_stack = VGroup(*[Rectangle(width=1.5, height=2, color=self.COLOR_WHITE) for _ in range(5)]).arrange(DOWN)
        computer_display = Rectangle(width=4, height=3, color=self.COLOR_BLUE).shift(RIGHT * 3)
        document_icons = VGroup(*[Rectangle(width=0.5, height=0.5, color=self.COLOR_YELLOW) for _ in range(9)]).arrange_in_grid(buff=0.2).move_to(computer_display.get_center())
        self.play(FadeOut(non_editable_text, editable_document))
        self.play(FadeIn(paper_stack))
        self.wait(1)
        self.play(ReplacementTransform(paper_stack, document_icons), FadeIn(computer_display))
        self.wait(2)

        # Scene 6: Searchability and Editability of Text
        document = Rectangle(width=6, height=3, color=self.COLOR_WHITE)
        search_field = Rectangle(width=3, height=0.5, color=self.COLOR_GRAY).next_to(document, UP)
        self.play(FadeOut(document_icons, computer_display))
        self.play(FadeIn(search_field, document))
        self.wait(1)
        keyword_text = Text("Keyword", font_size=self.FONT_SIZE_EXTRA_SMALL, color=self.COLOR_RED).move_to(search_field.get_center())
        typing_cursor = Line(UP, DOWN, color=self.COLOR_BLACK).next_to(keyword_text, RIGHT)
        self.play(Write(keyword_text), Create(typing_cursor))
        self.wait(2)

        # Scene 7: Text Storage Capabilities
        digital_cloud = Circle(radius=3, color=self.COLOR_WHITE)
        cloud_files = VGroup(*[Rectangle(width=0.5, height=0.75, color=self.COLOR_YELLOW) for _ in range(5)]).arrange(buff=0.5)
        self.play(FadeOut(search_field, document, keyword_text, typing_cursor))
        self.play(DrawBorderThenFill(digital_cloud))
        self.wait(1)
        self.play(cloud_files.animate.shift(UP * 3), FadeOut(cloud_files, shift=UP * 3))
        self.wait(2)

        # Scene 8: Application in Document Management
        office_desk = Rectangle(width=6, height=2, color=self.COLOR_GRAY).shift(DOWN * 1.5)
        office_employee = Circle(radius=0.5, color=self.COLOR_BLUE).next_to(office_desk, UP, buff=0.1)
        office_computer = Rectangle(width=1, height=0.75, color=self.COLOR_BLACK).next_to(office_employee, UP, buff=0.3)
        self.play(FadeOut(digital_cloud))
        self.play(FadeIn(office_desk, office_employee, office_computer))
        self.wait(1)
        
        screen_files = VGroup(*[Rectangle(width=0.2, height=0.3, color=self.COLOR_YELLOW) for _ in range(3)]).arrange_in_grid(buff=0.1).move_to(office_computer.get_center())
        self.play(FadeIn(screen_files))
        self.wait(2)
        
        # Scene 9: Book Digitization
        physical_book = VGroup(*[Rectangle(width=1, height=1.5, color=self.COLOR_WHITE) for _ in range(3)]).arrange(RIGHT, buff=MED_LARGE_BUFF)
        physical_book.move_to(ORIGIN)
        digital_ebook = Rectangle(width=2, height=3, color=self.COLOR_GREEN).next_to(physical_book, RIGHT, buff=LARGE_BUFF)
        self.play(FadeOut(office_desk, office_employee, office_computer, screen_files))
        self.play(FadeIn(physical_book))
        self.wait(1)
        self.play(physical_book.animate.shift(LEFT * 2), FadeIn(digital_ebook))
        self.wait(2)

        # Scene 10: Automated Text Recognition in Apps
        app_interface = Rectangle(width=1.5, height=3, color=self.COLOR_GRAY)
        camera_preview = VGroup(*[Rectangle(width=0.4, height=0.2, color=self.COLOR_WHITE) for _ in range(3)]).arrange(DOWN, buff=0.1)
        camera_preview.move_to(app_interface.get_center())
        
        self.play(FadeOut(physical_book, digital_ebook))
        self.play(FadeIn(app_interface))
        self.wait(1)
        self.play(FadeIn(camera_preview))
        self.wait(2)