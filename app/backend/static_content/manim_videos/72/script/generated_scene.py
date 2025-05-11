from manim import *

class AnimatedWorkflow(Scene):
    def construct(self):
        # Visual 1: Organizing Video Storage
        self.animate_file_directory()
        self.wait(1)

        # Visual 2: Real-Time Updates with WebSockets
        self.animate_websockets_communication()
        self.wait(1)

        # Visual 3: Understanding Job Statuses
        self.animate_job_statuses()
        self.wait(1)

        # Visual 4: Broadcasting Job Results
        self.animate_broadcasting_results()
        self.wait(1)

        # Visual 5: User Feedback Loop
        self.animate_user_feedback_loop()
        self.wait(1)

    def animate_file_directory(self):
        """Animate the presentation of a file directory path."""
        directory_tree = Text(
            "Ibackend/static/content/manim/videos/{job_id}/videos/",
            color="#00BFFF"
        )
        self.play(Write(directory_tree), run_time=3)
        self.play(FadeOut(directory_tree), run_time=1)

    def animate_websockets_communication(self):
        """Animate real-time communication using WebSockets."""
        server_icon = Circle(radius=0.5, color=BLUE).shift(2*LEFT)
        client_icons = VGroup(
            Circle(radius=0.3, color=GREEN).shift(2*RIGHT + UP),
            Circle(radius=0.3, color=GREEN).shift(2*RIGHT),
            Circle(radius=0.3, color=GREEN).shift(2*RIGHT + DOWN)
        )
        websocket_symbol = Line(UP, DOWN, color=YELLOW).next_to(server_icon, RIGHT, buff=0.5)
        connections = VGroup(
            *[Line(server_icon.get_right(), client.get_left(), color=ORANGE) for client in client_icons]
        )

        self.play(Create(server_icon), Create(client_icons), Write(websocket_symbol))
        self.play(Create(connections), run_time=2)
        self.play(FadeOut(VGroup(server_icon, client_icons, websocket_symbol, connections)), run_time=1)

    def animate_job_statuses(self):
        """Display and animate job status progression."""
        progress_bar = VGroup(
            Rectangle(width=1, height=0.5, color=YELLOW).shift(2*LEFT),
            Rectangle(width=1, height=0.5, color=ORANGE),
            Rectangle(width=1, height=0.5, color=GREEN).shift(2*RIGHT)
        ).arrange(RIGHT, buff=0.1)
        labels = VGroup(
            Text("PENDING", font_size=24).move_to(progress_bar[0]),
            Text("PROCESSING", font_size=24).move_to(progress_bar[1]),
            Text("COMPLETED", font_size=24).move_to(progress_bar[2])
        )

        self.play(Write(progress_bar), Write(labels))
        for bar in progress_bar:
            self.play(Indicate(bar), run_time=1)
        self.play(FadeOut(progress_bar), FadeOut(labels), run_time=1)

    def animate_broadcasting_results(self):
        """Showcase the broadcasting of job results."""

        dashboard = VGroup(
            Rectangle(width=3, height=1, color=BLUE).shift(UP),
            Rectangle(width=3, height=1, color=GREEN),
            Rectangle(width=3, height=1, color=RED).shift(DOWN),
            Rectangle(width=3, height=1, color=PURPLE).shift(2*DOWN)
        )
        labels = VGroup(
            Text("Explanation", font_size=24).move_to(dashboard[0]),
            Text("Storyboard", font_size=24).move_to(dashboard[1]),
            Text("Code", font_size=24).move_to(dashboard[2]),
            Text("Final Video URL", font_size=24).move_to(dashboard[3])
        )

        self.play(FadeIn(dashboard), Write(labels))
        self.play(FadeOut(dashboard, shift=2*DOWN), FadeOut(labels, shift=2*DOWN), run_time=1)

    def animate_user_feedback_loop(self):
        """Display the real-time updates in the user interface feedback loop."""
        ui_layout = VGroup(
            RoundedRectangle(corner_radius=0.2, width=6, height=4, color=WHITE),
            Text("Real-Time Updates", font_size=24).shift(1.5*UP),
            Text("Notification Panels", font_size=18).shift(UP),
            Text("Live Results Display", font_size=18).shift(DOWN)
        )

        self.play(FadeIn(ui_layout))
        self.play(FadeOut(ui_layout), run_time=1)