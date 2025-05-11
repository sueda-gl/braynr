from manim import *

class OCRDemo(Scene):
    """
    A Manim scene to demonstrate the functionalities of Optical Character Recognition (OCR).
    The animation includes various steps showing how OCR works, its benefits, and applications.
    """

    def construct(self):
        # Set up background music
        self.add_sound("background_music.mp3")

        # Create each step of the OCR demonstration with transitions
        self.create_step(
            image_path="device_scanning.jpg",
            text="Welcome to the world of Optical Character Recognition, or OCR, "
                 "a groundbreaking technology transforming the way we digitize text.",
            duration_text=5
        )

        self.create_step(
            image_path="document_processing.jpg",
            text="OCR technology allows for electronic recognition and the seamless "
                 "digitization of text from images or scanned documents.",
            duration_text=5,
            arrow=True
        )

        self.create_step(
            image_path="scanned_document.jpg",
            text="With precision, OCR identifies each letter and word in an image, "
                 "turning visual data into digital information.",
            duration_text=5
        )

        self.create_step(
            image_path="digital_document.jpg",
            text="The transformation of identified text into an editable format is "
                 "where OCR truly shines.",
            duration_text=5
        )

        self.create_step(
            image_path="digital_archive.jpg",
            text="In this digital age, OCR is essential for archiving printed documents "
                 "efficiently and effectively.",
            duration_text=5
        )

        self.create_step(
            image_path="book_scan.jpg",
            text="Extracting text from scanned book pages has never been easier, "
                 "thanks to OCR.",
            duration_text=5
        )

        self.create_step(
            image_path="edit_search.jpg",
            text="Extracted text becomes versatile, allowing for searching and editing "
                 "with just a few clicks.",
            duration_text=5
        )

        self.create_step(
            image_path="practical_uses.jpg",
            text="Whether it's preserving old books, digitizing receipts, or processing "
                 "paper documents, OCR captures information quickly and effectively.",
            duration_text=6
        )

    def create_step(self, image_path, text, duration_text, arrow=False):
        """
        Create a visual step with an image, description text, and optional arrows.

        Args:
            image_path (str): Path to the image file used in the step.
            text (str): The description text for the step.
            duration_text (int): The duration to display the text.
            arrow (bool): Whether to add an arrow animation. Default is False.
        """
        try:
            image = ImageMobject(image_path)
            description_text = Text(text, font_size=24)

            # Display the image, text, and optional arrow animation
            self.play(FadeIn(image))
            self.wait(1)
            if arrow:
                arrow_object = Arrow(start=LEFT, end=RIGHT, buff=0.3, stroke_width=3)
                self.play(ShowCreation(arrow_object))
            self.play(Write(description_text))
            self.wait(duration_text)
            
            # Fade out animations
            self.play(FadeOut(image, description_text))
            if arrow:
                self.play(FadeOut(arrow_object))
        
        except FileNotFoundError:
            print(f"Error: {image_path} does not exist.")