from manim import *

class DeterminantVideo(Scene):
    def construct(self):
        # Scene 1: Definition of a Square Matrix
        self.show_square_matrix()

        # Scene 2: Concept of Elements within a Matrix
        self.show_matrix_elements()

        # Scene 3: Definition and Notation of a Determinant
        self.show_determinant_notation()

        # Scene 4: Importance of the Determinant in Matrix Properties
        self.show_determinant_importance()

        # Scene 5: Calculation for 2x2 Matrix Determinants
        self.calculate_2x2_determinant()

        # Scene 6: Calculation for 3x3 Matrix Determinants
        self.calculate_3x3_determinant()

        # Scene 7: Methods for Larger Matrix Determinants
        self.show_large_determinants_methods()

        # Scene 8: Significance of the Determinant in Linear Algebra
        self.show_determinant_significance()

        # Scene 9: Application Examples of Determinants in Mathematical Concepts
        self.show_applications_of_determinants()

    def show_square_matrix(self):
        grid = VGroup(*[Square() for _ in range(9)]).arrange_in_grid(rows=3, cols=3, buff=0.1)
        number_labels = VGroup(*[Text(str(i+1)).move_to(square) for i, square in enumerate(grid)])

        self.play(Create(grid), run_time=2)
        self.play(Write(number_labels), run_time=1)
        self.wait(1)

    def show_matrix_elements(self):
        # Highlight each number in the grid
        number_labels = [Text(str(i+1)).move_to(Square().get_center()) for i in range(9)]
        self.play(AnimationGroup(*[Indicate(label) for label in number_labels], lag_ratio=0.5))
        self.wait(1)

    def show_determinant_notation(self):
        detA_text = Tex(r"\text{det A} \, \text{or} \, |A|").to_edge(UP)
        self.play(Write(detA_text), run_time=2)
        self.wait(1)

    def show_determinant_importance(self):
        scale = BalanceScale().set_height(2).to_edge(UP)
        matrix_box = Square().scale(0.6).next_to(scale.left_plate, UP, buff=0.1)
        number_box = Integer(5).scale(0.6).next_to(scale.right_plate, UP, buff=0.1)

        self.play(Create(scale), FadeIn(matrix_box), FadeIn(number_box), run_time=2)
        self.play(Rotate(scale, angle=PI/8, about_point=scale.center), run_time=1)
        self.play(Rotate(scale, angle=-PI/16, about_point=scale.center), run_time=1)
        self.wait(1)

    def calculate_2x2_determinant(self):
        matrix_2x2 = Matrix([["a", "b"], ["c", "d"]])
        formula_2x2 = Tex(r"\text{det}(A) = ad - bc").next_to(matrix_2x2, RIGHT, buff=1)

        self.play(Write(matrix_2x2), run_time=2)
        self.play(Write(formula_2x2), run_time=2)
        self.wait(1)

    def calculate_3x3_determinant(self):
        matrix_3x3 = Matrix([
            ["a", "b", "c"],
            ["d", "e", "f"],
            ["g", "h", "i"],
        ])
        formula_3x3 = Tex(r"a(ei - fh) - b(di - fg) + c(dh - eg)").next_to(matrix_3x3, RIGHT, buff=1)

        self.play(Write(matrix_3x3), run_time=2)
        self.play(Write(formula_3x3), run_time=2)
        self.wait(1)

    def show_large_determinants_methods(self):
        methods_text = VGroup(
            Tex("Expansion by Minors"),
            Tex("Row Reduction")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)

        self.play(Write(methods_text), run_time=2)
        self.wait(1)
        self.play(FadeOut(methods_text), run_time=2)
    
    def show_determinant_significance(self):
        equation_path = VGroup(*[Tex(str(i)) for i in range(1, 5)]).arrange(RIGHT, buff=0.5)

        self.play(Write(equation_path), run_time=2)
        self.play(equation_path.animate.shift(LEFT * 2), run_time=2)
        self.wait(1)

    def show_applications_of_determinants(self):
        real_world_scenario1 = Text("Graphics Transformations").to_edge(LEFT)
        real_world_scenario2 = Text("Physics Vectors").to_edge(RIGHT)

        self.play(Write(real_world_scenario1), run_time=1)
        self.play(ReplacementTransform(real_world_scenario1, real_world_scenario2), run_time=1)
        self.wait(1)