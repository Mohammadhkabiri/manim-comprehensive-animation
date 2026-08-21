from manim import *
import numpy as np

config.background_color = "#05060A"
config.frame_width = 16
config.frame_height = 9
config.pixel_width = 1920
config.pixel_height = 1080


class AudioFourierAI(Scene):
    def construct(self):
        self.font_name = "DejaVu Sans"

        self.intro_audio_processing()
        self.long_time_signal()
        self.global_fourier_transform()
        self.time_information_loss()
        self.short_frames()
        self.overlap_frames()
        self.final_frequency_message()

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------
    def make_text(self, text, size=30, color=WHITE, weight=NORMAL):
        return Text(
            text,
            font=self.font_name,
            font_size=size,
            color=color,
            weight=weight,
        )

    def show_caption(self, text, wait_time=2.0):
        box = RoundedRectangle(
            corner_radius=0.15,
            width=12.8,
            height=0.82,
            stroke_color=WHITE,
            stroke_opacity=0.15,
            fill_color="#0B0E16",
            fill_opacity=0.85,
        )
        box.to_edge(DOWN, buff=0.25)

        caption = self.make_text(text, size=24, color="#EAEAEA")
        caption.move_to(box.get_center())

        group = VGroup(box, caption)
        self.play(FadeIn(group, shift=UP * 0.08), run_time=0.35)
        self.wait(wait_time)
        self.play(FadeOut(group, shift=DOWN * 0.08), run_time=0.3)

    def title_block(self, title, subtitle=None):
        title_text = self.make_text(title, size=40, color=WHITE, weight=BOLD)
        title_text.to_edge(UP, buff=0.35)

        if subtitle:
            subtitle_text = self.make_text(subtitle, size=24, color="#B8C7FF")
            subtitle_text.next_to(title_text, DOWN, buff=0.12)
            return VGroup(title_text, subtitle_text)
        return VGroup(title_text)

    def waveform_function(self, x):
        env = 0.75 + 0.18 * np.sin(0.7 * x) + 0.1 * np.cos(1.3 * x)
        return env * (
            0.55 * np.sin(2.4 * x)
            + 0.28 * np.sin(5.2 * x + 0.8)
            + 0.18 * np.sin(8.8 * x + 1.7)
        )

    def make_wave_plot(self, axes, color="#6EC1FF", x_min=0, x_max=10):
        graph = axes.plot(
            lambda x: self.waveform_function(x),
            x_range=[x_min, x_max],
            color=color,
            stroke_width=2.6,
        )
        return graph

    def make_frequency_spectrum(self, origin=ORIGIN, scale_factor=1.0):
        bars = VGroup()

        freqs = [0.7, 1.4, 2.0, 2.8, 3.7, 4.3, 5.0, 5.8, 6.4, 7.2]
        amps =  [0.35, 0.70, 1.15, 0.95, 0.52, 0.82, 0.42, 0.28, 0.18, 0.10]

        for i, amp in enumerate(amps):
            rect = Rectangle(
                width=0.28,
                height=amp * 2.2,
                stroke_width=0,
                fill_color="#FFB14E",
                fill_opacity=0.95,
            )
            rect.align_to(ORIGIN, DOWN)
            rect.shift(RIGHT * (i * 0.42))
            rect.shift(UP * (rect.height / 2))
            bars.add(rect)

        bars.scale(scale_factor)
        bars.move_to(origin)
        return bars

    def make_frame_boxes_on_signal(self, axes, n_frames=6, width=1.25, gap=0.15, color="#FFD166"):
        boxes = VGroup()
        x0 = 0.8
        for i in range(n_frames):
            left = x0 + i * (width + gap)
            right = left + width
            p1 = axes.c2p(left, 1.55)
            p2 = axes.c2p(right, -1.55)

            rect = Rectangle(
                width=abs(p2[0] - p1[0]),
                height=abs(p1[1] - p2[1]),
                stroke_color=color,
                stroke_width=2.0,
                fill_color=color,
                fill_opacity=0.08,
            )
            rect.move_to((p1 + p2) / 2)
            boxes.add(rect)
        return boxes

    # ---------------------------------------------------------
    # Scene parts
    # ---------------------------------------------------------
    def intro_audio_processing(self):
        title = self.title_block(
            "Fourier Transform in AI: Audio Processing",
            "From waveform to frequency content"
        )

        
        try:
            mic = ImageMobject("microphone.png")
            mic.set_height(1.8)
        except:
            mic = VGroup(
                Circle(radius=0.45, color="#C9D6EA"),
                Line(UP * 0.45, DOWN * 0.45, color="#C9D6EA"),
                Line(DOWN * 0.45, DOWN * 0.9, color="#C9D6EA"),
                Arc(radius=0.5, start_angle=PI, angle=PI, color="#C9D6EA").shift(DOWN * 0.9),
            )
            mic.set_stroke(width=2.5)
            mic.set_height(1.8)
        mic.move_to(LEFT * 3.8 + DOWN * 0.2)

        sound_waves = VGroup()
        for r in [0.55, 0.85, 1.15]:
            arc = Arc(
                radius=r,
                start_angle=-PI / 4,
                angle=PI / 2,
                color="#6EC1FF",
                stroke_width=3,
            )
            arc.move_to(mic.get_right() + RIGHT * 0.1)
            sound_waves.add(arc)

        waveform_icon = Axes(
            x_range=[0, 6, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=4.6,
            y_length=2.4,
            axis_config={"include_ticks": False, "include_numbers": False, "stroke_opacity": 0.5},
            tips=False,
        )
        waveform_icon.move_to(RIGHT * 3.2 + DOWN * 0.1)

        wave = waveform_icon.plot(
            lambda x: 0.8 * np.sin(2.4 * x) + 0.35 * np.sin(5.4 * x + 1),
            x_range=[0, 6],
            color="#FF6B6B",
            stroke_width=2.8,
        )

        arrow = Arrow(
            mic.get_right() + RIGHT * 1.5,
            waveform_icon.get_left() + LEFT * 0.25,
            buff=0.15,
            color=WHITE,
            stroke_width=3,
        )

        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.7)
        self.play(FadeIn(mic, scale=0.9), run_time=0.6)
        self.play(LaggedStart(*[Create(a) for a in sound_waves], lag_ratio=0.12), run_time=0.9)
        self.play(GrowArrow(arrow), Create(waveform_icon), Create(wave), run_time=1.0)

        self.show_caption(
            "Now let’s focus on one of the most important applications of the Fourier transform in artificial intelligence: audio processing.",
            wait_time=3.0,
        )
        self.show_caption(
            "When we speak, what actually happens is that we create vibrations in the air. A microphone captures these vibrations and converts them into a signal over time.",
            wait_time=4.0,
        )

        self.play(
            FadeOut(title),
            FadeOut(mic),
            FadeOut(sound_waves),
            FadeOut(arrow),
            FadeOut(waveform_icon),
            FadeOut(wave),
            run_time=0.8,
        )

    def long_time_signal(self):
        title = self.title_block("A sound as a signal over time")

        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1.7, 1.7, 1],
            x_length=12.0,
            y_length=3.8,
            axis_config={
                "color": "#AAB4C3",
                "stroke_width": 2,
                "include_numbers": False,
            },
            tips=False,
        )
        axes.move_to(ORIGIN + DOWN * 0.2)

        x_label = self.make_text("time", size=24, color="#DDE3ED")
        x_label.next_to(axes.x_axis, DOWN, buff=0.28)

        y_label = self.make_text("amplitude", size=24, color="#DDE3ED")
        y_label.rotate(PI / 2)
        y_label.next_to(axes.y_axis, LEFT, buff=0.28)

        waveform = self.make_wave_plot(axes, color="#6EC1FF")

        waveform_label = self.make_text("waveform", size=24, color="#6EC1FF")
        waveform_label.next_to(axes, UP, buff=0.22).shift(LEFT * 4.7)

        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.65)
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=0.9)
        self.play(Create(waveform), FadeIn(waveform_label), run_time=1.2)

        self.show_caption(
            "If we look at this signal, what we see is basically a waveform — a curve that moves up and down very quickly.",
            wait_time=3.2,
        )
        self.show_caption(
            "But here’s an important question:",
            wait_time=1.6,
        )
        self.show_caption(
            "If we only look at this waveform, can we really understand what sound it represents?",
            wait_time=3.0,
        )
        self.show_caption(
            "For example, can we tell what word was spoken, or who the speaker is?",
            wait_time=3.0,
        )
        self.show_caption(
            "In most cases, the answer is no.",
            wait_time=2.0,
        )

        self.long_signal_axes = axes
        self.long_signal_waveform = waveform
        self.long_signal_title = title
        self.long_signal_labels = VGroup(x_label, y_label, waveform_label)

    def global_fourier_transform(self):
        axes = self.long_signal_axes
        waveform = self.long_signal_waveform
        title = self.long_signal_title
        labels = self.long_signal_labels

        question_box = RoundedRectangle(
            corner_radius=0.16,
            width=5.3,
            height=1.15,
            stroke_color="#FFFFFF",
            stroke_opacity=0.18,
            fill_color="#0B0E16",
            fill_opacity=0.82,
        )
        question_text = self.make_text(
            "Waveform alone is not enough",
            size=28,
            color="#F3F4F6",
            weight=BOLD,
        )
        question_text.move_to(question_box)
        question_group = VGroup(question_box, question_text)
        question_group.move_to(UP * 2.7 + RIGHT * 3.9)

        self.play(FadeIn(question_group, shift=LEFT * 0.1), run_time=0.55)

        self.show_caption(
            "That’s because the important information in sound is not just the overall shape of the wave. The real difference between sounds comes from the combination of frequencies inside that signal.",
            wait_time=5.2,
        )
        self.show_caption(
            "Every sound we hear is actually made of many different frequency components. Some frequencies are stronger, some are weaker, and the pattern of these frequencies is what makes one sound different from another.",
            wait_time=5.4,
        )
        self.show_caption(
            "For example, the sound of different vowels or consonants mainly differs in their frequency content.",
            wait_time=3.4,
        )
        self.show_caption(
            "And this is exactly where the Fourier transform becomes useful.",
            wait_time=2.6,
        )

        ft_arrow = Arrow(
            axes.get_right() + LEFT * 0.3,
            RIGHT * 5.9,
            buff=0.2,
            color="#FFCF66",
            stroke_width=4,
        )
        ft_label = MathTex(r"\mathcal{F}", font_size=54, color="#FFCF66")
        ft_label.next_to(ft_arrow, UP, buff=0.15)

        spectrum_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 2.8, 0.5],
            x_length=5.2,
            y_length=3.8,
            axis_config={
                "color": "#AAB4C3",
                "stroke_width": 2,
                "include_numbers": False,
            },
            tips=False,
        )
        spectrum_axes.move_to(RIGHT * 4.2 + DOWN * 0.2)

        f_label = self.make_text("frequency", size=22, color="#DDE3ED")
        f_label.next_to(spectrum_axes.x_axis, DOWN, buff=0.26)

        a_label = self.make_text("strength", size=22, color="#DDE3ED")
        a_label.rotate(PI / 2)
        a_label.next_to(spectrum_axes.y_axis, LEFT, buff=0.22)

        bars = VGroup()
        base_x = 0.7
        heights = [0.6, 1.3, 2.2, 1.8, 1.1, 1.5, 0.8, 0.45]
        colors = ["#FFB14E", "#FFB14E", "#FF8C42", "#FF8C42", "#FFB14E", "#FFB14E", "#FFD166", "#FFD166"]
        for i, h in enumerate(heights):
            bar = Rectangle(
                width=0.32,
                height=h * 0.95,
                stroke_width=0,
                fill_color=colors[i],
                fill_opacity=0.96,
            )
            x = base_x + i * 0.58
            y0 = spectrum_axes.c2p(x, 0)
            bar.move_to(y0 + UP * (bar.height / 2))
            bars.add(bar)

        spectrum_label = self.make_text("one global spectrum", size=23, color="#FFCF66")
        spectrum_label.next_to(spectrum_axes, UP, buff=0.18)

        left_group = VGroup(axes, waveform, labels, question_group)

        self.play(
            GrowArrow(ft_arrow),
            FadeIn(ft_label, shift=UP * 0.06),
            run_time=0.8,
        )
        self.play(
            left_group.animate.scale(0.82).move_to(LEFT * 4.2 + DOWN * 0.05),
            run_time=0.9,
        )
        self.play(
            Create(spectrum_axes),
            FadeIn(f_label),
            FadeIn(a_label),
            run_time=0.8,
        )
        self.play(LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.08), run_time=1.0)
        self.play(FadeIn(spectrum_label), run_time=0.4)

        self.show_caption(
            "The Fourier transform allows us to take a signal from the time domain and move it into the frequency domain.",
            wait_time=3.6,
        )
        self.show_caption(
            "In other words, it lets us see which frequencies are present in the sound and how strong they are.",
            wait_time=3.4,
        )

        self.global_left_group = left_group
        self.global_ft_arrow = VGroup(ft_arrow, ft_label)
        self.global_spectrum_group = VGroup(spectrum_axes, f_label, a_label, bars, spectrum_label)

    def time_information_loss(self):
        left_group = self.global_left_group
        spectrum_group = self.global_spectrum_group
        ft_group = self.global_ft_arrow

        cross = Line(LEFT * 0.55 + UP * 0.55, RIGHT * 0.55 + DOWN * 0.55, color="#FF5C7A", stroke_width=5)
        cross2 = Line(LEFT * 0.55 + DOWN * 0.55, RIGHT * 0.55 + UP * 0.55, color="#FF5C7A", stroke_width=5)
        cross_group = VGroup(cross, cross2)

        time_box = RoundedRectangle(
            corner_radius=0.16,
            width=4.9,
            height=1.25,
            stroke_color="#FF5C7A",
            stroke_opacity=0.55,
            fill_color="#18080D",
            fill_opacity=0.84,
        )
        time_text = self.make_text(
            "When in time did each frequency occur?",
            size=24,
            color="#FFE4EA",
        )
        time_text.move_to(time_box)
        time_group = VGroup(time_box, time_text)
        time_group.next_to(spectrum_group, DOWN, buff=0.45)

        missing_box = RoundedRectangle(
            corner_radius=0.16,
            width=4.2,
            height=1.05,
            stroke_color="#FFFFFF",
            stroke_opacity=0.18,
            fill_color="#0B0E16",
            fill_opacity=0.82,
        )
        missing_text = self.make_text(
            "time information is lost",
            size=25,
            color="#F1F5F9",
        )
        missing_text.move_to(missing_box)
        missing_group = VGroup(missing_box, missing_text)
        missing_group.move_to(RIGHT * 4.25 + UP * 2.6)

        self.play(
            FadeIn(cross_group, scale=0.7),
            run_time=0.45,
        )
        cross_group.move_to(spectrum_group.get_center())

        self.play(FadeIn(time_group, shift=UP * 0.06), FadeIn(missing_group, shift=DOWN * 0.06), run_time=0.6)

        self.show_caption(
            "But if we apply the Fourier transform to the whole sound at once, we only get one spectrum.",
            wait_time=3.2,
        )
        self.show_caption(
            "That spectrum tells us which frequencies exist, but not when they happened.",
            wait_time=3.0,
        )
        self.show_caption(
            "So the frequency content becomes visible, but the timing information is largely lost.",
            wait_time=3.2,
        )

        self.play(
            FadeOut(cross_group),
            FadeOut(time_group),
            FadeOut(missing_group),
            FadeOut(ft_group),
            FadeOut(left_group),
            FadeOut(spectrum_group),
            run_time=0.8,
        )

    def short_frames(self):
        title = self.title_block("Solution: analyze short time frames")

        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1.7, 1.7, 1],
            x_length=12.0,
            y_length=3.8,
            axis_config={
                "color": "#AAB4C3",
                "stroke_width": 2,
                "include_numbers": False,
            },
            tips=False,
        )
        axes.move_to(ORIGIN + DOWN * 0.2)

        waveform = self.make_wave_plot(axes, color="#6EC1FF")
        boxes = self.make_frame_boxes_on_signal(axes, n_frames=6, width=1.2, gap=0.22, color="#FFD166")

        frame_label = self.make_text("short frames", size=24, color="#FFD166")
        frame_label.next_to(axes, UP, buff=0.2).shift(LEFT * 4.7)

        mini_spectra = VGroup()
        for i in range(4):
            mini_axes = Axes(
                x_range=[0, 5, 1],
                y_range=[0, 2.3, 1],
                x_length=1.5,
                y_length=1.0,
                axis_config={"stroke_width": 1.2, "stroke_opacity": 0.5, "include_numbers": False},
                tips=False,
            )
            mini_axes.shift(RIGHT * (-3.2 + i * 2.1) + DOWN * 2.7)

            bars = VGroup()
            heights_set = [
                [0.3, 0.9, 0.55, 0.2],
                [0.55, 0.65, 0.95, 0.35],
                [0.2, 0.45, 1.0, 0.8],
                [0.15, 0.72, 0.52, 0.95],
            ][i]

            for j, h in enumerate(heights_set):
                bar = Rectangle(
                    width=0.14,
                    height=h * 0.7,
                    stroke_width=0,
                    fill_color="#FFB14E",
                    fill_opacity=0.95,
                )
                x = 0.55 + j * 0.33
                y0 = mini_axes.c2p(x, 0)
                bar.move_to(y0 + UP * (bar.height / 2))
                bars.add(bar)

            mini_spectra.add(VGroup(mini_axes, bars))

        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.65)
        self.play(Create(axes), Create(waveform), run_time=1.0)
        self.play(FadeIn(frame_label), run_time=0.35)
        self.play(LaggedStart(*[FadeIn(box) for box in boxes], lag_ratio=0.08), run_time=0.95)

        self.show_caption(
            "To really understand sound, we should not analyze the entire signal as one single block.",
            wait_time=3.5,
        )
        self.show_caption(
            "Instead, we divide the sound into small time windows.",
            wait_time=2.5,
        )

        arrows = VGroup()
        for i in range(4):
            arrow = Arrow(
                boxes[i].get_bottom() + DOWN * 0.05,
                mini_spectra[i].get_top() + UP * 0.05,
                buff=0.08,
                color="#FFCF66",
                stroke_width=2.3,
            )
            arrows.add(arrow)

        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        GrowArrow(arrows[i]),
                        FadeIn(mini_spectra[i], scale=0.92),
                    )
                    for i in range(4)
                ],
                lag_ratio=0.15,
            ),
            run_time=1.6,
        )

        self.show_caption(
            "Then we apply the Fourier transform to each short frame separately.",
            wait_time=2.8,
        )

        self.short_axes = axes
        self.short_waveform = waveform
        self.short_boxes = boxes
        self.short_title = title
        self.short_frame_label = frame_label
        self.short_mini_spectra = mini_spectra
        self.short_arrows = arrows

    def overlap_frames(self):
        axes = self.short_axes
        waveform = self.short_waveform
        boxes = self.short_boxes
        title = self.short_title
        frame_label = self.short_frame_label
        mini_spectra = self.short_mini_spectra
        arrows = self.short_arrows

        self.show_caption(
            "To make the analysis smoother, these frames usually overlap with each other.",
            wait_time=3.0,
        )

        old_boxes = boxes.copy()

        overlap_boxes = self.make_frame_boxes_on_signal(
            axes, n_frames=7, width=1.45, gap=-0.45, color="#FF8C42"
        )

        overlap_label_box = RoundedRectangle(
            corner_radius=0.16,
            width=4.2,
            height=0.9,
            stroke_color="#FF8C42",
            stroke_opacity=0.55,
            fill_color="#1A0F05",
            fill_opacity=0.84,
        )
        overlap_label = self.make_text("overlapping frames", size=25, color="#FFD9A8")
        overlap_label.move_to(overlap_label_box)
        overlap_group = VGroup(overlap_label_box, overlap_label)
        overlap_group.move_to(UP * 2.75 + RIGHT * 4.25)

        self.play(
            Transform(boxes, overlap_boxes),
            FadeIn(overlap_group, shift=LEFT * 0.08),
            run_time=1.1,
        )

        self.show_caption(
            "This way, we keep track of how the frequency content changes from one moment to the next.",
            wait_time=3.3,
        )

        stft_box = RoundedRectangle(
            corner_radius=0.18,
            width=5.1,
            height=1.35,
            stroke_color="#72A8FF",
            stroke_opacity=0.55,
            fill_color="#06111E",
            fill_opacity=0.84,
        )
        stft_text = self.make_text(
            "Short-Time Fourier Transform",
            size=28,
            color="#DDE8FF",
            weight=BOLD,
        )
        stft_text.move_to(stft_box)
        stft_group = VGroup(stft_box, stft_text)
        stft_group.to_edge(DOWN, buff=0.45)

        self.play(FadeIn(stft_group, shift=UP * 0.08), run_time=0.55)

        self.show_caption(
            "This is the basic idea behind the Short-Time Fourier Transform, which is widely used in speech and audio AI systems.",
            wait_time=4.0,
        )

        self.play(
            FadeOut(title),
            FadeOut(axes),
            FadeOut(waveform),
            FadeOut(boxes),
            FadeOut(frame_label),
            FadeOut(mini_spectra),
            FadeOut(arrows),
            FadeOut(overlap_group),
            FadeOut(stft_group),
            run_time=0.85,
        )

    def final_frequency_message(self):
        title = self.title_block("To understand sound, look at its frequencies")

        left = RoundedRectangle(
            corner_radius=0.18,
            width=5.0,
            height=2.3,
            stroke_color="#6EC1FF",
            stroke_opacity=0.5,
            fill_color="#07111E",
            fill_opacity=0.8,
        )
        left.move_to(LEFT * 3.6 + DOWN * 0.2)
        left_text = self.make_text(
            "time domain\nwaveform",
            size=30,
            color="#BFE3FF",
            weight=BOLD,
        )
        left_text.move_to(left)

        right = RoundedRectangle(
            corner_radius=0.18,
            width=5.0,
            height=2.3,
            stroke_color="#FFB14E",
            stroke_opacity=0.5,
            fill_color="#1A1006",
            fill_opacity=0.82,
        )
        right.move_to(RIGHT * 3.6 + DOWN * 0.2)
        right_text = self.make_text(
            "frequency domain\nspectrum",
            size=30,
            color="#FFE0B0",
            weight=BOLD,
        )
        right_text.move_to(right)

        arrow = Arrow(
            left.get_right(),
            right.get_left(),
            buff=0.25,
            color=WHITE,
            stroke_width=3,
        )

        final_note_box = RoundedRectangle(
            corner_radius=0.18,
            width=11.8,
            height=1.3,
            stroke_color=WHITE,
            stroke_opacity=0.18,
            fill_color="#0B0E16",
            fill_opacity=0.84,
        )
        final_note = self.make_text(
            "Sound is not just how a signal moves over time — it is the pattern of frequencies inside it.",
            size=28,
            color=WHITE,
        )
        final_note.move_to(final_note_box)
        final_group = VGroup(final_note_box, final_note)
        final_group.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.65)
        self.play(FadeIn(left, scale=0.95), FadeIn(left_text), run_time=0.7)
        self.play(GrowArrow(arrow), run_time=0.5)
        self.play(FadeIn(right, scale=0.95), FadeIn(right_text), run_time=0.7)
        self.play(FadeIn(final_group, shift=UP * 0.08), run_time=0.6)

        self.show_caption(
            "So in a very simple sense, if we want to really understand sound, we shouldn’t just look at how the signal changes over time — we should look at the frequencies that build that sound.",
            wait_time=4.8,
        )

        self.wait(0.7)
