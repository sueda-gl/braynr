from manim import *
import numpy as np

class ManimScene(Scene):
    def draw_intro_scene(self):
        # Draw the main computer screen with code editors
        computer_screen = Rectangle(width=4, height=3, color=WHITE)
        code_editor_left = Rectangle(width=1.5, height=3, color=BLUE).next_to(
            computer_screen, LEFT, buff=0.1
        )
        code_editor_right = Rectangle(width=1.5, height=3, color=GREEN).next_to(
            computer_screen, RIGHT, buff=0.1
        )
        
        # Simulate dataflow lines
        dataflow_lines = VGroup(*[
            Line(np.array([-2, 0.7 - i * 0.3, 0]), np.array([2, 0.7 - i * 0.3, 0]), color=YELLOW)
            for i in range(5)
        ])
        
        self.play(FadeIn(computer_screen), FadeIn(code_editor_left), FadeIn(code_editor_right))
        self.play(Create(dataflow_lines))
        self.wait(1)

    def draw_python_scene(self):
        python_logo = Circle(radius=1, color=ORANGE).add(
            MarkupText("Python", color=WHITE).scale(0.5)
        )
        main_stream = Arrow(LEFT*3, RIGHT*3, buff=0, color=BLUE)
        sub_streams = VGroup(*[
            Arrow(main_stream.get_end(), main_stream.get_end() + DOWN * i, buff=0.1, color=GREEN)
            for i in range(1, 4)
        ])
        
        self.play(FadeIn(python_logo), Create(main_stream))
        self.play(Create(sub_streams))
        self.wait(1)

    def draw_fastapi_scene(self):
        construction = VGroup(*[
            Rectangle(width=0.5, height=0.3, color=BLUE) for _ in range(5)
        ]).arrange(RIGHT, buff=0.2)
        workers = VGroup(*[
            MarkupText("W").scale(0.5) for _ in range(5)
        ]).arrange(RIGHT, buff=1)
        workers.next_to(construction, UP, buff=0.1)
        label = MarkupText("FastAPI", color=WHITE).next_to(workers, UP, buff=0.3)
        
        self.play(FadeIn(construction), FadeIn(workers), Write(label))
        self.wait(1)

    def draw_google_adk_scene(self):
        phone_parts = VGroup(*[
            Line(LEFT, RIGHT, color=GREY).shift(DOWN*i) for i in range(5)
        ]).arrange(DOWN, buff=0.1)
        tools = VGroup(*[
            Square(side_length=0.2, color=PURPLE).shift(RIGHT*j+UP*i) for i, j in [(0,1), (1,0), (-1,-1), (-1, 1)]
        ])
        self.play(LaggedStart(*[Create(part) for part in phone_parts], lag_ratio=0.1))
        self.play(LaggedStart(*[FadeIn(tool) for tool in tools], lag_ratio=0.2))
        self.wait(1)
        
    def draw_openai_scene(self):
        brain = VGroup(*[
            Circle(radius=0.3, color=BLUE).shift(RIGHT*i*0.3) for i in range(-3, 4)
        ])
        gears = VGroup(*[
            Polygon(LEFT, UP, RIGHT, DOWN, color=WHITE).scale(0.1).shift(RIGHT*0.6*i)
            for i in range(-4, 5)
        ])
        connections = VGroup(*[
            Line(RIGHT*0.6*i, RIGHT*0.6*(i+0.5), color=BLUE) for i in range(-3, 3)
        ])
        self.play(Create(brain))
        self.play(FadeIn(gears), Create(connections))
        self.wait(1)

    def draw_sqlalchemy_scene(self):
        books = VGroup(*[
            Rectangle(width=0.6, height=0.3, color=RED).shift(LEFT*2 + DOWN*i*0.4) for i in range(6)
        ])
        database = Cylinder(height=1, radius=0.5, direction=UP, fill_opacity=0.5).shift(2*RIGHT)
        self.play(LaggedStart(*[FadeIn(book) for book in books], lag_ratio=0.2))
        self.play(Transform(books, database))
        self.wait(1)

    def draw_postgresql_scene(self):
        castle = VGroup(*[
            Rectangle(width=0.3, height=1, color=GREY) for _ in range(7)
        ]).arrange(RIGHT, buff=0)
        data_streams = VGroup(*[
            Arrow(castle.get_center(), castle.get_center() + np.array([0.5*(-1)**i, -0.5, 0]), color=GREEN)
            for i in range(4)
        ])
        self.play(FadeIn(castle))
        self.play(Create(data_streams))
        self.wait(1)
        
    def draw_synergy_scene(self):
        gears = VGroup(*[
            Circle(radius=0.1*i, color=YELLOW).shift(RIGHT*i*0.3) for i in range(10)
        ])
        motor = Gear(outer_radius=2, inner_radius=1.5, teeth_count=12, color=BLUE).shift(LEFT*3)
        
        self.play(Create(gears))
        self.play(Transform(gears, motor))
        self.wait(1)

    def draw_family_coordination_scene(self):
        app_ui = RoundedRectangle(corner_radius=0.2, width=3, height=4, color=WHITE)
        calendar = VGroup(*[
            Rectangle(width=0.3, height=0.3, stroke_color=RED).shift(RIGHT*i*0.5+UP*j*0.5)
            for i in range(4) for j in range(-3, 0)
        ])
        notes = VGroup(*[
            MarkupText("Note", color=GREEN).scale(0.5).shift(DOWN*3+RIGHT*(i-1.5)) for i in range(4)
        ])
        
        self.play(FadeIn(app_ui))
        self.play(Create(calendar))
        self.play(FadeIn(notes))
        self.wait(1)

    def draw_conclusion_scene(self):
        family = VGroup(*[
            Rectangle(width=0.4, height=0.4, color=BLUE).shift(RIGHT*i) for i in range(5)
        ])
        activity = MarkupText("Family Activity", color=GREEN).scale(0.8).next_to(family, UP, buff=0.5)
        
        self.play(FadeIn(family), Write(activity))
        self.wait(1)

    def construct(self):
        super().construct()
        self.draw_intro_scene()
        self.play(ApplyMethod(self.camera.frame.scale, 1.2, run_time=1))
        self.draw_python_scene()
        self.transition()
        self.draw_fastapi_scene()
        self.transition()
        self.draw_google_adk_scene()
        self.transition()
        self.draw_openai_scene()
        self.transition()
        self.draw_sqlalchemy_scene()
        self.transition()
        self.draw_postgresql_scene()
        self.transition()
        self.draw_synergy_scene()
        self.transition()
        self.draw_family_coordination_scene()
        self.transition()
        self.draw_conclusion_scene()

    def transition(self):
        self.wait(0.5)
        self.play(FadeOut(*self.mobjects), rate_func=smooth)