from manim import *

class ManimScene(Scene):
    def construct(self):
        # Sequence of scenes in the storyboard
        self.introduction_to_determinants()
        self.understanding_square_matrices()
        self.notation_of_determinants()
        self.properties_highlight()
        self.applicability_in_math_and_engineering()
        self.simple_matrix_determinant()
        self.misconceptions_about_determinants()
        self.invertibility_information()
        self.further_exploration()

    def introduction_to_determinants(self):
        """Displays an introduction to the concept of determinants."""
        title = Text("Determinant: A Special Number", font_size=48).to_edge(UP)
        matrix = self.create_matrix([[1, 2], [3, 4]], 2, 2).scale(1.5)
        caption = Text("Determinante ist eine spezielle Zahl verbunden mit einer quadratischen Matrix.", font_size=24).next_to(matrix, DOWN)
        self.play(Write(title), Create(matrix), Write(caption))
        self.wait(2)
        self.play(Rotate(matrix, angle=PI, run_time=2, rate_func=smooth), FadeOut(caption))
        self.play(FadeOut(matrix, title))

    def understanding_square_matrices(self):
        """Explains what square matrices are, using different grid examples."""
        title = Text("What is a Square Matrix?", font_size=48).to_edge(UP)
        self.play(Write(title))
        
        matrices = [
            self.create_matrix([[1, 2], [3, 4]], 2, 2, color=BLUE),
            self.create_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 3, color=GREEN)
        ]
        captions = [
            Text("2x2 Square Matrix", font_size=24).next_to(matrices[0], DOWN),
            Text("3x3 Square Matrix", font_size=24).next_to(matrices[1], DOWN)
        ]
        
        for matrix, caption in zip(matrices, captions):
            self.play(Create(matrix), Write(caption), run_time=2)
            self.wait(1)
            self.play(FadeOut(matrix, caption), run_time=1)

    def notation_of_determinants(self):
        """Shows how to write the notation for determinants."""
        title = Text("How to Write a Determinant", font_size=48).to_edge(UP)
        notation = Text("det(A) or |A|", font_size=36)
        matrix = self.create_matrix([[1, 0], [0, 1]], 2, 2).next_to(notation, DOWN)
        caption = Text("Determinate wird oft als 'det A' oder |A| geschrieben.", font_size=24).next_to(matrix, DOWN)
        
        self.play(Write(title), Write(notation))
        self.play(Create(matrix), Write(caption))
        self.wait(2)
        self.play(FadeOut(matrix, notation, caption, title))

    def properties_highlight(self):
        """Highlights the properties conveyed by the determinant of a matrix."""
        title = Text("What Does a Determinant Tell Us?", font_size=48).to_edge(UP)
        matrix = self.create_matrix([[2, 3], [1, 4]], 2, 2)
        caption = Text("Sie zeigt bestimmte Eigenschaften der Matrix auf.", font_size=24).next_to(matrix, DOWN)
        
        self.play(Write(title), Create(matrix))
        self.play(Indicate(matrix[0][0], color=YELLOW), Indicate(matrix[1][1], color=YELLOW))
        self.play(Write(caption))
        self.wait(2)
        self.play(FadeOut(matrix, caption, title))

    def applicability_in_math_and_engineering(self):
        """Illustrates the usefulness of determinants in mathematics and engineering."""
        title = Text("Why Are Determinants Useful?", font_size=48).to_edge(UP)
        concepts = [
            Text("Physics Equation: F = ma", font_size=24, color=RED),
            Text("Blueprints for Structures", font_size=24, color=BLUE),
            Text("Mechanical Engineering", font_size=24, color=GREEN)
        ]
        
        self.play(Write(title))
        for concept in concepts:
            self.play(Write(concept))
            self.wait(3)
            self.play(FadeOut(concept))
        self.play(FadeOut(title))

    def simple_matrix_determinant(self):
        """Explains the determinant of a 1x1 matrix."""
        title = Text("Determinant of a 1x1 Matrix", font_size=48).to_edge(UP)
        number = Text("5", font_size=72)
        matrix_representation = self.create_matrix([[5]], 1, 1).next_to(number, RIGHT)
        equals = Text("=", font_size=36).next_to(number, LEFT)
        caption = Text("Für eine 1x1 Matrix ist die Determinante die Zahl selbst.", font_size=24).next_to(matrix_representation, DOWN)
        
        self.play(Write(title), Write(number), Write(equals), Create(matrix_representation), Write(caption))
        self.wait(3)
        self.play(FadeOut(number, equals, matrix_representation, caption, title))

    def misconceptions_about_determinants(self):
        """Clarifies common misconceptions about what a determinant is not."""
        title = Text("Understanding What a Determinant Is Not", font_size=48).to_edge(UP)
        misconceptions = [
            Text("Wert der Matrix"),
            Text("Modul der Matrix")
        ]
        matrix = self.create_matrix([[1, 2], [3, 4]], 2, 2)
        corrections = [term.copy().set_color(RED).next_to(matrix, RIGHT) for term in misconceptions]

        self.play(Write(title), Create(matrix))
        for term, correct in zip(misconceptions, corrections):
            self.play(Write(term), Transform(term, correct), run_time=2)
            self.wait(1)
        self.play(FadeOut(matrix, title, *misconceptions))

    def invertibility_information(self):
        """Shows the link between determinants and the invertibility of matrices."""
        title = Text("Determinants and Invertibility", font_size=48).to_edge(UP)
        matrix = self.create_matrix([[2, 1], [1, 2]], 2, 2)
        inverse_matrix = self.create_matrix([[2, -1], [-1, 2]], 2, 2).move_to(matrix)
        
        caption = Text("Sie liefert Informationen über die Umkehrbarkeit der Matrix.", font_size=24).next_to(matrix, DOWN)
        self.play(Write(title), Create(matrix), Write(caption))
        self.play(Transform(matrix, inverse_matrix, run_time=2))
        self.wait(2)
        self.play(FadeOut(matrix, caption, title))

    def further_exploration(self):
        """Encourages viewers to explore more about determinants and their properties."""
        title = Text("Learn More Through Determinants", font_size=48).to_edge(UP)
        matrices = [
            self.create_matrix([[1]], 1, 1, color=YELLOW),
            self.create_matrix([[0, 1], [1, 0]], 2, 2, color=ORANGE),
            self.create_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 3, color=PURPLE)
        ]
        
        self.play(Write(title))
        for matrix in matrices:
            self.play(Create(matrix))
            self.wait(2)
            self.play(FadeOut(matrix))
        self.play(FadeOut(title))

    def create_matrix(self, elements, rows, cols, color=WHITE):
        """Utility method to create a VGroup matrix with given elements and color."""
        matrix = VGroup()
        for i in range(rows):
            row = VGroup()
            for j in range(cols):
                element = Square()\
                    .scale(0.5)\
                    .set_stroke(color)\
                    .set_fill(opacity=0)\
                    .set_height(0.5)\
                    .shift(j*RIGHT*0.5 + i*DOWN*0.5)
                number = Text(str(elements[i][j]), font_size=24).move_to(element)
                row.add(VGroup(element, number))
            matrix.add(row)
        matrix.move_to(ORIGIN)
        return matrix