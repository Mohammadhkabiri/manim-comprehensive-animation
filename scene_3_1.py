from manim import *
import numpy as np


class FourierScene6(Scene):
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

        # ---------------------------------------------------------------
        # Helper: simple panel
        # ---------------------------------------------------------------
        def panel(w, h, stroke=BLUE_D, fill="#111522", opacity=0.6):
            return RoundedRectangle(width=w, height=h, corner_radius=0.2,
                                    stroke_color=stroke, stroke_width=1.6,
                                    fill_color=fill, fill_opacity=opacity)

        # ================================================================
        # SECTION TITLE
        # ================================================================
        title = Text("From Human Analysis to Machine Analysis",
                     font_size=34, weight=BOLD, color=BLUE_B,
                     font="DejaVu Sans").to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.9)

        # ================================================================
        # PART 1 — Time-domain signal
        # ================================================================
        show_caption(
            "In the previous section, we saw how humans use the Fourier Transform "
            "to analyze data — for example, identifying cycles and hidden patterns "
            "in financial markets.",
            run_time=5.5, wait_time=0.2)

        # Axes + noisy signal
        axes_t = Axes(
            x_range=[0, 6 * PI, PI], y_range=[-2, 2, 1],
            x_length=9, y_length=3.2,
            axis_config={"color": GREY_B, "stroke_width": 1.4},
        ).shift(DOWN * 0.1)

        x_label = Text("Time", font_size=18, color=GREY_A,
                       font="DejaVu Sans").next_to(axes_t, DOWN, buff=0.18)
        y_label = Text("Signal", font_size=18, color=GREY_A,
                       font="DejaVu Sans").next_to(axes_t, LEFT, buff=0.12)

        np.random.seed(7)
        noise = np.random.normal(0, 0.18, 400)

        def noisy_signal(x):
            idx = int(x / (6 * PI) * 399)
            idx = min(idx, 399)
            return np.sin(x) + 0.5 * np.sin(2.3 * x) + 0.3 * np.sin(4.7 * x) + noise[idx]

        signal_curve = axes_t.plot(noisy_signal, x_range=[0, 6 * PI, 6 * PI / 400],
                                   color=YELLOW, stroke_width=2.2)

        self.play(Create(axes_t), FadeIn(x_label), FadeIn(y_label), run_time=0.9)
        self.play(Create(signal_curve), run_time=2.0)

        show_caption(
            "The main idea is simple: if we can observe the hidden structure of a signal, "
            "understanding its behavior becomes easier.",
            run_time=4.5, wait_time=0.2)

        # Highlight that patterns are hidden
        hidden_label = Text("Hidden patterns?", font_size=22, color=RED_B,
                            font="DejaVu Sans").next_to(axes_t, UP, buff=0.12)
        self.play(FadeIn(hidden_label, shift=DOWN * 0.1), run_time=0.7)

        show_caption(
            "But in real-world situations, data is often larger, more complex, "
            "and noisier than what human analysis alone can handle.",
            run_time=5.0, wait_time=0.2)

        # ================================================================
        # PART 2 — FFT → Frequency Domain
        # ================================================================
        self.play(FadeOut(hidden_label), run_time=0.4)

        transform_arrow = Arrow(LEFT * 0.3, RIGHT * 0.3, color=BLUE_B,
                                stroke_width=3).scale(2).move_to(ORIGIN + DOWN * 0.5)
        transform_label = Text("Fourier Transform", font_size=20, color=BLUE_B,
                               font="DejaVu Sans").next_to(transform_arrow, UP, buff=0.5)

        # Shrink time-domain to left, show arrow, then freq domain on right
        self.play(
            axes_t.animate.scale(0.52).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3),
            signal_curve.animate.scale(0.52).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3),
            x_label.animate.scale(0.52).to_edge(LEFT, buff=0.5).shift(DOWN * 1.1),
            y_label.animate.fade(1),
            run_time=1.2,
        )
        self.play(GrowArrow(transform_arrow), FadeIn(transform_label, shift=UP * 0.05),
                  run_time=0.8)

        show_caption(
            "This is where machine learning enters. The time-domain data is first "
            "transformed into the frequency domain.",
            run_time=4.5, wait_time=0.15)

        # Frequency domain bar chart
        axes_f = Axes(
            x_range=[0, 6, 1], y_range=[0, 1.1, 0.5],
            x_length=4.5, y_length=2.8,
            axis_config={"color": GREY_B, "stroke_width": 1.4},
        ).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.05)

        freq_label = Text("Frequency", font_size=18, color=GREY_A,
                          font="DejaVu Sans").next_to(axes_f, DOWN, buff=0.18)
        amp_label  = Text("Amplitude", font_size=18, color=GREY_A,
                          font="DejaVu Sans").next_to(axes_f, LEFT, buff=0.08)

        # Frequency peaks: (freq, amplitude, color)
        peaks = [(1.0, 1.0, YELLOW), (2.3, 0.55, BLUE_B), (4.7, 0.32, GREEN_B)]
        bars = VGroup()
        for f, a, c in peaks:
            bar = axes_f.get_lines_to_point(axes_f.c2p(f, a))
            dot = Dot(axes_f.c2p(f, a), radius=0.09, color=c)
            stem = Line(axes_f.c2p(f, 0), axes_f.c2p(f, a),
                        color=c, stroke_width=3.5)
            bars.add(VGroup(stem, dot))

        self.play(Create(axes_f), FadeIn(freq_label), FadeIn(amp_label), run_time=0.8)
        self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.3), run_time=1.5)

        show_caption(
            "The frequency spectrum reveals dominant frequencies and the distribution "
            "of energy — features that are invisible in the raw time signal.",
            run_time=5.0, wait_time=0.2)

        # ================================================================
        # PART 3 — Features → ML Model
        # ================================================================
        # Clear middle area and show feature extraction
        self.play(
            FadeOut(VGroup(axes_t, signal_curve, x_label, y_label,
                           transform_arrow, transform_label)),
            run_time=0.8,
        )

        show_caption(
            "If the Fourier Transform helps humans visualize structure, "
            "artificial intelligence can process this on a much larger scale "
            "and discover patterns difficult for human analysts to detect.",
            run_time=6.0, wait_time=0.2)

        # Feature boxes (extracted from spectrum)
        feat_panel = panel(4.8, 2.6, stroke=BLUE_D, fill="#101828", opacity=0.7)
        feat_panel.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        feat_title = Text("Extracted Features", font_size=20, color=BLUE_B,
                          weight=BOLD, font="DejaVu Sans").move_to(
            feat_panel.get_top() + DOWN * 0.3)

        feature_items = VGroup(
            Text("• Dominant frequency: 1.0 Hz", font_size=17, color=YELLOW, font="DejaVu Sans"),
            Text("• Secondary peak:  2.3 Hz",    font_size=17, color=BLUE_B,  font="DejaVu Sans"),
            Text("• Energy ratio (low/high)",     font_size=17, color=GREEN_B, font="DejaVu Sans"),
            Text("• Spectral entropy",            font_size=17, color=GREY_A,  font="DejaVu Sans"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(
            feat_panel.get_center() + DOWN * 0.15)

        feed_arrow = Arrow(feat_panel.get_right(), feat_panel.get_right() + RIGHT * 1.6,
                           color=BLUE_B, stroke_width=2.8,
                           max_tip_length_to_length_ratio=0.18)

        # ML Model block
        ml_panel = panel(3.6, 2.6, stroke=GREEN_D, fill="#0f1f12", opacity=0.72)
        ml_panel.next_to(feed_arrow.get_end(), RIGHT, buff=0.1)
        ml_title = Text("Machine\nLearning Model", font_size=22, color=GREEN_B,
                        weight=BOLD, line_spacing=1.1,
                        font="DejaVu Sans").move_to(ml_panel.get_center())

        # Output arrow + label
        out_arrow = Arrow(ml_panel.get_right(), ml_panel.get_right() + RIGHT * 1.4,
                          color=TEAL_B, stroke_width=2.8,
                          max_tip_length_to_length_ratio=0.18)
        out_label = Text("Prediction /\nDecision", font_size=20, color=TEAL_B,
                         line_spacing=1.1,
                         font="DejaVu Sans").next_to(out_arrow.get_end(), RIGHT, buff=0.1)

        self.play(
            FadeOut(VGroup(axes_f, freq_label, amp_label, bars)),
            run_time=0.6,
        )

        self.play(FadeIn(feat_panel), FadeIn(feat_title), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.12) for f in feature_items],
                              lag_ratio=0.25), run_time=1.8)

        show_caption(
            "These frequency features are then fed into a machine learning model, "
            "which learns patterns from data and makes predictions about system behavior.",
            run_time=5.5, wait_time=0.2)

        self.play(GrowArrow(feed_arrow), run_time=0.7)
        self.play(FadeIn(ml_panel), Write(ml_title), run_time=1.0)
        self.play(GrowArrow(out_arrow), FadeIn(out_label, shift=RIGHT * 0.1), run_time=0.8)

        show_caption(
            "In this process, the Fourier Transform reveals the structure of the data, "
            "while artificial intelligence uses that structure for learning and decision-making.",
            run_time=6.0, wait_time=0.3)

        # ================================================================
        # ENDING
        # ================================================================
        remove_caption()

        self.play(
            FadeOut(VGroup(title, feat_panel, feat_title, feature_items,
                           feed_arrow, ml_panel, ml_title, out_arrow, out_label),
                    shift=UP * 0.15),
            run_time=1.1,
        )

        closing = Text(
            "Fourier Transform: the bridge\nbetween raw data and machine intelligence.",
            font_size=32, line_spacing=1.3, color=WHITE,
            font="DejaVu Sans").move_to(ORIGIN)
        self.play(Write(closing), run_time=2.2)
        self.wait(2.0)

        transition = Text("But how exactly does a machine learn from frequencies?",
                          font_size=30, color=YELLOW,
                          font="DejaVu Sans").move_to(ORIGIN)
        self.play(FadeOut(closing, shift=UP * 0.25))
        self.play(FadeIn(transition, shift=DOWN * 0.15))
        self.wait(2.5)
        self.play(FadeOut(transition))
        self.wait(0.8)