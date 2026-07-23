from manim import *
import numpy as np


class FourierScene7(Scene):
    def construct(self):
        self.camera.background_color = "#0f1117"

        # ---------------------------------------------------------------
        # Subtitle System
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

        def build_caption(text, font_size=19, max_chars=64):
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

        def soft_panel(w, h, stroke=BLUE_D, fill="#111522", opacity=0.6):
            return RoundedRectangle(width=w, height=h, corner_radius=0.2,
                                    stroke_color=stroke, stroke_width=1.6,
                                    fill_color=fill, fill_opacity=opacity)

        def section_label(text, color=BLUE_B):
            return Text(text, font_size=20, color=color, weight=BOLD,
                        font="DejaVu Sans")

        # ================================================================
        # SECTION TITLE
        # ================================================================
        title = Text("Applications of Fourier Transform in AI",
                     font_size=34, weight=BOLD, color=BLUE_B,
                     font="DejaVu Sans").to_edge(UP, buff=0.32)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.8)

        show_caption(
            "Analyzing time-series data is not the only application of the Fourier "
            "Transform in artificial intelligence. Whenever data changes over time or "
            "space, frequency analysis can reveal important information about its structure.",
            run_time=6.5, wait_time=0.2)

        show_caption(
            "For this reason, the Fourier Transform is used in many different areas of AI.",
            run_time=3.2, wait_time=0.2)

        # ================================================================
        # PART 1 — Image Processing
        # ================================================================
        tag1 = section_label("① Image Processing", color=YELLOW)
        tag1.next_to(title, DOWN, buff=0.28)
        self.play(FadeIn(tag1, shift=RIGHT * 0.1), run_time=0.6)

        show_caption(
            "In image processing, a digital image can be considered a function "
            "representing brightness intensity across spatial locations.",
            run_time=4.8, wait_time=0.15)

        # Draw a simple pixel-grid "image" (6x6 squares with brightness values)
        np.random.seed(3)
        grid_size = 6
        cell = 0.45
        img_group = VGroup()
        brightness = np.array([
            [0.9, 0.8, 0.7, 0.6, 0.5, 0.4],
            [0.8, 0.85, 0.75, 0.55, 0.45, 0.3],
            [0.7, 0.72, 0.9, 0.8, 0.4, 0.25],
            [0.5, 0.6, 0.78, 0.88, 0.5, 0.3],
            [0.35, 0.45, 0.55, 0.65, 0.7, 0.4],
            [0.2, 0.3, 0.4, 0.5, 0.45, 0.6],
        ])
        for i in range(grid_size):
            for j in range(grid_size):
                b = brightness[i][j]
                gray_c = interpolate_color(BLACK, WHITE, b)
                sq = Square(side_length=cell,
                            fill_color=gray_c,
                            fill_opacity=1, stroke_color=GREY_B, stroke_width=0.6)
                sq.move_to(LEFT * 3.8 + RIGHT * j * cell + DOWN * i * cell + UP * 0.5)
                img_group.add(sq)

        img_label = Text("Spatial Domain", font_size=17, color=GREY_A,
                         font="DejaVu Sans").next_to(img_group, UP, buff=0.14)

        arrow_img = Arrow(LEFT * 1.4 + UP * 0.5, RIGHT * 0.1 + UP * 0.5,
                          color=BLUE_B, stroke_width=2.6,
                          max_tip_length_to_length_ratio=0.15)
        fft_tag = Text("FFT", font_size=18, color=BLUE_B,
                       font="DejaVu Sans").next_to(arrow_img, UP, buff=0.08)

        # Frequency domain: glowing center (low freq) + dim outer (high freq)
        freq_grid = VGroup()
        center = np.array([2, 2])
        freq_bright = np.zeros((grid_size, grid_size))
        for i in range(grid_size):
            for j in range(grid_size):
                dist = np.sqrt((i - 2.5) ** 2 + (j - 2.5) ** 2)
                freq_bright[i][j] = max(0, 1.0 - dist * 0.32)

        for i in range(grid_size):
            for j in range(grid_size):
                b = freq_bright[i][j]
                c = interpolate_color(BLACK, ManimColor("#00aaff"), b)
                sq = Square(side_length=cell, fill_color=c,
                            fill_opacity=1, stroke_color=GREY_B, stroke_width=0.6)
                sq.move_to(RIGHT * 1.6 + RIGHT * j * cell + DOWN * i * cell + UP * 0.5)
                freq_grid.add(sq)

        freq_label = Text("Frequency Domain", font_size=17, color=GREY_A,
                          font="DejaVu Sans").next_to(freq_grid, UP, buff=0.14)

        low_tag  = Text("Low freq = structure", font_size=19, color=YELLOW,
                        font="DejaVu Sans").next_to(freq_grid, RIGHT, buff=0.3).shift(UP * 0.3)
        high_tag = Text("High freq = edges & details", font_size=19, color=GREEN_B,
                        font="DejaVu Sans").next_to(low_tag, DOWN, buff=0.22).shift(RIGHT * 0.2)

        self.play(FadeIn(img_group), FadeIn(img_label), run_time=1.0)
        self.play(GrowArrow(arrow_img), FadeIn(fft_tag), run_time=0.7)
        self.play(FadeIn(freq_grid), FadeIn(freq_label), run_time=1.0)

        show_caption(
            "Low-frequency components describe the overall structure, while "
            "high-frequency components correspond to details and edges — "
            "widely used in noise removal and texture analysis.",
            run_time=5.5, wait_time=0.2)

        self.play(FadeIn(low_tag, shift=LEFT * 0.1),
                  FadeIn(high_tag, shift=LEFT * 0.1), run_time=0.8)
        self.wait(0.5)

        self.play(FadeOut(VGroup(img_group, img_label, arrow_img, fft_tag,
                                 freq_grid, freq_label, low_tag, high_tag, tag1)),
                  run_time=0.8)

        # ================================================================
        # PART 2 — Biological Signals (ECG)
        # ================================================================
        tag2 = section_label("② Biological Signal Analysis", color=GREEN_B)
        tag2.next_to(title, DOWN, buff=0.28)
        self.play(FadeIn(tag2, shift=RIGHT * 0.1), run_time=0.6)

        show_caption(
            "Another application appears in the analysis of biological signals. "
            "Signals such as the electrical activity of the brain or heart are "
            "time-based signals containing multiple frequency components.",
            run_time=5.5, wait_time=0.2)

        # ECG-like signal
        axes_ecg = Axes(
            x_range=[0, 4 * PI, PI], y_range=[-1.5, 2.0, 1],
            x_length=5.5, y_length=2.6,
            axis_config={"color": GREY_B, "stroke_width": 1.3},
        ).to_edge(LEFT, buff=0.6).shift(UP * 0.3)

        def ecg_wave(x):
            # simplified ECG shape: baseline + P + QRS spike + T
            base = 0.15 * np.sin(x)
            p    = 0.3 * np.exp(-((x % (2 * PI) - 1.2) ** 2) / 0.06)
            qrs  = (1.6 * np.exp(-((x % (2 * PI) - 2.0) ** 2) / 0.008)
                    - 0.4 * np.exp(-((x % (2 * PI) - 1.85) ** 2) / 0.012)
                    - 0.3 * np.exp(-((x % (2 * PI) - 2.15) ** 2) / 0.012))
            t    = 0.35 * np.exp(-((x % (2 * PI) - 3.0) ** 2) / 0.12)
            return base + p + qrs + t

        ecg_curve = axes_ecg.plot(ecg_wave, x_range=[0, 4 * PI, 4 * PI / 500],
                                  color=GREEN_B, stroke_width=2.4)
        ecg_label = Text("ECG / Brain Signal", font_size=17, color=GREY_A,
                         font="DejaVu Sans").next_to(axes_ecg, DOWN, buff=0.12)

        # Frequency spectrum of ECG (stem plot)
        axes_ecgf = Axes(
            x_range=[0, 8, 2], y_range=[0, 1.1, 0.5],
            x_length=4.5, y_length=2.6,
            axis_config={"color": GREY_B, "stroke_width": 1.3},
        ).to_edge(RIGHT, buff=0.6).shift(UP * 0.3)

        ecg_peaks = [(0.8, 0.9, GREEN_B), (2.5, 0.55, TEAL_B), (5.0, 0.28, BLUE_B)]
        ecg_bars = VGroup()
        for f, a, c in ecg_peaks:
            stem = Line(axes_ecgf.c2p(f, 0), axes_ecgf.c2p(f, a),
                        color=c, stroke_width=3.5)
            dot  = Dot(axes_ecgf.c2p(f, a), radius=0.09, color=c)
            ecg_bars.add(VGroup(stem, dot))

        ecg_freq_label = Text("Frequency Spectrum", font_size=17, color=GREY_A,
                              font="DejaVu Sans").next_to(axes_ecgf, DOWN, buff=0.12)

        mid_arrow = Arrow(axes_ecg.get_right(), axes_ecgf.get_left(),
                          buff=0.18, color=BLUE_B, stroke_width=2.5,
                          max_tip_length_to_length_ratio=0.15)

        self.play(Create(axes_ecg), FadeIn(ecg_label), run_time=0.7)
        self.play(Create(ecg_curve), run_time=1.8)
        self.play(GrowArrow(mid_arrow), run_time=0.6)
        self.play(Create(axes_ecgf), FadeIn(ecg_freq_label), run_time=0.7)
        self.play(LaggedStart(*[Create(b) for b in ecg_bars], lag_ratio=0.3), run_time=1.2)

        show_caption(
            "By analyzing the frequency spectrum of these signals, we can extract "
            "important information about the state of biological systems.",
            run_time=4.8, wait_time=0.2)

        self.play(FadeOut(VGroup(axes_ecg, ecg_curve, ecg_label, mid_arrow,
                                 axes_ecgf, ecg_bars, ecg_freq_label, tag2)),
                  run_time=0.8)

        # ================================================================
        # PART 3 — Neural Networks & Convolution
        # ================================================================
        tag3 = section_label("③ Neural Networks & Convolution", color=ORANGE)
        tag3.next_to(title, DOWN, buff=0.28)
        self.play(FadeIn(tag3, shift=RIGHT * 0.1), run_time=0.6)

        show_caption(
            "Additionally, in some neural network computations — especially those "
            "involving convolution operations — frequency analysis can help simplify "
            "certain calculations.",
            run_time=5.5, wait_time=0.2)

        # Simple CNN diagram: Input → Conv layer → Feature map (3 blocks)
        def make_block(label, w, h, stroke, fill):
            box = RoundedRectangle(width=w, height=h, corner_radius=0.18,
                                   stroke_color=stroke, stroke_width=1.8,
                                   fill_color=fill, fill_opacity=0.72)
            txt = Text(label, font_size=18, color=WHITE, font="DejaVu Sans")
            txt.move_to(box.get_center())
            return VGroup(box, txt)

        b_input  = make_block("Input\nImage",   1.8, 1.5, GREY_B,   "#1a1a2e").shift(LEFT * 4.5 + DOWN * 0.3)
        b_conv   = make_block("Conv\nLayer",    1.8, 1.5, BLUE_B,   "#0d1b3e").shift(LEFT * 2.1 + DOWN * 0.3)
        b_fft    = make_block("FFT\nDomain",    1.8, 1.5, YELLOW,   "#2a1f00").shift(RIGHT * 0.3 + DOWN * 0.3)
        b_feat   = make_block("Feature\nMap",   1.8, 1.5, GREEN_B,  "#0d2e1a").shift(RIGHT * 2.7 + DOWN * 0.3)
        b_output = make_block("Output /\nPred", 1.8, 1.5, ORANGE,   "#2e1800").shift(RIGHT * 5.1 + DOWN * 0.3)

        blocks = VGroup(b_input, b_conv, b_fft, b_feat, b_output)
        cnn_arrows = VGroup()
        for a, b in zip([b_input, b_conv, b_fft, b_feat],
                        [b_conv,  b_fft,  b_feat, b_output]):
            cnn_arrows.add(Arrow(a.get_right(), b.get_left(), buff=0.1,
                                 color=GREY_B, stroke_width=2.2,
                                 max_tip_length_to_length_ratio=0.18))

        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.08) for b in blocks],
                              lag_ratio=0.18), run_time=1.6)
        self.play(LaggedStart(*[GrowArrow(a) for a in cnn_arrows],
                              lag_ratio=0.18), run_time=1.2)
        self.wait(0.4)

        show_caption(
            "Across all these examples, the same core idea appears: the Fourier "
            "Transform reveals the frequency structure of data, and artificial "
            "intelligence uses that structure for learning and analysis.",
            run_time=6.0, wait_time=0.3)

        self.play(FadeOut(VGroup(blocks, cnn_arrows, tag3)), run_time=0.8)

        # ================================================================
        # PART 4 — Final Pipeline
        # ================================================================
        show_caption(
            "In all these domains, the pipeline is the same: raw data enters, "
            "frequency analysis reveals its structure, and the AI model learns from it.",
            run_time=5.5, wait_time=0.2)

        def pipe_block(label, stroke, fill):
            box = RoundedRectangle(width=2.8, height=1.4, corner_radius=0.2,
                                   stroke_color=stroke, stroke_width=1.8,
                                   fill_color=fill, fill_opacity=0.75)
            txt = Text(label, font_size=19, color=WHITE, line_spacing=1.1,
                       font="DejaVu Sans").move_to(box.get_center())
            return VGroup(box, txt)

        p1 = pipe_block("Raw Data",           GREY_B,  "#1a1a2e").shift(LEFT * 3.8)
        p2 = pipe_block("Frequency\nAnalysis", YELLOW, "#2a1f00")
        p3 = pipe_block("AI Model",           GREEN_B, "#0d2e1a").shift(RIGHT * 3.8)

        pa1 = Arrow(p1.get_right(), p2.get_left(), buff=0.1, color=BLUE_B,
                    stroke_width=2.8, max_tip_length_to_length_ratio=0.18)
        pa2 = Arrow(p2.get_right(), p3.get_left(), buff=0.1, color=BLUE_B,
                    stroke_width=2.8, max_tip_length_to_length_ratio=0.18)

        pipe_group = VGroup(p1, p2, p3, pa1, pa2).move_to(ORIGIN + DOWN * 0.3)

        self.play(LaggedStart(FadeIn(p1, shift=RIGHT * 0.1),
                              GrowArrow(pa1),
                              FadeIn(p2, shift=RIGHT * 0.1),
                              GrowArrow(pa2),
                              FadeIn(p3, shift=RIGHT * 0.1),
                              lag_ratio=0.25), run_time=2.5)
        self.wait(1.0)

        # ================================================================
        # ENDING
        # ================================================================
        remove_caption()

        self.play(FadeOut(VGroup(title, pipe_group), shift=UP * 0.15), run_time=1.0)

        closing = Text(
            "From images to heartbeats to neural networks —\nFourier analysis is everywhere in AI.",
            font_size=30, line_spacing=1.3, color=WHITE,
            font="DejaVu Sans").move_to(ORIGIN)
        self.play(Write(closing), run_time=2.2)
        self.wait(2.2)

        transition = Text("Next: how AI learns directly in the frequency domain.",
                          font_size=28, color=YELLOW,
                          font="DejaVu Sans").move_to(ORIGIN)
        self.play(FadeOut(closing, shift=UP * 0.25))
        self.play(FadeIn(transition, shift=DOWN * 0.15))
        self.wait(2.5)
        self.play(FadeOut(transition))
        self.wait(0.8)