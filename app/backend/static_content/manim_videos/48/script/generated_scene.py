from manim import *
import numpy as np

class TrustAndCultureScene(Scene):
    def construct(self):
        # Set theme colors for consistent styling
        theme_colors = {
            "handshake": YELLOW,
            "meeting": RED,
            "consultant": GREEN,
            "client": BLUE,
            "text": WHITE
        }

        # Execute each scene method
        self.trust_foundation_scene(theme_colors)
        self.influence_of_trust_scene(theme_colors)
        self.cultural_factors_scene(theme_colors)
        self.communication_styles_scene(theme_colors)
        self.cultural_differences_scene(theme_colors)
        self.trust_approaches_scene(theme_colors)
        self.relationship_navigation_scene(theme_colors)
        self.adaptive_methods_scene(theme_colors)
        self.scenario_demonstration_scene(theme_colors)
        self.tips_for_enhancement_scene(theme_colors)
        self.stronger_relationships_scene(theme_colors)
        self.successful_outcomes_scene(theme_colors)

    def trust_foundation_scene(self, colors):
        left_hand = Line(start=LEFT * 0.5, end=ORIGIN, color=colors["consultant"]).rotate(PI/4)
        right_hand = Line(start=RIGHT * 0.5, end=ORIGIN, color=colors["client"]).rotate(-PI/4)
        hands = VGroup(left_hand, right_hand).shift(UP)

        self.play(GrowFromCenter(hands, rate_func=smooth), run_time=1.5)
        glowing_hands = hands.copy().set_color(colors["handshake"])
        self.play(Transform(hands, glowing_hands, rate_func=smooth), run_time=1.5)

        self.wait(1)
        self.play(FadeOut(hands))

    def influence_of_trust_scene(self, colors):
        heights = [1, 2, 2.5, 3]
        bars = VGroup(*[Rectangle(width=0.3, height=h, color=colors["meeting"]).shift(RIGHT * i) for i, h in enumerate(heights)])
        line_graph = Line(start=bars[0].get_top(), end=bars[-1].get_top() + UP * 0.5, color=colors["handshake"]).shift(LEFT * 0.3)
        self.play(Create(bars, rate_func=smooth), Create(line_graph, rate_func=smooth), run_time=2)

        self.wait(1)
        self.play(FadeOut(bars, line_graph))

    def cultural_factors_scene(self, colors):
        globe = Circle(radius=2, color=colors["consultant"]).shift(DOWN)
        self.play(Rotate(globe, angle=2 * PI, run_time=1.5))

        icons = VGroup(*[Triangle(color=colors["text"]).shift(RIGHT * i) for i in np.arange(-2, 3)])
        self.play(LaggedStartMap(FadeIn, icons, rate_func=smooth), run_time=2)

        self.wait(1)
        self.play(FadeOut(globe, icons))

    def communication_styles_scene(self, colors):
        bubbles = VGroup(
            Text("Hello", color=colors["text"]).scale(0.5), 
            Text("Hola", color=colors["text"]).scale(0.5).shift(UP), 
            Text("Bonjour", color=colors["text"]).scale(0.5).shift(DOWN)
        )
        self.play(FadeIn(bubbles, rate_func=smooth), run_time=1.5)

        self.wait(1)
        self.play(FadeOut(bubbles))

    def cultural_differences_scene(self, colors):
        consultant = Square(side_length=1, color=colors["consultant"])
        clients = VGroup(*[Circle(radius=0.4, color=colors["meeting"]).shift(RIGHT * i) for i in range(1, 4)])

        self.play(DrawBorderThenFill(consultant), LaggedStartMap(GrowFromCenter, clients, rate_func=smooth), run_time=2)
        map_arrow = Arrow(start=consultant.get_top(), end=clients[-1].get_bottom(), color=colors["handshake"])
        self.play(GrowArrow(map_arrow), run_time=1.5)

        self.play(FadeOut(consultant, clients, map_arrow))

    def trust_approaches_scene(self, colors):
        handshake = Square(side_length=1, color=colors["handshake"])
        meeting = Polygon(LEFT, UP, RIGHT, DOWN, color=colors["meeting"]).scale(0.5)

        self.play(handshake.animate.to_edge(LEFT), meeting.animate.to_edge(RIGHT), run_time=1.5)
        sparkle = Dot(color=colors["text"]).move_to(handshake.get_center())
        self.play(FadeIn(sparkle), run_time=1)
        
        self.play(FadeOut(handshake, meeting, sparkle))

    def relationship_navigation_scene(self, colors):
        map_rect = Rectangle(width=3, height=2, color=colors["consultant"])
        compass_needle = Line(start=ORIGIN, end=UP, color=colors["meeting"])
        
        self.play(GrowFromCenter(map_rect), Rotate(compass_needle, angle=PI, run_time=1.5))
        path_line = Line(start=map_rect.get_corner(DL), end=map_rect.get_corner(UR), color=colors["client"])
        self.play(Create(path_line, rate_func=smooth), run_time=1.5)
        
        self.play(FadeOut(map_rect, compass_needle, path_line))

    def adaptive_methods_scene(self, colors):
        consultant = Circle(radius=1, color=colors["consultant"])
        self.play(DrawBorderThenFill(consultant))

        alternative_attire = VGroup(Square(side_length=1, color=colors["handshake"]), Circle(radius=0.5, color=colors["meeting"]))
        self.play(Transform(consultant, alternative_attire[0]), Transform(consultant, alternative_attire[1]), run_time=2)

        self.play(FadeOut(consultant))

    def scenario_demonstration_scene(self, colors):
        consultant = Square(side_length=1, color=colors["consultant"])
        client = Circle(radius=0.5, color=colors["client"]).next_to(consultant, RIGHT, buff=1)

        self.play(Create(consultant), GrowFromCenter(client), run_time=2)
        self.play(consultant.animate.shift(LEFT * 0.5), client.animate.shift(RIGHT * 0.5), run_time=1.5)

        self.play(FadeOut(consultant, client))

    def tips_for_enhancement_scene(self, colors):
        notebook = Rectangle(width=3, height=2, color=colors["text"]).shift(LEFT)
        page1 = Text("Tip 1: Know Your Client", color=BLACK).scale(0.5).move_to(notebook)
        page2 = Text("Tip 2: Be Adaptable", color=BLACK).scale(0.5).move_to(notebook)

        self.play(FadeIn(notebook), Write(page1), run_time=1.5)
        self.play(Transform(page1, page2), run_time=1.5)
        self.play(FadeOut(notebook, page2))

    def stronger_relationships_scene(self, colors):
        person1 = Square(side_length=1, color=colors["consultant"])
        person2 = Square(side_length=1, color=colors["meeting"]).next_to(person1, RIGHT, buff=1)

        handshake = Line(person1.get_right(), person2.get_left(), color=colors["handshake"])
        self.play(DrawBorderThenFill(person1), DrawBorderThenFill(person2), GrowArrow(handshake), run_time=2)

        golden_glow = SurroundingRectangle(handshake, color=colors["text"], buff=0.2)
        self.play(Create(golden_glow), run_time=1.5)

        self.play(FadeOut(person1, person2, handshake, golden_glow))

    def successful_outcomes_scene(self, colors):
        consultant = Square(side_length=1, color=colors["consultant"])
        clients = VGroup(*[Triangle(color=colors["meeting"]).shift(RIGHT * i) for i in range(1, 3)])

        self.play(GrowFromCenter(consultant), LaggedStartMap(Create, clients, rate_func=smooth), run_time=2)

        confetti = VGroup(*[Dot(color=colors["meeting"]).shift(RIGHT * dx + UP * dy) for dx in np.arange(-1, 2) for dy in np.arange(-1, 2)])
        clients_clap = clients.copy().set_color(colors["handshake"])
        self.play(Transform(clients, clients_clap), LaggedStartMap(FadeIn, confetti), run_time=2)

        self.wait(1)
        self.play(FadeOut(consultant, clients, confetti))