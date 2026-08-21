from manim import *
import numpy as np


class FourierScene3(Scene):
    def construct(self):
        self.camera.background_color = "#0f1117"

        # --- سیستم زیرنویس (دقیقاً مشابه سکانس‌های قبلی برای حفظ یکدستی) ---
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

        def build_caption(text, font_size=22, max_chars=62):
            words = text.split()
            lines = wrap_words(words, max_chars)
            full_str = "\n".join(lines)
            full_text = Text(
                full_str,
                font_size=font_size,
                color=WHITE,
                line_spacing=1.0,
                font="DejaVu Sans",
            )
            caption_bg = RoundedRectangle(
                corner_radius=0.18,
                height=full_text.height + 0.5,
                width=min(full_text.width + 0.9, 12.8),
                stroke_color=BLUE_D,
                stroke_width=1.4,
                fill_color="#0a0c14",
                fill_opacity=0.82,
            )
            accent = RoundedRectangle(
                corner_radius=0.05,
                height=caption_bg.height - 0.22,
                width=0.08,
                fill_color=BLUE_B,
                fill_opacity=0.9,
                stroke_opacity=0,
            )
            full_text.move_to(caption_bg.get_center())
            VGroup(caption_bg, full_text).to_edge(DOWN, buff=0.4)
            accent.next_to(caption_bg.get_left(), RIGHT, buff=0.12)
            word_groups, idx = [], 0
            for w in words:
                n = len(w)
                word_groups.append(VGroup(*full_text[idx: idx + n]))
                idx += n
            return caption_bg, accent, full_text, word_groups

        def show_caption(text, run_time=3.5, wait_time=0.25, font_size=22):
            new_bg, new_accent, full_text, word_groups = build_caption(text, font_size)
            if not bg_on[0]:
                self.play(
                    FadeIn(new_bg, shift=UP * 0.18),
                    FadeIn(new_accent, shift=UP * 0.18),
                    run_time=0.5,
                )
                cap_bg[0], cap_accent[0], bg_on[0] = new_bg, new_accent, True
            else:
                anims = [
                    Transform(cap_bg[0], new_bg),
                    Transform(cap_accent[0], new_accent),
                ]
                if cap_words[0] is not None:
                    anims.append(FadeOut(cap_words[0], shift=DOWN * 0.08))
                self.play(*anims, run_time=0.5)
            words_vgroup = VGroup(*word_groups)
            self.play(
                LaggedStart(
                    *[FadeIn(g, shift=UP * 0.14) for g in word_groups],
                    lag_ratio=0.38,
                ),
                run_time=run_time,
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
                self.play(*anims, run_time=0.5)
                bg_on[0] = False

        # ================================================================
        # سکانس ۳ – از طبیعت تا بازارهای مالی
        # ================================================================

        # --- بخش ۱: عنوان و بازگشت به فوریه ---
        title = Text(
            "From Nature to Financial Markets",
            font_size=38,
            weight=BOLD,
            color=BLUE_B,
        ).to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.2))
        self.wait(0.3)

        show_caption(
            "In the previous section, we showed how the Fourier transform reveals "
            "the hidden order of nature; from the vibration of a guitar string to "
            "the light waves of distant galaxies.",
            run_time=5.5,
            wait_time=0.3,
        )

        # --- تصویرسازی: امواج طبیعت (گیتار + نور) ---
        axes_nat = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=2.5,
            axis_config={"color": GREY_A, "stroke_width": 1.5},
        ).shift(DOWN * 0.5)

        guitar_wave = axes_nat.plot(
            lambda x: (
                np.sin(x)
                + 0.5 * np.sin(2 * x)
                + 0.25 * np.sin(3 * x)
                + 0.12 * np.sin(5 * x)
            ) * 0.7,
            x_range=[0, 4 * PI],
            color=YELLOW,
            stroke_width=2.5,
        )
        light_wave = axes_nat.plot(
            lambda x: np.sin(2.7 * x + 0.5) * 0.55,
            x_range=[0, 4 * PI],
            color="#9B59B6",
            stroke_width=2.5,
        )

        guitar_label = Text("Guitar String", font_size=20, color=YELLOW).next_to(
            axes_nat.get_corner(UL), RIGHT, buff=0.2
        ).shift(DOWN * 0.1 + LEFT * 1.8)
        light_label = Text("Light Wave", font_size=20, color="#9B59B6").next_to(
            guitar_label, DOWN, buff=0.25
        ).shift(LEFT * 0.1 + DOWN * 0.02)

        self.play(Create(axes_nat), run_time=1)
        self.play(Create(guitar_wave), FadeIn(guitar_label), run_time=1.8)
        self.play(Create(light_wave), FadeIn(light_label), run_time=1.5)

        show_caption(
            "Almost every phenomenon in nature has a rhythm and a frequency structure.",
            run_time=3.5,
            wait_time=0.3,
        )

        # --- بخش ۲: سوال بنیادی ---
        self.play(
            FadeOut(
                VGroup(axes_nat, guitar_wave, light_wave, guitar_label, light_label)
            ),
            run_time=1,
        )

        question_line1 = Text(
            "But here, a fundamental question arises:",
            font_size=30,
            color=GREY_A,
        ).shift(UP * 1.0)
        question_line2 = Text(
            "Can the most complex and chaotic phenomenon on Earth",
            font_size=28,
            color=WHITE,
        ).shift(UP * 0.1)
        question_line3 = Text(
            "— the collective behavior of human beings —",
            font_size=28,
            color=BLUE_B,
        ).shift(DOWN * 0.55)
        question_line4 = Text(
            "also be analyzed?",
            font_size=28,
            color=WHITE,
        ).shift(DOWN * 1.1)

        remove_caption()
        self.play(
            LaggedStart(
                FadeIn(question_line1, shift=UP * 0.15),
                FadeIn(question_line2, shift=UP * 0.15),
                FadeIn(question_line3, shift=UP * 0.15),
                FadeIn(question_line4, shift=UP * 0.15),
                lag_ratio=0.45,
            ),
            run_time=3.5,
        )
        self.wait(1.5)

        show_caption(
            "If nature can be described by differential equations and frequency "
            "analysis, can the collective behavior of human beings also be analyzed?",
            run_time=4.5,
            wait_time=0.3,
        )

        self.play(
            FadeOut(
                VGroup(question_line1, question_line2, question_line3, question_line4)
            ),
            run_time=0.8,
        )

        # --- بخش ۳: بازار مالی به عنوان محیط تحلیل ---
        show_caption(
            "To answer this question, we need a real environment for data analysis; "
            "a space where fear, greed, hope, and the decisions of millions of people "
            "are turned into data moment by moment.",
            run_time=6.0,
            wait_time=0.3,
        )

        # نمودار روانشناسی سیکل بازار، پیاده‌سازی‌شده با خود مانیم
        market_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 6, 1],
            x_length=8.6,
            y_length=3.15,
            axis_config={"include_ticks": False, "stroke_opacity": 0},
            tips=False,
        ).move_to([0, 0.22, 0])

        x_axis_line = DashedLine(
            market_axes.c2p(0, 0.7),
            market_axes.c2p(10, 0.7),
            dash_length=0.14,
            color=GREY_B,
            stroke_width=2.0,
        )
        y_axis_line = DashedLine(
            market_axes.c2p(0.2, 0),
            market_axes.c2p(0.2, 6),
            dash_length=0.14,
            color=GREY_B,
            stroke_width=2.0,
        )

        cycle_title = Text(
            "PSYCHOLOGY OF A MARKET CYCLE",
            font_size=24,
            color=GREY_A,
            weight=BOLD,
            font="DejaVu Sans",
        ).next_to(market_axes, UP, buff=0.16)

        y_label = Text(
            "PRICE",
            font_size=20,
            color=GREY_A,
            weight=BOLD,
            font="DejaVu Sans",
        ).next_to(y_axis_line, LEFT, buff=0.25)

        x_label = Text(
            "TIME",
            font_size=20,
            color=GREY_A,
            weight=BOLD,
            font="DejaVu Sans",
        ).next_to(x_axis_line, DOWN, buff=0.2)

        cycle_points = [
            (0.0, 1.6),
            (0.5, 2.0),
            (0.8, 1.7),
            (1.4, 2.3),
            (1.7, 2.1),
            (2.6, 3.4),
            (2.9, 3.1),
            (4.0, 5.3),
            (4.25, 4.5),
            (4.6, 4.9),
            (4.85, 4.0),
            (5.1, 4.45),
            (5.35, 3.4),
            (5.7, 3.7),
            (5.9, 2.9),
            (6.2, 1.95),
            (6.9, 2.35),
            (7.3, 1.92),
            (8.0, 2.2),
            (8.4, 1.9),
            (8.95, 2.35),
            (9.15, 2.05),
            (9.35, 2.25),
        ]

        cycle_curve = VMobject(color=GREY_A, stroke_width=2.2)
        cycle_curve.set_points_as_corners(
            [market_axes.c2p(x, y) for x, y in cycle_points]
        )

        tail_arrow = Arrow(
            market_axes.c2p(9.35, 2.25),
            market_axes.c2p(9.9, 2.7),
            buff=0,
            color=GREY_A,
            stroke_width=2.0,
            max_tip_length_to_length_ratio=0.18,
        )

        phase_specs = [
            ("DISBELIEF", 0.75, 1.72, "#ff4d5a", DOWN * 0.23),
            ("HOPE", 1.45, 2.28, YELLOW, DOWN * 0.30),
            ("BELIEF", 2.9, 3.1, YELLOW, DOWN * 0.28),
            ("EUPHORIA", 4.0, 5.3, GREEN, UP * 0.26),
            ("ANXIETY", 4.6, 4.9, YELLOW, UP * 0.25),
            ("DENIAL", 5.1, 4.45, YELLOW, UP * 0.22),
            ("PANIC", 5.85, 3.1, YELLOW, RIGHT * 0.55 + UP * 0.10),
            ("CAPITULATION", 6.2, 1.95, YELLOW, DOWN * 0.30),
            ("ANGER", 7.3, 1.92, YELLOW, DOWN * 0.28),
            ("DEPRESSION", 8.4, 1.9, YELLOW, DOWN * 0.28),
            ("DISBELIEF", 9.35, 2.25, "#ff4d5a", UP * 0.24 + LEFT * 0.28),
        ]

        phase_dots = VGroup()
        phase_labels = VGroup()
        for text, x, y, color, offset in phase_specs:
            dot = Dot(market_axes.c2p(x, y), radius=0.08, color=color)
            label = Text(
                text,
                font_size=13,
                color=color,
                weight=BOLD,
                font="DejaVu Sans",
            ).move_to(dot.get_center() + offset)
            phase_dots.add(dot)
            phase_labels.add(label)

        market_cycle_group = VGroup(
            x_axis_line,
            y_axis_line,
            cycle_title,
            y_label,
            x_label,
            cycle_curve,
            tail_arrow,
            phase_dots,
            phase_labels,
        )

        self.play(
            FadeIn(x_axis_line),
            FadeIn(y_axis_line),
            FadeIn(cycle_title),
            FadeIn(y_label),
            FadeIn(x_label),
            run_time=0.8,
        )
        self.play(Create(cycle_curve), run_time=2.2)
        self.play(
            GrowArrow(tail_arrow),
            LaggedStart(
                *[FadeIn(dot, scale=0.8) for dot in phase_dots],
                *[FadeIn(label, shift=UP * 0.05) for label in phase_labels],
                lag_ratio=0.08,
            ),
            run_time=2.0,
        )

        show_caption(
            "That environment is definitely the financial market.",
            run_time=2.5,
            wait_time=0.2,
        )

        # --- بخش ۴: تعریف بازار مالی ---
        show_caption(
            "The financial market is not just a place for buying and selling; "
            "rather, it is a representation of the collective psychology of human beings, "
            "recorded in the language of numbers.",
            run_time=6.0,
            wait_time=0.3,
        )

        # نمایش ایکون‌های احساسات



        show_caption(
            "In other words, every buying and selling decision is transformed into measurable data.",
            run_time=3.8,
            wait_time=0.3,
        )

        # --- بخش ۵: ریاضیات مهندسی وارد مالی می‌شود ---
        self.play(
            FadeOut(
                VGroup(
                    market_cycle_group,
                )
            ),
            run_time=1,
        )

        show_caption(
            "And it is exactly from this point that engineering mathematics "
            "enters the world of finance.",
            run_time=3.8,
            wait_time=0.3,
        )

        # نمایش معادله فوریه + فلش به نمودار مالی
        fourier_eq = MathTex(
            r"X(f) = \int_{-\infty}^{\infty} x(t)\, e^{-i 2\pi f t}\, dt",
            font_size=40,
            color=YELLOW,
        ).shift(UP * 0.8)

        bridge_arrow = Arrow(
            fourier_eq.get_bottom() + DOWN * 0.1,
            fourier_eq.get_bottom() + DOWN * 1.5,
            buff=0.05,
            color=BLUE_B,
            stroke_width=3,
        )

        finance_label_bottom = Text(
            "Financial Market Analysis",
            font_size=28,
            color=BLUE_B,
            weight=BOLD,
        ).next_to(bridge_arrow.get_end(), DOWN, buff=0.15)

        self.play(Write(fourier_eq), run_time=2)
        self.play(
            GrowArrow(bridge_arrow),
            FadeIn(finance_label_bottom, shift=DOWN * 0.1),
            run_time=1.5,
        )
        self.wait(0.5)

        # برچسب‌های توضیحی در کنار معادله
        label_x = MathTex(
            r"x(t): \text{price signal}",
            font_size=22,
            color=GREY_A,
        ).next_to(fourier_eq, RIGHT, buff=0.5).shift(UP * 0.35)

        label_f = MathTex(
            r"X(f): \text{frequency spectrum}",
            font_size=22,
            color=GREY_A,
        ).next_to(fourier_eq, RIGHT, buff=0.5).shift(DOWN * 0.1)

        self.play(
            LaggedStart(
                FadeIn(label_x, shift=LEFT * 0.1),
                FadeIn(label_f, shift=LEFT * 0.1),
                lag_ratio=0.5,
            ),
            run_time=1.5,
        )
        self.wait(0.5)

        remove_caption()

        # --- پیام پایانی سکانس ۳ ---
        self.play(
            FadeOut(
                VGroup(
                    title,
                    fourier_eq,
                    bridge_arrow,
                    finance_label_bottom,
                    label_x,
                    label_f,
                )
            ),
            run_time=1,
        )

        final_msg = Text(
            "The financial market:\na mirror of human psychology\nin the language of mathematics.",
            font_size=34,
            line_spacing=1.3,
            color=WHITE,
        ).move_to(ORIGIN)

        self.play(Write(final_msg), run_time=3)
        self.wait(1.5)

        transition_text = Text(
            "Now let us see what this analysis reveals.",
            color=YELLOW,
            font_size=32,
        ).move_to(ORIGIN)

        self.play(FadeOut(final_msg, shift=UP * 0.3))
        self.play(FadeIn(transition_text, shift=DOWN * 0.2))
        self.wait(2.5)

        self.play(FadeOut(transition_text))
        self.wait(1)
