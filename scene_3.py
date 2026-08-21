
from manim import *
import numpy as np

class FourierScene3(Scene):
    def construct(self):
        self.camera.background_color = "#0f1117"

        # --- سیستم زیرنویس: هماهنگ با سکانس ۱ و ۲ ---
        bg_on = [False]
        cap_bg = [None]
        cap_accent = [None]
        cap_words = [None]

        def wrap_words(words, max_chars):
            lines, cur, cur_len = [], [], 0
            for w in words:
                add = len(w) + (1 if cur else 0)
                if cur_len + add <= max_chars:
                    cur.append(w)
                    cur_len += add
                else:
                    lines.append(" ".join(cur))
                    cur, cur_len = [w], len(w)
            if cur:
                lines.append(" ".join(cur))
            return lines

        def build_caption(text, font_size=24, max_chars=58):
            words = text.split()
            lines = wrap_words(words, max_chars)
            full_str = "\n".join(lines)

            full_text = Text(
                full_str,
                font_size=font_size,
                color=WHITE,
                line_spacing=1.0,
                font="DejaVu Sans"
            )

            caption_bg = RoundedRectangle(
                corner_radius=0.18,
                height=full_text.height + 0.5,
                width=min(full_text.width + 0.9, 12.8),
                stroke_color=BLUE_D,
                stroke_width=1.4,
                fill_color="#0a0c14",
                fill_opacity=0.82
            )

            accent = RoundedRectangle(
                corner_radius=0.05,
                height=caption_bg.height - 0.22,
                width=0.08,
                fill_color=BLUE_B,
                fill_opacity=0.9,
                stroke_opacity=0
            )

            full_text.move_to(caption_bg.get_center())
            VGroup(caption_bg, full_text).to_edge(DOWN, buff=0.4)
            accent.next_to(caption_bg.get_left(), RIGHT, buff=0.12)

            word_groups, idx = [], 0
            for w in words:
                n = len(w)
                word_groups.append(VGroup(*full_text[idx:idx + n]))
                idx += n

            return caption_bg, accent, full_text, word_groups

        def show_caption(text, run_time=3.5, wait_time=0.25, font_size=24):
            new_bg, new_accent, full_text, word_groups = build_caption(text, font_size)

            if not bg_on[0]:
                self.play(
                    FadeIn(new_bg, shift=UP * 0.18),
                    FadeIn(new_accent, shift=UP * 0.18),
                    run_time=0.5
                )
                cap_bg[0], cap_accent[0], bg_on[0] = new_bg, new_accent, True
            else:
                anims = [
                    Transform(cap_bg[0], new_bg),
                    Transform(cap_accent[0], new_accent)
                ]
                if cap_words[0] is not None:
                    anims.append(FadeOut(cap_words[0], shift=DOWN * 0.08))
                self.play(*anims, run_time=0.5)

            words_vgroup = VGroup(*word_groups)
            if len(word_groups) > 0:
                self.play(
                    LaggedStart(
                        *[FadeIn(g, shift=UP * 0.14) for g in word_groups],
                        lag_ratio=0.38
                    ),
                    run_time=run_time
                )
            cap_words[0] = words_vgroup
            self.wait(wait_time)

        def remove_caption():
            if bg_on[0]:
                anims = [
                    FadeOut(cap_bg[0], shift=DOWN * 0.18),
                    FadeOut(cap_accent[0], shift=DOWN * 0.18)
                ]
                if cap_words[0] is not None:
                    anims.append(FadeOut(cap_words[0], shift=DOWN * 0.1))
                self.play(*anims, run_time=0.5)
                bg_on[0] = False
                cap_bg[0] = None
                cap_accent[0] = None
                cap_words[0] = None

        # -------------------------------------------------
        # Title
        # -------------------------------------------------
        title = Text(
            "Finding the Hidden Frequencies",
            font_size=40,
            weight=BOLD,
            color=BLUE_B
        )
        subtitle = Text(
            "From Signal to Spectrum",
            font_size=28,
            color=GREY_B
        ).next_to(title, DOWN, buff=0.15)

        title_group = VGroup(title, subtitle).to_edge(UP, buff=0.4)

        self.play(FadeIn(title_group, shift=DOWN * 0.2), run_time=1.2)

        show_caption(
            "At the end of the last part, we asked a natural question: how do we actually find the hidden waves inside a signal?",
            run_time=4.8
        )

        # -------------------------------------------------
        # Axes for time-domain signal
        # -------------------------------------------------
        time_axes = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-2.2, 2.2, 1],
            x_length=5.2,
            y_length=2.8,
            axis_config={"color": GREY_A, "stroke_width": 2},
            tips=False
        ).shift(LEFT * 3.3 + UP * 0.45)

        time_label = Text("Signal", font_size=26, color=GREY_B).next_to(time_axes, UP, buff=0.2)

        signal_graph = time_axes.plot(
            lambda x: np.sin(x) + 0.5 * np.sin(3 * x) + 0.3 * np.sin(7 * x),
            x_range=[0, 2 * PI],
            color=BLUE_B,
            stroke_width=5
        )

        signal_glow = time_axes.plot(
            lambda x: np.sin(x) + 0.5 * np.sin(3 * x) + 0.3 * np.sin(7 * x),
            x_range=[0, 2 * PI],
            color=BLUE_D,
            stroke_width=10,
            stroke_opacity=0.15
        )

        self.play(Create(time_axes), FadeIn(time_label), run_time=1.4)
        self.play(Create(signal_glow), Create(signal_graph), run_time=2.0)

        show_caption(
            "Here is a signal that looks complicated on the surface, but we already know it is built from simpler sine waves.",
            run_time=4.2
        )

        # -------------------------------------------------
        # Spectrum axes
        # -------------------------------------------------
        freq_axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 1.4, 0.2],
            x_length=5.2,
            y_length=2.8,
            axis_config={"color": GREY_A, "stroke_width": 2},
            tips=False
        ).shift(RIGHT * 3.3 + UP *0.45)

        freq_label = Text("Spectrum", font_size=26, color=GREY_B).next_to(freq_axes, UP, buff=0.2)

        freq_marks = VGroup(
            MathTex("1", font_size=24, color=GREY_B).next_to(freq_axes.c2p(1, 0), DOWN, buff=0.2),
            MathTex("3", font_size=24, color=GREY_B).next_to(freq_axes.c2p(3, 0), DOWN, buff=0.2),
            MathTex("7", font_size=24, color=GREY_B).next_to(freq_axes.c2p(7, 0), DOWN, buff=0.2)
        )

        self.play(Create(freq_axes), FadeIn(freq_label), FadeIn(freq_marks), run_time=1.4)

        show_caption(
            "The main idea of Fourier analysis is to test the signal against one frequency at a time.",
            run_time=4.0
        )

        # -------------------------------------------------
        # Scanner / testing frequencies
        # -------------------------------------------------
        test_dot = Dot(freq_axes.c2p(0, 0), color=YELLOW, radius=0.08)
        test_label = Text(
            "Testing frequencies...",
            font_size=22,
            color=YELLOW,
            font="DejaVu Sans"
        ).next_to(freq_axes, UP, buff=0.01).shift(DOWN * 0.28)


        self.play(FadeIn(test_dot), FadeIn(test_label), run_time=0.8)

        show_caption(
            "You can think of it like tuning a radio dial and checking which frequencies resonate strongly with the signal.",
            run_time=4.4
        )

        self.play(
            test_dot.animate.move_to(freq_axes.c2p(1, 0)),
            run_time=0.8
        )
        self.play(
            Indicate(signal_graph, color=YELLOW),
            run_time=0.8
        )

        self.play(
            test_dot.animate.move_to(freq_axes.c2p(2, 0)),
            run_time=0.5
        )
        self.play(
            test_dot.animate.move_to(freq_axes.c2p(3, 0)),
            run_time=0.8
        )
        self.play(
            Indicate(signal_graph, color=RED_B),
            run_time=0.8
        )

        self.play(
            test_dot.animate.move_to(freq_axes.c2p(5, 0)),
            run_time=0.5
        )
        self.play(
            test_dot.animate.move_to(freq_axes.c2p(7, 0)),
            run_time=0.8
        )
        self.play(
            Indicate(signal_graph, color=GREEN_B),
            run_time=0.8
        )

        show_caption(
            "When a frequency matches an actual ingredient inside the signal, its response becomes noticeably stronger.",
            run_time=4.2
        )

        # -------------------------------------------------
        # Bars appearing in spectrum
        # -------------------------------------------------
        bar1 = Line(freq_axes.c2p(1, 0), freq_axes.c2p(1, 1.0), color=YELLOW, stroke_width=8)
        bar3 = Line(freq_axes.c2p(3, 0), freq_axes.c2p(3, 0.5), color=RED_B, stroke_width=8)
        bar7 = Line(freq_axes.c2p(7, 0), freq_axes.c2p(7, 0.3), color=GREEN_B, stroke_width=8)

        self.play(GrowFromEdge(bar1, DOWN), run_time=0.8)
        self.play(GrowFromEdge(bar3, DOWN), run_time=0.8)
        self.play(GrowFromEdge(bar7, DOWN), run_time=0.8)

        show_caption(
            "Those strong responses can be plotted as a spectrum, showing not where the signal is in time, but which frequencies are present and how much of each one exists.",
            run_time=5.4
        )

        # -------------------------------------------------
        # Transformation arrow
        # -------------------------------------------------
        transform_arrow = Arrow(
            time_axes.get_right() + RIGHT * 0.2,
            freq_axes.get_left() + LEFT * 0.2,
            color=BLUE_B,
            buff=0.2,
            stroke_width=4
        )

        transform_text = Text(
            "Fourier Transform",
            font_size=26,
            color=BLUE_B,
            weight=BOLD
        ).next_to(transform_arrow, UP, buff=0.15)

        self.play(Create(transform_arrow), FadeIn(transform_text), run_time=1.4)

        show_caption(
            "That shift in perspective, from the original signal to its frequency content, is the heart of the Fourier transform.",
            run_time=4.4
        )


