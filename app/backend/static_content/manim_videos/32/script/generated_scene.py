from manim import *

class OCROverview(Scene):
    def construct(self):
        # Call separate methods for each storyboard step
        self.introduction_to_ocr()
        self.digitalization_of_documents()
        self.editable_text_from_images()
        self.handwritten_notes_conversion()
        self.text_utilization()
        self.versatile_information_extraction()

    def introduction_to_ocr(self):
        """
        Animates the introduction to OCR by demonstrating its role in transforming image text to digital text.
        """
        try:
            computer = Rectangle(width=3, height=2).shift(LEFT * 3)
            document = Rectangle(width=1.5, height=2).shift(RIGHT * 3)
            ocr_text = Text("Optische Zeichenerkennung (OCR)").scale(0.5).next_to(document, UP)

            scanner_light = Line(LEFT, RIGHT).set_color(YELLOW).next_to(document, DOWN, buff=0.1)
            ocr_highlight = Text("OCR").scale(1.5).set_color(RED).move_to(computer.get_center())

            self.play(FadeIn(computer), FadeIn(document), Write(ocr_text))
            self.play(scanner_light.animate.shift(UP * 2), run_time=2)
            self.play(FadeIn(ocr_highlight, scale=1.2))
            self.play(ocr_highlight.animate.scale(0.7).move_to(computer.get_center()), run_time=2)
            self.wait(3)

            narration_1 = Text("Optische Zeichenerkennung, auch bekannt als OCR, verwandelt schriftlichen Text aus Bildern in digitale Daten.", font_size=24)
            self.play(Write(narration_1), run_time=5)
            self.wait()
            self.clear()
        except Exception as e:
            print(f"Error during 'Introduction to OCR': {e}")

    def digitalization_of_documents(self):
        """
        Illustrates how OCR digitizes physical documents.
        """
        try:
            hand = SVGMobject("hand.svg").scale(0.5).to_edge(DOWN)
            digital_doc = Rectangle(width=3, height=2).next_to(Rectangle(width=3, height=2).shift(LEFT * 3), RIGHT, buff=1)
            progress_bar = Rectangle(width=4, height=0.3).set_color(BLUE).shift(UP)
            progress_fill = Rectangle(width=0, height=0.3).set_fill(BLUE, opacity=1).align_to(progress_bar, LEFT)

            self.play(FadeIn(hand), FadeIn(Rectangle(width=1.5, height=2).shift(RIGHT * 3)))
            self.play(hand.animate.shift(UP * 1.5), run_time=1)
            self.play(Rectangle(width=1.5, height=2).shift(RIGHT * 3).animate.shift(UP * 1.5).next_to(hand, UP), run_time=1)
            self.play(FadeIn(progress_bar))
            self.play(self.Progress(progress_fill, width=4), run_time=4)
            self.play(FadeOut(progress_fill), FadeOut(hand), FadeOut(progress_bar), FadeIn(digital_doc))
            self.wait(2)

            narration_2 = Text("OCR bietet die Möglichkeit, physische Dokumente mühelos zu digitalisieren und den Textinhalt in Fotos zu erkennen.", font_size=24)
            self.play(Write(narration_2), run_time=5)
            self.wait()
            self.clear()
        except Exception as e:
            print(f"Error during 'Digitalization of Documents': {e}")

    def editable_text_from_images(self):
        """
        Demonstrates conversion of static image text to editable digital text.
        """
        try:
            photo = Rectangle(width=2.5, height=2, color=GREY).shift(LEFT * 3)
            photo_text = Text("This is an image").scale(0.5).move_to(photo.get_center())
            editable_text = VGroup(*(Text(word).set_color(TEAL).shift(RIGHT * 3 + i * UP * 0.5) for i, word in enumerate("This is an image".split())))

            self.play(FadeIn(photo), Write(photo_text))
            self.play(photo_text.animate.move_to(editable_text.get_center()), run_time=2)
            self.play(Transform(photo_text, editable_text), run_time=2)
            self.wait(2)

            narration_3 = Text("Texte, die vorher statisch im Bild festgehalten waren, können jetzt nach Belieben bearbeitet werden.", font_size=24)
            self.play(Write(narration_3), run_time=5)
            self.wait()
            self.clear()
        except Exception as e:
            print(f"Error during 'Editable Text from Images': {e}")

    def handwritten_notes_conversion(self):
        """
        Shows how OCR converts handwritten notes to digital text.
        """
        try:
            notes = SVGMobject("handwritten.svg").scale(0.8).to_edge(LEFT)
            tablet = RoundedRectangle(width=3, height=2).set_color(PURPLE).to_edge(RIGHT)
            camera_flash = Flash(tablet.get_center(), line_length=0.2, num_lines=12)

            self.play(DrawBorderThenFill(notes))
            self.play(ShowCreation(camera_flash), run_time=2)
            self.play(FadeOut(notes), FadeIn(tablet))
            typed_text = Text("Converted Notes").scale(0.5).move_to(tablet.get_center())
            self.play(Write(typed_text))
            self.wait(3)

            narration_4 = Text("Von Notizen zur digitalen Kopie – OCR erkennt und wandelt Handschriften direkt um.", font_size=24)
            self.play(Write(narration_4), run_time=5)
            self.wait()
            self.clear()
        except Exception as e:
            print(f"Error during 'Handwritten Notes Conversion': {e}")

    def text_utilization(self):
        """
        Depicts how OCR-processed text can be edited and searched.
        """
        try:
            document_interface = RoundedRectangle(width=4, height=3, fill_color="#DDD").shift(LEFT * 2)
            highlighted_text = Text("OCR Makes Editing").scale(0.5).set_color(YELLOW).move_to(document_interface.get_center() + UP)

            cursor = Square(0.1).set_color(BLACK).next_to(highlighted_text, RIGHT)
            search_text = Text("Find OCR").scale(0.4).to_edge(UP)

            self.play(FadeIn(document_interface), Write(highlighted_text))
            self.play(FadeIn(cursor))
            self.play(cursor.animate.next_to(search_text, RIGHT))
            self.play(CircleIndicate(highlighted_text))
            self.wait(3)

            narration_5 = Text("Die digitale Bearbeitung bietet erweiterte Möglichkeiten der Texterstellung und -suche.", font_size=24)
            self.play(Write(narration_5), run_time=5)
            self.wait()
            self.clear()
        except Exception as e:
            print(f"Error during 'Text Utilization': {e}")

    def versatile_information_extraction(self):
        """
        Illustrates OCR's ability to extract diverse information types from images.
        """
        try:
            journal = Rectangle(width=1.5, height=2.5, fill_color=GREY).to_edge(LEFT)
            poem = Rectangle(width=1.5, height=2.5, fill_color=GREY).next_to(journal, RIGHT, buff=0.5)
            annotated_journal = SVGMobject("annotation.svg").scale(0.3).next_to(journal, RIGHT, buff=1)
            annotated_poem = SVGMobject("annotation.svg").scale(0.3).next_to(poem, RIGHT, buff=1)

            self.play(FadeIn(journal), FadeIn(poem))
            self.play(FadeIn(annotated_journal), FadeIn(annotated_poem))
            self.play(annotated_journal.animate.shift(UP), run_time=2)
            self.play(annotated_poem.animate.shift(DOWN), run_time=2)
            self.wait(3)

            narration_6 = Text("OCR-unterstützte Bilder vereinfachen den Zugriff auf unterschiedlichste Inhalte – von Poesie bis hin zu sachlichen Artikeln.", font_size=24)
            self.play(Write(narration_6), run_time=7)
            self.wait()
        except Exception as e:
            print(f"Error during 'Versatile Information Extraction': {e}")

    @staticmethod
    def Progress(bar_in, width):
        """
        Creates a progression effect for a progress bar.

        Args:
        - bar_in: Rectangle object representing the progress fill.
        - width: The target width the bar should fill to simulate progression.
        
        Returns:
        - Animation: The animation object for the progress effect.
        """
        return bar_in.animate.set_width(width, stretch=True)