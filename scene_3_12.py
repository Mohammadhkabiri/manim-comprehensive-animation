from manim import *
import numpy as np

class FourierScene12(Scene):
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
        title = Text("Text-to-Speech (TTS)",
                     font_size=32, weight=BOLD, color=BLUE_B,
                     font="DejaVu Sans").to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.9)

        # ================================================================
        # PART 1 — Intro & Text
        # ================================================================
        show_caption("So far, we have mostly discussed analyzing audio signals—that is, how to extract linguistic information from an input sound.", run_time=6.0, wait_time=0.2)
        show_caption("In text-to-speech, however, the process works in the opposite direction.", run_time=4.5, wait_time=0.2)

        text_input = Text('"Hello World"', font_size=36, color=WHITE).move_to(UP * 1.5)
        text_label = Text("Text Input", font_size=20, color=LIGHT_GREY).next_to(text_input, UP, buff=0.2)
        text_group = VGroup(text_input, text_label)

        self.play(FadeIn(text_group, shift=UP * 0.2), run_time=1.0)
        show_caption("Instead of starting with sound, we provide the system with written text, and the goal is to generate a natural-sounding audio signal from it.", run_time=8.5, wait_time=0.2)

        # ================================================================
        # PART 2 — Phonemes
        # ================================================================
        show_caption("In the first step, the input text is analyzed to determine its linguistic structure.", run_time=6.0, wait_time=0.2)

        # Move text_group to the left first, then build phoneme group at fixed position
        self.play(text_group.animate.move_to(LEFT * 4.5 + UP * 1.5), run_time=1.0)

        phonemes = Text("/h/ /e/ /l/ /ou/", font_size=32, color=YELLOW).move_to(UP * 1.5)
        phoneme_label = Text("Phonemes", font_size=20, color=YELLOW).next_to(phonemes, UP, buff=0.2)
        phoneme_group = VGroup(phonemes, phoneme_label)

        arrow_to_phonemes = Arrow(
            start=text_group.get_right(),
            end=phoneme_group.get_left(),
            buff=0.3, color=WHITE
        )

        self.play(FadeIn(arrow_to_phonemes), FadeIn(phoneme_group, shift=LEFT * 0.2), run_time=1.0)
        show_caption("For example, the system needs to determine how words should be pronounced and convert them into smaller phonetic units called phonemes.", run_time=8.0, wait_time=0.2)

        # ================================================================
        # PART 3 — ML Model & Spectrogram
        # ================================================================
        # Place ML Model to the RIGHT of phoneme_group at a fixed position
        model_box = RoundedRectangle(
            width=2.5, height=1.5, corner_radius=0.15,
            fill_color=PURPLE, fill_opacity=0.3, stroke_color=PURPLE
        )
        model_text = Text("ML Model", font_size=24, weight=BOLD, color=WHITE).move_to(model_box.get_center())
        model_group = VGroup(model_box, model_text).move_to(RIGHT * 2.5 + UP * 1.5)

        # Build spectrogram at fixed position to the right of model_group
        np.random.seed(42)
        spectrogram = VGroup()
        for r in range(4):
            row = VGroup()
            for c in range(8):
                val = np.random.uniform(0.1, 0.9)
                square = Square(side_length=0.25).set_fill(
                    color=interpolate_color(DARK_BLUE, ORANGE, val), opacity=1
                ).set_stroke(width=0.5, color=BLACK)
                row.add(square)
            row.arrange(RIGHT, buff=0)
            spectrogram.add(row)
        spectrogram.arrange(DOWN, buff=0).move_to(RIGHT * 5.5 + UP * 1.5)
        spec_label = Text("Spectral Representation", font_size=18, color=WHITE).next_to(spectrogram, DOWN, buff=0.2)
        spec_group = VGroup(spectrogram, spec_label)

        # Arrows using fixed positions
        arrow_to_model = Arrow(
            start=phoneme_group.get_right(),
            end=model_group.get_left(),
            buff=0.3, color=WHITE
        )
        arrow_to_spec = Arrow(
            start=model_group.get_right(),
            end=spec_group.get_left(),
            buff=0.3, color=WHITE
        )

        self.play(
            FadeOut(text_group),
            FadeOut(arrow_to_phonemes),
            phoneme_group.animate.move_to(LEFT * 2.5 + UP * 1.5),
            run_time=1.0
        )

        # Rebuild arrow after phoneme_group has moved
        arrow_to_model2 = Arrow(
            start=LEFT * 2.5 + UP * 1.5 + RIGHT * 1.4,
            end=RIGHT * 2.5 + UP * 1.5 + LEFT * 1.25,
            buff=0.0, color=WHITE
        )

        self.play(
            FadeIn(model_group, shift=LEFT * 0.2),
            FadeIn(arrow_to_model2),
            run_time=1.0
        )

        show_caption("After this step, a machine learning model predicts what the corresponding speech should sound like from an acoustic perspective.", run_time=8.0, wait_time=0.2)

        self.play(FadeIn(arrow_to_spec), FadeIn(spec_group, shift=LEFT * 0.2), run_time=1.0)

        show_caption("The output of this stage is usually a spectral representation of speech—a representation that is structurally very similar to a Mel spectrogram.", run_time=9.0, wait_time=0.2)
        show_caption("However, this representation is not yet actual sound.", run_time=4.0, wait_time=0.2)
        show_caption("At this point we only have a frequency-based description of speech, not the real waveform.", run_time=6.5, wait_time=0.2)

        # ================================================================
        # PART 4 — Vocoder & Waveform
        # ================================================================
        self.play(
            FadeOut(phoneme_group),
            FadeOut(arrow_to_model2),
            FadeOut(model_group),
            FadeOut(arrow_to_spec),
            spec_group.animate.move_to(LEFT * 4.5 + UP * 1.5),
            run_time=1.5
        )

        vocoder_box = RoundedRectangle(
            width=2.5, height=1.5, corner_radius=0.15,
            fill_color=TEAL, fill_opacity=0.3, stroke_color=TEAL
        )
        vocoder_text = Text("Vocoder", font_size=24, weight=BOLD, color=WHITE).move_to(vocoder_box.get_center())
        vocoder_sub = Text("(Inverse STFT)", font_size=16, color=LIGHT_GREY).next_to(vocoder_text, DOWN, buff=0.1)
        vocoder_group = VGroup(vocoder_box, vocoder_text, vocoder_sub).move_to(UP * 1.5)

        arrow_to_vocoder = Arrow(
            start=spec_group.get_right(),
            end=vocoder_group.get_left(),
            buff=0.3, color=WHITE
        )

        # Waveform axes placed to the right of vocoder_group
        axes = Axes(
            x_range=[0, 4, 1], y_range=[-1.5, 1.5, 1],
            x_length=3.5, y_length=1.5
        ).move_to(RIGHT * 4.5 + UP * 1.5)
        wave = axes.plot(
            lambda x: np.sin(4 * x) * np.exp(-0.2 * x) + 0.3 * np.sin(10 * x),
            color=GREEN_C
        )
        wave_label = Text("Audio Waveform", font_size=18, color=GREEN_C).next_to(axes, DOWN, buff=0.2)
        waveform_group = VGroup(axes, wave, wave_label)

        arrow_to_wave = Arrow(
            start=vocoder_group.get_right(),
            end=waveform_group.get_left(),
            buff=0.3, color=WHITE
        )

        self.play(FadeIn(arrow_to_vocoder), FadeIn(vocoder_group, shift=LEFT * 0.2), run_time=1.0)

        show_caption("To convert this spectral representation into an actual audio signal, a component called a vocoder is used.", run_time=7.5, wait_time=0.2)
        show_caption("The role of the vocoder is to reconstruct a time-domain waveform from the spectral information.", run_time=7.0, wait_time=0.2)

        self.play(FadeIn(arrow_to_wave), Create(axes), Create(wave), FadeIn(wave_label), run_time=1.5)

        show_caption("In many approaches, this reconstruction relies on spectral processing methods, and techniques such as the Inverse Fourier Transform or Inverse STFT are used to convert the frequency information back into a time-domain signal.", run_time=12.5, wait_time=0.2)
        show_caption("So if in speech analysis we transformed sound from the time domain into the frequency domain, in text-to-speech we first generate a suitable frequency representation, and then reconstruct it into a listenable audio waveform.", run_time=12.0, wait_time=0.2)
        show_caption("In this way, modern Text-to-Speech systems can take a simple piece of text and generate speech that is continuous, intelligible, and increasingly close to natural human speech.", run_time=11.0, wait_time=0.2)

        # ================================================================
        # ENDING
        # ================================================================
        remove_caption()

        self.play(
            FadeOut(VGroup(title, spec_group, arrow_to_vocoder, vocoder_group,
                           arrow_to_wave, waveform_group), shift=UP * 0.15),
            run_time=1.1
        )

        closing = Text("Next: Conclusion",
                       font_size=30, color=YELLOW,
                       font="DejaVu Sans").move_to(ORIGIN)
        self.play(FadeIn(closing, shift=DOWN * 0.15))
        self.wait(2.5)
        self.play(FadeOut(closing))
        self.wait(0.8)