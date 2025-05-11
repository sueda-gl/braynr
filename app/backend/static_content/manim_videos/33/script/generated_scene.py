from manim import *
import os

class OCRExplainer(Scene):
    """This scene explains OCR (Optical Character Recognition) through a series of animations,
    demonstrating its concept, functionality, applications, and benefits."""

    def construct(self):
        # Helper function to safely load images
        def safe_image_load(filepath, **kwargs):
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Required image file '{filepath}' not found.")
            return ImageMobject(filepath, **kwargs)

        # Scene 1: Introduction to OCR
        computer_screen = safe_image_load("computer_screen.png").scale(0.5)
        documents = VGroup(
            safe_image_load("document_1.png").scale(0.2).shift(LEFT * 3),
            safe_image_load("document_2.png").scale(0.2).shift(LEFT),
            safe_image_load("document_3.png").scale(0.2).shift(RIGHT),
        )
        intro_text = Text("Willkommen in der Welt der Bildverarbeitung mit OCR.", language="de").shift(DOWN * 2)

        self.play(FadeIn(computer_screen))
        self.wait(1)
        self.play(computer_screen.animate.shift(UP * 2))
        self.play(FadeIn(documents))
        self.play(Write(intro_text))
        self.wait(2)
        self.play(FadeOut(computer_screen, documents, intro_text))

        # Scene 2: What is OCR?
        handwritten_image = safe_image_load("handwritten_notes.png").scale(0.5).to_edge(LEFT)
        digital_text = Text("Digitaler Text", language="de").to_edge(RIGHT)
        arrow = Arrow(handwritten_image.get_right(), digital_text.get_left())

        ocr_text = Text("OCR steht für Optische Zeichenerkennung...", language="de").next_to(digital_text, DOWN)

        self.play(FadeIn(handwritten_image))
        self.play(GrowArrow(arrow))
        self.play(Write(digital_text))
        self.play(Write(ocr_text))
        self.wait(3)
        self.play(*map(FadeOut, [handwritten_image, arrow, digital_text, ocr_text]))

        # Scene 3: How OCR Works
        document = safe_image_load("text_document.png").scale(0.7)
        highlight_box = SurroundingRectangle(document).set_color(YELLOW)
        extracted_text_box = Text("Extrahierter Text", color=YELLOW, language="de").next_to(document, DOWN)

        ocr_work_text = Text("So funktioniert's: OCR erkennt Text im Bild...", language="de").next_to(extracted_text_box, DOWN)

        self.play(FadeIn(document))
        self.play(ShowCreation(highlight_box))
        self.play(Write(extracted_text_box))
        self.play(Write(ocr_work_text))
        self.wait(2)
        self.play(FadeOut(document, highlight_box, extracted_text_box, ocr_work_text))

        # Scene 4: OCR in Action
        newspaper = safe_image_load("newspaper.png").scale(0.5).to_edge(LEFT)
        editor_window = safe_image_load("text_editor.png").scale(0.5).to_edge(RIGHT)

        action_text = Text("Im Einsatz: Text aus einem Zeitungsartikel...", language="de").next_to(editor_window, DOWN)

        self.play(FadeIn(newspaper))
        self.play(FadeIn(editor_window))
        self.play(Write(action_text))
        self.wait(3)
        self.play(FadeOut(newspaper, editor_window, action_text))

        # Scene 5: Benefits of Using OCR
        search_icon = safe_image_load("search_icon.png").scale(0.3).shift(LEFT * 4)
        copy_icon = safe_image_load("copy_icon.png").scale(0.3).shift(LEFT * 2)
        edit_icon = safe_image_load("edit_icon.png").scale(0.3).shift(RIGHT * 0)

        benefits_text = Text("Mit OCR können Sie Text durchsuchen, kopieren und bearbeiten...", language="de").to_edge(DOWN)

        self.play(FadeIn(search_icon))
        self.play(FadeIn(copy_icon))
        self.play(FadeIn(edit_icon))
        self.play(Write(benefits_text))
        self.wait(4)
        self.play(FadeOut(search_icon, copy_icon, edit_icon, benefits_text))

        # Scene 6: Mystery of 'hkh'
        question_mark = Text("?", font_size=144)
        mystery_text = Text("Die Bedeutung von 'hkh' bleibt ein Rätsel...", language="de").next_to(question_mark, DOWN)

        self.play(GrowFromCenter(question_mark))
        self.play(Write(mystery_text))
        self.wait(4)
        self.play(FadeOut(question_mark, mystery_text))