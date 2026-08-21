from manim import *
import numpy as np

class FourierScene6(Scene):
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
        # Subtitle system — same style as Scene 5
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

        def show_caption(text, run_time=3.5, wait_time=0.25, font_size=20):
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
        # Title
        # =================================================
        title = Text(
            "Spectral Shifts and Cosmic Motion",
            font_size=32,
            weight=BOLD,
            color=BLUE_B
        )
        subtitle = Text(
            "From moving stars to the expanding universe",
            font_size=22,
            color=GREY_B
        ).next_to(title, DOWN, buff=0.12)

        title_group = VGroup(title, subtitle).to_edge(UP, buff=0.28)

        self.play(FadeIn(title_group, shift=DOWN * 0.2), run_time=1.2)

        show_caption(
            "In the last scene, we saw that spectral lines can shift toward red or toward blue. Now we ask the next question: what does that shift actually mean?",
            run_time=5.0
        )

        # =================================================
        # Section 1 — Review of redshift / blueshift
        # =================================================
        shift_img = ImageMobject("Rednadblueshift.png")
        # shift_img.set_stroke(width=0)
        fit_to_safe_area(shift_img, max_width=9.6, max_height=3.8, y_shift=0.0)

        shift_frame = RoundedRectangle(
            corner_radius=0.10,
            width=shift_img.width + 0.14,
            height=shift_img.height + 0.14,
            stroke_color=GREY_B,
            stroke_width=1.0
        ).move_to(shift_img)

        section_label = Text(
            "Same pattern, different position",
            font_size=24,
            color=YELLOW
        ).next_to(shift_img, UP, buff=0.10)

        self.play(
            FadeIn(shift_img, shift=UP * 0.2),
            Create(shift_frame),
            FadeIn(section_label),
            run_time=1.5
        )

        show_caption(
            "The key idea is not the color by itself, but the displacement of the same pattern. The lines stay recognizable, yet the whole pattern slides left or right.",
            run_time=5.0
        )

        red_box = SurroundingRectangle(shift_img, color=RED_B, buff=0.08)
        self.play(Create(red_box), run_time=0.8)
        self.play(FadeOut(red_box), run_time=0.5)

        show_caption(
            "When the pattern shifts toward longer wavelengths, we call it redshift. When it shifts toward shorter wavelengths, we call it blueshift.",
            run_time=4.8
        )

        # =================================================
        # Section 2 — Motion interpretation
        # =================================================
        away_label = Text("moving away", font_size=22, color=RED_B, weight=BOLD).move_to(LEFT * 4.2 + UP *0.1)
        toward_label = Text("moving closer", font_size=22, color=BLUE_B, weight=BOLD).move_to(RIGHT * 4.2 + UP * 0.1)

        away_arrow = Arrow(
            start=LEFT * 2 + DOWN * 0.3,
            end=LEFT * 3.5 + DOWN * 0.3,
            buff=0,
            color=RED_B,
            stroke_width=8
        )
        toward_arrow = Arrow(
            start=RIGHT * 2 + DOWN * 0.3,
            end=RIGHT * 3.5 + DOWN * 0.3,
            buff=0,
            color=BLUE_B,
            stroke_width=8
        )

        motion_hint = RoundedRectangle(
            corner_radius=0.16,
            width=3.3,
            height=1.0,
            stroke_color=BLUE_D,
            stroke_width=1.5,
            fill_color="#10131c",
            fill_opacity=0.88
        ).to_edge(RIGHT, buff=0.6).shift(UP * 1.4)

        motion_text = VGroup(
            Text("Redshift  → receding source", font_size=16, color=WHITE),
            Text("Blueshift → approaching source", font_size=16, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(motion_hint.get_center())

        self.play(
            GrowArrow(away_arrow),
            FadeIn(away_label),
            GrowArrow(toward_arrow),
            FadeIn(toward_label),
            FadeIn(motion_hint),
            FadeIn(motion_text),
            run_time=1.5
        )

        show_caption(
            "This is the Doppler idea expressed in light. Redshift suggests the source is receding from us, while blueshift suggests it is approaching us.",
            run_time=5.0
        )

        # =================================================
        # Section 3 — Host star / exoplanet image
        # =================================================
        star_img = ImageMobject("1.jpg")
        fit_to_safe_area(star_img, max_width=8.8, max_height=4.3, y_shift=0.05)

        star_frame = RoundedRectangle(
            corner_radius=0.10,
            width=star_img.width + 0.14,
            height=star_img.height + 0.14,
            stroke_color=GREY_B,
            stroke_width=1.0
        ).move_to(star_img)

        star_title = Text(
            "A moving star changes the light we receive",
            font_size=24,
            color=YELLOW
        ).next_to(star_img, UP, buff=0.08)

        self.play(
            FadeOut(shift_img),
            FadeOut(shift_frame),
            FadeOut(section_label),
            FadeOut(away_arrow),
            FadeOut(away_label),
            FadeOut(toward_arrow),
            FadeOut(toward_label),
            FadeOut(motion_hint),
            FadeOut(motion_text),
            run_time=0.8
        )

        self.play(
            FadeIn(star_img, shift=UP * 0.2),
            Create(star_frame),
            FadeIn(star_title),
            run_time=1.5
        )

        show_caption(
            "Here the idea becomes physical. If a star moves slightly toward us or away from us, the light arriving at Earth is shifted accordingly.",
            run_time=5.0
        )

        show_caption(
            "That means motion can be inferred from light alone. We may never touch the star, yet its spectrum still reveals how it moves along our line of sight.",
            run_time=5.2
        )

        radial_box = RoundedRectangle(
            corner_radius=0.16,
            width=3.6,
            height=0.9,
            stroke_color=BLUE_D,
            stroke_width=1.6,
            fill_color="#111622",
            fill_opacity=0.88
        ).to_edge(LEFT, buff=0.60).shift(UP * 1.45 + LEFT * 0.1)

        radial_text = Text(
            "What we measure is radial motion",
            font_size=17,
            color=WHITE
        ).move_to(radial_box.get_center())

        self.play(FadeIn(radial_box), FadeIn(radial_text), run_time=0.9)

        show_caption(
            "More precisely, spectral shift tells us about motion toward us or away from us. It is especially sensitive to radial velocity.",
            run_time=5.1
        )

        # =================================================
        # Section 4 — Distant galaxies and expansion
        # =================================================
        galaxy_img = ImageMobject("4.png")
        fit_to_safe_area(galaxy_img, max_width=10.0, max_height=4.2, y_shift=0.02)

        galaxy_frame = RoundedRectangle(
            corner_radius=0.10,
            width=galaxy_img.width + 0.14,
            height=galaxy_img.height + 0.14,
            stroke_color=GREY_B,
            stroke_width=1.0
        ).move_to(galaxy_img)

        galaxy_title = Text(
            "On larger scales, the same logic reaches cosmology",
            font_size=24,
            color=BLUE_B
        ).next_to(galaxy_img, UP, buff=0.08)

        self.play(
            FadeOut(star_img),
            FadeOut(star_frame),
            FadeOut(star_title),
            FadeOut(radial_box),
            FadeOut(radial_text),
            run_time=0.8
        )

        self.play(
            FadeIn(galaxy_img, shift=UP * 0.2),
            Create(galaxy_frame),
            FadeIn(galaxy_title),
            run_time=1.5
        )

        show_caption(
            "And then the same reasoning scales upward. If light from distant galaxies arrives systematically redshifted, that is not just a local curiosity.",
            run_time=5.0
        )

        show_caption(
            "It becomes evidence that on cosmic scales, space itself is stretching the light on its journey to us.",
            run_time=4.8
        )

        expand_box = RoundedRectangle(
            corner_radius=0.16,
            width=2.9,
            height=1.0,
            stroke_color=BLUE_D,
            stroke_width=1.7,
            fill_color="#10131c",
            fill_opacity=0.88
        ).to_edge(RIGHT, buff=0.28).shift(UP * 3.1)

        expand_text = VGroup(
            Text("Spectral shift → motion", font_size=16, color=WHITE),
            Text("Large-scale redshift → expansion", font_size=16, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(expand_box.get_center())

        self.play(FadeIn(expand_box), FadeIn(expand_text), run_time=0.9)

        show_caption(
            "So a mathematical pattern in light becomes a statement about the universe itself. Spectral analysis connects observation to motion, and motion to cosmology.",
            run_time=5.4
        )

        # =================================================
        # Final summary
        # =================================================
        remove_caption()

        summary_box = RoundedRectangle(
            corner_radius=0.18,
            width=9.0,
            height=1.35,
            stroke_color=BLUE_D,
            fill_color="#10131c",
            fill_opacity=0.84
        ).to_edge(DOWN, buff=0.55)

        summary_text = Text(
            "Shifted spectral lines reveal motion.\nAt the largest scales, they also reveal an expanding universe.",
            font_size=22,
            color=WHITE,
            line_spacing=1.0,
            weight=BOLD,
            font="DejaVu Sans"
        ).move_to(summary_box.get_center())

        self.play(FadeIn(summary_box), Write(summary_text), run_time=1.4)
        self.wait(2.0)

        final_text = Text(
            "Next: from measured shifts\nto velocity, distance, and cosmic history.",
            font_size=30,
            color=BLUE_B,
            line_spacing=1.08,
            weight=BOLD,
            font="DejaVu Sans"
        ).move_to(ORIGIN)

        self.play(
            FadeOut(galaxy_img),
            FadeOut(galaxy_frame),
            FadeOut(galaxy_title),
            FadeOut(expand_box),
            FadeOut(expand_text),
            FadeOut(summary_box),
            FadeOut(summary_text),
            FadeOut(title_group),
            run_time=1.8
        )

        self.play(FadeIn(final_text, shift=DOWN * 0.2), run_time=1.8)
        self.wait(2.5)
        self.play(FadeOut(final_text), run_time=1.2)
        self.wait(0.5)
