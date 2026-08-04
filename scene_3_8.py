from manim import *
import numpy as np

class FourierScene8(Scene):
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
        title = Text("Spectrogram",
                     font_size=32, weight=BOLD, color=BLUE_B,
                     font="DejaVu Sans").to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.9)

        # ================================================================
        # PART 1 — Arranging Spectra into a 2D Image
        # ================================================================
        show_caption(
            "Now, if we arrange these outputs properly next to each other, we arrive at one of the most "
            "important representations of sound: the spectrogram.",
            run_time=8.0, wait_time=0.2)

        # Create a grid of cells to represent frequency bins over time (Spectrogram)
        rows, cols = 8, 12
        cell_size = 0.28
        grid = VGroup()
        
        # We'll create columns (spectra) first, spread out
        cols_group = VGroup()
        np.random.seed(42)
        
        for c in range(cols):
            col_cells = VGroup()
            for r in range(rows):
                # Calculate color intensity (simulating energy)
                energy = np.random.uniform(0.1, 1.0)
                if r == 2 or r == 5: # Create some "dominant frequency" bands
                    energy = np.random.uniform(0.7, 1.0)
                
                # Dark blue for low energy, Yellow/Red for high energy
                color = interpolate_color(ManimColor("#1b243b"), YELLOW, energy)

                
                cell = Rectangle(height=cell_size, width=cell_size, 
                                 stroke_width=0.5, stroke_color="#0f1117", 
                                 fill_color=color, fill_opacity=0.9)
                col_cells.add(cell)
            col_cells.arrange(UP, buff=0)
            cols_group.add(col_cells)
            
        cols_group.arrange(RIGHT, buff=0.25).scale(0.82).shift(UP * 1.2)

        self.play(FadeIn(cols_group, shift=UP*0.2), run_time=2.0)

        show_caption(
            "A spectrogram is essentially a visual representation of sound.",
            run_time=4.0, wait_time=0.2)

        # Bring columns together to form the image
        self.play(cols_group.animate.arrange(RIGHT, buff=0), run_time=2.0)
        grid_outline = SurroundingRectangle(cols_group, color=BLUE_C, buff=0)
        self.play(Create(grid_outline), run_time=1.0)

        # ================================================================
        # PART 2 — Axes and Color Meaning
        # ================================================================
        show_caption(
            "In this image, the horizontal axis represents time, the vertical axis represents frequency, and "
            "the color intensity or brightness of each point indicates how much energy that frequency has at that particular moment.",
            run_time=11.0, wait_time=0.2)

        # Draw Axes
        x_axis = Arrow(start=cols_group.get_corner(DL) + DOWN*0.2, 
                       end=cols_group.get_corner(DR) + DOWN*0.2 + RIGHT*0.5, 
                       buff=0, color=WHITE)
        y_axis = Arrow(start=cols_group.get_corner(DL) + LEFT*0.2, 
                       end=cols_group.get_corner(UL) + LEFT*0.2 + UP*0.5, 
                       buff=0, color=WHITE)
        
        x_label = Text("Time", font_size=18, color=YELLOW).next_to(x_axis, DOWN, buff=0.1)
        y_label = Text("Frequency", font_size=18, color=YELLOW).next_to(y_axis, LEFT, buff=0.1).rotate(PI/2)

        color_legend = Text("Color Brightness = Energy", font_size=16, color=LIGHT_GREY).next_to(cols_group, UP, buff=0.2)

        self.play(Create(x_axis), Create(y_axis), run_time=1.0)
        self.play(FadeIn(x_label), FadeIn(y_label), FadeIn(color_legend), run_time=1.5)

        # ================================================================
        # PART 3 — Viewing Sound as an Image
        # ================================================================
        show_caption(
            "So instead of only looking at a raw waveform, we can now view sound as an image—an image "
            "where the frequency changes of the signal over time become clearly visible.",
            run_time=9.5, wait_time=0.2)

        # Highlight a specific pattern in the grid
        highlight_box = Rectangle(width=cell_size*4, height=cell_size*2, color=RED, stroke_width=2)
        highlight_box.move_to(cols_group[4][2].get_center() + RIGHT*(cell_size*1.5) + UP*(cell_size*0.5))
        self.play(Create(highlight_box), run_time=1.0)

        show_caption(
            "This is very important, because many audio patterns that are difficult to see in the raw waveform "
            "become much clearer in a spectrogram.",
            run_time=8.5, wait_time=0.2)

        show_caption(
            "For example, different parts of speech, changes in energy, or the presence of dominant "
            "frequencies can be identified much more easily in this representation.",
            run_time=9.0, wait_time=0.2)
            
        self.play(FadeOut(highlight_box))

        # ================================================================
        # PART 4 — The Formula
        # ================================================================
        show_caption(
            "For this reason, the spectrogram is one of the most fundamental representations in speech and audio processing.",
            run_time=7.0, wait_time=0.2)

        remove_caption()

        # Display formula higher so it never touches the subtitle area
        formula = MathTex(r"S(m, k) = \left| X(m, k) \right|^2")
        formula.set_color(WHITE).scale(0.75)
        formula.next_to(cols_group, RIGHT, buff=0.55)
        formula.shift(UP * 0.3)

        self.play(Write(formula), run_time=1.5)


        # ================================================================
        # PART 5 — Connection to AI Models
        # ================================================================
        show_caption(
            "In fact, in many applications, artificial intelligence models do not work directly with the raw "
            "audio signal. Instead, they operate on visual representations like the spectrogram.",
            run_time=10.0, wait_time=0.2)

        # Group everything and move left
        spectrogram_group = VGroup(cols_group, grid_outline, x_axis, y_axis, x_label, y_label, color_legend, formula)
        self.play(spectrogram_group.animate.scale(0.8).to_edge(LEFT, buff=1.0), run_time=1.5)

        # Create AI Box
        ai_box = RoundedRectangle(width=2.5, height=1.5, corner_radius=0.1, stroke_color=PURPLE, fill_color="#181324", fill_opacity=0.8)
        ai_text = Text(
            "AI Model\n(CNN / Transformer)",
            font_size=14,
            color=WHITE,
            font="DejaVu Sans"
        )
        ai_text.move_to(ai_box.get_center())


        ai_group = VGroup(ai_box, ai_text).next_to(spectrogram_group, RIGHT, buff=1.5)
        
        # Arrow to AI
        ai_arrow = Arrow(start=spectrogram_group.get_right(), end=ai_group.get_left(), color=GREEN_C, buff=0.2)

        self.play(Create(ai_arrow), FadeIn(ai_group, shift=LEFT*0.2), run_time=1.5)

        show_caption(
            "So if we consider STFT as the step that extracts time–frequency information, the spectrogram "
            "is the visible and practical representation of that information.",
            run_time=9.0, wait_time=0.2)

        self.play(Indicate(ai_box, color=YELLOW), run_time=1.0)

        # ================================================================
        # ENDING
        # ================================================================
        remove_caption()
        
        self.play(
            FadeOut(VGroup(title, spectrogram_group, ai_arrow, ai_group), shift=UP * 0.15),
            run_time=1.1
        )

        closing = Text("Next: Mel Filterbanks",
                          font_size=30, color=YELLOW,
                          font="DejaVu Sans").move_to(ORIGIN)
        self.play(FadeIn(closing, shift=DOWN * 0.15))
        self.wait(2.5)
        self.play(FadeOut(closing))
        self.wait(0.8)
