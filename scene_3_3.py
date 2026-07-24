from manim import *
import numpy as np


class FourierScene3(Scene):
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
        title = Text("Why Audio Processing Is Especially Important",
                     font_size=32, weight=BOLD, color=BLUE_B,
                     font="DejaVu Sans").to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.9)

        # ================================================================
        # PART 1 — Microphone & Sound
        # ================================================================
        show_caption(
            "Among all the applications we mentioned, there is one field where frequency "
            "analysis plays an even more fundamental role.",
            run_time=4.5, wait_time=0.2)
        
        show_caption("That field is audio processing.", run_time=2.0, wait_time=0.3)

        # Simple Microphone shape
        mic_head = Ellipse(width=0.6, height=1.2, fill_color=GREY_C, fill_opacity=1, stroke_width=0)
        mic_body = ArcBetweenPoints(mic_head.get_left() + DOWN*0.2 + LEFT*0.1, 
                                    mic_head.get_right() + DOWN*0.2 + RIGHT*0.1, 
                                    angle=-PI, color=WHITE, stroke_width=4)
        mic_stand = Line(mic_body.get_bottom(), mic_body.get_bottom() + DOWN*0.6, stroke_width=4)
        mic_base = Line(mic_stand.get_bottom() + LEFT*0.4, mic_stand.get_bottom() + RIGHT*0.4, stroke_width=4)
        microphone = VGroup(mic_head, mic_body, mic_stand, mic_base).shift(LEFT * 3)

        # Sound waves
        waves = VGroup(*[
            Arc(radius=r, angle=PI/2, color=BLUE_A, stroke_width=3).rotate(-PI/4).next_to(microphone, RIGHT, buff=0.2 + r*0.5)
            for r in [0.5, 1.0, 1.5]
        ])

        self.play(FadeIn(microphone, shift=UP*0.2), run_time=1)
        self.play(LaggedStart(*[Create(w) for w in waves], lag_ratio=0.4), run_time=1.5)

        # Applications
        show_caption(
            "Today, many artificial intelligence systems can hear human speech, recognize "
            "spoken language, and even interact with people in natural conversations.",
            run_time=5.5, wait_time=0.2)

        app_panel1 = panel(3.5, 1.0, stroke=TEAL_D, fill="#102020", opacity=0.8).shift(RIGHT * 2.5 + UP * 0.8)
        app_text1 = Text("Voice Assistants", font_size=20, color=TEAL_B, font="DejaVu Sans").move_to(app_panel1)
        
        app_panel2 = panel(3.5, 1.0, stroke=GREEN_D, fill="#102010", opacity=0.8).shift(RIGHT * 2.5 + DOWN * 0.8)
        app_text2 = Text("Speech-to-Text", font_size=20, color=GREEN_B, font="DejaVu Sans").move_to(app_panel2)

        self.play(FadeIn(app_panel1), FadeIn(app_text1), shift=LEFT*0.2, run_time=1)
        self.play(FadeIn(app_panel2), FadeIn(app_text2), shift=LEFT*0.2, run_time=1)

        show_caption(
            "Voice assistants, speech-to-text systems, and many modern interactive tools "
            "are all built on audio processing technologies. The Fourier Transform plays an essential role.",
            run_time=6.5, wait_time=0.2)

        # ================================================================
        # PART 2 — Raw Waveform vs Computer
        # ================================================================
        self.play(FadeOut(VGroup(microphone, waves, app_panel1, app_text1, app_panel2, app_text2)), run_time=0.8)

        show_caption(
            "However, for a machine, sound is not the same as the human listening experience.",
            run_time=4.0, wait_time=0.2)

        # Axes + noisy signal (Raw Waveform)
        axes_t = Axes(
            x_range=[0, 4*PI, PI], y_range=[-2, 2, 1],
            x_length=5.5, y_length=2.5,
            axis_config={"color": GREY_B, "stroke_width": 1.4},
        ).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        
        y_label = Text("Raw Audio", font_size=18, color=YELLOW, font="DejaVu Sans").next_to(axes_t, UP, buff=0.1)

        np.random.seed(42)
        def raw_audio(x):
            return np.sin(2*x) * np.exp(-0.1*x) + 0.5 * np.sin(5*x) + np.random.normal(0, 0.1)
        
        signal_curve = axes_t.plot(raw_audio, x_range=[0, 4*PI, 4*PI/200], color=YELLOW, stroke_width=2.0)

        # Computer Box
        pc_panel = panel(3.0, 2.5, stroke=RED_D, fill="#201010", opacity=0.8).to_edge(RIGHT, buff=1.0).shift(DOWN*0.2)
        pc_text = Text("Computer / AI", font_size=22, color=RED_B, weight=BOLD, font="DejaVu Sans").move_to(pc_panel)
        
        question_marks = Text("???", font_size=40, color=RED_A, weight=BOLD, font="DejaVu Sans").next_to(pc_text, UP, buff=0.2)

        self.play(Create(axes_t), FadeIn(y_label), Create(signal_curve), run_time=1.5)
        
        show_caption(
            "A computer does not naturally understand speech or sound in its raw waveform format.",
            run_time=4.0, wait_time=0.2)
        
        self.play(FadeIn(pc_panel), FadeIn(pc_text), run_time=0.8)
        self.play(FadeIn(question_marks, shift=UP*0.2), run_time=0.8)

        # ================================================================
        # PART 3 — Mathematical Transformation Pipeline
        # ================================================================
        show_caption(
            "Instead, we must apply a series of mathematical operations that transform the raw "
            "audio signal into structured representations.",
            run_time=6.0, wait_time=0.2)

        # Replace PC with Math Arrow and Spectrogram (Structured representation)
        self.play(FadeOut(VGroup(pc_panel, pc_text, question_marks)), run_time=0.6)

        math_arrow = Arrow(axes_t.get_right() + RIGHT*0.2, axes_t.get_right() + RIGHT*2.0, color=BLUE_B, stroke_width=3)
        math_text = Text("Math / Fourier", font_size=18, color=BLUE_B, font="DejaVu Sans").next_to(math_arrow, UP, buff=0.1)

        # Structured Representation (Simple Grid/Spectrogram)
        struct_panel = panel(3.5, 2.5, stroke=TEAL_D, fill="#102020", opacity=0.8).next_to(math_arrow, RIGHT, buff=0.2)
        struct_label = Text(
            "Structured\nRepresentation",
            font_size=18,
            color=TEAL_B,
            font="DejaVu Sans"
        ).move_to(struct_panel.get_top() + DOWN * 0.4)

        
        # Draw some colored bars inside to look like frequency features
        bars = VGroup(*[
            Rectangle(width=0.3, height=np.random.uniform(0.3, 1.2), fill_color=c, fill_opacity=0.8, stroke_width=0)
            for c in [BLUE, TEAL, GREEN, YELLOW, RED]
        ]).arrange(RIGHT, aligned_edge=DOWN, buff=0.15).next_to(struct_label, DOWN, buff=0.3)

        self.play(GrowArrow(math_arrow), FadeIn(math_text, shift=UP*0.1), run_time=0.8)
        self.play(FadeIn(struct_panel), FadeIn(struct_label), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), run_time=1.5)

        show_caption(
            "Only after this transformation can machine learning algorithms analyze the signal "
            "and extract its true meaning.",
            run_time=5.5, wait_time=0.2)

        # ================================================================
        # PART 4 — ML Extraction
        # ================================================================
        self.play(
            FadeOut(VGroup(axes_t, y_label, signal_curve, math_arrow, math_text)),
            VGroup(struct_panel, struct_label, bars).animate.to_edge(LEFT, buff=1.0),
            run_time=1.0
        )

        ml_arrow = Arrow(struct_panel.get_right() + RIGHT*0.2, struct_panel.get_right() + RIGHT*1.8, color=GREEN_B, stroke_width=3)
        
        ml_panel = panel(3.5, 2.5, stroke=GREEN_D, fill="#0f1f12", opacity=0.8).next_to(ml_arrow, RIGHT, buff=0.2)
        ml_title = Text(
    "Machine Learning\nAnalysis",
    font_size=20,
    color=GREEN_B,
    weight=BOLD,
    font="DejaVu Sans"
).move_to(ml_panel)


        self.play(GrowArrow(ml_arrow), run_time=0.6)
        self.play(FadeIn(ml_panel), FadeIn(ml_title), run_time=1.0)
        
        self.wait(2.0)

        # ================================================================
        # ENDING
        # ================================================================
        remove_caption()
        
        self.play(
            FadeOut(VGroup(title, struct_panel, struct_label, bars, ml_arrow, ml_panel, ml_title), shift=UP * 0.15),
            run_time=1.1
        )

        closing = Text("Next: How do we actually separate these frequencies?",
                          font_size=30, color=YELLOW,
                          font="DejaVu Sans").move_to(ORIGIN)
        self.play(FadeIn(closing, shift=DOWN * 0.15))
        self.wait(2.5)
        self.play(FadeOut(closing))
        self.wait(0.8)
