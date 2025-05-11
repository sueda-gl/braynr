from manim import *

# Helper function to create a square matrix with numbers
def create_matrix(m, n):
    if m <= 0 or n <= 0:
        raise ValueError("Matrix dimensions must be positive integers.")
    return VGroup(*[
        VGroup(*[
            Rectangle(width=0.8, height=0.8, color=WHITE)
            .move_to((x, y, 0))
            for x in range(n)
        ]) for y in range(m)
    ]).arrange(DOWN, buff=0)

# Helper function to fill the matrix with numbers
def fill_matrix(matrix, start=1):
    numbers = VGroup(*[
        Text(str(start + i), font_size=24).move_to(cell)
        for i, cell in enumerate(matrix)
    ])
    return numbers

class ManimScene(Scene):
    def construct(self):
        # Illustrate the concept of a matrix
        self.understanding_matrix()
        
        # Explain what a square matrix is
        self.square_matrix_explained()
        
        # Introduce the concept of the determinant
        self.introduction_to_determinant()
        
        # Showcase types of determinant values
        self.types_of_determinant_values()
        
        # Highlight the importance of determinants
        self.importance_of_determinants()
        
        # Show relationship between determinat and invertibility
        self.determinant_and_invertibility()
        
        # Explain notation of determinants
        self.notation_of_determinants()
        
        # Discuss determinant calculation based on matrix size
        self.calculating_determinants_by_size()
        
        # Show complexity for larger matrices
        self.complexity_with_larger_matrices()
        
        # Provide a concrete example with a 2x2 matrix
        self.example_of_twobytwo_matrix()
        
        # Discuss methods for larger matrices
        self.methods_for_larger_matrices()
        
        # Provide a general explanation note
        self.general_explanation_note()
        
        # Offer further elaboration on the topic
        self.further_elaboration()

    def understanding_matrix(self):
        # Step 1: Understanding a Matrix
        matrix_3x3 = create_matrix(3, 3).to_edge(UP)
        matrix_numbers = fill_matrix([cell for row in matrix_3x3 for cell in row])
        self.play(Create(matrix_3x3))
        self.play(Write(matrix_numbers))
        matrix_caption = Text(
            "A matrix is an arrangement of numbers in rows and columns.", 
            font_size=30
        ).to_edge(DOWN)
        self.play(Write(matrix_caption))
        self.wait(5)
        self.play(FadeOut(matrix_3x3), FadeOut(matrix_numbers), FadeOut(matrix_caption))

    def square_matrix_explained(self):
        # Step 2: Square Matrix Explained
        square_matrix = create_matrix(3, 3)
        self.play(Create(square_matrix), run_time=2)
        square_caption = Text(
            "A square matrix has an equal number of rows and columns.", 
            font_size=30
        ).to_edge(DOWN)
        self.play(Write(square_caption))
        self.wait(4)
        self.play(FadeOut(square_matrix), FadeOut(square_caption))

    def introduction_to_determinant(self):
        # Step 3: Introduction to the Determinant
        square_matrix = create_matrix(3, 3)
        determinant_label = Text("Determinant", font_size=30).next_to(square_matrix, UP)
        self.play(Create(square_matrix), Write(determinant_label), run_time=2)
        self.wait(4)
        self.play(FadeOut(square_matrix), FadeOut(determinant_label))

    def types_of_determinant_values(self):
        # Step 4: Types of Determinant Values
        real_value = Text("Real", font_size=24, color=GREEN).to_edge(LEFT)
        complex_value = Text("Complex", font_size=24, color=BLUE).to_edge(RIGHT)
        self.play(Write(real_value), Write(complex_value))
        self.wait(4)
        self.play(FadeOut(real_value), FadeOut(complex_value))

    def importance_of_determinants(self):
        # Step 5: Importance of Determinants
        magnifying_glass = Square(color=YELLOW).scale(1.5).to_edge(UP)
        self.play(Create(magnifying_glass))
        self.wait(5)
        self.play(FadeOut(magnifying_glass))

    def determinant_and_invertibility(self):
        # Step 6: Determinant and Invertibility
        matrix_a = create_matrix(3, 3).to_edge(LEFT)
        matrix_b = create_matrix(3, 3).to_edge(RIGHT)
        self.play(Create(matrix_a), Create(matrix_b))
        inverse_label = Text("Inverse", font_size=24, color=RED).next_to(matrix_b, UP)
        self.play(Write(inverse_label))
        self.wait(6)
        self.play(FadeOut(matrix_a), FadeOut(matrix_b), FadeOut(inverse_label))

    def notation_of_determinants(self):
        # Step 7: Notation of Determinants
        det_notation = Text("det(A)", font_size=24).to_edge(LEFT)
        abs_notation = Text("|A|", font_size=24).to_edge(RIGHT)
        self.play(Write(det_notation), Write(abs_notation))
        self.wait(3)
        self.play(FadeOut(det_notation), FadeOut(abs_notation))

    def calculating_determinants_by_size(self):
        # Step 8: Calculating Determinants by Size
        small_matrix = create_matrix(2, 2).to_edge(LEFT)
        large_matrix = create_matrix(4, 4).to_edge(RIGHT)
        self.play(Create(small_matrix), Create(large_matrix))
        self.wait(5)
        self.play(FadeOut(small_matrix), FadeOut(large_matrix))

    def complexity_with_larger_matrices(self):
        # Step 9: Complexity with Larger Matrices
        complex_matrix = create_matrix(5, 5).scale(0.5)
        self.play(Create(complex_matrix))
        self.wait(4)
        self.play(FadeOut(complex_matrix))

    def example_of_twobytwo_matrix(self):
        # Step 10: Example of a 2x2 Matrix
        twobytwo_matrix = VGroup(
            Text("a", font_size=24).move_to([-1, 1, 0]),
            Text("b", font_size=24).move_to([1, 1, 0]),
            Text("c", font_size=24).move_to([-1, -1, 0]),
            Text("d", font_size=24).move_to([1, -1, 0]),
        )
        self.play(Write(twobytwo_matrix))
        determinant_formula = Text("ad - bc", font_size=24, color=RED).next_to(twobytwo_matrix, DOWN)
        self.play(Write(determinant_formula))
        self.wait(5)
        self.play(FadeOut(twobytwo_matrix), FadeOut(determinant_formula))

    def methods_for_larger_matrices(self):
        # Step 11: Methods for Larger Matrices
        detailed_matrix = create_matrix(4, 4).scale(0.5)
        self.play(Create(detailed_matrix))
        self.wait(6)
        self.play(FadeOut(detailed_matrix))

    def general_explanation_note(self):
        # Step 12: General Explanation Note
        explanation_note = Text("This is a general explanation due to the request 'DSFADF.'", font_size=30).to_edge(UP)
        self.play(Write(explanation_note))
        self.wait(3)
        self.play(FadeOut(explanation_note))

    def further_elaboration(self):
        # Step 13: Further Elaboration
        book_icon = Square(color=ORANGE).scale(1.5).to_edge(DOWN)
        further_details_text = Text(
            "Specific aspects of determinants can be further elaborated if needed.", 
            font_size=24
        ).next_to(book_icon, UP)
        self.play(Create(book_icon), Write(further_details_text))
        self.wait(5)
        self.play(FadeOut(book_icon), FadeOut(further_details_text))