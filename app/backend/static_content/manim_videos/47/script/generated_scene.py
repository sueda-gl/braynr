from manim import *
import numpy as np

class ManimScene(Scene):
    def construct(self):
        # Scene 1: The Connected Consultant
        self.create_connected_consultant_scene()
        
        # Scene 2: Navigating Uncertainty
        self.create_navigating_uncertainty_scene()
        
        # Scene 3: Dimension 1: Public Reputation
        self.create_public_reputation_scene()
        
        # Scene 4: Dimension 2: Institutional Reputation
        self.create_institutional_reputation_scene()
        
        # Scene 5: Dimension 3: Personal Experience
        self.create_personal_experience_scene()
        
        # Scene 6: The Reputation Web
        self.create_reputation_web_scene()
        
        # Scene 7: Public Meets Personal
        self.create_public_meets_personal_scene()
        
        # Scene 8: The Complete Picture
        self.create_complete_picture_scene()

    def create_stick_figure(self, height=1, color=WHITE, business_attire=True):
        """Create a simple stick figure with optional business attire."""
        # Create a simple stick figure
        head = Circle(radius=0.15, color=color, fill_opacity=0)
        body = Line(ORIGIN, DOWN * 0.5, color=color)
        arms = Line(LEFT * 0.3, RIGHT * 0.3, color=color).shift(DOWN * 0.25)
        left_leg = Line(ORIGIN, DOWN * 0.5 + LEFT * 0.2, color=color).shift(DOWN * 0.5)
        right_leg = Line(ORIGIN, DOWN * 0.5 + RIGHT * 0.2, color=color).shift(DOWN * 0.5)
        
        figure = VGroup(head, body, arms, left_leg, right_leg)
        
        if business_attire:
            # Add a simple tie
            tie = Triangle(color=RED, fill_opacity=0.8).scale(0.07).rotate(PI).shift(DOWN * 0.3)
            # Add suit outline
            suit = RoundedRectangle(height=0.7, width=0.5, corner_radius=0.1, color=BLUE_E, fill_opacity=0).shift(DOWN * 0.25)
            figure.add(tie, suit)
        
        figure.height = height
        return figure

    def create_connected_consultant_scene(self):
        """Create scene showing consultant at center of networks."""
        # Title
        title = Text("THE CONNECTED CONSULTANT", font_size=36).to_edge(UP, buff=0.5)
        
        # Create consultant stick figure
        consultant = self.create_stick_figure(height=2, color=WHITE, business_attire=True)
        
        # Create network circles
        client_circle = Circle(radius=1.5, color=BLUE, fill_opacity=0.2)
        industry_circle = Circle(radius=1.5, color=GREEN, fill_opacity=0.2).shift(UP * 1.2 + LEFT * 1.2)
        association_circle = Circle(radius=1.5, color=RED, fill_opacity=0.2).shift(UP * 1.2 + RIGHT * 1.2)
        
        # Create circle labels
        client_label = Text("Clients", font_size=20, color=BLUE).move_to(client_circle.get_bottom() + DOWN * 0.3)
        industry_label = Text("Industry", font_size=20, color=GREEN).move_to(industry_circle.get_top() + UP * 0.3)
        association_label = Text("Professional\nAssociations", font_size=20, color=RED).move_to(association_circle.get_top() + UP * 0.3)
        
        # Create connection lines
        client_line = Line(consultant.get_center(), client_circle.get_center(), color=BLUE_B)
        industry_line = Line(consultant.get_center(), industry_circle.get_center(), color=GREEN_B)
        association_line = Line(consultant.get_center(), association_circle.get_center(), color=RED_B)
        
        # Caption
        caption = Text("Consultants operate within interconnected networks, not in isolation", 
                      font_size=24).to_edge(DOWN, buff=0.5)
        
        # Animations
        self.play(FadeIn(consultant), run_time=1)
        self.wait(0.5)
        
        self.play(
            Create(client_circle),
            Create(industry_circle),
            Create(association_circle),
            run_time=2
        )
        
        self.play(
            Write(client_label),
            Write(industry_label),
            Write(association_label),
            run_time=1.5
        )
        
        self.play(
            Create(client_line),
            Create(industry_line),
            Create(association_line),
            run_time=1.5
        )
        
        self.play(Write(title), run_time=1)
        self.play(Write(caption), run_time=1)
        
        self.wait(1)
        
        # Group everything for scene transition
        scene1_elements = VGroup(
            consultant, client_circle, industry_circle, association_circle,
            client_label, industry_label, association_label,
            client_line, industry_line, association_line,
            title, caption
        )
        
        self.play(
            scene1_elements.animate.scale(0.6).to_edge(UP),
            run_time=1.5
        )
        
        self.remove(scene1_elements)

    def create_navigating_uncertainty_scene(self):
        """Create scene showing consultant crossing bridge over turbulent waters."""
        # Create bridge elements
        bridge_base = Line(LEFT * 6, RIGHT * 6, color=GOLD_E, stroke_width=5)
        
        # Bridge cables
        cables = VGroup()
        supports = VGroup()
        
        for x in np.linspace(-5, 5, 6):
            cable = Line(bridge_base.get_point_from_proportion((x+6)/12), 
                        bridge_base.get_point_from_proportion((x+6)/12) + UP * 1.5,
                        color=BLUE_B)
            cables.add(cable)
            
            support = RoundedRectangle(height=0.2, width=0.3, corner_radius=0.05, color=GOLD_E, fill_opacity=1)
            support.move_to(bridge_base.get_point_from_proportion((x+6)/12))
            supports.add(support)
        
        # Create water (wavy lines)
        wavy_lines = VGroup()
        for y_offset in np.linspace(-2, -3.5, 6):
            wave_points = []
            for x in np.linspace(-6, 6, 50):
                y = 0.2 * np.sin(x + y_offset) + y_offset
                wave_points.append([x, y, 0])
            
            wavy_line = VMobject(color=BLUE)
            wavy_line.set_points_as_corners(wave_points)
            wavy_lines.add(wavy_line)
        
        # Create consultant
        consultant = self.create_stick_figure(height=1, business_attire=True)
        consultant.move_to(LEFT * 5 + UP * 0.5)
        
        # Create title and caption
        title = Text("NAVIGATING UNCERTAINTY", font_size=36).to_edge(UP, buff=0.5)
        caption = Text("Networks help consultants manage risk and uncertainty", 
                      font_size=24).to_edge(DOWN, buff=0.5)
        
        # Add all elements
        bridge_group = VGroup(bridge_base, cables, supports)
        
        # Start animation
        self.play(Write(title), run_time=1)
        
        self.play(
            Create(wavy_lines, lag_ratio=0.1),
            run_time=2
        )
        
        self.play(Create(bridge_base), run_time=1)
        
        self.play(
            FadeIn(supports, lag_ratio=0.1),
            run_time=1
        )
        
        self.play(
            Create(cables, lag_ratio=0.1),
            run_time=1.5
        )
        
        self.play(FadeIn(consultant), run_time=0.5)
        self.play(Write(caption), run_time=1)
        
        # Animate consultant walking across bridge
        self.play(
            consultant.animate.move_to(RIGHT * 5 + UP * 0.5),
            rate_func=linear,
            run_time=3
        )
        
        self.wait(1)
        
        # Transition out
        all_elements = VGroup(
            bridge_group, wavy_lines, consultant, title, caption
        )
        
        self.play(FadeOut(all_elements), run_time=1)

    def create_public_reputation_scene(self):
        """Create scene showing public reputation dimension."""
        # Initial "1" that transforms to title
        number_1 = Text("1", font_size=120, color=YELLOW)
        
        title = Text("PUBLIC REPUTATION", font_size=36, color=YELLOW)
        title.to_edge(UP, buff=0.7)
        
        self.play(FadeIn(number_1, scale=1.5), run_time=0.8)
        self.play(Transform(number_1, title), run_time=1)
        
        # Central consulting firm "logo" (simplified as a shape)
        logo = RoundedRectangle(height=1, width=1.5, corner_radius=0.2, color=BLUE, fill_opacity=0.8)
        logo_text = Text("FIRM", font_size=24, color=WHITE).move_to(logo)
        logo_group = VGroup(logo, logo_text)
        
        self.play(FadeIn(logo_group), run_time=1)
        
        # Media headlines as rectangular boxes
        headlines = VGroup()
        headline_texts = ["Industry Leader", "Top Rankings", "Expert Analysis"]
        
        for i, headline_text in enumerate(headline_texts):
            headline_box = Rectangle(height=0.6, width=3, color=WHITE, fill_opacity=0.1)
            headline = Text(headline_text, font_size=18, color=WHITE)
            headline_group = VGroup(headline_box, headline)
            
            # Position in different locations around the logo
            angle = i * TAU / 3
            radius = 2.5
            headline_group.move_to(logo_group.get_center() + radius * np.array([np.cos(angle), np.sin(angle), 0]))
            headlines.add(headline_group)
        
        # Industry ranking charts
        charts = VGroup()
        for i in range(3):
            chart_base = Line(LEFT * 0.5, RIGHT * 0.5, color=WHITE)
            
            # Create growing bars
            bars = VGroup()
            heights = [0.5, 0.8, 1.2]  # Different heights for bars
            
            for j, height in enumerate(heights):
                bar = Rectangle(height=height, width=0.15, color=GREEN, fill_opacity=0.8)
                bar.move_to(chart_base.get_center() + RIGHT * (j * 0.2 - 0.2) + UP * height/2)
                bars.add(bar)
            
            chart_group = VGroup(chart_base, bars)
            
            # Position charts
            angle = i * TAU / 3 + TAU/6
            radius = 2.5
            chart_group.move_to(logo_group.get_center() + radius * np.array([np.cos(angle), np.sin(angle), 0]))
            charts.add(chart_group)
        
        # Social media icons (simplified)
        social_media = VGroup()
        
        # Twitter-like icon (bird shape approximated with triangle)
        twitter = VGroup(
            Triangle(color=BLUE_A, fill_opacity=0.8),
            Circle(radius=0.15, color=BLUE_A, fill_opacity=0)
        ).arrange(RIGHT, buff=0.1).scale(0.4)
        
        # LinkedIn-like icon (simplified as square with "in")
        linkedin = VGroup(
            Square(side_length=0.4, color=BLUE_D, fill_opacity=0.8),
            Text("in", font_size=16, color=WHITE)
        ).arrange(ORIGIN, buff=0)
        
        social_media.add(twitter, linkedin)
        
        # Position social media icons
        twitter.move_to(logo_group.get_center() + UP * 2 + LEFT * 2)
        linkedin.move_to(logo_group.get_center() + UP * 2 + RIGHT * 2)
        
        # Notification counters
        counter1 = VGroup(
            Circle(radius=0.2, color=RED, fill_opacity=1),
            Text("5", font_size=16, color=WHITE)
        ).arrange(ORIGIN, buff=0)
        counter1.next_to(twitter, UP, buff=0.1)
        
        counter2 = VGroup(
            Circle(radius=0.2, color=RED, fill_opacity=1),
            Text("8", font_size=16, color=WHITE)
        ).arrange(ORIGIN, buff=0)
        counter2.next_to(linkedin, UP, buff=0.1)
        
        # Caption
        caption = Text("Public reputation represents how a firm is perceived within the broader industry", 
                      font_size=24).to_edge(DOWN, buff=0.5)
        
        # Animations
        self.play(
            FadeIn(headlines, lag_ratio=0.2),
            run_time=1.5
        )
        
        self.play(
            FadeIn(charts, lag_ratio=0.2),
            run_time=1.5
        )
        
        self.play(
            FadeIn(social_media),
            run_time=1
        )
        
        self.play(
            FadeIn(counter1),
            FadeIn(counter2),
            run_time=1
        )
        
        self.play(Write(caption), run_time=1)
        
        # Orbit animation
        orbit_group = VGroup(headlines, charts, social_media, counter1, counter2)
        
        self.play(
            Rotate(orbit_group, angle=PI/4, about_point=logo_group.get_center()),
            run_time=3,
            rate_func=smooth
        )
        
        self.wait(1)
        
        # Group everything for transition
        scene3_elements = VGroup(
            logo_group, headlines, charts, social_media, counter1, counter2, number_1, caption
        )
        
        # Move to left side for next scene
        self.play(
            scene3_elements.animate.scale(0.4).to_edge(LEFT, buff=1),
            run_time=1.5
        )

    def create_institutional_reputation_scene(self):
        """Create scene showing institutional reputation dimension."""
        # Initial "2" that transforms to title
        number_2 = Text("2", font_size=120, color=GREEN)
        
        title = Text("INSTITUTIONAL REPUTATION", font_size=36, color=GREEN)
        title.to_edge(UP, buff=0.7)
        
        self.play(FadeIn(number_2, scale=1.5), run_time=0.8)
        self.play(Transform(number_2, title), run_time=1)
        
        # Certificate icons with seals
        certificates = VGroup()
        
        for i in range(3):
            cert_bg = Rectangle(height=1, width=1.5, color=GOLD_E, fill_opacity=0.1)
            cert_border = Rectangle(height=1.1