from manim import *
import numpy as np

class FourierScene7(Scene):
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
        title = Text("Short-Time Fourier Transform (STFT)",
                     font_size=32, weight=BOLD, color=BLUE_B,
                     font="DejaVu Sans").to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.9)

        # ================================================================
        # PART 1 — Audio Frames Sequence
        # ================================================================
        show_caption(
            "Up to this point, we have divided the audio signal into short frames, and we have also prepared "
            "each frame for analysis using a window. Now we can perform the main step of extracting frequency information.",
            run_time=8.5, wait_time=0.2)

        # Create 3 stylized windowed frames
        frames = VGroup()
        for i in range(3):
            box = RoundedRectangle(width=1.8, height=1.2, corner_radius=0.15, stroke_color=BLUE_D, fill_color="#111522", fill_opacity=0.6)
            # A simple windowed sine wave for visualization inside the box
            wave = FunctionGraph(lambda x: 0.4 * np.sin((5 + i) * x) * np.exp(-(x**2)), x_range=[-1, 1], color=GREEN_C)
            wave.move_to(box.get_center())
            frames.add(VGroup(box, wave))
        
        frames.arrange(RIGHT, buff=0.6).shift(UP * 1.2)
        frames_label = Text("Windowed Frames (Time)", font_size=18, color=LIGHT_GREY).next_to(frames, UP, buff=0.2)
        
        self.play(FadeIn(frames_label), LaggedStart(*[FadeIn(f, shift=UP*0.1) for f in frames], lag_ratio=0.2), run_time=2.0)

        # ================================================================
        # PART 2 — Applying Fourier Transform to one frame
        # ================================================================
        show_caption(
            "What we do here is compute a Fourier Transform for each short frame of the signal.",
            run_time=4.0, wait_time=0.2)

        # Highlight first frame
        self.play(frames[0][0].animate.set_stroke(color=YELLOW, width=3))

        show_caption(
            "In other words, instead of transforming the entire audio signal into the frequency domain at once, "
            "we perform this operation separately for each frame.",
            run_time=7.5, wait_time=0.2)

        # ================================================================
        # PART 3 — Displaying Spectra
        # ================================================================
        show_caption(
            "As a result, for every frame of the signal we obtain a frequency spectrum. This spectrum shows "
            "which frequencies are present in that short time interval and how much energy each of them has.",
            run_time=8.5, wait_time=0.2)

        # Create spectra and arrows
        arrows = VGroup()
        spectra = VGroup()
        
        for i in range(3):
            arrow = Arrow(start=frames[i].get_bottom(), end=frames[i].get_bottom() + DOWN*1.0, 
                          color=WHITE, buff=0.1, max_tip_length_to_length_ratio=0.15)
            arrows.add(arrow)
            
            # Simple spectrum (Axes + Peak)
            ax = Axes(x_range=[0, 3], y_range=[0, 2], x_length=1.6, y_length=1.0, 
                      axis_config={"include_tip": False, "color": GREY_B}).next_to(arrow, DOWN, buff=0.1)
            # Different peak position for each frame to simulate change
            peak_x = 1.0 + i*0.5 
            peak = ax.plot(lambda x: 1.5 * np.exp(-30 * (x - peak_x)**2), color=YELLOW)
            spectra.add(VGroup(ax, peak))

        # Show first arrow and spectrum
        ft_label = Text("FFT", font_size=16, color=BLUE_B).next_to(arrows[0], RIGHT, buff=0.1)
        self.play(GrowArrow(arrows[0]), FadeIn(ft_label), Create(spectra[0]), run_time=1.5)

        show_caption(
            "If we compute these spectra for all the frames of the signal, we will obtain a collection of "
            "frequency spectra, each corresponding to a short moment in the sound.",
            run_time=7.5, wait_time=0.2)

        # Show remaining arrows and spectra quickly
        self.play(frames[0][0].animate.set_stroke(color=BLUE_D, width=2), FadeOut(ft_label))
        self.play(LaggedStart(
            AnimationGroup(GrowArrow(arrows[1]), Create(spectra[1])),
            AnimationGroup(GrowArrow(arrows[2]), Create(spectra[2])),
            lag_ratio=0.4
        ), run_time=2.0)

        show_caption(
            "Placing these spectra next to one another allows us to observe how the structure of the sound changes over time.",
            run_time=6.0, wait_time=0.2)

        # ================================================================
        # PART 4 — Time-Frequency Representation & Formula
        # ================================================================
        show_caption(
            "This process—where the Fourier Transform is calculated for short segments of a signal—is "
            "called the Short-Time Fourier Transform, or STFT.",
            run_time=7.5, wait_time=0.2)

        # Morph individual spectra into a Spectrogram Block to save space
        spectrogram_box = RoundedRectangle(width=3.2, height=1.5, corner_radius=0.1, stroke_color=BLUE_C, fill_color="#182035", fill_opacity=0.8)
        spectrogram_box.next_to(frames, DOWN, buff=0.45).shift(LEFT * 1.35+ UP * 0.15)
        
        # Fake grid inside spectrogram
        grid_lines = VGroup()
        for x in np.linspace(-1.45, 1.45, 7):
            grid_lines.add(Line(spectrogram_box.get_bottom() + RIGHT*x, spectrogram_box.get_top() + RIGHT*x, color=GREY_D, stroke_opacity=0.3))
        spectrogram = VGroup(spectrogram_box, grid_lines)
        
        spec_label_time = Text("Time →", font_size=13, color=GREY_A).next_to(spectrogram_box, DOWN, buff=0.04)
        spec_label_freq = Text("Freq ↑", font_size=13, color=GREY_A).next_to(spectrogram_box, LEFT, buff=0.08).rotate(PI/2)
        
        stft_title = Text("STFT (Time-Frequency Representation)", font_size=12, color=YELLOW).next_to(spectrogram_box, UP, buff=0.03)

        self.play(
            FadeOut(arrows),
            Transform(spectra, spectrogram),
            FadeIn(spec_label_time), FadeIn(spec_label_freq), FadeIn(stft_title),
            run_time=2.0
        )

        remove_caption()

        formula = MathTex(
            r"X(m, k) = \sum_{n=0}^{N-1} x[n] w[n - mH] e^{-j \frac{2\pi k n}{N}}"
        )
        formula.set_color(WHITE).scale(0.43).next_to(spectrogram_box, RIGHT, buff=0.45)
        formula.shift(UP * 0.05)


        self.play(Write(formula), run_time=2.0)

        
        self.play(Write(formula), run_time=2.0)

        # ================================================================
        # PART 5 — Explaining the Two Dimensions
        # ================================================================
        show_caption(
            "In simple terms, STFT allows us to analyze a signal simultaneously in two dimensions: "
            "We can see which frequencies exist in the sound, and we can also see when those frequencies appear or change over time.",
            run_time=11.0, wait_time=0.2)

        self.play(Indicate(spec_label_freq, color=YELLOW), run_time=1.0)
        self.play(Indicate(spec_label_time, color=YELLOW), run_time=1.0)

        show_caption(
            "For this reason, STFT is one of the most important tools in audio signal processing. Many "
            "techniques used in speech analysis, sound recognition, and even music analysis are built upon this time–frequency representation.",
            run_time=10.5, wait_time=0.2)

        self.play(spectrogram_box.animate.set_stroke(color=YELLOW, width=4), run_time=1.0)
        self.play(spectrogram_box.animate.set_stroke(color=BLUE_C, width=2), run_time=1.0)

        show_caption(
            "From this point on, we are no longer working with just a simple waveform in time. Instead, we "
            "work with a representation that shows how the frequency structure of the sound evolves over time.",
            run_time=9.5, wait_time=0.2)

        # Final visual wrap-up
        self.play(frames.animate.set_opacity(0.3), frames_label.animate.set_opacity(0.3))
        self.play(Indicate(stft_title, color=GREEN))

        # ================================================================
        # ENDING
        # ================================================================
        remove_caption()
        
        self.play(
            FadeOut(VGroup(title, frames, frames_label, spectra, spectrogram, spec_label_time, spec_label_freq, stft_title, formula), shift=UP * 0.15),
            run_time=1.1
        )

        closing = Text("Next: Spectrogram (Visualization)",
                          font_size=30, color=YELLOW,
                          font="DejaVu Sans").move_to(ORIGIN)
        self.play(FadeIn(closing, shift=DOWN * 0.15))
        self.wait(2.5)
        self.play(FadeOut(closing))
        self.wait(0.8)
