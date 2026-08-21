from manim import *

class LTCMAndMarketScene(Scene):
    def construct(self):
        # ==========================================
        # Theme Setup
        # ==========================================
        self.camera.background_color = "#0f1117"

        # --- Helper functions for subtitles (adjust to your existing system) ---
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
        # PART 1 — Centered Text (Math vs Market)
        # ================================================================
        text_math_power = MarkupText(
            "If mathematics is this powerful, does that mean all\n"
            "mathematicians were successful in the market?\n\n"
            "<span foreground='#FF4444'>No.</span>\n\n"
            "That is because the financial market is a\n"
            "non-stationary system.",
            font_size=36,
            justify=True,
            color=WHITE
        )

        
        self.play(Write(text_math_power), run_time=4)
        self.wait(3)
        self.play(FadeOut(text_math_power))

        # ================================================================
        # PART 2 — Video Placeholder Frame
        # ================================================================
        video_box = RoundedRectangle(width=8, height=4.5, corner_radius=0.2, stroke_color=BLUE, stroke_width=4, fill_color=WHITE, fill_opacity=0.05)
        video_placeholder_text = Text("Insert 22s Video Here", font_size=36, color=GRAY).move_to(video_box.get_center())
        video_credit = Text("MIT finance Lecture, professor Andrew Lo", font_size=24, color=WHITE).next_to(video_box, DOWN, buff=0.5)
        
        video_group = VGroup(video_box, video_placeholder_text, video_credit)

        self.play(FadeIn(video_group, shift=UP*0.3))
        self.wait(4) # You will replace this wait time in video editor with the 22s clip
        self.play(FadeOut(video_group))

        # ================================================================
        # PART 3 — Physics vs Market (Subtitle)
        # ================================================================
        show_caption("So In physics, the laws do not change; but in the market, human behavior constantly changes the rules.", run_time=4)

        # ================================================================
        # PART 4 — LTCM Chart Reconstruction
        # ================================================================
        show_caption("A famous example of this is the LTCM fund.", run_time=2)

        # Setup Axes
        chart_axes = Axes(
            x_range=[0, 15, 1],
            y_range=[0, 5.5, 1],
            x_length=9,
            y_length=5,
            axis_config={"color": GRAY, "include_numbers": False},
            y_axis_config={"numbers_to_include": [1, 2, 3, 4, 5]}
        ).move_to(UP * 0.5)

        # Custom Y-axis labels (US$1b, etc.)
        y_labels = chart_axes.get_y_axis().numbers
        for num, val in zip(y_labels, [1, 2, 3, 4, 5]):
            label = Text(f"US${val}b", font_size=20, color=WHITE).next_to(num, LEFT, buff=0.2)
            chart_axes.add(label)
            chart_axes.get_y_axis().remove(num) # Replace default numbers

        # Chart Title
        chart_title = Text(
    "Long-Term Capital Management\n- value over time -",
    font_size=32,
    color=WHITE
).next_to(chart_axes, UP, buff=0.01)


        # Data Points (Approximate from the image)
        x_vals = list(range(16))
        # Treasury Bonds (Red) - steady slow growth
        bonds_y = [1.0, 1.02, 1.04, 1.06, 1.08, 1.10, 1.12, 1.14, 1.16, 1.18, 1.20, 1.22, 1.24, 1.26, 1.28, 1.30]
        # DJI (Green) - volatile steady growth
        dji_y = [1.0, 1.05, 0.98, 1.15, 1.25, 1.45, 1.50, 1.65, 1.85, 1.80, 2.20, 2.05, 2.40, 2.45, 2.15, 2.35]
        # LTCM (Blue) - exponential growth then crash
        ltcm_y = [1.0, 1.15, 1.18, 1.40, 1.65, 2.05, 2.65, 2.90, 3.25, 3.50, 3.75, 3.95, 4.05, 4.25, 1.10, 0.90]

        line_bonds = chart_axes.plot_line_graph(x_values=x_vals, y_values=bonds_y, line_color=RED, add_vertex_dots=False)
        line_dji = chart_axes.plot_line_graph(x_values=x_vals, y_values=dji_y, line_color=GREEN, add_vertex_dots=False)
        line_ltcm = chart_axes.plot_line_graph(x_values=x_vals, y_values=ltcm_y, line_color=BLUE, add_vertex_dots=False)
        line_ltcm["line_graph"].set_stroke(width=5) # Make LTCM thicker

        # Legend
        legend_ltcm = VGroup(Line(LEFT, RIGHT, color=BLUE, stroke_width=5), Text("LTCM", font_size=20)).arrange(RIGHT)
        legend_dji = VGroup(Line(LEFT, RIGHT, color=GREEN, stroke_width=4), Text("DJI", font_size=20)).arrange(RIGHT)
        legend_bonds = VGroup(Line(LEFT, RIGHT, color=RED, stroke_width=4), Text("US Treasury Bonds", font_size=20)).arrange(RIGHT)
        legend = VGroup(legend_ltcm, legend_dji, legend_bonds).arrange(DOWN, aligned_edge=LEFT).next_to(chart_axes, RIGHT, buff=0.5)

        chart_group = VGroup(chart_title, chart_axes, legend)

        # Draw Chart
        self.play(FadeIn(chart_group))
        self.play(Create(line_bonds), Create(line_dji), run_time=2)
        self.play(Create(line_ltcm), run_time=3)
        
        show_caption("A fund that was managed by a team of outstanding mathematicians, and even by Scholes and Merton themselves.", run_time=4)
        show_caption("The models looked excellent on paper, but when the market regime changed during the financial crisis...", run_time=4)
        
        # Highlight Crash
        crash_circle = Circle(radius=0.8, color=RED).move_to(chart_axes.c2p(14, 1))
        self.play(Create(crash_circle))
        
        show_caption("...the assumptions of the model no longer held, and the fund faced a severe loss.", run_time=4)

        remove_caption()
        self.play(FadeOut(chart_group), FadeOut(line_bonds), FadeOut(line_dji), FadeOut(line_ltcm), FadeOut(crash_circle))

        # ================================================================
        # PART 5 — Centered Text (Conclusion)
        # ================================================================
        text_conclusion = MarkupText(
            "This reminds us that mathematics is a powerful tool\n"
            "for modeling uncertainty, <span foreground='#FF4444'>not</span> a tool for making\n"
            "certain predictions about the future.",
            font_size=36,
            justify=True,
            color=WHITE
        )

        
        self.play(Write(text_conclusion), run_time=4)
        self.wait(3)
        self.play(FadeOut(text_conclusion))

        # ================================================================
        # PART 6 — Centered Text (The Question)
        text_question = MarkupText(
            "Now the question is this:\n\n"
            "If a purely mathematical model can fail in the market,\n"
            "then what is the solution?",
            font_size=36,
            justify=True,
            color=WHITE
        )

        
        self.play(Write(text_question), run_time=4)
        self.wait(3)
        self.play(FadeOut(text_question))
