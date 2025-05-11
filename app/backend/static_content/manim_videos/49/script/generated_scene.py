from manim import *

class ManimScene(Scene):
    def construct(self):
        def display_text_and_fade(text_content, wait_time=2, font_size=24):
            """Helper function to display, wait, and fade out text."""
            caption = Text(text_content, font_size=font_size)
            self.play(FadeIn(caption))
            self.wait(wait_time)
            self.play(FadeOut(caption))
        
        # Step 1: Introduction to the Study
        display_text_and_fade("Exploring the Dynamics of Consultant-Client Relationships")

        # Step 2: Importance in Business and Management
        key_texts = ["Business", "Management", "Success"]
        key_objects = VGroup(*[Text(word, font_size=32) for word in key_texts])
        key_objects.arrange(DOWN, buff=0.5)
        
        for obj in key_objects:
            self.play(Write(obj))
            self.wait(1)
            self.play(FadeToColor(obj, color=YELLOW))
            self.wait(1)
        
        self.play(FadeOut(key_objects))

        # Step 3: The Consultant as a Professional Advisor
        display_text_and_fade("Consultants: Your Professional Advisors")

        # Step 4: Provision of Expertise and Advice
        display_text_and_fade("Offering Expertise to Improve Business Outcomes")

        # Step 5: Clear Communication and Trust
        handshake = VGroup(
            Line(ORIGIN, RIGHT, color=WHITE).shift(UP / 2),
            Line(RIGHT, RIGHT + DOWN, color=WHITE).shift(UP / 2),
            Line(ORIGIN, LEFT, color=WHITE).shift(DOWN / 2),
            Line(LEFT, LEFT + UP, color=WHITE).shift(DOWN / 2)
        )
        
        dialogue_bubbles = VGroup(
            RoundedRectangle(width=3, height=1, corner_radius=0.15).next_to(handshake, UP, buff=0.5),
            RoundedRectangle(width=3, height=1, corner_radius=0.15).next_to(handshake, DOWN, buff=0.5)
        )
        
        communication_caption = Text("Building Relationships on Communication and Trust", font_size=24)
        self.play(Create(handshake), FadeIn(dialogue_bubbles), FadeIn(communication_caption))
        self.wait(2)
        self.play(FadeOut(handshake), FadeOut(dialogue_bubbles), FadeOut(communication_caption))

        # Step 6: Understanding Client Needs and Goals
        display_text_and_fade("Understanding Your Needs and Goals")

        # Step 7: Client Conveying Challenges and Openness
        display_text_and_fade("Expressing Challenges and Embracing Advice")

        # Step 8: Relationship Effectiveness and Project Success
        success_stamp = Text("Success", font_size=52, color=GREEN).rotate(PI / 12)
        effectiveness_caption = Text("Effective Partnerships Drive Project Success", font_size=24)
        self.play(FadeIn(success_stamp), FadeIn(effectiveness_caption))
        self.wait(2)
        self.play(FadeOut(success_stamp), FadeOut(effectiveness_caption))

        # Step 9: Influence on Business Growth
        bar_chart = VGroup(
            Rectangle(height=2, width=0.5, color=BLUE).shift(DOWN * 2 + LEFT * 2),
            Rectangle(height=3, width=0.5, color=GREEN).shift(DOWN * 2),
            Rectangle(height=4, width=0.5, color=YELLOW).shift(DOWN * 2 + RIGHT * 2)
        )
        
        growth_caption = Text("Impacting Overall Business Growth", font_size=24)
        self.play(Create(bar_chart), FadeIn(growth_caption))
        self.wait(2)
        self.play(FadeOut(bar_chart), FadeOut(growth_caption))

        # Step 10: Real-World Insights
        display_text_and_fade("Hear From the Experts: Consultants & Clients")

        # Step 11: Visual Aids and Conceptual Explanation
        flow_chart = VGroup(
            RoundedRectangle(width=3, height=1, corner_radius=0.15).shift(UP * 3),
            Arrow(start=DOWN + LEFT, end=UP + RIGHT),
            RoundedRectangle(width=3, height=1, corner_radius=0.15).shift(UP)
        )
        
        visualization_caption = Text("Visualizing Concepts with Charts and Diagrams", font_size=24)
        self.play(Create(flow_chart), FadeIn(visualization_caption))
        self.wait(2)
        self.play(FadeOut(flow_chart), FadeOut(visualization_caption))

        # Step 12: Conclusion
        display_text_and_fade("Cultivating Effective Consultant-Client Relationships")