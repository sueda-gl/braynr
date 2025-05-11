from manim import *

class AgentFace(VGroup):
    """Represents the agent's face."""
    def __init__(self, agent, **kwargs):
        super().__init__(**kwargs)
        self.agent = agent
        self.eyes = VGroup(
            Dot(self.agent.get_center() + UP * 0.2 + LEFT * 0.1, color=BLACK),
            Dot(self.agent.get_center() + UP * 0.2 + RIGHT * 0.1, color=BLACK)
        )
        self.mouth = Arc(radius=0.2, angle=PI)
        self.mouth.move_to(self.agent.get_center() + DOWN * 0.15)
        self.add(self.eyes, self.mouth)
        self.eyes.set_z_index(1)
        self.mouth.set_z_index(1)

class ManimScene(Scene):
    def construct(self):
        """Orchestrates the animation."""
        self.scene1()
        self.scene2()
        self.scene3()

    def create_dust_particles(self, center):
        """Creates dust particles around a given center."""
        return VGroup(*[Dot(center + UP*i*0.2 + LEFT*j*0.1, radius=0.02, color=WHITE) for i in range(-2, 3) for j in range(-2,3)])

    def bouncing_rate_func(self, t):
         # Custom rate function for a bouncing effect
        return np.abs(np.sin(t * PI * 2))
    def scene1(self):
        """Scene 1: Empty Toolbox - Lack of Functionality."""
        machine = RoundedRectangle(corner_radius=0.3, width=4, height=3, color=BLUE).move_to(RIGHT * 2)
        agent = Circle(radius=0.5, color=YELLOW).move_to(LEFT * 3)
        agent_face = AgentFace(agent)
        toolbox = Rectangle(width=0.8, height=0.5, color=GRAY).move_to(agent.get_center() + DOWN * 0.7)
        toolbox_handle = Line(toolbox.get_top() + LEFT * 0.4, toolbox.get_top() + RIGHT * 0.4, color=BLACK)
        toolbox_group = VGroup(toolbox, toolbox_handle)

        agent_face.add_updater(lambda m: m.move_to(agent.get_center()))
        toolbox_group.add_updater(lambda m: m.move_to(agent.get_center() + DOWN*0.7))

        self.play(FadeIn(machine), Create(agent), Create(agent_face), Create(toolbox_group))
        self.wait(0.2)
        self.play(agent.animate.move_to(LEFT * 1), run_time=2)
        self.wait(0.2)
        self.play(toolbox_group.animate.rotate(PI/2, about_point=toolbox.get_center()), run_time=2)
        self.wait(0.2)

        dust_particles = self.create_dust_particles(toolbox.get_center())
        self.play(Create(dust_particles), run_time=0.5)
        self.wait(0.2)
        self.play(dust_particles.animate.shift(UP*0.5), run_time=0.5)
        self.wait(0.2)
        self.play(FadeOut(dust_particles), run_time=0.5)
        self.wait(0.2)

        cogwheel = RegularPolygon(num_sides=6, start_angle=PI/6, color=GRAY)
        cogwheel_x = Cross(cogwheel, color=RED)
        thought_bubble = Bubble(direction=LEFT, height=2, width=2)
        thought_bubble.move_to(agent.get_center() + UP * 2)
        thought_group = VGroup(cogwheel, cogwheel_x).move_to(thought_bubble.get_center())

        self.play(Create(thought_bubble), Create(thought_group))
        self.wait(2)
        self.play(FadeOut(thought_bubble), FadeOut(thought_group), run_time=1)
        self.wait(0.2)
        self.play(toolbox_group.animate.rotate(-PI/2, about_point=toolbox.get_center()), run_time=1)
        self.wait(0.2)


        agent_face.remove_updater(agent_face.updaters[0])
        toolbox_group.remove_updater(toolbox_group.updaters[0])


    def scene2(self):
        """Scene 2: Request Blocked - Inability to Process."""
        machine = self.mobjects[0] # Access the existing machine object
        agent = self.mobjects[1]
        agent_face = next(obj for obj in self.mobjects if isinstance(obj, AgentFace))
        toolbox_group = next(obj for obj in self.mobjects if isinstance(obj, VGroup) and len(obj) == 2 and isinstance(obj[0], Rectangle) and isinstance(obj[1], Line))
        self.play(machine.animate.set_color(RED), run_time=1)
        self.wait(0.2)
        red_light = Circle(radius=0.1, color=RED, fill_opacity=1).move_to(machine.get_center() + UP * 1)
        self.add(red_light)
        self.play(red_light.animate.set_fill_opacity(0), rate_func=rate_functions.there_and_back, run_time=1)
        self.wait(0.2)
        self.play(red_light.animate.set_fill_opacity(1), rate_func=rate_functions.there_and_back, run_time=1)
        self.wait(0.2)
        self.play(red_light.animate.set_fill_opacity(0), rate_func=rate_functions.there_and_back, run_time=1)
        self.wait(0.2)


        request_icon = Triangle(color=GREEN).move_to(RIGHT * 5)
        barrier = CurvedArrow(machine.get_center() + LEFT*0.8 + UP*1.5, machine.get_center() + LEFT*0.8 + DOWN*1.5, color=YELLOW, tip_length=0.3, stroke_width=10)
        self.play(request_icon.animate.move_to(machine.get_center() + LEFT * 1.2), run_time=2)
        self.wait(0.2)
        self.play(request_icon.animate.shift(LEFT*0.5), rate_func=self.bouncing_rate_func, run_time=0.5)
        self.wait(0.2)
        self.play(FadeOut(barrier), request_icon.animate.shift(DOWN*2), run_time=1)
        self.wait(0.2)

    def scene3(self):
        """Scene 3: Offering Help - Further Assistance."""
        machine = self.mobjects[0] # Access the existing machine object
        agent = self.mobjects[1]
        agent_face = next(obj for obj in self.mobjects if isinstance(obj, AgentFace))
        toolbox_group = next(obj for obj in self.mobjects if isinstance(obj, VGroup) and len(obj) == 2 and isinstance(obj[0], Rectangle) and isinstance(obj[1], Line))
        red_light = next((obj for obj in self.mobjects if isinstance(obj, Circle) and obj.color == RED), None)

        self.play(machine.animate.set_color(BLUE), run_time=1)
        self.wait(0.2)
        if red_light is not None:
            self.remove(red_light)
        self.play(agent.animate.move_to(LEFT * 3), run_time=1)
        self.wait(0.2)
        self.play(agent.animate.shift(RIGHT*1), run_time=0.5)
        self.wait(0.2)
        self.play(agent.animate.shift(UP * 0.2), run_time=0.5)
        self.wait(0.2)


        question_mark = Tex("?", font_size=72).move_to(agent.get_center() + UP * 2)
        self.play(Create(question_mark), run_time=1)
        self.wait(0.2)
        self.play(Rotate(question_mark, angle=PI/6), run_time=0.5)
        self.wait(0.2)
        self.play(Rotate(question_mark, angle=-PI/6), run_time=0.5)
        self.wait(0.2)


        help_text = Text("Is there anything else I can help with?", color=WHITE).move_to(DOWN * 2)
        self.play(FadeIn(help_text), run_time=2)
        self.wait(3)