from manim import *

class ManimScene(Scene):
    """
    A Manim scene for teaching the concept of determinants in linear algebra.
    The scene includes several animations that visually explain determinants,
    their calculation, and their significance in transformations.
    """
    def construct(self):
        self.introduction_to_square_matrices()
        self.understanding_the_determinant()
        self.importance_of_determinants()
        self.determinant_as_scaling_measure()
        self.calculating_for_2x2_matrix()
        self.interpretation_of_the_determinant()
        self.higher_dimensions()
        self.determinants_in_linear_algebra()

    def introduction_to_square_matrices(self):
        """
        Introduces square matrices using a 3x3 grid.
        Grids are visually appealing and help recognize the layout of matrices.
        """
        grid = VGroup(*[Text(f"{i+j+1}", font_size=36)
                        for i in range(3) for j in range(3)]
                      ).arrange_in_grid(rows=3, buff=0.5)
        caption = Text("A square matrix is a table of numbers with the same number of rows and columns.", font_size=24, color=YELLOW)
        narration = Text("Matrices form the cornerstone of linear algebra. Here's your simplest form—a square matrix.", font_size=24, color=WHITE)

        self.play(Create(grid), run_time=3)
        self.wait(2)
        self.play(Write(caption, run_time=3), Write(narration, run_time=3))
        self.wait(3)

    def understanding_the_determinant(self):
        """
        Explains the concept of the determinant with visual transformation
        of a matrix into a clear, conceptual representation ('?') followed by 'Determinant'.
        """
        matrix_elements = VGroup(*[Text(str(i), font_size=36) for i in range(1, 10)]).arrange_in_grid(rows=3, buff=0.5)
        question_mark = Text("?", font_size=72, color=RED).move_to(matrix_elements)
        determinant_word = Text("Determinant", font_size=48, color=BLUE).next_to(question_mark, DOWN)

        self.play(FadeIn(matrix_elements), run_time=2)
        self.play(Transform(matrix_elements, question_mark), run_time=3)
        self.play(Transform(question_mark, determinant_word), run_time=2)
        self.wait(3)

    def importance_of_determinants(self):
        """
        Highlights the importance of determinants in linear algebra.
        Uses lock and key symbolism to represent unlocking matrix properties.
        """
        matrix = Square(side_length=2)
        lock = Text("🔒", font_size=48).move_to(matrix)
        key = Text("🔑", font_size=48).next_to(lock, LEFT)
        properties = Text("Invertibility & Transformations", font_size=36, color=GREEN).next_to(lock, DOWN)

        self.play(Create(matrix))
        self.play(FadeIn(lock), FadeIn(key))
        self.play(Rotate(key, angle=PI / 2), run_time=2)
        self.play(FadeOut(lock), FadeOut(key), FadeIn(properties))
        self.wait(3)

    def determinant_as_scaling_measure(self):
        """
        Demonstrates how determinants measure scaling by transforming a small
        square into a larger one, indicating area expansion.
        """
        square = Square(side_length=1, color=BLUE)
        big_square = Square(side_length=2, color=GREEN).move_to(square)

        self.play(GrowFromCenter(square))
        self.play(Transform(square, big_square), run_time=3)
        caption = Text("Determinants measure how much a transformation scales areas or volumes.", font_size=24, color=YELLOW).to_edge(DOWN)
        self.wait(1)
        self.play(Write(caption), run_time=3)
        self.wait(2)

    def calculating_for_2x2_matrix(self):
        """
        Provides a straightforward example of calculating the determinant
        for a 2x2 matrix using the formula `ad - bc`.
        """
        matrix = Text("Matrix | a  b |\n      | c  d |", font_size=36)
        formula = Text("Formula: ad - bc", font_size=36).next_to(matrix, DOWN)

        self.play(FadeIn(matrix))
        self.wait(2)
        self.play(Write(formula), run_time=3)
        self.wait(3)

    def interpretation_of_the_determinant(self):
        """
        Illustrates the interpretation of determinant values.
        Uses shapes and arrows to show stable areas, flipping, and collapsing.
        """
        stable_area = Square(side_length=1, color=WHITE)
        flipping_arrow = Arrow(LEFT, RIGHT, color=RED)
        collapse_line = Line(LEFT, RIGHT, color=YELLOW)

        scenarios = VGroup(stable_area, flipping_arrow, collapse_line).arrange(RIGHT, buff=1.5)

        self.play(Create(stable_area), Create(flipping_arrow), Create(collapse_line))
        self.wait(3)
        caption = Text("The value of a determinant indicates how space transformation impacts, such as flipping or collapsing.",
                       font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(Write(caption), run_time=3)
        self.wait(3)

    def higher_dimensions(self):
        """
        Explores determinants in higher dimensions with complex object visualizations.
        Utilizes a 3D cube and swirling numbers to portray complexity.
        """
        complex_object = Cube().scale(0.5)
        swirling_numbers = Tex("1", "2", "3", "4", "5").arrange_in_grid(buff=1).next_to(complex_object, UP)

        self.play(ShowCreation(complex_object))
        self.play(FadeIn(swirling_numbers))
        self.wait(2)
        caption = Text("In higher dimensions, determinants are more complex, maintaining insights into spatial changes.",
                       font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(Write(caption), run_time=3)
        self.wait(3)

    def determinants_in_linear_algebra(self):
        """
        Concludes with the role of determinants in linear algebra.
        Shows algebraic equations emphasizing the significance of determinants.
        """
        equation = Text("Equation: Ax = y", font_size=36)
        glowing_det = Text("det(A)", font_size=36, color=YELLOW).next_to(equation, RIGHT)

        self.play(Write(equation))
        self.play(FadeIn(glowing_det))
        self.wait(2)
        caption = Text("Determinants are key in linear algebra, essential for operations and applications.",
                       font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(Write(caption), run_time=3)
        self.wait(3)