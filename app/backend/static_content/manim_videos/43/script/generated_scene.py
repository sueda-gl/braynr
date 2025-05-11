from manim import *

class ManimScene(Scene):
    def construct(self):
        """Constructs the entire sequence of animations following the storyboard plan."""
        self.step_1_cultural_spheres()
        self.step_2_role_of_consultants()
        self.step_3_introducing_clients()
        self.step_4_interaction_and_collaboration()
        self.step_5_outcome_and_impact()

    def step_1_cultural_spheres(self):
        """Illustrates the concept of cultural spheres using a globe and cultural icons."""
        globe = Sphere(radius=2, color=BLUE).rotate_about_origin(PI / 4)
        globe.set_fill(BLUE, opacity=0.5)
        
        culture_icons = VGroup(
            self.create_icon(LEFT + UP, color=YELLOW), 
            self.create_icon(RIGHT + UP, color=RED),
            self.create_icon(LEFT + DOWN, color=GREEN),
            self.create_icon(RIGHT + DOWN, color=ORANGE)
        )
        
        people_animations = VGroup(
            self.create_person(LEFT * 2, color=WHITE),
            self.create_person(RIGHT * 2, color=WHITE),
            self.create_pyramid(UP * 2.5, color=GOLD)
        )
        
        caption = Text(
            "Cultural Spheres define who we are through traditions, values, and languages.",
            font_size=24
        ).to_edge(DOWN)

        self.play(Create(globe), run_time=3)
        self.play(Create(culture_icons), Create(people_animations), run_time=5)
        self.play(Write(caption), run_time=6)
        self.wait(1)
        self.clear()

    def step_2_role_of_consultants(self):
        """Depicts consultants in an office setting using graphs and data charts."""
        office = Rectangle(width=8, height=5, color=GREY, fill_opacity=0.3)
        graphs = VGroup(
            Line(UL, DR, color=GREEN),
            Line(DL, UR, color=RED),
            Line(LEFT, RIGHT, color=BLUE)
        ).arrange_in_grid(buff=0.5).scale(0.6)

        consultants = VGroup(
            self.create_person(LEFT, color=BLUE),
            self.create_person(RIGHT, color=BLUE)
        )
        
        caption = Text(
            "Consultants provide expert advice to navigate complex challenges and cultural diversities",
            font_size=24
        ).to_edge(DOWN)

        self.play(FadeIn(office), run_time=1)
        self.play(Create(graphs), run_time=4)
        self.play(ApplyWave(consultants))
        self.play(Write(caption), run_time=5)
        self.clear()

    def step_3_introducing_clients(self):
        """Shows clients with their unique challenges and needs."""
        clients = VGroup(
            self.create_person(LEFT*2, color=PURPLE),
            self.create_person(RIGHT*2, color=ORANGE)
        )
        
        challenges = VGroup(
            Polygon([-0.5, 0.5, 0], [0.5, 0.5, 0], [0, 1, 0], color=RED),
            Tex("?").to_corner(UP + RIGHT)
        )

        caption = Text(
            "Clients seek solutions to their unique needs, looking for guidance and expertise",
            font_size=24
        ).to_edge(DOWN)

        self.play(Create(clients), run_time=2)
        self.play(Create(challenges), run_time=3)
        self.play(Write(caption), run_time=5)
        self.clear()

    def step_4_interaction_and_collaboration(self):
        """Illustrates interaction and collaboration between consultants and clients."""
        table = RoundedRectangle(corner_radius=0.2, width=3, height=1.5, color=WHITE)
        whiteboard = Rectangle(width=4, height=3, color=GREY)
        
        consultants_clients = VGroup(
            self.create_person(LEFT * 1.5 + UP, color=BLUE),
            self.create_person(RIGHT * 1.5 + UP, color=ORANGE)
        )

        dialog_symbols = VGroup(
            self.create_icon(LEFT + 0.5*UP, color=YELLOW),
            self.create_icon(RIGHT + 0.5*UP, color=RED)
        )

        caption = Text(
            "Through collaboration, ideas are exchanged, respecting and embracing cultural differences",
            font_size=24
        ).to_edge(DOWN)

        self.play(DrawBorderThenFill(table), DrawBorderThenFill(whiteboard))
        self.play(FadeIn(consultants_clients))
        self.play(GrowFromCenter(dialog_symbols), run_time=5)
        self.play(Write(caption), run_time=6)
        self.clear()

    def step_5_outcome_and_impact(self):
        """Highlights the positive outcomes and impacts of successful collaborative projects."""
        success_signs = VGroup(
            self.create_thumbs_up(LEFT),
            self.create_thumbs_up(RIGHT)
        )

        multicultural_team = VGroup(
            self.create_person(LEFT, color=GREEN),
            self.create_person(RIGHT, color=PINK)
        )

        results = VGroup(
            self.create_graph(ORIGIN, direction=UP+RIGHT, color=GREEN)
        )

        caption = Text(
            "Positive outcomes arise from understanding, leading to successful projects and enriched cultural relations",
            font_size=24
        ).to_edge(DOWN)

        self.play(FadeIn(success_signs), run_time=4)
        self.play(Circumscribe(multicultural_team, color=WHITE, fade_out=True))
        self.play(Create(results), run_time=5)
        self.play(Write(caption), run_time=6)
        self.wait(2)

    # Helper functions
    def create_icon(self, position, color):
        """Creates a colored icon at a specified position."""
        return Dot(point=position, color=color).set_fill(color, opacity=0.8)

    def create_person(self, position, color):
        """Creates a simple representation of a person (circle for the head) at a given position."""
        body = Circle(radius=0.2, color=color).move_to(position)
        return body

    def create_pyramid(self, position, color):
        """Creates a pyramid shape at a specified position with a given color."""
        return Polygon(position + [-0.5, -0.5, 0], position + [0.5, -0.5, 0], position + [0, 0.5, 0], color=color)

    def create_thumbs_up(self, position):
        """Creates a thumbs-up symbol at a specified position."""
        return Triangle().rotate(-PI / 2).move_to(position).scale(0.5).set_fill(BLUE, opacity=0.8)

    def create_graph(self, position, direction, color):
        """Creates a graph arrow to indicate positive results in a given direction."""
        return Arrow(start=position, end=position + direction, color=color)