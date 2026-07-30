from manim import *
import numpy as np


class FourierScene6(Scene):
    def construct(self):
        self.camera.background_color = "#0f1117"

        # ---------------------------------------------------------------
        # Subtitle System (Copied from template)
        # ---------------------------------------------------------------
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

        def build_caption(text, font_size=18, max_chars=64):
            words = text.split()
            lines = wrap_words(words, max_chars)
            full_str = "\n".join(lines)
            full_text = Text(full_str, font_size=font_size, color=WHITE,
                             line_spacing=1.0, font="DejaVu Sans")
            caption_bg = RoundedRectangle(
                corner_radius=0.18, height=full_text.height + 0.5,
                width=min(full_text.width + 0.9, 12.8),
                stroke_color=BLUE_D, stroke_width=1.4,
                fill_color="#0a0c14", fill_opacity=0.82)
            accent = RoundedRectangle(
                corner_radius=0.05, height=caption_bg.height - 0.22,
                width=0.08, fill_color=BLUE_B, fill_opacity=0.9, stroke_opacity=0)
            full_text.move_to(caption_bg.get_center())
            VGroup(caption_bg, full_text).to_edge(DOWN, buff=0.4)
            accent.next_to(caption_bg.get_left(), RIGHT, buff=0.12)
            word_groups, idx = [], 0
            for w in words:
                n = len(w)
                word_groups.append(VGroup(*full_text[idx: idx + n]))
                idx += n
            return caption_bg, accent, full_text, word_groups

        def show_caption(text, run_time=3.5, wait_time=0.25, font_size=19):
            new_bg, new_accent, full_text, word_groups = build_caption(text, font_size)
            if not bg_on[0]:
                self.play(FadeIn(new_bg, shift=UP * 0.18),
                          FadeIn(new_accent, shift=UP * 0.18), run_time=0.5)
                cap_bg[0], cap_accent[0], bg_on[0] = new_bg, new_accent, True
            else:
                anims = [Transform(cap_bg[0], new_bg), Transform(cap_accent[0], new_accent)]
                if cap_words[0] is not None:
                    anims.append(FadeOut(cap_words[0], shift=DOWN * 0.08))
                self.play(*anims, run_time=0.5)
            words_vgroup = VGroup(*word_groups)
            self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.14) for g in word_groups],
                                  lag_ratio=0.38), run_time=run_time)
            cap_words[0] = words_vgroup
            self.wait(wait_time)

        def remove_caption():
            if bg_on[0]:
                anims = [FadeOut(cap_bg[0], shift=DOWN * 0.18),
                         FadeOut(cap_accent[0], shift=DOWN * 0.18)]
                if cap_words[0] is not None:
                    anims.append(FadeOut(cap_words[0], shift=DOWN * 0.1))
                self.play(*anims, run_time=0.5)
                bg_on[0] = False

        # ================================================================
        # SECTION TITLE
        # ================================================================
        title = Text("Windowing in Audio Processing",
                     font_size=32, weight=BOLD, color=BLUE_B,
                     font="DejaVu Sans").to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.9)

        # ================================================================
        # PART 1 — The Abrupt Frame Cut
        # ================================================================
        show_caption(
            "After dividing the signal into short frames, a small issue appears.",
            run_time=3.5, wait_time=0.2)

        # Axes for a single frame
        axes = Axes(
            x_range=[0, 10, 2], y_range=[-1.5, 1.5, 1],
            x_length=8.0, y_length=3.0,
            axis_config={"color": GREY_B, "stroke_width": 1.4, "include_numbers": False},
        ).shift(UP * 0.2)

        # Raw frame function (intentionally not zero at edges)
        def raw_func(x):
            return np.sin(1.2 * x) + 0.5 * np.cos(3.5 * x)

        raw_curve = axes.plot(raw_func, x_range=[0, 10, 0.05], color=YELLOW, stroke_width=3)
        
        self.play(Create(axes), Create(raw_curve), run_time=2.0)

        show_caption(
            "When we isolate a frame from the signal, we are essentially cutting the waveform "
            "abruptly at the beginning and the end. However, in the original signal, the waveform continues smoothly over time.",
            run_time=7.5, wait_time=0.2)

        # Highlight edges
        start_point = axes.c2p(0, raw_func(0))
        end_point = axes.c2p(10, raw_func(10))
        edge_circle1 = Circle(radius=0.2, color=RED).move_to(start_point)
        edge_circle2 = Circle(radius=0.2, color=RED).move_to(end_point)

        self.play(Create(edge_circle1), Create(edge_circle2), run_time=1.0)
        self.play(Indicate(edge_circle1, color=RED), Indicate(edge_circle2, color=RED))

        # ================================================================
        # PART 2 — Spectral Leakage
        # ================================================================
        show_caption(
            "This sudden truncation can cause problems in frequency analysis and may spread the energy "
            "of some frequencies incorrectly across the spectrum. This phenomenon is known as spectral leakage.",
            run_time=8.5, wait_time=0.2)

        leakage_text = Text("Spectral Leakage", color=RED, font_size=24, weight=BOLD).next_to(axes, UP, buff=0.2)
        self.play(FadeIn(leakage_text, shift=UP*0.1))
        self.wait(1.0)
        self.play(FadeOut(leakage_text), FadeOut(edge_circle1), FadeOut(edge_circle2))

        # ================================================================
        # PART 3 — The Windowing Concept & Formula
        # ================================================================
        show_caption(
            "To reduce this problem, before performing frequency analysis we multiply each frame "
            "by a window function. This step is called windowing.",
            run_time=6.5, wait_time=0.2)

        # Shrink axes slightly and move down to make room for math
        group_axes = VGroup(axes, raw_curve)
        self.play(group_axes.animate.scale(0.85).shift(DOWN * 0.5))

        formula_main = MathTex(r"x_w[n] = x[n] \cdot w[n]").set_color(WHITE).scale(1.1)
        formula_main.next_to(group_axes, UP, buff=0.4)
        
        self.play(Write(formula_main), run_time=1.5)

        # ================================================================
        # PART 4 — Smoothing the Edges
        # ================================================================
        show_caption(
            "The main idea is that the signal values near the beginning and the end of the frame "
            "gradually decrease, while the center of the frame receives more weight. This makes the edges of the frame smoother and allows the frequency analysis to be more accurate.",
            run_time=9.5, wait_time=0.2)

        # Window function curve
        def window_func(x):
            # Hamming shape mapped to [0, 10]
            return 0.54 - 0.46 * np.cos(2 * np.pi * x / 10)

        window_curve = axes.plot(window_func, x_range=[0, 10, 0.05], color=BLUE_C, stroke_width=3)
        window_label = Text("Window Function w[n]", color=BLUE_C, font_size=18).next_to(window_curve, UP, buff=0.1)

        self.play(Create(window_curve), FadeIn(window_label, shift=UP*0.1), run_time=2.0)

        # Tapered frame function
        def tapered_func(x):
            return raw_func(x) * window_func(x)

        tapered_curve = axes.plot(tapered_func, x_range=[0, 10, 0.05], color=GREEN_C, stroke_width=3)

        self.play(Transform(raw_curve, tapered_curve), run_time=2.0)
        self.wait(0.5)

        # ================================================================
        # PART 5 — Hamming Window Formula
        # ================================================================
        show_caption(
            "One of the most widely used windows in speech processing is the Hamming window.",
            run_time=5.0, wait_time=0.2)

        formula_hamming = MathTex(r"w[n] = 0.54 - 0.46\cos\left(\frac{2\pi n}{N - 1}\right)").set_color(BLUE_C).scale(0.7)
        formula_hamming.next_to(formula_main, UP, buff=0.2)

        self.play(FadeIn(formula_hamming, shift=UP*0.1), run_time=1.0)
        self.wait(1.0)

        # ================================================================
        # PART 6 — Conclusion
        # ================================================================
        show_caption(
            "After this step, each frame of the signal is ready for frequency analysis.",
            run_time=4.5, wait_time=0.2)

        self.play(FadeOut(window_curve), FadeOut(window_label), run_time=1.0)
        self.play(Indicate(raw_curve, color=GREEN_B)) # raw_curve is now the tapered curve

        # ================================================================
        # ENDING
        # ================================================================
        remove_caption()
        
        self.play(
            FadeOut(VGroup(title, group_axes, formula_main, formula_hamming), shift=UP * 0.15),
            run_time=1.1
        )

        closing = Text("Next: Short-Time Fourier Transform (STFT)",
                          font_size=30, color=YELLOW,
                          font="DejaVu Sans").move_to(ORIGIN)
        self.play(FadeIn(closing, shift=DOWN * 0.15))
        self.wait(2.5)
        self.play(FadeOut(closing))
        self.wait(0.8)
