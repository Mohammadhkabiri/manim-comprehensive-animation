from manim import *
import numpy as np

class FourierScene7(Scene):
    def construct(self):
        self.camera.background_color = "#0f1117"

        # =================================================
        # Safe content area
        # =================================================
        SAFE_TOP_Y = 1.75
        SAFE_BOTTOM_Y = -1.45
        SAFE_HEIGHT = SAFE_TOP_Y - SAFE_BOTTOM_Y
        SAFE_CENTER_Y = (SAFE_TOP_Y + SAFE_BOTTOM_Y) / 2
        SAFE_WIDTH = 10.4

        def fit_to_safe_area(mobj, max_width=SAFE_WIDTH, max_height=SAFE_HEIGHT, y_shift=0):
            mobj.scale_to_fit_width(max_width)
            mobj.scale_to_fit_height(max_height)
            mobj.move_to([0, SAFE_CENTER_Y + y_shift, 0])
            return mobj

        # =================================================
        # Subtitle system — same style as Scene 6
        # =================================================
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

        def build_caption(text, font_size=20, max_chars=64):
            words = text.split()
            lines = wrap_words(words, max_chars)
            full_str = "\n".join(lines)

            full_text = Text(
                full_str,
                font_size=font_size,
                color=WHITE,
                line_spacing=1.0,
                font="DejaVu Sans"
            )

            caption_bg = RoundedRectangle(
                corner_radius=0.18,
                height=full_text.height + 0.5,
                width=min(full_text.width + 0.9, 12.8),
                stroke_color=BLUE_D,
                stroke_width=1.4,
                fill_color="#0a0c14",
                fill_opacity=0.82
            )

            accent = RoundedRectangle(
                corner_radius=0.05,
                height=caption_bg.height - 0.22,
                width=0.08,
                fill_color=BLUE_B,
                fill_opacity=0.9,
                stroke_opacity=0
            )

            full_text.move_to(caption_bg.get_center())
            VGroup(caption_bg, full_text).to_edge(DOWN, buff=0.22)
            accent.next_to(caption_bg.get_left(), RIGHT, buff=0.12)

            word_groups, idx = [], 0
            for w in words:
                n = len(w)
                word_groups.append(VGroup(*full_text[idx:idx + n]))
                idx += n

            return caption_bg, accent, full_text, word_groups

        def show_caption(text, run_time=3.8, wait_time=0.25, font_size=20):
            new_bg, new_accent, full_text, word_groups = build_caption(text, font_size)

            if not bg_on[0]:
                self.play(
                    FadeIn(new_bg, shift=UP * 0.18),
                    FadeIn(new_accent, shift=UP * 0.18),
                    run_time=0.5
                )
                cap_bg[0], cap_accent[0], bg_on[0] = new_bg, new_accent, True
            else:
                anims = [
                    Transform(cap_bg[0], new_bg),
                    Transform(cap_accent[0], new_accent)
                ]
                if cap_words[0] is not None:
                    anims.append(FadeOut(cap_words[0], shift=DOWN * 0.08))
                self.play(*anims, run_time=0.5)

            words_vgroup = VGroup(*word_groups)
            if len(word_groups) > 0:
                self.play(
                    LaggedStart(
                        *[FadeIn(g, shift=UP * 0.14) for g in word_groups],
                        lag_ratio=0.38
                    ),
                    run_time=run_time
                )
            cap_words[0] = words_vgroup
            self.wait(wait_time)

        def remove_caption():
            if bg_on[0]:
                anims = [
                    FadeOut(cap_bg[0], shift=DOWN * 0.18),
                    FadeOut(cap_accent[0], shift=DOWN * 0.18)
                ]
                if cap_words[0] is not None:
                    anims.append(FadeOut(cap_words[0], shift=DOWN * 0.1))
                self.play(*anims, run_time=0.5)
                bg_on[0] = False
                cap_bg[0] = None
                cap_accent[0] = None
                cap_words[0] = None

        # =================================================
        # Opening — direct continuity from Scene 6
        # =================================================
        title = Text(
            "From Redshift to Cosmic History",
            font_size=32,
            weight=BOLD,
            color=BLUE_B,
            font="DejaVu Sans"
        )
        subtitle = Text(
            "Measured shifts, velocity, distance, and time",
            font_size=22,
            color=GREY_B,
            font="DejaVu Sans"
        ).next_to(title, DOWN, buff=0.12)

        title_group = VGroup(title, subtitle).to_edge(UP, buff=0.28)

        self.play(FadeIn(title_group, shift=DOWN * 0.2), run_time=1.2)

        show_caption(
            "In the last scene, spectral shifts revealed motion and cosmic expansion. Now we take the next step: we measure those shifts and turn them into physical information.",
            run_time=5.0
        )

        # =================================================
        # Section 1 — Rest vs observed spectrum (Manim-built)
        # =================================================
        sec1_label = Text(
            "1. Measuring the shift",
            font_size=24,
            color=YELLOW,
            font="DejaVu Sans"
        ).move_to([0, 1.45, 0])

        self.play(FadeIn(sec1_label), run_time=0.8)

        x_left = -3.9
        x_right = 4.4

        rest_axis = Line([x_left, 0.65, 0], [x_right, 0.65, 0], color=GREY_B, stroke_width=3)
        obs_axis  = Line([x_left, -0.25, 0], [x_right, -0.25, 0], color=GREY_B, stroke_width=3)

        rest_label = Text("Rest spectrum", font_size=22, color=WHITE, font="DejaVu Sans").next_to(rest_axis, LEFT, buff=0.22)
        obs_label  = Text("Observed spectrum", font_size=22, color=WHITE, font="DejaVu Sans").next_to(obs_axis, LEFT, buff=0.22)

        line_color = BLUE_B
        shifted_color = RED_B

        rest_positions = [-2.8, -0.9, 1.3]
        shift_amount = 0.9
        obs_positions = [x + shift_amount for x in rest_positions]

        rest_lines = VGroup(*[
            Line([x, 0.28, 0], [x, 1.02, 0], color=line_color, stroke_width=6)
            for x in rest_positions
        ])

        obs_lines = VGroup(*[
            Line([x, -0.62, 0], [x, 0.12, 0], color=shifted_color, stroke_width=6)
            for x in obs_positions
        ])
        
        spectrum_group = VGroup(
        rest_axis, obs_axis,
        rest_label, obs_label,
        rest_lines, obs_lines
    )
        spectrum_group.shift(RIGHT * 0.65)


        self.play(
            Create(rest_axis),
            Create(obs_axis),
            FadeIn(rest_label),
            FadeIn(obs_label),
            run_time=1.2
        )
        self.play(LaggedStart(*[GrowFromCenter(l) for l in rest_lines], lag_ratio=0.18), run_time=1.0)
        self.play(LaggedStart(*[GrowFromCenter(l) for l in obs_lines], lag_ratio=0.18), run_time=1.0)

        show_caption(
            "We begin with a reference spectrum and compare it with the spectrum we actually observe. The recognizable lines are still there, but they appear at shifted wavelengths.",
            run_time=5.0
        )

        match_guides = VGroup()
        for xr, xo in zip(rest_positions, obs_positions):
            guide = DashedLine(
                [xr, 0.65, 0],
                [xo, -0.25, 0],
                dash_length=0.1,
                color=GREY_C,
                stroke_width=2
            )
            match_guides.add(guide)
        match_guides.shift(RIGHT * 0.65)
        self.play(Create(match_guides), run_time=1.0)

        delta_arrow = DoubleArrow(
            [rest_positions[1], -1.0, 0],
            [obs_positions[1], -1.0, 0],
            buff=0,
            color=YELLOW,
            stroke_width=6
        )
        delta_text = MathTex(
            r"\Delta \lambda",
            color=YELLOW
        ).scale(0.95).next_to(delta_arrow, DOWN, buff=0.12)
        
        delta_group = VGroup(delta_arrow, delta_text)
        delta_group.shift(RIGHT * 0.65)


        self.play(GrowArrow(delta_arrow), FadeIn(delta_text), run_time=1.0)

        show_caption(
            "That shift can be measured and written as a number: the redshift z.",
            run_time=4.2
        )


        # =================================================
        # Section 2 — Formula for redshift z
        # =================================================
        sec2_label = Text(
            "2. Turning shift into a number",
            font_size=24,
            color=YELLOW,
            font="DejaVu Sans"
        ).move_to([0, 1.68, 0])

        formula_box = RoundedRectangle(
            corner_radius=0.18,
            width=4.3,
            height=1.28,
            stroke_color=BLUE_D,
            stroke_width=1.6,
            fill_color="#10131c",
            fill_opacity=0.88
        ).move_to([0, -0.05, 0]).shift(DOWN * 1.33)

        formula = MathTex(
            r"z = \frac{\lambda_{\mathrm{obs}} - \lambda_{\mathrm{rest}}}{\lambda_{\mathrm{rest}}}",
            color=WHITE
        ).scale(0.80).move_to(formula_box.get_center())

        self.play(
            FadeOut(sec1_label),
            FadeIn(sec2_label),
            FadeOut(match_guides),
            FadeOut(delta_arrow),
            FadeOut(delta_text),
            run_time=0.8
        )

        focus_rect = SurroundingRectangle(obs_lines[1], color=RED_B, buff=0.08)
        self.play(Create(focus_rect), run_time=0.7)
        self.play(FadeOut(focus_rect), run_time=0.4)

        self.play(FadeIn(formula_box), Write(formula), run_time=1.6)
      

        show_caption(
            "Astronomers summarize that measured shift with a dimensionless quantity called redshift.",
            run_time=5.2
        )

        show_caption(
            "For relatively small shifts, redshift can be related to recession velocity. On larger scales, it becomes part of the language of cosmic expansion itself.",
            run_time=5.0
        )

        # =================================================
        # Section 3 — Hubble plot
        # Source: Ley_de_Hubble_(datos_de_1929).svg.png
        # =================================================
        hubble_img = ImageMobject("Distance_v_velocity.svg.png")
        fit_to_safe_area(hubble_img, max_width=9.6, max_height=4.2, y_shift=0.0)

        hubble_frame = RoundedRectangle(
            corner_radius=0.10,
            width=hubble_img.width + 0.14,
            height=hubble_img.height + 0.14,
            stroke_color=GREY_B,
            stroke_width=1.0
        ).move_to(hubble_img)

        sec3_label = Text(
            "3. From single objects to a cosmic pattern",
            font_size=24,
            color=BLUE_B,
            font="DejaVu Sans"
        ).next_to(hubble_img, UP, buff=0.10)

        relation_box = RoundedRectangle(
            corner_radius=0.16,
            width=3.6,
            height=1.18,
            stroke_color=BLUE_D,
            stroke_width=1.6,
            fill_color="#10131c",
            fill_opacity=0.88
        ).to_edge(RIGHT, buff=0.35).shift(UP * 3.35 + RIGHT *0.3)

        relation_text = VGroup(
            Text("more distant galaxies", font_size=14, color=WHITE, font="DejaVu Sans"),
            Text("→ larger recession speeds / redshifts", font_size=16, color=WHITE, font="DejaVu Sans")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to(relation_box.get_center())

        self.play(
            FadeOut(sec2_label),
            FadeOut(rest_axis), FadeOut(obs_axis),
            FadeOut(rest_label), FadeOut(obs_label),
            FadeOut(rest_lines), FadeOut(obs_lines),
            FadeOut(formula_box), FadeOut(formula),
            run_time=0.9
        )

        self.play(
            FadeIn(hubble_img, shift=UP * 0.2),
            Create(hubble_frame),
            FadeIn(sec3_label),
            run_time=1.5
        )

        self.play(FadeIn(relation_box), FadeIn(relation_text), run_time=0.9)

        show_caption(
            "When many galaxies are measured, those individual shifts reveal a larger pattern. The farther a galaxy is, the greater its recession tends to be.",
            run_time=5.0
        )

        show_caption(
            "That is the core idea behind the Hubble relation: redshift is not just a property of one object, but part of a systematic structure across the universe.",
            run_time=5.0
        )

        # =================================================
        # Section 4 — Cosmic history timeline
        # Source: CMB_Timeline300_no_WMAP.jpg
        # =================================================
        timeline_img = ImageMobject("CMB_Timeline300_no_WMAP.jpg")
        fit_to_safe_area(timeline_img, max_width=10.1, max_height=4.45, y_shift=0.0)

        timeline_frame = RoundedRectangle(
            corner_radius=0.10,
            width=timeline_img.width + 0.14,
            height=timeline_img.height + 0.14,
            stroke_color=GREY_B,
            stroke_width=1.0
        ).move_to(timeline_img)

        sec4_label = Text(
            "4. Redshift as a window into cosmic history",
            font_size=24,
            color=BLUE_B,
            font="DejaVu Sans"
        ).next_to(timeline_img, UP, buff=0.08)

        lookback_box = RoundedRectangle(
            corner_radius=0.16,
            width=3.7,
            height=1.2,
            stroke_color=BLUE_D,
            stroke_width=1.7,
            fill_color="#10131c",
            fill_opacity=0.88
        ).to_edge(RIGHT, buff=0.26).shift(UP * 1.32 + RIGHT *0.8)

        lookback_text = VGroup(
            Text("greater distance → older light", font_size=16, color=WHITE, font="DejaVu Sans"),
            Text("greater redshift → deeper look into the past", font_size=16, color=WHITE, font="DejaVu Sans")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to(lookback_box.get_center())

        self.play(
            FadeOut(hubble_img),
            FadeOut(hubble_frame),
            FadeOut(sec3_label),
            FadeOut(relation_box),
            FadeOut(relation_text),
            run_time=0.9
        )

        self.play(
            FadeIn(timeline_img, shift=UP * 0.2),
            Create(timeline_frame),
            FadeIn(sec4_label),
            run_time=1.5
        )

        self.play(FadeIn(lookback_box), FadeIn(lookback_text), run_time=0.9)

        show_caption(
            "At this point, redshift becomes more than a velocity clue. Because light takes time to travel, observing more distant galaxies also means observing older light.",
            run_time=5.3
        )

        show_caption(
            "So larger redshifts do not merely tell us that the universe is expanding. They help place galaxies along the long unfolding history of the cosmos.",
            run_time=5.1
        )

        show_caption(
            "In this way, spectral analysis links a tiny displacement in wavelength to one of the largest stories science can tell: how the universe changes through time.",
            run_time=5.4
        )

        # =================================================
        # Final summary
        # =================================================
        remove_caption()

        summary_box = RoundedRectangle(
            corner_radius=0.18,
            width=9.2,
            height=1.45,
            stroke_color=BLUE_D,
            fill_color="#10131c",
            fill_opacity=0.84
        ).to_edge(DOWN, buff=0.55)

        summary_text = Text(
            "Measure the shift → define redshift z → relate it to distance → read cosmic history",
            font_size=18,
            color=WHITE,
            line_spacing=1.0,
            weight=BOLD,
            font="DejaVu Sans"
        ).move_to(summary_box.get_center())

        self.play(FadeIn(summary_box), Write(summary_text), run_time=1.5)
        self.wait(2.0)

        final_text = Text(
            "Next: how expansion became evidence,\nand how the early universe left a measurable signal.",
            font_size=28,
            color=BLUE_B,
            line_spacing=1.08,
            weight=BOLD,
            font="DejaVu Sans"
        ).move_to(ORIGIN)

        self.play(
            FadeOut(timeline_img),
            FadeOut(timeline_frame),
            FadeOut(sec4_label),
            FadeOut(lookback_box),
            FadeOut(lookback_text),
            FadeOut(summary_box),
            FadeOut(summary_text),
            FadeOut(title_group),
            run_time=1.8
        )

        self.play(FadeIn(final_text, shift=DOWN * 0.2), run_time=1.8)
        self.wait(2.5)
        self.play(FadeOut(final_text), run_time=1.2)
        self.wait(0.5)
