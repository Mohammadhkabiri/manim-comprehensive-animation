from manim import *
import numpy as np

class FourierScene4(Scene):
    def construct(self):
        self.camera.background_color = "#0f1117"

        # --- سیستم زیرنویس: هماهنگ با سکانس‌های قبل ---
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

        def build_caption(text, font_size=20, max_chars=64):
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
            VGroup(caption_bg, full_text).to_edge(DOWN, buff=0.22)
            accent.next_to(caption_bg.get_left(), RIGHT, buff=0.12)

            word_groups, idx = [], 0
            for w in words:
                n = len(w)
                word_groups.append(VGroup(*full_text[idx:idx + n]))
                idx += n

            return caption_bg, accent, full_text, word_groups

        def show_caption(text, run_time=3.5, wait_time=0.25, font_size=20):
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
            "How the Matching Works",
            font_size=40,
            weight=BOLD,
            color=BLUE_B
        )
        subtitle = Text(
            "A Simple Picture Behind Fourier Analysis",
            font_size=28,
            color=GREY_B
        ).next_to(title, DOWN, buff=0.15)

        title_group = VGroup(title, subtitle).to_edge(UP, buff=0.4)

        self.play(FadeIn(title_group, shift=DOWN * 0.2), run_time=1.2)

        show_caption(
            "In the last part, we said Fourier analysis works by testing one frequency at a time. Now let’s see what that matching really means.",
            run_time=4.8
        )

        # -------------------------------------------------
        # Main axes
        # -------------------------------------------------
        main_axes = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-2.2, 2.2, 1],
            x_length=10.5,
            y_length=2.4,
            axis_config={"color": GREY_A, "stroke_width": 2},
            tips=False
        ).shift(UP * 1)

        signal_label = Text("Signal", font_size=24, color=BLUE_B).next_to(main_axes, UP, buff=0.15)

        signal_graph = main_axes.plot(
            lambda x: np.sin(x) + 0.5 * np.sin(3 * x),
            x_range=[0, 2 * PI],
            color=BLUE_B,
            stroke_width=5
        )

        signal_glow = main_axes.plot(
            lambda x: np.sin(x) + 0.5 * np.sin(3 * x),
            x_range=[0, 2 * PI],
            color=BLUE_D,
            stroke_width=10,
            stroke_opacity=0.14
        )

        self.play(Create(main_axes), FadeIn(signal_label), run_time=1.3)
        self.play(Create(signal_glow), Create(signal_graph), run_time=1.8)

        show_caption(
            "Suppose this is our signal. We already know it contains some hidden ingredients, but now we want a way to measure one specific frequency.",
            run_time=4.8
        )

        # -------------------------------------------------
        # Test wave: matching frequency
        # -------------------------------------------------
        test_axes = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-1.5, 1.5, 1],
            x_length=10.5,
            y_length=1.2,
            axis_config={"color": GREY_A, "stroke_width": 1.5},
            tips=False
        ).next_to(main_axes, DOWN, buff=0.55)

        test_label = Text("Test wave", font_size=22, color=YELLOW).next_to(test_axes, UP, buff=0.08)

        test_graph_match = test_axes.plot(
            lambda x: np.sin(x),
            x_range=[0, 2 * PI],
            color=YELLOW,
            stroke_width=5
        )

        self.play(Create(test_axes), FadeIn(test_label), run_time=1.0)
        self.play(Create(test_graph_match), run_time=1.6)

        show_caption(
            "So we bring in a test wave. At first, let’s choose a wave with frequency one, and compare it against the signal.",
            run_time=4.5
        )

        # -------------------------------------------------
        # Visual matching lines
        # -------------------------------------------------
        sample_x = np.linspace(0.4, 2 * np.pi - 0.4, 7)
        match_lines = VGroup()

        for x in sample_x:
            p1 = main_axes.c2p(x, np.sin(x) + 0.5 * np.sin(3 * x))
            p2 = test_axes.c2p(x, np.sin(x))
            line = DashedLine(p1 + DOWN* 0.08, p2+ UP *0.08, dash_length=0.12, color=YELLOW, stroke_opacity=0.5)
            match_lines.add(line)

        self.play(LaggedStart(*[Create(line) for line in match_lines], lag_ratio=0.08), run_time=1.4)

        show_caption(
            "Notice that a big part of this test wave rises and falls in step with the signal. They are not identical, but they do line up in an important way.",
            run_time=5.0
        )

        # -------------------------------------------------
        # Match score box
        # -------------------------------------------------
        score_box = RoundedRectangle(
            corner_radius=0.16,
            width=2.35,
            height=0.82,
            stroke_color=YELLOW,
            fill_color="#151821",
            fill_opacity=0.9
        ).to_edge(RIGHT, buff=0.11).shift(UP * 0.05)

        score_title = Text("Match strength", font_size=16, color=YELLOW).move_to(score_box.get_center() + UP * 0.12)
        score_value = DecimalNumber(
            0.00, num_decimal_places=2, font_size=20, color=WHITE
        ).move_to(score_box.get_center() + DOWN * 0.11)

        self.play(FadeIn(score_box), FadeIn(score_title), FadeIn(score_value), run_time=1.0)
        self.play(score_value.animate.set_value(0.86), run_time=1.4)

        show_caption(
            "When the test wave matches a real ingredient inside the signal, the overlap adds up instead of canceling out, so the score becomes strong.",
            run_time=4.8
        )

        # -------------------------------------------------
        # Switch to mismatched wave
        # -------------------------------------------------
        mismatch_graph = test_axes.plot(
            lambda x: np.sin(2 * x),
            x_range=[0, 2 * PI],
            color=RED_B,
            stroke_width=5
        )

        mismatch_label = Text("Test wave", font_size=24, color=RED_B).move_to(test_label)

        new_lines = VGroup()
        for x in sample_x:
            p1 = main_axes.c2p(x, np.sin(x) + 0.5 * np.sin(3 * x))
            p2 = test_axes.c2p(x, np.sin(2 * x))
            line = DashedLine(p1, p2, dash_length=0.12, color=RED_B, stroke_opacity=0.55)
            new_lines.add(line)

        self.play(
            Transform(test_graph_match, mismatch_graph),
            Transform(test_label, mismatch_label),
            FadeOut(match_lines),
            run_time=1.6
        )
        self.play(LaggedStart(*[Create(line) for line in new_lines], lag_ratio=0.08), run_time=1.2)
        self.play(score_value.animate.set_value(0.08), run_time=1.2)

        show_caption(
            "But if we try a frequency that does not really belong to the signal, some parts agree while other parts disagree, and the total effect mostly cancels away.",
            run_time=5.1
        )

        # -------------------------------------------------
        # Positive / negative contribution idea
        # -------------------------------------------------
        plus_text = Text("agreement", font_size=17, color=GREEN_B).next_to(score_box, LEFT, buff=0.12).shift(UP * 0.15)
        minus_text = Text("cancellation", font_size=17, color=RED_B).next_to(score_box, LEFT, buff=0.12).shift(DOWN * 0.15)

        self.play(FadeIn(plus_text), FadeIn(minus_text), run_time=0.8)

        show_caption(
            "That is the key idea: good alignment contributes positively, bad alignment contributes negatively, and the final result tells us how much that frequency is really there.",
            run_time=5.0
        )

        # -------------------------------------------------
        # Switch to second real ingredient
        # -------------------------------------------------
        real3_graph = test_axes.plot(
            lambda x: np.sin(3 * x),
            x_range=[0, 2 * PI],
            color=GREEN_B,
            stroke_width=5
        )
        real3_label = Text("Test wave", font_size=24, color=GREEN_B).move_to(test_label)

        real3_lines = VGroup()
        for x in sample_x:
            p1 = main_axes.c2p(x, np.sin(x) + 0.5 * np.sin(3 * x))
            p2 = test_axes.c2p(x, np.sin(3 * x))
            line = DashedLine(p1, p2, dash_length=0.12, color=GREEN_B, stroke_opacity=0.55)
            real3_lines.add(line)

        self.play(
            Transform(test_graph_match, real3_graph),
            Transform(test_label, real3_label),
            FadeOut(new_lines),
            run_time=1.6
        )
        self.play(LaggedStart(*[Create(line) for line in real3_lines], lag_ratio=0.08), run_time=1.2)
        self.play(score_value.animate.set_value(0.43), run_time=1.2)

        show_caption(
            "And if we test another frequency that actually is present, like frequency three, the score rises again — maybe not as much, but clearly not zero.",
            run_time=4.9
        )

        # -------------------------------------------------
        # Mini interpretation panel
        # -------------------------------------------------
        idea_box = RoundedRectangle(
            corner_radius=0.16,
            width=3.55,
            height=0.95,
            stroke_color=BLUE_D,
            stroke_width=2.0,
            fill_color="#10131c",
            fill_opacity=0.82
        )
        idea_box.to_edge(LEFT,buff=0.22)
        idea_box.shift(UP * 2.75)

        idea_text = VGroup(
            Text("Strong match → frequency present", font_size=14, color=WHITE),
            Text("Weak match → little or no presence", font_size=14, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10).move_to(idea_box.get_center())

        self.play(FadeIn(idea_box), FadeIn(idea_text), run_time=1.0)

        show_caption(
            "So Fourier analysis is not magic. It is really a systematic way of asking, for each possible frequency, how well does this wave match the signal?",
            run_time=5.2
        )

        # -------------------------------------------------
        # Transition toward formula / next step
        # -------------------------------------------------
        brace_x = main_axes.get_left()[0] - 0.18

        brace = BraceBetweenPoints(
            np.array([brace_x, main_axes.get_bottom()[1] + 0.05, 0]),
            np.array([brace_x, test_axes.get_top()[1] - 0.05, 0]),
            direction=LEFT,
            color=BLUE_B
        )

        brace_text = Text(
            "compare\nand\naccumulate",
            font_size=15,
            line_spacing=0.75,
            font="DejaVu Sans",
            color=BLUE_B
        ).next_to(brace, LEFT, buff=0.08)


        self.play(Create(brace), FadeIn(brace_text), run_time=1.0)

        show_caption(
            "In the next step, we can make this idea precise with mathematics. We will turn this visual matching into an actual numerical recipe.",
            run_time=4.8
        )

        # -------------------------------------------------
        # Final summary
        # -------------------------------------------------
        remove_caption()

        summary_box = RoundedRectangle(
            corner_radius=0.18,
            width=7.4,
            height=1.6,
            stroke_color=BLUE_D,
            fill_color="#10131c",
            fill_opacity=0.82
        ).to_edge(DOWN * 0.35)

        summary_text = Text(
            "Fourier idea: test a frequency,\nmeasure the match, keep the score.",
            font_size=28,
            color=WHITE,
            line_spacing=1.0,
            weight=BOLD,
            font="DejaVu Sans"
        ).move_to(summary_box.get_center())

        self.play(FadeIn(summary_box), Write(summary_text), run_time=1.4)
        self.wait(2.0)

        next_text = Text(
            "Now we are ready to turn this intuition\ninto the real mathematical machinery.",
            font_size=30,
            color=BLUE_B,
            line_spacing=1.1,
            weight=BOLD,
            font="DejaVu Sans"
        ).move_to(ORIGIN)

        self.play(
            FadeOut(main_axes),
            FadeOut(test_axes),
            FadeOut(signal_label),
            FadeOut(test_label),
            FadeOut(signal_graph),
            FadeOut(signal_glow),
            FadeOut(test_graph_match),
            FadeOut(real3_lines),
            FadeOut(score_box),
            FadeOut(score_title),
            FadeOut(score_value),
            FadeOut(plus_text),
            FadeOut(minus_text),
            FadeOut(idea_box),
            FadeOut(idea_text),
            FadeOut(brace),
            FadeOut(brace_text),
            FadeOut(summary_box),
            FadeOut(summary_text),
            FadeOut(title_group),
            run_time=1.8
        )

        self.play(FadeIn(next_text, shift=DOWN * 0.2), run_time=1.8)
        self.wait(2.5)
        self.play(FadeOut(next_text), run_time=1.2)
        self.wait(0.5)
