from manim import *
import numpy as np


class FourierScene4(Scene):
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
        title = Text("Why Audio Needs Frequency Analysis",
                     font_size=32, weight=BOLD, color=BLUE_B,
                     font="DejaVu Sans").to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.9)

        # ================================================================
        # PART 1 — Time Domain & Digital Signal
        # ================================================================
        show_caption(
            "When we store an audio file on a computer, we actually represent it as a digital signal—"
            "a sequence of samples recorded over time.",
            run_time=6.0, wait_time=0.2)
        
        # Time Domain Axes
        axes_time = Axes(
            x_range=[0, 10, 2], y_range=[-2.5, 2.5, 1],
            x_length=8.0, y_length=3.0,
            axis_config={"color": GREY_B, "stroke_width": 1.4},
        ).shift(UP * 0.5)
        
        t_label = Text("Time Domain", font_size=20, color=YELLOW).next_to(axes_time, UP, buff=0.2)

        # Complex sound waveform
        def sound_wave(x):
            return np.sin(x) + 0.5 * np.sin(3*x) + 0.3 * np.cos(7*x)
        
        wave_curve = axes_time.plot(sound_wave, x_range=[0, 10, 0.05], color=YELLOW, stroke_width=2.5)
        
        # Show discrete samples
        samples = VGroup(*[
            Dot(axes_time.c2p(x, sound_wave(x)), radius=0.04, color=WHITE)
            for x in np.arange(0, 10, 0.25)
        ])

        self.play(Create(axes_time), FadeIn(t_label), run_time=1.0)
        self.play(Create(wave_curve), run_time=1.5)
        self.play(FadeIn(samples), run_time=1.0)

        show_caption(
            "If we plot this signal, what we see is a waveform along the time axis.",
            run_time=3.5, wait_time=0.2)
        
        # ================================================================
        # PART 2 — Limitations of Time Domain
        # ================================================================
        show_caption(
            "However, if we only look at this time-domain graph, understanding the true "
            "structure of the sound is not very easy.",
            run_time=5.0, wait_time=0.2)
        
        question_mark = Text("?", font_size=60, color=RED, weight=BOLD).move_to(axes_time.get_center())
        self.play(FadeIn(question_mark, shift=UP*0.2))

        show_caption(
            "In this plot, we only see amplitude changes, but it’s not clear what components "
            "the sound is made of or what distinguishes it from other sounds.",
            run_time=6.5, wait_time=0.2)

        # ================================================================
        # PART 3 — Frequencies carry the information
        # ================================================================
        self.play(FadeOut(question_mark))
        
        # Shrink and move time domain left
        time_group = VGroup(axes_time, t_label, wave_curve, samples)
        self.play(time_group.animate.scale(0.6).to_edge(LEFT, buff=0.5).shift(DOWN*0.5), run_time=1.0)

        show_caption(
            "A significant portion of the information in a sound actually lies in its frequencies.",
            run_time=4.0, wait_time=0.2)

        # Frequency Domain Axes
        axes_freq = Axes(
            x_range=[0, 10, 2], y_range=[0, 1.5, 0.5],
            x_length=5.0, y_length=2.5,
            axis_config={"color": GREY_B, "stroke_width": 1.4},
        ).to_edge(RIGHT, buff=0.5).shift(UP * 0.2)
        
        f_label = Text("Frequency Domain", font_size=18, color=GREEN_C).next_to(axes_freq, UP, buff=0.2)

        # Transformation Arrow
        transform_arrow = Arrow(time_group.get_right() + RIGHT*0.2, axes_freq.get_left() + LEFT*0.2, 
                                color=BLUE, stroke_width=3)
        transform_text = Text("Fourier Transform", font_size=16, color=BLUE).next_to(transform_arrow, UP, buff=0.1)

        self.play(GrowArrow(transform_arrow), FadeIn(transform_text, shift=UP*0.1), run_time=1.0)
        self.play(Create(axes_freq), FadeIn(f_label), run_time=1.0)

        show_caption(
            "Every sound is a combination of multiple frequency components.",
            run_time=3.5, wait_time=0.2)
        
        # Draw peaks representing the components: sin(x), 0.5*sin(3x), 0.3*cos(7x)
        peaks = [
            (1.0, 1.0, YELLOW),
            (3.0, 0.5, TEAL),
            (7.0, 0.3, BLUE_C)
        ]
        stems = VGroup()
        for x, y, c in peaks:
            line = Line(axes_freq.c2p(x, 0), axes_freq.c2p(x, y), color=c, stroke_width=4)
            dot = Dot(axes_freq.c2p(x, y), color=c, radius=0.06)
            stems.add(VGroup(line, dot))

        self.play(LaggedStart(*[GrowFromEdge(stem, DOWN) for stem in stems], lag_ratio=0.3), run_time=1.5)

        show_caption(
            "The difference between various sounds—such as two spoken letters or two musical "
            "instruments—is mainly reflected in this frequency pattern.",
            run_time=6.5, wait_time=0.2)

        # ================================================================
        # PART 4 — Transforming to Frequency Domain
        # ================================================================
        show_caption(
            "That’s why in audio processing, we usually transform the signal from the time domain "
            "to the frequency domain.",
            run_time=5.0, wait_time=0.2)
        
        show_caption(
            "This allows us to see which frequencies are present in the sound and how much energy each one carries.",
            run_time=5.0, wait_time=0.2)

        # ================================================================
        # PART 5 — Time-varying nature of sound
        # ================================================================
        self.play(FadeOut(VGroup(time_group, transform_arrow, transform_text, axes_freq, f_label, stems)), run_time=1.0)

        show_caption(
            "Of course, sound is a time-varying signal. This means the frequencies present at one moment "
            "may change just a few milliseconds later.",
            run_time=6.5, wait_time=0.2)

        # Simple Spectrogram-like Representation (Grid)
        spec_panel = panel(6.0, 3.0, stroke=PURPLE_D, fill="#120c18", opacity=0.8)
        spec_title = Text("Time + Frequency (Spectrogram)", font_size=20, color=PURPLE_B).move_to(spec_panel.get_top() + DOWN*0.4)
        
        # Grid blocks to simulate changing frequencies over time
        blocks = VGroup()
        for t_idx in range(6):
            for f_idx in range(4):
                # Random opacity to look like varying energy
                opac = np.random.uniform(0.1, 0.9)
                block = Rectangle(width=0.7, height=0.4, fill_color=TEAL, fill_opacity=opac, stroke_width=1, stroke_color=GREY_E)
                block.move_to(spec_panel.get_bottom() + UP*0.6 + UP*f_idx*0.45 + LEFT*2.0 + RIGHT*t_idx*0.8)
                blocks.add(block)

        self.play(FadeIn(spec_panel), FadeIn(spec_title), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(b) for b in blocks], lag_ratio=0.05), run_time=2.0)

        show_caption(
            "Therefore, to analyze sound properly, we need a method that can also take these "
            "temporal changes into account.",
            run_time=5.5, wait_time=0.2)

        # ================================================================
        # ENDING
        # ================================================================
        remove_caption()
        
        self.play(
            FadeOut(VGroup(title, spec_panel, spec_title, blocks), shift=UP * 0.15),
            run_time=1.1
        )

        closing = Text("Next: Short-Time Fourier Transform (STFT)",
                          font_size=30, color=YELLOW,
                          font="DejaVu Sans").move_to(ORIGIN)
        self.play(FadeIn(closing, shift=DOWN * 0.15))
        self.wait(2.5)
        self.play(FadeOut(closing))
        self.wait(0.8)
