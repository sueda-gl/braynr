from manim import *
import numpy as np

class ManimScene(Scene):
    def construct(self):
        # Scene 1: The Bridge
        self.foundation_scene()
        
        # Scene 2: Three Pillars
        self.dimensions_scene()
        
        # Scene 3: Growing Tree
        self.development_scene()
        
        # Scene 4: Obstacle Course
        self.barriers_scene()
        
        # Scene 5: Treasure Chest
        self.benefits_scene()
        
        # Scene 6: The Summit
        self.success_scene()
        
        # Scene 7: The Toolkit
        self.understanding_scene()
        
        # Conclusion
        self.conclusion_scene()
    
    def create_stick_figure(self, color=BLUE):
        """Create a simple stick figure with the given color."""
        head = Circle(radius=0.2, color=color, fill_opacity=0.8)
        body = Line([0, 0, 0], [0, -0.8, 0], color=color)
        left_arm = Line([0, -0.3, 0], [-0.3, -0.5, 0], color=color)
        right_arm = Line([0, -0.3, 0], [0.3, -0.5, 0], color=color)
        left_leg = Line([0, -0.8, 0], [-0.3, -1.2, 0], color=color)
        right_leg = Line([0, -0.8, 0], [0.3, -1.2, 0], color=color)
        
        figure = VGroup(head, body, left_arm, right_arm, left_leg, right_leg)
        return figure
    
    def foundation_scene(self):
        # Title
        title = Text("Trust as the Foundation", color=YELLOW)
        self.play(FadeIn(title), run_time=1)
        self.wait(2)
        self.play(FadeOut(title), run_time=1)
        
        # Create two cliff edges
        left_cliff = Polygon([-7, -1, 0], [-3, -1, 0], [-2.5, 1, 0], [-7, 1, 0], color=BROWN, fill_opacity=0.8)
        right_cliff = Polygon([3, -1, 0], [7, -1, 0], [7, 1, 0], [2.5, 1, 0], color=BROWN, fill_opacity=0.8)
        
        self.play(FadeIn(left_cliff, right_cliff), run_time=1)
        
        # Build the bridge
        bridge_segments = []
        for i in range(10):
            segment = Rectangle(height=0.2, width=0.6, color=GOLD_E, fill_opacity=0.9)
            segment.move_to([-2.5 + i*0.6, 0, 0])
            bridge_segments.append(segment)
        
        for segment in bridge_segments:
            self.play(GrowFromCenter(segment), run_time=0.5)
        
        # Create consultant and client figures
        consultant = self.create_stick_figure(color=BLUE)
        client = self.create_stick_figure(color=RED)
        
        consultant.move_to([-5, 1.2, 0])
        client.move_to([5, 1.2, 0])
        
        self.play(FadeIn(consultant, client), run_time=1)
        
        # Move towards center
        self.play(
            consultant.animate.move_to([-0.5, 1.2, 0]),
            client.animate.move_to([0.5, 1.2, 0]),
            run_time=4
        )
        
        # Handshake effect
        consultant_hand = Dot(color=BLUE).move_to([-0.1, 1.1, 0])
        client_hand = Dot(color=RED).move_to([0.1, 1.1, 0])
        glow = Circle(radius=0.3, color=YELLOW).move_to([0, 1.1, 0])
        glow.set_opacity(0)
        
        self.play(
            FadeIn(consultant_hand, client_hand, glow),
            run_time=1
        )
        self.play(
            glow.animate.set_opacity(0.7),
            run_time=1
        )
        self.play(
            glow.animate.set_opacity(0),
            run_time=1
        )
        
        # Camera pulls back
        group = VGroup(left_cliff, right_cliff, *bridge_segments, consultant, client, consultant_hand, client_hand)
        self.play(
            group.animate.scale(0.8),
            run_time=2
        )
        
        self.wait(1)
        self.play(FadeOut(group), run_time=1)
    
    def dimensions_scene(self):
        # Title
        title = Text("Three Dimensions of Trust", color=YELLOW)
        self.play(FadeIn(title), run_time=1)
        self.wait(2)
        self.play(FadeOut(title), run_time=1)
        
        # Temple foundation
        foundation = Rectangle(width=6, height=0.5, color=BROWN, fill_opacity=0.8)
        foundation.move_to([0, -2, 0])
        foundation_outline = Rectangle(width=8, height=0.5, stroke_opacity=0.4, color=BROWN)
        foundation_outline.move_to([0, -2, 0])
        
        self.play(FadeIn(foundation_outline), run_time=1)
        self.play(FadeIn(foundation), run_time=1)
        
        # Pillars
        pillar1 = Rectangle(width=1, height=4, color=BLUE, fill_opacity=0.7)
        pillar1.move_to([-2, 0, 0])
        pillar1_label = Text("Competence", color=WHITE, font_size=24)
        pillar1_label.move_to(pillar1.get_center())
        
        pillar2 = Rectangle(width=1, height=4, color=GREEN, fill_opacity=0.7)
        pillar2.move_to([0, 0, 0])
        pillar2_label = Text("Integrity", color=WHITE, font_size=24)
        pillar2_label.move_to(pillar2.get_center())
        
        pillar3 = Rectangle(width=1, height=4, color=RED, fill_opacity=0.7)
        pillar3.move_to([2, 0, 0])
        pillar3_label = Text("Benevolence", color=WHITE, font_size=24)
        pillar3_label.rotate(PI/2)
        pillar3_label.move_to(pillar3.get_center())
        
        # Animate pillars rising
        pillar1_bottom = pillar1.copy().scale([1, 0.01, 1]).move_to([-2, -1.75, 0])
        pillar2_bottom = pillar2.copy().scale([1, 0.01, 1]).move_to([0, -1.75, 0])
        pillar3_bottom = pillar3.copy().scale([1, 0.01, 1]).move_to([2, -1.75, 0])
        
        self.play(FadeIn(pillar1_bottom), run_time=0.5)
        self.play(ReplacementTransform(pillar1_bottom, pillar1), run_time=2)
        self.play(FadeIn(pillar1_label), run_time=0.5)
        
        self.play(FadeIn(pillar2_bottom), run_time=0.5)
        self.play(ReplacementTransform(pillar2_bottom, pillar2), run_time=2)
        self.play(FadeIn(pillar2_label), run_time=0.5)
        
        self.play(FadeIn(pillar3_bottom), run_time=0.5)
        self.play(ReplacementTransform(pillar3_bottom, pillar3), run_time=2)
        self.play(FadeIn(pillar3_label), run_time=0.5)
        
        # Temple roof
        roof = Polygon([-3, 2, 0], [3, 2, 0], [2.5, 3, 0], [-2.5, 3, 0], color=GOLD_E, fill_opacity=0.8)
        
        self.play(FadeIn(roof), run_time=2)
        
        # Light beams
        beam1 = Line(pillar1.get_center(), pillar2.get_center(), color=YELLOW)
        beam2 = Line(pillar2.get_center(), pillar3.get_center(), color=YELLOW)
        beam3 = Line(pillar3.get_center(), pillar1.get_center(), color=YELLOW)
        
        self.play(
            Create(beam1),
            Create(beam2),
            Create(beam3),
            run_time=2
        )
        
        self.wait(1)
        
        temple_group = VGroup(foundation, foundation_outline, pillar1, pillar2, pillar3, 
                             pillar1_label, pillar2_label, pillar3_label, roof, beam1, beam2, beam3)
        
        self.play(FadeOut(temple_group), run_time=1)
    
    def development_scene(self):
        # Title
        title = Text("Trust Development Stages", color=YELLOW)
        self.play(FadeIn(title), run_time=1)
        self.wait(2)
        self.play(FadeOut(title), run_time=1)
        
        # Soil with hole
        soil = Rectangle(width=8, height=1, color=BROWN, fill_opacity=0.8)
        soil.move_to([0, -3, 0])
        
        hole = Circle(radius=0.2, color=BLACK, fill_opacity=1)
        hole.move_to([0, -2.5, 0])
        
        self.play(FadeIn(soil), run_time=1)
        self.play(FadeIn(hole), run_time=1)
        
        # Seed drops
        seed = Circle(radius=0.1, color=GOLD_E, fill_opacity=1)
        seed.move_to([0, 1, 0])
        
        self.play(FadeIn(seed), run_time=0.5)
        self.play(seed.animate.move_to([0, -2.5, 0]), run_time=1)
        
        # Soil covers hole
        patch = Rectangle(width=0.5, height=0.2, color=BROWN, fill_opacity=0.9)
        patch.move_to([0, -2.5, 0])
        
        self.play(
            FadeOut(seed),
            FadeOut(hole),
            FadeIn(patch),
            run_time=1
        )
        
        # Stage 1: Seedling
        stem1 = Line([0, -2.5, 0], [0, -1.5, 0], color=GREEN)
        leaf1 = Triangle(color=GREEN).scale(0.2).move_to([0.2, -1.6, 0])
        leaf2 = Triangle(color=GREEN).scale(0.2).move_to([-0.2, -1.7, 0])
        leaf2.rotate(PI)
        
        seedling = VGroup(stem1, leaf1, leaf2)
        seedling_label = Text("Initial Trust", color=WHITE, font_size=24)
        seedling_label.next_to(seedling, RIGHT)
        
        self.play(
            GrowFromPoint(stem1, [0, -2.5, 0]),
            run_time=2
        )
        self.play(
            FadeIn(leaf1, leaf2),
            run_time=1
        )
        self.play(Write(seedling_label), run_time=1)
        
        self.wait(1)
        
        # Stage 2: Sapling
        stem2 = Line([0, -2.5, 0], [0, -0.5, 0], color=GREEN)
        leaves = []
        for i in range(6):
            leaf = Triangle(color=GREEN).scale(0.3)
            angle = i * PI / 3
            leaf.move_to([0.5 * np.cos(angle), -0.5 + 0.3 * np.sin(angle), 0])
            leaf.rotate(angle - PI/2)
            leaves.append(leaf)
        
        sapling = VGroup(stem2, *leaves)
        sapling_label = Text("Performance Trust", color=WHITE, font_size=24)
        sapling_label.next_to(sapling, RIGHT)
        
        self.play(
            ReplacementTransform(stem1, stem2),
            ReplacementTransform(VGroup(leaf1, leaf2), VGroup(*leaves)),
            ReplacementTransform(seedling_label, sapling_label),
            run_time=4
        )
        
        self.wait(1)
        
        # Stage 3: Mature tree
        trunk = Rectangle(width=0.4, height=3, color=BROWN, fill_opacity=0.8)
        trunk.move_to([0, -1, 0])
        
        # Create canopy
        canopy = Circle(radius=1.5, color=GREEN, fill_opacity=0.8)
        canopy.move_to([0, 0.5, 0])
        
        # Create roots
        roots = []
        for i in range(5):
            angle = PI/6 + i * PI / 5
            length = 0.5 + 0.3 * i % 3
            root = Line([0, -2.5, 0], 
                       [length * np.cos(angle), -2.5 - length * np.sin(angle), 0],
                       color=BROWN)
            roots.append(root)
        
        tree = VGroup(trunk, canopy, *roots)
        tree_label = Text("Relationship Trust", color=WHITE, font_size=24)
        tree_label.next_to(tree, RIGHT)
        
        self.play(
            ReplacementTransform(stem2, trunk),
            ReplacementTransform(VGroup(*leaves), canopy),
            *[GrowFromPoint(root, [0, -2.5, 0]) for root in roots],
            ReplacementTransform(sapling_label, tree_label),
            run_time=4
        )
        
        # Seasons animation (simplified with color changes)
        seasons = [GREEN_E, YELLOW_E, RED_E, WHITE]
        for color in seasons:
            self.play(canopy.animate.set_color(color), run_time=0.5)
        
        # Return to green
        self.play(canopy.animate.set_color(GREEN), run_time=0.5)
        
        self.wait(1)
        tree_group = VGroup(soil, patch, trunk, canopy, *roots, tree_label)
        self.play(FadeOut(tree_group), run_time=1)
    
    def barriers_scene(self):
        # Title
        title = Text("Common Trust Barriers", color=YELLOW)
        self.play(FadeIn(title), run_time=1)
        self.wait(2)
        self.play(FadeOut(title), run_time=1)
        
        # Create winding path
        path_points = [
            [-6, -2, 0], [-4, -1, 0], [-2, -2, 0], [0, -1, 0],
            [2, -2,