from manim import *
import numpy as np

class FourierScene10(Scene):
    def construct(self):
        self.camera.background_color = "#0f1117"

        # ---------------------------------------------------------------
        # Subtitle System (Copied exactly from template)
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
        title = Text("Log Mel Spectrum",
                     font_size=32, weight=BOLD, color=BLUE_B,
                     font="DejaVu Sans").to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.9)

        # ================================================================
        # PART 1 — Linear Energy Representation
        # ================================================================
        show_caption("However, there is still another important property of human perception that we need to consider.", run_time=5.5, wait_time=0.2)
        show_caption("Just as we do not perceive frequency changes linearly, we also do not perceive loudness in a linear way.", run_time=6.5, wait_time=0.2)

        # Display Linear Energy Bars
        np.random.seed(42)
        num_bars = 10
        linear_energies = np.array([0.05, 0.1, 0.8, 2.5, 5.0, 1.2, 0.3, 0.08, 0.02, 0.01])
        
        bars_group = VGroup()
        for i, energy in enumerate(linear_energies):
            bar = Rectangle(width=0.4, height=max(energy, 0.05), fill_color=TEAL, fill_opacity=0.8, stroke_width=0)
            bars_group.add(bar)
        
        bars_group.arrange(RIGHT, aligned_edge=DOWN, buff=0.16)
        bars_group.scale(0.72)
        bars_group.shift(UP * 1.15)

        
        linear_label = Text(
    "Filter Bank Energies (Linear)",
    font_size=20,
    color=LIGHT_GREY,
    font="DejaVu Sans"
).next_to(bars_group, DOWN, buff=0.22)

        
        self.play(FadeIn(bars_group, shift=UP*0.2), FadeIn(linear_label), run_time=2.0)

        show_caption("In simple terms, our ears are very sensitive to changes in quiet sounds, but as sounds become louder, our sensitivity to amplitude changes decreases.", run_time=9.5, wait_time=0.2)

        # ================================================================
        # PART 2 — Logarithmic Curve & Transformation
        # ================================================================
        show_caption("To simulate this characteristic of human hearing in audio processing, we take the logarithm of the filter bank energies.", run_time=7.5, wait_time=0.2)

        # Shift bars to the left to make room
        left_block = VGroup(bars_group, linear_label)
        self.play(
            left_block.animate.scale(0.88).shift(LEFT * 3.2 + UP * 0.45),
            run_time=1.5
        )


        # Show Log Curve
        axes = Axes(
            x_range=[0.1, 6, 1],
            y_range=[-2.5, 2, 1],
            x_length=3.4,
            y_length=2.6,
            axis_config={"color": GREY, "include_ticks": False}
        ).shift(RIGHT * 3.25 + UP * 1.0)

        
        log_curve = axes.plot(lambda x: np.log(x), color=YELLOW)
        curve_label = MathTex(r"y = \log(x)", font_size=24, color=YELLOW).next_to(log_curve, UP, buff=0.2)

        self.play(Create(axes), Create(log_curve), FadeIn(curve_label), run_time=2.0)

        show_caption("This mathematical operation not only makes the representation closer to how we actually perceive loudness, but it also provides an important technical advantage.", run_time=9.0, wait_time=0.2)
        show_caption("In real environments, the strength of a sound can change due to factors such as the distance from the microphone or background noise.", run_time=8.5, wait_time=0.2)
        show_caption("Applying the logarithm helps convert these multiplicative variations in the signal into additive ones, which makes them easier to handle or remove in later analysis.", run_time=9.5, wait_time=0.2)

        # Apply Log to Bars
        log_energies = np.log(linear_energies + 1e-2) # Add small epsilon
        # Normalize for display
        log_energies = (log_energies - np.min(log_energies)) / (np.max(log_energies) - np.min(log_energies)) * 3.0 + 0.5
        
        log_bars = VGroup()
        for i, energy in enumerate(log_energies):
            bar = Rectangle(width=0.4, height=energy, fill_color=ORANGE, fill_opacity=0.8, stroke_width=0)
            log_bars.add(bar)
        log_bars.arrange(RIGHT, aligned_edge=DOWN, buff=0.2).move_to(bars_group.get_center())

        log_label_text = Text("Log Energies", font_size=20, color=ORANGE).next_to(log_bars, DOWN, buff=0.4)

        formula = MathTex(
            r"S_{\log}(m, i) = \log(E_m(i))",
            font_size=28,
            color=WHITE
        ).next_to(axes, DOWN, buff=0.3)
        formula.shift(UP * 0.45)


        self.play(
            Transform(bars_group, log_bars),
            Transform(linear_label, log_label_text),
            FadeIn(formula, shift=UP*0.2),
            run_time=2.5
        )

        # ================================================================
        # PART 3 — The Log-Mel Spectrogram Concept
        # ================================================================
        show_caption("The output of this stage is called the Log-Mel Spectrum, or a Mel-scaled spectrogram with logarithmic amplitude.", run_time=7.5, wait_time=0.2)
        show_caption("This representation provides a robust and informative description of the audio structure.", run_time=6.0, wait_time=0.2)
        
        # Clean up to show a single robust representation block
        self.play(
            FadeOut(axes), FadeOut(log_curve), FadeOut(curve_label),
            FadeOut(formula), FadeOut(bars_group), FadeOut(linear_label),
            run_time=1.0
        )

        # Simple grid representing Log-Mel Spectrogram
        grid = VGroup()
        for r in range(5):
            row = VGroup()
            for c in range(12):
                val = np.random.uniform(0.2, 1.0)
                square = Square(side_length=0.4).set_fill(color=interpolate_color(DARK_BLUE, ORANGE, val), opacity=1).set_stroke(width=0.5, color=BLACK)
                row.add(square)
            row.arrange(RIGHT, buff=0)
            grid.add(row)
        grid.arrange(DOWN, buff=0).move_to(ORIGIN)
        
        spec_label = Text("Log-Mel Spectrogram", font_size=24, color=WHITE).next_to(grid, UP, buff=0.3)

        self.play(FadeIn(grid, shift=UP*0.2), FadeIn(spec_label), run_time=2.0)

        show_caption("In fact, many modern models in speech and audio processing use this logarithmic representation directly as input features.", run_time=8.5, wait_time=0.2)

        # ================================================================
        # ENDING
        # ================================================================
        remove_caption()
        
        self.play(
            FadeOut(VGroup(title, grid, spec_label), shift=UP * 0.15),
            run_time=1.1
        )

        closing = Text("Next: Discrete Cosine Transform (DCT) & MFCC",
                          font_size=30, color=YELLOW,
                          font="DejaVu Sans").move_to(ORIGIN)
        self.play(FadeIn(closing, shift=DOWN * 0.15))
        self.wait(2.5)
        self.play(FadeOut(closing))
        self.wait(0.8)
