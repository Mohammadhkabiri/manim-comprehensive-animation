from manim import *
import numpy as np

class FourierScene11(Scene):
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
        title = Text("Using Audio Features in Machine Learning",
                     font_size=32, weight=BOLD, color=BLUE_B,
                     font="DejaVu Sans").to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.9)

        # ================================================================
        # PART 1 — The Log-Mel Spectrogram Representation
        # ================================================================
        show_caption("Up to this point, the raw audio signal has gone through several processing stages and has been transformed into a set of features.", run_time=7.0, wait_time=0.2)
        
        # Simple Spectrogram Grid
        np.random.seed(42)
        spectrogram = VGroup()
        for r in range(4):
            row = VGroup()
            for c in range(10):
                val = np.random.uniform(0.1, 0.9)
                square = Square(side_length=0.35).set_fill(color=interpolate_color(DARK_BLUE, ORANGE, val), opacity=1).set_stroke(width=0.5, color=BLACK)
                row.add(square)
            row.arrange(RIGHT, buff=0)
            spectrogram.add(row)
        spectrogram.arrange(DOWN, buff=0).shift(UP * 1.5)
        
        spec_label = Text("Log-Mel Spectrogram", font_size=20, color=WHITE).next_to(spectrogram, DOWN, buff=0.2)
        spec_group = VGroup(spectrogram, spec_label)

        self.play(FadeIn(spec_group, shift=UP*0.2), run_time=1.5)

        show_caption("These features are commonly represented as a Log-Mel Spectrogram—a representation in which the horizontal axis corresponds to time, the vertical axis represents frequency bands on the Mel scale, and each cell indicates the energy intensity of the signal.", run_time=12.0, wait_time=0.2)
        show_caption("This time–frequency representation serves as the main input for many machine learning models used in audio analysis.", run_time=8.0, wait_time=0.2)

        # ================================================================
        # PART 2 — Training Phase & Labeled Data
        # ================================================================
        show_caption("During the training phase, the model is presented with a collection of labeled data. Each example consists of an audio signal converted into a Log-Mel Spectrogram along with a corresponding label.", run_time=10.0, wait_time=0.2)

        # Move spectrogram left and add Label box
        label_box = RoundedRectangle(width=2.5, height=1.0, corner_radius=0.1, fill_color=TEAL, fill_opacity=0.3, stroke_color=TEAL)
        label_text = Text('Label: "Hello"', font_size=22, color=WHITE).move_to(label_box.get_center())
        label_group = VGroup(label_box, label_text)

        self.play(
            spec_group.animate.shift(LEFT * 3),
            run_time=1.0
        )
        
        plus_sign = Text("+", font_size=36, color=WHITE).move_to(UP * 1.5)
        label_group.move_to(UP * 1.5 + RIGHT * 3)

        self.play(FadeIn(plus_sign), FadeIn(label_group, shift=LEFT*0.2), run_time=1.5)

        show_caption("This label might represent a spoken word, the identity of a speaker, or a type of sound.", run_time=6.5, wait_time=0.2)
        show_caption("By observing a large number of these examples, the model gradually learns the statistical patterns that exist in the data.", run_time=8.0, wait_time=0.2)

        # ================================================================
        # PART 3 — CNN Model
        # ================================================================
        show_caption("One commonly used model for this task is the Convolutional Neural Network (CNN).", run_time=6.0, wait_time=0.2)
        
        # Transform setup to show Model
        model_box = RoundedRectangle(width=3.5, height=2.0, corner_radius=0.2, fill_color=PURPLE, fill_opacity=0.3, stroke_color=PURPLE)
        model_text = Text("CNN Model", font_size=28, weight=BOLD, color=WHITE).move_to(model_box.get_center())
        model_group = VGroup(model_box, model_text).move_to(UP * 1.5)

        arrow_in = Arrow(start=LEFT*3, end=model_box.get_left(), buff=0.2, color=WHITE)
        
        self.play(
            FadeOut(plus_sign), FadeOut(label_group),
            spec_group.animate.scale(0.7).move_to(UP * 1.5 + LEFT * 4.5),
            FadeIn(model_box), FadeIn(model_text), FadeIn(arrow_in),
            run_time=2.0
        )

        show_caption("Since the Log-Mel Spectrogram has a structure similar to an image, convolutional layers can detect local patterns in small time–frequency regions and transform them into higher-level features.", run_time=11.0, wait_time=0.2)

        # ================================================================
        # PART 4 — Backpropagation / Error Calculation
        # ================================================================
        show_caption("During training, the model’s prediction is compared with the correct label. The error is calculated, and the weights of the network are adjusted so that the model’s accuracy improves over time.", run_time=11.0, wait_time=0.2)

        pred_box = Rectangle(width=2.5, height=0.8, fill_color=DARK_GRAY, fill_opacity=0.8, stroke_color=LIGHT_GREY).next_to(model_box, RIGHT, buff=1.0)
        pred_text = Text("Prediction", font_size=20, color=WHITE).move_to(pred_box.get_center())
        pred_group = VGroup(pred_box, pred_text)
        
        arrow_out = Arrow(start=model_box.get_right(), end=pred_box.get_left(), buff=0.2, color=WHITE)
        
        # Error / Update arrow
        update_arrow = CurvedArrow(start_point=pred_box.get_bottom(), end_point=model_box.get_bottom(), angle=PI/3, color=RED)
        update_text = Text("Update Weights", font_size=16, color=RED).next_to(update_arrow, DOWN, buff=0.1)

        self.play(FadeIn(pred_group), FadeIn(arrow_out), run_time=1.0)
        self.play(Create(update_arrow), FadeIn(update_text), run_time=1.5)

        # ================================================================
        # PART 5 — Inference / Final Decision
        # ================================================================
        show_caption("After training is complete, the model can analyze a new audio input.", run_time=5.5, wait_time=0.2)
        
        # Clean up training elements
        self.play(FadeOut(update_arrow), FadeOut(update_text), run_time=0.8)
        
        # Change label to indicate "New Input" and "Trained Model"
        new_spec_label = Text("New Input", font_size=18, color=YELLOW).move_to(spec_label.get_center())
        trained_model_text = Text("Trained Model", font_size=28, weight=BOLD, color=GREEN_C).move_to(model_text.get_center())
        final_decision_text = Text("Final Decision", font_size=20, color=GREEN_C).move_to(pred_text.get_center())

        self.play(
            Transform(spec_label, new_spec_label),
            Transform(model_text, trained_model_text),
            model_box.animate.set_fill(GREEN_E, opacity=0.3).set_stroke(GREEN_C),
            Transform(pred_text, final_decision_text),
            run_time=1.5
        )

        show_caption("In this stage, the time–frequency structure of the input is compared with the patterns the model learned during training, and based on this similarity, the input is assigned to the most appropriate category.", run_time=12.0, wait_time=0.2)
        show_caption("In this way, the machine learning model acts as a bridge between the extracted audio features and the final decision of the system.", run_time=9.0, wait_time=0.2)

        # ================================================================
        # ENDING
        # ================================================================
        remove_caption()
        
        self.play(
            FadeOut(VGroup(title, spec_group, spec_label, arrow_in, model_box, model_text, arrow_out, pred_box, pred_text), shift=UP * 0.15),
            run_time=1.1
        )

        closing = Text("Next: Summary / Conclusion",
                          font_size=30, color=YELLOW,
                          font="DejaVu Sans").move_to(ORIGIN)
        self.play(FadeIn(closing, shift=DOWN * 0.15))
        self.wait(2.5)
        self.play(FadeOut(closing))
        self.wait(0.8)
