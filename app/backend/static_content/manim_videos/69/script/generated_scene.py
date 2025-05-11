from manim import *

class FileProcessingAnimation(Scene):
    def construct(self):
        self.constants()
        self.scene_upload_and_storage()
        self.scene_local_storage()
        self.scene_server_communication()
        self.scene_agent_job_creation()
        self.scene_auto_redirect()
        self.scene_realtime_updates()
        self.scene_constant_communication()
        self.scene_display_status()

    def constants(self):
        # Define constants for colors and dimensions
        self.BUTTON_WIDTH = 2
        self.BUTTON_HEIGHT = 1
        self.BUTTON_RADIUS = 0.2
        self.PROGRESS_BAR_WIDTH = 5
        self.PROGRESS_BAR_HEIGHT = 0.2
        self.TEXT_COLOR = WHITE
        self.BUTTON_COLOR = BLUE
        self.PROGRESS_COLOR = GREEN
        self.SERVER_COLOR = ORANGE
        self.DASHBOARD_COLOR = LIGHT_BLUE
        self.GRAY_COLOR = GRAY
        self.LIGHT_GREY_COLOR = LIGHT_GREY
        
    def scene_upload_and_storage(self):
        # Button for uploading files and its progress
        ui_button = RoundedRectangle(corner_radius=self.BUTTON_RADIUS, width=self.BUTTON_WIDTH, height=self.BUTTON_HEIGHT, color=self.BUTTON_COLOR).shift(LEFT * 3)
        upload_text = Text("Upload", color=self.TEXT_COLOR).move_to(ui_button)
        progress_bar = Rectangle(width=self.PROGRESS_BAR_WIDTH, height=self.PROGRESS_BAR_HEIGHT, color=self.PROGRESS_COLOR).next_to(ui_button, RIGHT, buff=1)
        upload_indicator = Rectangle(width=0, height=self.PROGRESS_BAR_HEIGHT, color=self.PROGRESS_COLOR).next_to(progress_bar.get_left(), RIGHT, buff=0)

        self.play(Create(ui_button), Write(upload_text))
        self.wait(1)
        self.play(
            upload_indicator.animate.set_width(progress_bar.width),
            rate_func=linear, run_time=3
        )
        self.wait(1)

    def scene_local_storage(self):
        # Indicate use of localStorage
        try:
            cloud_icon = SVGMobject("cloud_upload.svg").scale(0.5).shift(UP * 2)
        except FileNotFoundError:
            self.play(Write(Text("Cloud icon missing", font_size=24).shift(UP * 2)))
            return
        
        popup_text = Text("Ihr Dateiupload-Verlauf wird sicher im Browser gespeichert.", font_size=24).next_to(cloud_icon, DOWN, buff=0.5)

        self.play(FadeIn(cloud_icon), FadeIn(popup_text))
        self.wait(2)

    def scene_server_communication(self):
        # Show server communication
        browser_icon = RoundedRectangle(corner_radius=self.BUTTON_RADIUS, width=self.BUTTON_WIDTH, height=self.BUTTON_HEIGHT, color=self.BUTTON_COLOR).to_corner(DOWN + LEFT)
        server_icon = RoundedRectangle(corner_radius=self.BUTTON_RADIUS, width=self.BUTTON_WIDTH, height=self.BUTTON_HEIGHT, color=self.SERVER_COLOR).to_corner(UP + RIGHT)
        line = DashedLine(browser_icon.get_top(), server_icon.get_bottom(), color=self.GRAY_COLOR)
        file_transfer = Rectangle(width=0.5, height=0.5, color=self.BUTTON_COLOR).move_to(line.get_start())

        self.play(Create(browser_icon), Create(server_icon))
        self.play(Create(line))
        self.play(file_transfer.animate.move_to(line.get_end()), rate_func=smooth, run_time=3)
        self.wait(1)

    def scene_agent_job_creation(self):
        # Indicate task creation (AgentJob) on the server
        gears = VGroup(
            Circle(radius=0.3, color=YELLOW).rotate(PI/4),
            Circle(radius=0.2, color=YELLOW).next_to([0.5, 0.5, 0], UR)
        ).next_to(server_icon, LEFT, buff=0.5)
        
        job_card = RoundedRectangle(corner_radius=0.15, width=1.5, height=0.5, fill_color=WHITE, fill_opacity=0.75).shift(server_icon.get_center() + UP * 1.5)
        job_text = Text("AgentJob erstellt", font_size=18).move_to(job_card)

        self.play(Create(gears))
        self.play(Flash(job_card, flash_radius=0.8))
        self.play(FadeIn(job_text))
        self.wait(1)

    def scene_auto_redirect(self):
        # Automatic redirection to the monitoring page
        dashboard_screen = Rectangle(width=5, height=3, color=self.DASHBOARD_COLOR).shift(DOWN)
        loading_icon = Dot().scale(0.5).move_to(dashboard_screen.get_center())

        self.play(
            ReplacementTransform(ui_button, dashboard_screen),
            ReplacementTransform(upload_text, loading_icon)
        )
        self.wait(1)
        self.play(
            Transform(loading_icon, Text("Dashboard", font_size=22).move_to(dashboard_screen)),
            rate_func=linear, run_time=2
        )
        self.wait(1)

    def scene_realtime_updates(self):
        # Display real-time updates via WebSocket
        ws_symbols = VGroup(
            Circle(color=self.PROGRESS_COLOR).shift(RIGHT),
            Circle(color=self.PROGRESS_COLOR).shift(RIGHT + UP)
        ).arrange(RIGHT, buff=0.2)

        self.play(FadeIn(ws_symbols), rate_func=smooth, run_time=1)
        self.wait(1)

    def scene_constant_communication(self):
        # Constant communication via WebSocket
        arrows = VGroup(
            Arrow(browser_icon.get_center(), server_icon.get_center(), color=self.PROGRESS_COLOR),
            Arrow(server_icon.get_center(), browser_icon.get_center(), color=RED)
        )
        self.play(Write(arrows), run_time=2)
        self.wait(1)

    def scene_display_status(self):
        # Display status updates, interim results, and video
        progress_section = VGroup(
            Rectangle(width=4, height=0.5, color=self.DASHBOARD_COLOR).align_to(dashboard_screen, UP + LEFT),
            Text("Statusaktualisierungen", font_size=18).next_to(dashboard_screen, UP, buff=0.1)
        )
        interim_results = Rectangle(width=4, height=1, color=self.LIGHT_GREY_COLOR).next_to(progress_section, DOWN, buff=0.1)
        video_section = Rectangle(width=4, height=2, color=self.GRAY_COLOR).next_to(interim_results, DOWN, buff=0.1)

        self.play(FadeIn(progress_section), FadeIn(interim_results), FadeIn(video_section))
        self.wait(1)