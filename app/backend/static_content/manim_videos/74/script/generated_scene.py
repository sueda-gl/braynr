from manim import *

class ManimScene(Scene):
    def construct(self):
        # Step 1: Understanding Square Matrices
        matrix = self.create_matrix([[5, 3, 1], [2, 7, 4], [6, 9, 8]])
        self.play(Create(matrix), run_time=2)
        self.play(matrix.animate.rotate(0.1 * PI), matrix.animate.rotate(-0.1 * PI), run_time=3, rate_func=smooth)
        self.add_caption("A square matrix is a grid of numbers with identical rows and columns, like this 3x3 matrix.")
        
        # Step 2: Introduction to the Determinant
        mystery_number = Tex("|A|").next_to(matrix, DOWN)
        arrow = Arrow(start=mystery_number.get_top(), end=matrix.get_bottom(), buff=0.1)
        self.play(Indicate(matrix), FadeIn(mystery_number), GrowArrow(arrow), run_time=3)
        self.add_caption("The determinant is a special number we can calculate from a square matrix.")
        
        # Step 3: Real or Complex Values
        real_numbers = Text("Real: -1, 0, 2").to_edge(LEFT)
        complex_numbers = Text("Complex: 2 + 3i").to_edge(RIGHT)
        self.play(LaggedStart(FadeIn(real_numbers), FadeIn(complex_numbers), lag_ratio=0.5), run_time=2)
        self.play(real_numbers.animate.set_color(YELLOW), complex_numbers.animate.set_color(PURPLE),
                  run_time=2, rate_func=there_and_back)
        self.add_caption("A determinant can be a real number or a complex number with an imaginary part.")
        
        # Step 4: Importance of the Determinant
        scale1 = self.create_scale("Inverse Exists", 1)
        scale2 = self.create_scale("No Inverse", 0)
        self.play(FadeIn(scale1), FadeIn(scale2), run_time=2)
        self.add_caption("The determinant tells us if a matrix has an inverse. A zero determinant means no inverse!")
        
        # Step 5: Notation for Determinants
        matrix.generate_target()
        matrix.target.shift(UP * 2)
        notation_text1 = Tex("|A|").next_to(matrix.target, 0.5 * RIGHT)
        notation_text2 = Tex("det A").next_to(matrix.target, 0.5 * RIGHT)
        self.play(MoveToTarget(matrix), Transform(mystery_number, notation_text1), run_time=2)
        self.play(Transform(mystery_number, notation_text2), run_time=2)
        self.add_caption("We denote the determinant of a matrix A by |A| or det A.")
        
        # Step 6: Calculation Method
        step_by_step = VGroup(
            self.step_text("det(A) = a*d - b*c", color=BLUE),
            self.arrow_obj(a='a', b='b', c='c', d='d')
        ).arrange(DOWN, buff=0.5).to_edge(DOWN)
        self.play(Write(step_by_step), run_time=3)
        self.add_caption("Different sized matrices have specific methods to calculate their determinants.")
        
        # Step 7: Video Explanation
        video_button = RoundedRectangle(corner_radius=0.2, width=3, height=1, color=YELLOW).shift(DOWN * 3)
        play_icon = Triangle().scale(0.4).move_to(video_button)
        self.play(FadeIn(video_button), DrawBorderThenFill(play_icon))
        self.add_caption("Watch a video for a clear explanation and detailed steps in calculating determinants in linear algebra!")
        
    def create_matrix(self, matrix_values):
        assert all(len(row) == len(matrix_values) for row in matrix_values), "Matrix must be square"
        matrix_mobjects = [[Text(str(item)).scale(0.7) for item in row] for row in matrix_values]
        return VGroup(*[VGroup(*row).arrange(RIGHT, buff=0.5) for row in matrix_mobjects]).arrange(DOWN, buff=0.5).to_edge(UP)
    
    def create_scale(self, label, position_factor):
        scale = VGroup(
            Line(LEFT, RIGHT, color=WHITE),
            Line(DOWN, UP, color=WHITE).shift(LEFT * 2),
            Line(DOWN, UP, color=WHITE).shift(RIGHT * 2),
            Text(label).scale(0.5).next_to(DOWN * 0.5, UP)
        ).arrange(RIGHT, buff=0.5)
        return scale.shift(position_factor * UP * 0.2)

    def step_text(self, text, color=WHITE):
        return Tex(text, color=color).scale(0.7)

    def arrow_obj(self, **kwargs):
        a = Text(f"{kwargs.get('a', '')}".upper()).scale(0.7)
        b = Text(f"{kwargs.get('b', '')}".upper()).scale(0.7)
        c = Text(f"{kwargs.get('c', '')}".upper()).scale(0.7)
        d = Text(f"{kwargs.get('d', '')}".upper()).scale(0.7)
        arrow = Arrow(a.get_center(), d.get_center(), buff=0.1)
        return VGroup(a, b, c, d, arrow).arrange(RIGHT, buff=0.5)
    
    def add_caption(self, text):
        caption = Text(text, color=GREY, font_size=24).to_corner(DOWN)
        self.play(Write(caption), run_time=4)