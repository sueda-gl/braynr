from manim import *

class ManimScene(Scene):
    def construct(self):
        # Scene 1: Video Storage
        self.create_video_storage_scene()
        
        # Scene 2: Real-Time Updates with Websockets
        self.create_real_time_updates_scene()

        # Scene 3: Transmission of Results
        self.create_transmission_of_results_scene()

        # Scene 4: Database Management
        self.create_database_management_scene()
        
        # Scene 5: Virtual Python Environment
        self.create_virtual_python_environment_scene()

    def create_video_storage_scene(self):
        """Creates the video storage animation scene."""
        screen = RoundedRectangle(corner_radius=0.2, width=6, height=4, color=BLUE)
        self.play(Create(screen))

        labels = ["pplbackend", "static", "content", "animations", "videos", "{job_id}"]
        paths = self.create_labels(labels, screen)
        
        self.play(Write(paths))

        for path in paths:
            self.play(
                path.animate.scale(1.2).set_color(YELLOW), run_time=0.5,
                path.animate.scale(1 / 1.2).set_color(WHITE), run_time=0.5
            )
        
        self.wait(1)
        self.play(FadeOut(screen), FadeOut(paths))

    def create_real_time_updates_scene(self):
        """Creates the real-time updates with websockets scene."""
        server = Square(side_length=1, color=GREEN).shift(LEFT * 3)
        devices = VGroup(
            *[Circle(radius=0.5, color=ORANGE).shift(RIGHT * i + UP * ((-1) ** i)) for i in range(4)]
        )
        self.play(Create(server), Create(devices))

        arrows = VGroup(
            *[Arrow(server.get_right(), device.get_left(), color=YELLOW) for device in devices]
        )
        self.play(Create(arrows))

        statuses = ["PENDING", "PROCESSING", "COMPLETED", "FAILED"]
        self.animate_arrows_statuses(arrows, statuses)
        
        self.wait(1)
        self.play(*[arrow.animate.set_color(WHITE) for arrow in arrows], run_time=0.5)
        self.wait(0.5)

    def create_transmission_of_results_scene(self):
        """Creates the transmission of results scene."""
        progress_bar = Line(LEFT * 2, RIGHT * 2, color=WHITE)
        progress = Line(LEFT * 2, LEFT * 2, color=GREEN)
        snippets = VGroup(
            Text("Explanations", font_size=24),
            Text("Storyboards", font_size=24),
            Text("Code Snippets", font_size=24),
            Text("Final Video URL", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(RIGHT * 3)

        self.play(Create(progress_bar))
        for index, snippet in enumerate(snippets):
            self.play(
                Write(snippet),
                progress.animate.put_start_and_end_on(
                    progress_bar.get_start(),
                    progress_bar.point_from_proportion((index + 1) / len(snippets))
                )
            )
            self.wait(0.5)

        self.wait(1)
        self.play(FadeOut(progress_bar), FadeOut(progress), FadeOut(snippets))

    def create_database_management_scene(self):
        """Creates the database management scene."""
        database_server = Rectangle(width=4, height=2, color=PURPLE)
        job_entries = self.create_job_entries(database_server)
        
        self.play(Create(database_server))
        self.play(Write(job_entries))

        self.wait(1)
        
        self.highlight_job_entries(job_entries)
        self.play(FadeOut(database_server), FadeOut(job_entries))

    def create_virtual_python_environment_scene(self):
        """Creates the virtual python environment scene."""
        terminal_box = Rectangle(width=7, height=2.5, color=GRAY_A)
        commands = [
            "source venv/bin/activate",
            "python script.py"
        ]

        self.play(Create(terminal_box))
        for cmd in commands:
            cmd_text = Text(cmd, font_size=20).next_to(
                terminal_box.get_top() + DOWN * 0.5, DOWN, buff=0.3
            ).align_on_border(LEFT)
            self.play(Write(cmd_text), run_time=1.5)
            self.wait(0.5)
        
        self.play(FadeOut(terminal_box), run_time=1)
        self.wait(0.5)
    
    def create_labels(self, labels, screen):
        """Creates label text objects next to the screen."""
        return VGroup(*[
            Text(label, font_size=22).next_to(
                screen.get_edge_center(UP), DOWN + RIGHT * (i - len(labels) / 2), buff=0.05
            ) for i, label in enumerate(labels)
        ])

    def animate_arrows_statuses(self, arrows, statuses):
        """Animates arrows with status updates."""
        for i, arrow in enumerate(arrows):
            status_text = Text(statuses[i % len(statuses)], font_size=18).next_to(
                arrow.get_center(), UP, buff=0.1
            )
            self.play(Write(status_text))
            self.play(arrow.animate.shift(UP * 0.2).set_color_by_gradient(RED, BLUE))
            self.play(FadeOut(status_text))
            self.play(arrow.animate.shift(DOWN * 0.2).set_color(YELLOW))
    
    def create_job_entries(self, database_server):
        """Creates job entries for the database management scene."""
        return VGroup(*[
            Text(f"Job {i + 1}", font_size=18, color=WHITE).next_to(
                database_server.get_top() + DOWN, DOWN, buff=0.3 + i * 0.5
            ) for i in range(3)
        ])

    def highlight_job_entries(self, job_entries):
        """Highlights job entries with a hover effect."""
        database_hover = Rectangle(width=3, height=0.5, color=YELLOW).move_to(job_entries[1])
        self.play(Create(database_hover), run_time=0.5)
        self.play(database_hover.animate.move_to(job_entries[2]), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(database_hover))