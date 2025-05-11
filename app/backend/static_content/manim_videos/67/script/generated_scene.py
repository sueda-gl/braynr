from manim import *

class ManimScene(Scene):
    """
    This class demonstrates an animation sequence explaining the concept of determinants
    using Manim. It includes scenes for introducing determinants, their applications,
    calculations for 2x2 and 3x3 matrices, implications of zero and non-zero determinants,
    geometric significance, and their importance in math and engineering.
    """
    def construct(self):
        def fade_out_sequence(*mobjects, run_time=2):
            """Reusable fade-out sequence for multiple objects."""
            self.play(*[FadeOut(mob) for mob in mobjects], run_time=run_time)

        def write_text_objects(*texts):
            """Reusable write animation for sequential text objects."""
            for text in texts:
                self.play(Write(text))
                self.wait(1)

        # 1. Introducing Determinants
        matrix_2x2 = Matrix([[Text("a"), Text("b")], [Text("c"), Text("d")]], element_alignment_corner=DOWN)
        matrix_3x3 = Matrix([
            [Text("a"), Text("b"), Text("c")],
            [Text("d"), Text("e"), Text("f")],
            [Text("g"), Text("h"), Text("i")]
        ], element_alignment_corner=DOWN)
        matrix_2x2.shift(LEFT * 3)
        self.play(Create(matrix_2x2))
        self.wait(1)

        self.play(ReplacementTransform(matrix_2x2, matrix_3x3))
        self.wait(1)
        
        fade_out_sequence(matrix_3x3)

        # 2. Applications of Determinants
        equations = Text("Solving Linear Equations")
        transformations = Text("Geometry Transformations")
        inverse_check = Text("Matrix Invertibility")
        applications_group = VGroup(equations, transformations, inverse_check).arrange(RIGHT, buff=2)
        self.play(Write(applications_group))
        self.wait(2)

        fade_out_sequence(applications_group, run_time=3)

        # 3. 2x2 Matrix Determinant Calculation
        det_2x2 = Matrix([[Text("a"), Text("b")], [Text("c"), Text("d")]], element_alignment_corner=DOWN)
        arrow_ad = Arrow(det_2x2.get_center() + LEFT * 0.5 + UP * 0.5, det_2x2.get_center() + RIGHT * 0.5 + DOWN * 0.5, buff=0)
        arrow_bc = Arrow(det_2x2.get_center() + RIGHT * 0.5 + UP * 0.5, det_2x2.get_center() + LEFT * 0.5 + DOWN * 0.5, buff=0)
        self.play(Create(det_2x2), Create(arrow_ad), Create(arrow_bc))
        self.wait(1)

        minus_sign = Text("-").next_to(det_2x2, RIGHT)
        self.play(Write(minus_sign))
        self.wait(1)

        fade_out_sequence(det_2x2, arrow_ad, minus_sign, arrow_bc)

        # 4. 3x3 Matrix Determinant
        det_3x3 = Matrix([
            [Text("a"), Text("b"), Text("c")],
            [Text("d"), Text("e"), Text("f")],
            [Text("g"), Text("h"), Text("i")]
        ], element_alignment_corner=DOWN)
        self.play(Create(det_3x3))
        self.wait(1)

        factor_matrix = Matrix([[Text("e"), Text("f")], [Text("h"), Text("i")]], element_alignment_corner=DOWN).move_to(det_3x3.get_center() + RIGHT * 3)
        self.play(Write(factor_matrix))
        self.wait(2)

        fade_out_sequence(det_3x3, factor_matrix, run_time=4)

        # 5. Higher Order Matrices
        large_matrix = Matrix([[Text("a"), Text("b"), Text("c"), Text("d")],
                               [Text("e"), Text("f"), Text("g"), Text("h")],
                               [Text("i"), Text("j"), Text("k"), Text("l")],
                               [Text("m"), Text("n"), Text("o"), Text("p")]])
        self.play(Create(large_matrix))
        self.wait(2)

        fade_out_sequence(large_matrix, run_time=5)

        # 6. Zero Determinant Implications
        zero_det_text = Text("Zero Determinant")
        no_inverse = Text("No Inverse", color=RED).next_to(zero_det_text, DOWN)
        no_solution = Text("No Unique Solution", color=RED).next_to(no_inverse, DOWN)
        write_text_objects(zero_det_text, no_inverse, no_solution)

        fade_out_sequence(zero_det_text, no_inverse, no_solution, run_time=3)

        # 7. Non-zero Determinant Implications
        non_zero_det_text = Text("Non-zero Determinant")
        has_inverse = Text("Has Inverse", color=GREEN).next_to(non_zero_det_text, DOWN)
        unique_solution = Text("Unique Solution", color=GREEN).next_to(has_inverse, DOWN)
        write_text_objects(non_zero_det_text, has_inverse, unique_solution)

        fade_out_sequence(non_zero_det_text, has_inverse, unique_solution, run_time=3)

        # 8. Geometric Significance
        shapes = VGroup(
            Square(color=BLUE).shift(LEFT),
            Triangle(color=ORANGE).shift(RIGHT)
        ).arrange(buff=1)
        self.play(Create(shapes))
        self.wait(1)

        for shape in shapes:
            self.play(shape.animate.scale(0.5))
        
        self.wait(1)
        fade_out_sequence(shapes, run_time=4)

        # 9. Importance in Math and Engineering
        importance_texts = VGroup(
            Text("Mathematicians:"),
            Text("Engineers:")
        ).arrange(DOWN, aligned_edge=LEFT)
        self.play(Write(importance_texts))

        self.wait(2)
        fade_out_sequence(importance_texts, run_time=3)

        # 10. Conclusion
        conclusion = Text("Explore Determinants", color=YELLOW)
        self.play(Write(conclusion))

        self.wait(3)
        fade_out_sequence(conclusion)