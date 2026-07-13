from manim import *
import numpy as np

# =========================================================
# Scene 1: The Fundamental Idea — A Single Sine Wave
# =========================================================


class FourierScene1(Scene):
    def construct(self):
        self.camera.background_color = "#0f1117"

        # -------------------------------------------------
        # Helper: caption box (FIXED)
        # -------------------------------------------------
        # ما یک VGroup ثابت روی صحنه نگه می‌داریم و فقط
        # محتوای آن را با become به‌روزرسانی می‌کنیم تا
        # موبجکت قدیمی روی صحنه باقی نماند.
# -------------------------------------------------
# -------------------------------------------------
        # Helper: word-by-word caption (smooth + styled)
        # -------------------------------------------------
        bg_on = [False]
        cap_bg = [None]       # background فعلی
        cap_accent = [None]   # نوار رنگی کنار کپشن
        cap_words = [None]    # گروه کلماتِ فعلی

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

        def build_caption(text, font_size=28, max_chars=52):
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
                stroke_opacity=0.45,
                fill_color="#0a0c14",
                fill_opacity=0.82
            )

            # نوار رنگیِ ظریف سمت چپ برای ظاهر بهتر
            accent = RoundedRectangle(
                corner_radius=0.05,
                height=caption_bg.height - 0.22,
                width=0.08,
                stroke_opacity=0,
                fill_color=BLUE_B,
                fill_opacity=0.9
            )

            full_text.move_to(caption_bg.get_center())
            group = VGroup(caption_bg, full_text).to_edge(DOWN, buff=0.4)
            accent.next_to(caption_bg.get_left(), RIGHT, buff=0.12)

            # نگاشت کلمات -> گلیف‌ها
            word_groups, idx = [], 0
            for w in words:
                n = len(w)
                word_groups.append(VGroup(*full_text[idx:idx + n]))
                idx += n

            return caption_bg, accent, full_text, word_groups

        def show_caption(text, run_time=3.5, wait_time=0.25, font_size=28):
            new_bg, new_accent, full_text, word_groups = build_caption(text, font_size)

            # 1) پس‌زمینه: کراس‌فید نرم
            if not bg_on[0]:
                self.play(
                    FadeIn(new_bg, shift=UP * 0.18),
                    FadeIn(new_accent, shift=UP * 0.18),
                    run_time=0.5,
                    rate_func=rate_functions.ease_out_sine
                )
                cap_bg[0] = new_bg
                cap_accent[0] = new_accent
                bg_on[0] = True
            else:
                anims = [
                    Transform(cap_bg[0], new_bg),
                    Transform(cap_accent[0], new_accent),
                ]
                if cap_words[0] is not None:
                    anims.append(FadeOut(cap_words[0], shift=DOWN * 0.08))
                self.play(*anims, run_time=0.5,
                          rate_func=rate_functions.ease_in_out_sine)
                cap_words[0] = None
            words_vgroup = VGroup(*word_groups)
            if len(word_groups) > 0:
                self.play(
                    LaggedStart(
                        *[
                            FadeIn(g, shift=UP * 0.14, scale=1.04)
                            for g in word_groups
                        ],
                        lag_ratio=0.38
                    ),
                    run_time=run_time,
                    rate_func=rate_functions.ease_out_sine
                )
            cap_words[0] = words_vgroup
            self.wait(wait_time)

        def remove_caption():
            if bg_on[0]:
                anims = [
                    FadeOut(cap_bg[0], shift=DOWN * 0.18),
                    FadeOut(cap_accent[0], shift=DOWN * 0.18),
                ]
                if cap_words[0] is not None:
                    anims.append(FadeOut(cap_words[0], shift=DOWN * 0.1))
                self.play(*anims, run_time=0.5,
                          rate_func=rate_functions.ease_in_sine)
                bg_on[0] = False
                cap_bg[0] = None
                cap_accent[0] = None
                cap_words[0] = None
        # -------------------------------------------------
        # Title
        # -------------------------------------------------
        title = Text(
            "The Fundamental Idea",
            font_size=40,
            weight=BOLD,
            color=BLUE_B
        )
        subtitle = Text(
            "A Single Sine Wave",
            font_size=28,
            color=GREY_B
        ).next_to(title, DOWN, buff=0.15)

        title_group = VGroup(title, subtitle).to_edge(UP, buff=0.4)

        self.play(FadeIn(title_group, shift=DOWN * 0.2), run_time=1.2)

        show_caption(
            "We begin with the most fundamental building block of periodic motion: the sine wave.",
            run_time=4.2
        )

        # -------------------------------------------------
        # Axes
        # -------------------------------------------------
        axes = Axes(
            x_range=[0, 2 * PI + 0.2, PI / 2],
            y_range=[-1.6, 1.6, 0.5],
            x_length=10,
            y_length=4.8,
            axis_config={
                "color": GREY_A,
                "stroke_width": 2
            },
            tips=False
        )

        axes_labels = VGroup(
            Text("x", font_size=24, color=GREY_A).next_to(axes.x_axis.get_end(), RIGHT, buff=0.15),
            Text("f(x)", font_size=24, color=GREY_A).next_to(axes.y_axis.get_top(), UP, buff=0.15)
        )

        x_marks = VGroup(
            # به جای DOWN از UL استفاده می‌کنیم تا برود بالا سمت چپ
            MathTex("0", font_size=26, color=GREY_B).next_to(axes.c2p(0, 0), UL, buff=0.1),
            MathTex(r"\pi", font_size=28, color=GREY_B).next_to(axes.c2p(PI, 0), DOWN, buff=0.25),
            MathTex(r"2\pi", font_size=28, color=GREY_B).next_to(axes.c2p(2*PI, 0), DOWN, buff=0.25)
        )



        self.play(Create(axes), FadeIn(axes_labels), FadeIn(x_marks), run_time=1.8)

        show_caption(
            "A sine wave represents a smooth and continuous oscillation.",
            run_time=3.2
        )

        # -------------------------------------------------
        # Base sine wave
        # -------------------------------------------------
        sine_graph = axes.plot(
            lambda x: np.sin(x),
            x_range=[0, 2 * PI],
            color=YELLOW,
            stroke_width=5
        )

        glow_graph = axes.plot(
            lambda x: np.sin(x),
            x_range=[0, 2 * PI],
            color=YELLOW_E,
            stroke_width=10,
            stroke_opacity=0.18
        )

        self.play(Create(glow_graph), Create(sine_graph), run_time=2.2)

        show_caption(
            "Its shape repeats in a regular way, making it an ideal model for periodic behavior.",
            run_time=3.8
        )

        # -------------------------------------------------
        # Formula (FIXED position — کمی پایین‌تر تا با تایتل تداخل نکند)
        # -------------------------------------------------
        formula = MathTex(
            r"f(x)=A\sin(\omega x+\phi)",
            font_size=42,
            color=WHITE
        ).to_corner(UR, buff=0.6).shift(DOWN * 1.1)

        formula_box = SurroundingRectangle(
            formula,
            corner_radius=0.15,
            color=BLUE_D,
            buff=0.2,
            stroke_width=2
        )

        self.play(FadeIn(formula_box), Write(formula), run_time=1.5)

        show_caption(
            "Mathematically, we can write it as f of x equals A sine of omega x plus phi.",
            run_time=4.0
        )

        # -------------------------------------------------
        # Amplitude
        # -------------------------------------------------
        amp_line = DashedLine(
            axes.c2p(PI / 2, 0),
            axes.c2p(PI / 2, 1),
            color=GREEN_B,
            stroke_width=3
        )

        amp_brace = BraceBetweenPoints(
            axes.c2p(PI / 2, 0),
            axes.c2p(PI / 2, 1),
            direction=RIGHT,
            color=GREEN_B
        )

        amp_label = MathTex("A", font_size=34, color=GREEN_B).next_to(amp_brace, RIGHT, buff=0.12)

        amp_text = Text(
            "Amplitude",
            font_size=26,
            color=GREEN_B,
            weight=BOLD
        ).next_to(formula, DOWN, aligned_edge=LEFT, buff=0.35)

        self.play(
            Create(amp_line),
            GrowFromCenter(amp_brace),
            FadeIn(amp_label),
            FadeIn(amp_text),
            run_time=1.5
        )

        show_caption(
            "The amplitude determines how far the wave rises and falls from its central position.",
            run_time=4.0
        )

        # -------------------------------------------------
        # Frequency
        # -------------------------------------------------
        self.play(
            FadeOut(amp_line),
            FadeOut(amp_brace),
            FadeOut(amp_label),
            FadeOut(amp_text),
            run_time=0.8
        )

        freq_text = Text(
            "Frequency",
            font_size=26,
            color=RED_B,
            weight=BOLD
        ).next_to(formula, DOWN, aligned_edge=LEFT, buff=0.35)

        sine_graph_highfreq = axes.plot(
            lambda x: np.sin(2 * x),
            x_range=[0, 2 * PI],
            color=RED_B,
            stroke_width=5
        )

        glow_graph_highfreq = axes.plot(
            lambda x: np.sin(2 * x),
            x_range=[0, 2 * PI],
            color=RED_E,
            stroke_width=10,
            stroke_opacity=0.15
        )

        self.play(
            Transform(glow_graph, glow_graph_highfreq),
            Transform(sine_graph, sine_graph_highfreq),
            FadeIn(freq_text),
            run_time=2.0
        )

        show_caption(
            "The frequency controls how rapidly the oscillation repeats within a given interval.",
            run_time=4.0
        )

        # -------------------------------------------------
        # Phase
        # -------------------------------------------------
        self.play(FadeOut(freq_text), run_time=0.5)

        phase_text = Text(
            "Phase Shift",
            font_size=26,
            color=PURPLE_B,
            weight=BOLD
        ).next_to(formula, DOWN, aligned_edge=LEFT, buff=0.35)

        sine_graph_phase = axes.plot(
            lambda x: np.sin(2 * x + PI / 3),
            x_range=[0, 2 * PI],
            color=PURPLE_B,
            stroke_width=5
        )

        glow_graph_phase = axes.plot(
            lambda x: np.sin(2 * x + PI / 3),
            x_range=[0, 2 * PI],
            color=PURPLE_E,
            stroke_width=10,
            stroke_opacity=0.15
        )

        shift_arrow = CurvedArrow(
            start_point=axes.c2p(0.8, 1),
            end_point=axes.c2p(0.2, 0.8),
            color=PURPLE_B,
            angle=PI / 2
        )

        self.play(
            Transform(glow_graph, glow_graph_phase),
            Transform(sine_graph, sine_graph_phase),
            FadeIn(phase_text),
            Create(shift_arrow),
            run_time=2.0
        )

        show_caption(
            "The phase shift moves the wave left or right, changing where the oscillation begins.",
            run_time=4.2
        )

        # -------------------------------------------------
        # Return to clean base sine
        # -------------------------------------------------
        # -------------------------------------------------
        # Return to clean base sine
        # -------------------------------------------------
        clean_graph = axes.plot(
            lambda x: np.sin(x),
            x_range=[0, 2 * PI],
            color=YELLOW,
            stroke_width=5
        )

        clean_glow = axes.plot(
            lambda x: np.sin(x),
            x_range=[0, 2 * PI],
            color=YELLOW_E,
            stroke_width=10,
            stroke_opacity=0.18
        )

        self.play(
            FadeOut(shift_arrow),
            FadeOut(phase_text),
            Transform(glow_graph, clean_glow),
            Transform(sine_graph, clean_graph),
            run_time=1.8
        )

        show_caption(
            "Now let us return to the simplest form: a single, clean sine wave.",
            run_time=3.5
        )

        # -------------------------------------------------
        # Moving dot + traced path
        # -------------------------------------------------
        remove_caption()

        tracker = ValueTracker(0)

        moving_dot = always_redraw(
            lambda: Dot(
                point=axes.c2p(tracker.get_value(), np.sin(tracker.get_value())),
                color=WHITE,
                radius=0.09
            )
        )

        trail = TracedPath(
            moving_dot.get_center,
            stroke_color=BLUE_B,
            stroke_width=4,
            stroke_opacity=0.85
        )

        self.add(trail, moving_dot)

        show_caption(
            "We can follow a single point as it traces the wave, revealing the motion behind the curve.",
            run_time=4.0
        )
        self.play(
            tracker.animate.set_value(2 * PI),
            run_time=4.5,
            rate_func=linear
        )

        self.wait(0.3)

        self.play(
            FadeOut(moving_dot),
            FadeOut(trail),
            run_time=0.8
        )

        # -------------------------------------------------
        # Closing message
        # -------------------------------------------------
        show_caption(
            "The sine wave is one of the most important shapes in all of mathematics and physics.",
            run_time=4.0
        )

        remove_caption()

        final_text = Text(
            "A simple oscillation can become the foundation\n"
            "for understanding much more complex signals.",
            font_size=30,
            color=WHITE,
            line_spacing=1.1,
            font="DejaVu Sans"
        ).move_to(ORIGIN)

        # محو کردن اجزای صحنه برای تمرکز روی پیام پایانی
        self.play(
            FadeOut(axes),
            FadeOut(axes_labels),
            FadeOut(x_marks),
            FadeOut(sine_graph),
            FadeOut(glow_graph),
            FadeOut(formula),
            FadeOut(formula_box),
            FadeOut(title_group),
            run_time=1.5
        )

        self.play(Write(final_text), run_time=2.5)
        self.wait(2.0)

        conclusion = Text(
            "And this is exactly where Fourier analysis begins.",
            font_size=32,
            color=BLUE_B,
            weight=BOLD,
            font="DejaVu Sans"
        ).move_to(ORIGIN)

        self.play(
            FadeOut(final_text, shift=UP * 0.3),
            run_time=1.0
        )
        self.play(
            FadeIn(conclusion, shift=DOWN * 0.2),
            run_time=2.0
        )
        self.wait(2.5)

        self.play(FadeOut(conclusion), run_time=1.5)
        self.wait(0.5)
