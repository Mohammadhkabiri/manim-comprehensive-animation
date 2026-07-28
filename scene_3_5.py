from manim import *
import numpy as np


class FourierScene5(Scene):
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
        title = Text("Audio Signal Segmentation (Framing)",
                     font_size=32, weight=BOLD, color=BLUE_B,
                     font="DejaVu Sans").to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.9)

        # ================================================================
        # PART 1 — The Long Audio Waveform
        # ================================================================
        show_caption(
            "So, let’s answer this question first: Can we analyze the entire audio file all at once?",
            run_time=4.5, wait_time=0.2)

        # Long axes for the entire signal
        axes_full = Axes(
            x_range=[0, 12, 2], y_range=[-2.5, 2.5, 1],
            x_length=10.0, y_length=2.5,
            axis_config={"color": GREY_B, "stroke_width": 1.4, "include_numbers": False},
        ).shift(UP * 0.5)
        
        # A varying waveform to represent speech
        def speech_wave(x):
            # Combines different frequencies at different times
            part1 = np.sin(3*x) * np.exp(-0.2*(x-2)**2)
            part2 = 0.8 * np.sin(8*x) * np.exp(-0.3*(x-6)**2)
            part3 = 0.6 * np.sin(1.5*x) * np.cos(5*x) * np.exp(-0.1*(x-10)**2)
            return part1 + part2 + part3 + 0.1 * np.random.normal() * np.sin(10*x)

        wave_curve = axes_full.plot(speech_wave, x_range=[0, 12, 0.05], color=YELLOW, stroke_width=2.5)
        
        self.play(Create(axes_full), run_time=1.0)
        self.play(Create(wave_curve), run_time=2.0)

        show_caption(
            "In most cases, the answer is no. The reason is that sound—especially human speech—"
            "constantly changes over time.",
            run_time=6.0, wait_time=0.2)

        show_caption(
            "Each letter or short portion of a word can have a different frequency structure.",
            run_time=5.0, wait_time=0.2)

        # ================================================================
        # PART 2 — Problem of Global Analysis
        # ================================================================
        cross = Cross(scale_factor=0.8, stroke_width=8, stroke_color=RED).move_to(axes_full.get_center())
        
        show_caption(
            "If we analyze the entire signal at once, these temporal changes become mixed together, "
            "and it becomes unclear which features belong to which moment in the sound.",
            run_time=7.5, wait_time=0.2)
        
        self.play(FadeIn(cross, scale=0.5))
        self.wait(1.0)
        self.play(FadeOut(cross))

        # ================================================================
        # PART 3 — Framing / Segmentation
        # ================================================================
        show_caption(
            "To solve this problem, we divide the audio signal into short time intervals. "
            "This process is called segmentation, or framing.",
            run_time=6.0, wait_time=0.2)

        # Add slicing lines and non-overlapping frames
        frame_width = 1.5 # visual width of a frame
        slices = VGroup()
        frames_non_overlap = VGroup()
        
        for x in np.arange(0, 12, frame_width):
            p1 = axes_full.c2p(x, -2.5)
            p2 = axes_full.c2p(x, 2.5)
            line = DashedLine(p1, p2, color=GREY_C, dash_length=0.1)
            slices.add(line)
            
            if x + frame_width <= 12:
                # Add a slightly transparent block for the frame
                p_center = axes_full.c2p(x + frame_width/2, 0)
                frame_rect = Rectangle(width=axes_full.x_length * (frame_width/12), height=2.5, 
                                       fill_color=TEAL, fill_opacity=0.2, stroke_color=TEAL, stroke_width=1)
                frame_rect.move_to(p_center)
                frames_non_overlap.add(frame_rect)

        self.play(LaggedStart(*[Create(line) for line in slices], lag_ratio=0.1), run_time=1.5)
        self.play(FadeIn(frames_non_overlap), run_time=1.0)

        # ================================================================
        # PART 4 — 20 to 30 ms Label
        # ================================================================
        show_caption(
            "In practice, the signal is divided into frames with a length of about 20 to 30 milliseconds.",
            run_time=5.0, wait_time=0.2)

        # Highlight one frame and label it
        target_frame = frames_non_overlap[3]
        brace = Brace(target_frame, DOWN, buff=0.1)
        brace_text = brace.get_text("20 - 30 ms").set_color(YELLOW).scale(0.7)
        
        self.play(GrowFromCenter(brace), FadeIn(brace_text, shift=UP*0.1))

        show_caption(
            "Within such a short interval, we can assume that the signal’s behavior is relatively stable, "
            "which makes frequency analysis more meaningful.",
            run_time=6.5, wait_time=0.2)

        # ================================================================
        # PART 5 — Overlapping Frames
        # ================================================================
        show_caption(
            "Another important point is that these frames usually overlap slightly so that "
            "transitions in the sound are captured more smoothly.",
            run_time=6.5, wait_time=0.2)

        # Show overlapping frames (staggered visually to show overlap without making it messy)
        self.play(FadeOut(slices), FadeOut(brace), FadeOut(brace_text), FadeOut(frames_non_overlap))
        
        frames_overlap = VGroup()
        step = frame_width * 0.5 # 50% overlap
        
        for i, x in enumerate(np.arange(0, 12 - frame_width + 0.1, step)):
            p_center = axes_full.c2p(x + frame_width/2, 0)
            rect = Rectangle(width=axes_full.x_length * (frame_width/12), height=2.5, 
                             fill_color=BLUE_E, fill_opacity=0.3, stroke_color=BLUE_B, stroke_width=1.5)
            # Offset every other frame slightly up/down to show the overlap clearly
            offset = UP * 0.15 if i % 2 == 0 else DOWN * 0.15
            rect.move_to(p_center).shift(offset)
            frames_overlap.add(rect)

        self.play(LaggedStart(*[FadeIn(f, scale=0.9) for f in frames_overlap], lag_ratio=0.1), run_time=2.5)

        # ================================================================
        # PART 6 — Sequence of Frames
        # ================================================================
        show_caption(
            "As a result, the long signal is converted into a sequence of short frames, "
            "each of which can be analyzed separately.",
            run_time=6.0, wait_time=0.2)

        # Animate frames moving down to form a sequence
        sequence_group = frames_overlap.copy()
        # Scale down and arrange in a row below the axes
        sequence_group.generate_target()
        sequence_group.target.arrange(RIGHT, buff=0.1).scale(0.4).shift(DOWN * 1.5)
        
        # Remove offset from target
        for r in sequence_group.target:
            r.set_y(sequence_group.target.get_y())

        self.play(MoveToTarget(sequence_group), run_time=2.0)
        
        arrow = Arrow(axes_full.get_bottom() + DOWN*0.2, sequence_group.get_top() + UP*0.2, color=WHITE)
        self.play(GrowArrow(arrow))

        # ================================================================
        # ENDING
        # ================================================================
        remove_caption()
        
        self.play(
            FadeOut(VGroup(title, axes_full, wave_curve, frames_overlap, sequence_group, arrow), shift=UP * 0.15),
            run_time=1.1
        )

        closing = Text("Next: Windowing (Hamming / Hann)",
                          font_size=30, color=YELLOW,
                          font="DejaVu Sans").move_to(ORIGIN)
        self.play(FadeIn(closing, shift=DOWN * 0.15))
        self.wait(2.5)
        self.play(FadeOut(closing))
        self.wait(0.8)
