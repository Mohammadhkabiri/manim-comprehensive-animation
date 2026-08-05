from manim import *
import numpy as np

class FourierScene9(Scene):
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
        title = Text("Mel Scale and Mel Filter Banks",
                     font_size=32, weight=BOLD, color=BLUE_B,
                     font="DejaVu Sans").to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.9)

        # ================================================================
        # PART 1 — Linear Frequency Representation
        # ================================================================
        show_caption("Up to this point, we have transformed the audio signal into a time–frequency representation and obtained the spectrogram.", run_time=6.5, wait_time=0.2)
        
        # Linear Axis
        axis_length = 9
        linear_axis = Line(LEFT * (axis_length/2), RIGHT * (axis_length/2), stroke_width=2, color=WHITE)
        linear_axis.shift(UP * 0.5)
        
        linear_ticks = VGroup()
        for i in range(11):
            x_pos = -axis_length/2 + (axis_length/10) * i
            tick = Line(UP * 0.1, DOWN * 0.1, color=WHITE).move_to(RIGHT * x_pos + UP * 0.5)
            linear_ticks.add(tick)

        axis_label = Text("Linear Frequency (Hz)", font_size=20, color=LIGHT_GREY).next_to(linear_axis, DOWN, buff=0.3)
        
        linear_group = VGroup(linear_axis, linear_ticks, axis_label)
        self.play(Create(linear_axis), Create(linear_ticks), FadeIn(axis_label), run_time=2.0)

        show_caption("However, this representation still does not fully match the way humans perceive sound.", run_time=5.0, wait_time=0.2)
        show_caption("The reason is that the human ear does not perceive frequencies linearly.", run_time=5.0, wait_time=0.2)
        show_caption("In lower frequency ranges, we can distinguish differences much more precisely, while in higher frequencies our sensitivity gradually decreases.", run_time=8.0, wait_time=0.2)

        # ================================================================
        # PART 2 — Transformation to Mel Scale
        # ================================================================
        show_caption("To make signal analysis closer to human auditory perception, we convert frequency into a scale called the Mel scale.", run_time=7.5, wait_time=0.2)

        # Mel Axis (Logarithmic spacing simulation)
        mel_ticks = VGroup()
        # Create non-linear points
        mel_points = []
        for i in range(11):
            # mapping 0-10 to a log-like curve
            norm_val = i / 10.0
            log_val = np.log1p(norm_val * 9) / np.log1p(9) # 0 to 1
            x_pos = -axis_length/2 + log_val * axis_length
            mel_points.append(RIGHT * x_pos + UP * 0.5)
            tick = Line(UP * 0.1, DOWN * 0.1, color=YELLOW).move_to(mel_points[-1])
            mel_ticks.add(tick)

        mel_label = Text("Mel Scale (Perceptual)", font_size=20, color=YELLOW).next_to(linear_axis, DOWN, buff=0.3)

        self.play(
            Transform(linear_ticks, mel_ticks),
            Transform(axis_label, mel_label),
            linear_axis.animate.set_color(YELLOW),
            run_time=2.5
        )

        show_caption("This scale is designed so that its behavior better reflects how humans perceive pitch.", run_time=5.5, wait_time=0.2)

        # ================================================================
        # PART 3 — Mel Filter Banks (Triangles)
        # ================================================================
        show_caption("After this conversion, we apply a set of filters along this axis called the Mel filter bank.", run_time=6.0, wait_time=0.2)

        filters = VGroup()
        colors = [RED_A, RED_C, ORANGE, YELLOW, GREEN_C, GREEN_D, TEAL, BLUE_C, PURPLE, MAROON_B]
        
        for i in range(1, len(mel_points)-1):
            left_p = mel_points[i-1]
            center_p = mel_points[i] + UP * 1.5
            right_p = mel_points[i+1]
            
            triangle = Polygon(left_p, center_p, right_p, 
                               stroke_color=colors[i-1], stroke_width=2, 
                               fill_color=colors[i-1], fill_opacity=0.3)
            filters.add(triangle)

        self.play(LaggedStart(*[FadeIn(f, shift=DOWN*0.2) for f in filters], lag_ratio=0.15), run_time=2.5)

        show_caption("Each filter collects the energy of the signal within a specific frequency region.", run_time=5.5, wait_time=0.2)
        
        show_caption("An important property of these filters is that they are closer together in low frequencies and spread farther apart in higher frequencies.", run_time=8.5, wait_time=0.2)

        # Highlight low vs high
        low_brace = Brace(VGroup(filters[0], filters[2]), UP, color=WHITE)
        low_text = low_brace.get_text("Narrow / High Detail").scale(0.6)
        
        high_brace = Brace(VGroup(filters[-3], filters[-1]), UP, color=WHITE)
        high_text = high_brace.get_text("Wide / Low Detail").scale(0.6)

        self.play(GrowFromCenter(low_brace), FadeIn(low_text), run_time=1.0)
        self.play(GrowFromCenter(high_brace), FadeIn(high_text), run_time=1.0)

        # ================================================================
        # PART 4 — Compact Representation
        # ================================================================
        show_caption("In this way, instead of leaving the frequency information in a raw and scattered form, the signal’s spectral information is summarized into several meaningful frequency bands that are well suited for speech analysis.", run_time=11.5, wait_time=0.2)

        self.play(
            FadeOut(low_brace), FadeOut(low_text),
            FadeOut(high_brace), FadeOut(high_text),
            run_time=1.0
        )

        # Transform filters into a compact vector (Mel-Spectrogram frame)
        compact_box = RoundedRectangle(width=6, height=0.6, corner_radius=0.1, color=BLUE_D, fill_color="#181324", fill_opacity=0.8)
        compact_box.move_to(UP * 0.5)
        
        bands = VGroup()
        band_w = 5.8 / len(filters)
        for i, c in enumerate(colors):
            band = Rectangle(width=band_w, height=0.5, color=c, fill_opacity=0.8)
            bands.add(band)
        bands.arrange(RIGHT, buff=0.05).move_to(compact_box.get_center())
        
        compact_label = Text("Compact Perceptual Features", font_size=20, color=WHITE).next_to(compact_box, UP, buff=0.3)

        self.play(
            Transform(filters, bands),
            FadeIn(compact_box),
            FadeOut(linear_axis), FadeOut(linear_ticks), FadeOut(axis_label),
            FadeIn(compact_label, shift=DOWN*0.2),
            run_time=2.5
        )

        show_caption("As a result, the output of this stage becomes a more compact and perceptually meaningful representation of the signal—one that plays a fundamental role in many audio feature extraction methods.", run_time=11.0, wait_time=0.2)

        # ================================================================
        # ENDING
        # ================================================================
        remove_caption()
        
        self.play(
            FadeOut(VGroup(title, filters, compact_box, compact_label), shift=UP * 0.15),
            run_time=1.1
        )

        closing = Text("Next: Mel-Frequency Cepstral Coefficients (MFCC)",
                          font_size=30, color=YELLOW,
                          font="DejaVu Sans").move_to(ORIGIN)
        self.play(FadeIn(closing, shift=DOWN * 0.15))
        self.wait(2.5)
        self.play(FadeOut(closing))
        self.wait(0.8)
