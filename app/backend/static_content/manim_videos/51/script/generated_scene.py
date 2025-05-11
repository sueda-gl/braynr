from manim import *

class ManimScene(Scene):
    def construct(self):
        """Construct the scene with individual educational steps."""
        self.introduction_to_square_matrices()
        self.understanding_determinants()
        self.notation_of_determinants()
        self.determinants_for_square_matrices_only()
        self.purpose_of_determinants()
        self.reading_the_notation()
        self.calculating_determinants_for_2x2_matrix()

    def introduction_to_square_matrices(self):
        """Introduce square matrices and display a 3x3 example."""
        title = Text("What is a Square Matrix?", font_size=40).to_edge(UP)
        matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.play(Write(title), Create(matrix))
        self.wait(5)
        self.play(FadeOut(matrix, title))

    def understanding_determinants(self):
        """Explain the concept of the determinant with a visual example."""
        title = Text("The Special Number - Determinant", font_size=40).to_edge(UP)
        matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        det_label = MathTex(r"|A|", r"\text{ or }", r"\text{det}(A)").next_to(matrix, RIGHT)
        
        self.play(Write(title), Create(matrix))
        self.wait(1)
        self.play(matrix.animate.scale(0.7).shift(LEFT), FadeIn(det_label))
        self.wait(6)
        self.play(FadeOut(matrix, det_label, title))

    def notation_of_determinants(self):
        """Show notation forms for determinants."""
        title = Text("How to Write Determinants", font_size=40).to_edge(UP)
        matrix_label = MathTex("A").next_to(ORIGIN, LEFT)
        det_label_abs = MathTex(r"|A|").next_to(matrix_label, RIGHT, buff=1)
        det_label_text = MathTex(r"\text{det}(A)").next_to(det_label_abs, RIGHT, buff=1)
        
        self.play(Write(title), Write(matrix_label))
        self.play(FadeIn(det_label_abs), FadeIn(det_label_text))
        self.wait(5)
        self.play(FadeOut(matrix_label, det_label_abs, det_label_text, title))

    def determinants_for_square_matrices_only(self):
        """Clarify that only square matrices can have determinants."""
        title = Text("Who can have Determinants?", font_size=40).to_edge(UP)
        square_matrix = Matrix([[1, 2], [3, 4]]).shift(LEFT)
        non_square_matrix = Matrix([[1, 2]]).shift(RIGHT)
        check_mark = Tex(r"\checkmark").set_color(GREEN).next_to(square_matrix, DOWN)
        cross_mark = Tex("X").set_color(RED).next_to(non_square_matrix, DOWN)
        
        self.play(Write(title), Create(square_matrix), Create(non_square_matrix))
        self.wait(1)
        self.play(FadeIn(check_mark), FadeIn(cross_mark))
        self.wait(5)
        self.play(FadeOut(square_matrix, non_square_matrix, check_mark, cross_mark, title))

    def purpose_of_determinants(self):
        """Explain the importance of determinants with visuals."""
        title = Text("Why are Determinants Important?", font_size=40).to_edge(UP)
        scale = VGroup(
            Tex("Invertibility").set_color(ORANGE),
            Line(LEFT, RIGHT),
            Tex("Applications").set_color(BLUE)
        ).arrange(DOWN, buff=1).scale(0.5)
        
        self.play(Write(title), FadeIn(scale))
        self.wait(1)
        self.play(Rotate(scale, angle=0.1, rate_func=there_and_back, run_time=4))
        self.wait(7)
        self.play(FadeOut(scale, title))

    def reading_the_notation(self):
        """Differentiate the notation of determinants from modulus."""
        title = Text("Understanding |A|", font_size=40).to_edge(UP)
        det_notation = VGroup(
            Tex(r"|A| \text{ (Determinant)}"),
            Tex(r"|\cdot| \text{ (Modulus)}")
        ).arrange(DOWN, buff=1)
        
        self.play(Write(title), FadeIn(det_notation))
        self.wait(6)
        self.play(FadeOut(det_notation, title))

    def calculating_determinants_for_2x2_matrix(self):
        """Show how to calculate the determinant of a 2x2 matrix."""
        title = Text("Calculating a 2x2 Determinant", font_size=40).to_edge(UP)
        matrix = Matrix([["a", "b"], ["c", "d"]])
        det_formula = MathTex(r"ad - bc").next_to(matrix, RIGHT, buff=1)
        
        self.play(Write(title), Create(matrix))
        self.wait(1)
        self.play(Write(det_formula))
        self.wait(8)
        self.play(FadeOut(matrix, det_formula, title))