# -------------------------------------------------
# Clean summary
# -------------------------------------------------
        show_caption(
            "So in a very practical sense, Fourier analysis gives us a way to open up a complicated signal and see the simple waves hidden inside it.",
            run_time=4.8
        )

        show_caption(
            "And once we can see those ingredients clearly, we can measure them, compare them, filter them, or even rebuild the signal from scratch.",
            run_time=5.0
        )

        remove_caption()

        summary_box = RoundedRectangle(
            corner_radius=0.18,
            width=4.6,
            height=1.2,
            stroke_color=BLUE_D,
            fill_color="#10131c",
            fill_opacity=0.75
        ).move_to(DOWN * 2.0)

        summary_text = Text(
            "Signal  →  Frequencies",
            font_size=24,
            color=WHITE,
            weight=BOLD,
            font="DejaVu Sans"
        ).move_to(summary_box.get_center())

        self.play(FadeIn(summary_box), Write(summary_text), run_time=1.2)
        self.wait(1.4)


        # -------------------------------------------------
        # Final transition
        # -------------------------------------------------
      

        final_text = Text(
            "This is why Fourier analysis is so powerful.",
            font_size=32,
            color=WHITE,
            font="DejaVu Sans"
        ).move_to(ORIGIN)

        self.play(
            FadeOut(time_axes),
            FadeOut(freq_axes),
            FadeOut(time_label),
            FadeOut(freq_label),
            FadeOut(freq_marks),
            FadeOut(signal_graph),
            FadeOut(signal_glow),
            FadeOut(bar1),
            FadeOut(bar3),
            FadeOut(bar7),
            FadeOut(test_dot),
            FadeOut(test_label),
            FadeOut(transform_arrow),
            FadeOut(transform_text),
            FadeOut(summary_box),
            FadeOut(summary_text),
            FadeOut(title_group),
            run_time=1.6
        )

        self.play(Write(final_text), run_time=2.2)
        self.wait(1.8)

        next_text = Text(
            "But to truly understand it,\nwe need to look at how this matching actually works.",
            font_size=30,
            color=BLUE_B,
            line_spacing=1.1,
            weight=BOLD,
            font="DejaVu Sans"
        ).move_to(ORIGIN)

        self.play(FadeOut(final_text, shift=UP * 0.3), run_time=0.9)
        self.play(FadeIn(next_text, shift=DOWN * 0.2), run_time=1.8)
        self.wait(2.5)

        self.play(FadeOut(next_text), run_time=1.2)
        self.wait(0.5)
