from manim import *
import numpy as np

class FourierScene5(Scene):
    def construct(self):
        self.camera.background_color = "#0f1117"

        # =================================================
        # Subtitle system — same style as previous scenes
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
            "Fourier and the Hidden Order of Light",
            font_size=38,
            weight=BOLD,
            color=BLUE_B
        )
        subtitle = Text(
            "From mathematical waves to the language of stars",
            font_size=26,
            color=GREY_B
        ).next_to(title, DOWN, buff=0.15)

        title_group = VGroup(title, subtitle).to_edge(UP, buff=0.35)

        self.play(FadeIn(title_group, shift=DOWN * 0.2), run_time=1.2)

        show_caption(
            "So far, Fourier analysis has helped us detect hidden structure inside a signal. But that idea does not stop with abstract waves on a graph.",
            run_time=4.8
        )

        show_caption(
            "In nature, too, there are signals filled with hidden patterns. And one of the most important of them is light.",
            run_time=4.6
        )

        # =================================================
        # Section 1 — Light as a natural signal
        # =================================================
        light_label = Text(
            "Light is also a signal",
            font_size=34,
            color=WHITE,
            weight=BOLD
        ).move_to(UP * 1.3)

        light_label_glow = light_label.copy().set_color(BLUE_D).set_opacity(0.22).scale(1.05)

        beam = Line(
            LEFT * 5.8 + UP * 0.15,
            RIGHT * 0.3 + UP * 0.15,
            stroke_color=WHITE,
            stroke_width=8
        )
        beam_glow = beam.copy().set_stroke(color=BLUE_E, width=18, opacity=0.18)

        source_dot = Dot(
            point=LEFT * 5.8 + UP * 0.15,
            radius=0.09,
            color=WHITE
        )
        source_glow = Dot(
            point=LEFT * 5.8 + UP * 0.15,
            radius=0.18,
            color=BLUE_D
        ).set_opacity(0.25)

        self.play(
            FadeIn(light_label_glow),
            FadeIn(light_label),
            FadeIn(source_glow),
            FadeIn(source_dot),
            Create(beam_glow),
            Create(beam),
            run_time=1.8
        )

        show_caption(
            "At first glance, light may seem simple — just brightness, just illumination. But physically, it is a rich signal carrying structure.",
            run_time=5.0
        )

        # =================================================
        # Section 2 — Prism image
        # =================================================
        prism_img = ImageMobject("Prism_flat_rainbow.jpg")
        prism_img.scale_to_fit_width(9.8)
        prism_img.scale_to_fit_height(4)
        prism_img.move_to(UP * 0.25)

        prism_frame = RoundedRectangle(
            corner_radius=0.12,
            width=prism_img.width + 0.16,
            height=prism_img.height + 0.16,
            stroke_color=GREY_B,
            stroke_width=1.2
        ).move_to(prism_img)

        prism_tag = Text(
            "White light → hidden components",
            font_size=20,
            color=YELLOW
        ).next_to(prism_img, UP, buff=0.18)

        self.play(
            FadeOut(light_label),
            FadeOut(light_label_glow),
            FadeOut(beam),
            FadeOut(beam_glow),
            FadeOut(source_dot),
            FadeOut(source_glow),
            run_time=0.8
        )

        self.play(
            FadeIn(prism_img, shift=UP * 0.2),
            Create(prism_frame),
            FadeIn(prism_tag, shift=UP * 0.1),
            run_time=1.6
        )

        show_caption(
            "When white light passes through a prism, what looked like one uniform beam spreads out into many visible colors.",
            run_time=4.7
        )

        show_caption(
            "That is already a powerful clue. What seemed simple was actually a combination — just as a complicated waveform can hide simpler ingredients inside it.",
            run_time=5.2
        )

        # =================================================
        # Section 3 — Spectrum as ordered structure
        # =================================================
        gradient_bar = Rectangle(
            width=9.6,
            height=0.65,
            stroke_width=1.2,
            stroke_color=GREY_B,
            fill_opacity=1
        )
        gradient_bar.set_fill(
            color=[PURPLE, BLUE, TEAL, GREEN, YELLOW, ORANGE, RED]
        )
        gradient_bar.move_to(UP * 0.25)

        wavelength_axis = NumberLine(
            x_range=[0, 1, 0.2],
            length=9.6,
            include_ticks=False,
            include_numbers=False,
            color=GREY_B
        ).next_to(gradient_bar, DOWN, buff=0.28)

        wave_label = Text("shorter wavelength", font_size=18, color=BLUE_B)\
            .next_to(wavelength_axis, DOWN, buff=0.12)\
            .align_to(wavelength_axis, LEFT)

        red_label = Text("longer wavelength", font_size=18, color=RED_B)\
            .next_to(wavelength_axis, DOWN, buff=0.12)\
            .align_to(wavelength_axis, RIGHT)

        center_label = Text("Spectrum", font_size=28, color=WHITE, weight=BOLD)\
            .next_to(gradient_bar, UP, buff=0.18)

        self.play(
            FadeOut(prism_img),
            FadeOut(prism_frame),
            FadeOut(prism_tag),
            run_time=0.8
        )

        self.play(
            FadeIn(gradient_bar),
            Create(wavelength_axis),
            FadeIn(center_label),
            FadeIn(wave_label),
            FadeIn(red_label),
            run_time=1.6
        )

        show_caption(
            "If we arrange light by wavelength, we get a spectrum. And a spectrum is not just a beautiful strip of color — it is an organized physical pattern.",
            run_time=5.2
        )

        signature_box = RoundedRectangle(
            corner_radius=0.16,
            width=3.2,
            height=0.86,
            stroke_color=BLUE_D,
            fill_color="#141924",
            fill_opacity=0.9
        ).to_edge(RIGHT, buff=0.3).shift(UP * 1.8)

        signature_text = Text(
            "A spectrum is a signature",
            font_size=18,
            color=WHITE
        ).move_to(signature_box.get_center())

        self.play(FadeIn(signature_box), FadeIn(signature_text), run_time=0.9)

        show_caption(
            "Once light is spread into its wavelengths, its internal structure becomes visible. In that sense, the spectrum acts like a signature.",
            run_time=4.9
        )

        # =================================================
        # Section 4 — Solar spectrum
        # =================================================
        solar_img = SVGMobject("Solar_spectrum_en.svg")
        solar_img.set_stroke(width=0)
        solar_img.scale_to_fit_width(10.2)
        solar_img.scale_to_fit_height(4)
        solar_img.move_to(UP * 0.28)

        solar_frame = RoundedRectangle(
            corner_radius=0.10,
            width=solar_img.width + 0.12,
            height=solar_img.height + 0.12,
            stroke_color=GREY_B,
            stroke_width=1.0
        ).move_to(solar_img)

        solar_title = Text(
            "Solar spectrum",
            font_size=24,
            color=YELLOW
        ).next_to(solar_img, UP, buff=0.14)

        self.play(
            FadeOut(gradient_bar),
            FadeOut(wavelength_axis),
            FadeOut(wave_label),
            FadeOut(red_label),
            FadeOut(center_label),
            FadeOut(signature_box),
            FadeOut(signature_text),
            run_time=0.8
        )

        self.play(
            FadeIn(solar_img, shift=UP * 0.2),
            Create(solar_frame),
            FadeIn(solar_title),
            run_time=1.5
        )

        show_caption(
            "Now look more carefully at real starlight. A stellar spectrum is not perfectly smooth. It contains dark lines and gaps at very specific places.",
            run_time=5.3
        )

        # =================================================
        # Section 5 — Fraunhofer lines close-up
        # =================================================
        fraunhofer_img = ImageMobject("Fraunhofer_lines.svg.png")
        fraunhofer_img.scale_to_fit_width(11.1)
        fraunhofer_img.move_to(UP * 0.28)

        fraunhofer_title = Text(
            "Absorption lines",
            font_size=28,
            color=BLUE_B
        ).next_to(fraunhofer_img, UP, buff=0.14)

        highlight_positions = [-3.1, -1.2, 0.4, 2.2]
        line_highlights = VGroup()

        for x in highlight_positions:
            hl = Rectangle(
                width=0.10,
                height=1.25,
                stroke_width=0,
                fill_color=YELLOW,
                fill_opacity=0.25
            ).move_to(np.array([x, 0.25, 0]))
            line_highlights.add(hl)

        self.play(
            FadeTransform(solar_img, fraunhofer_img),
            Transform(solar_title, fraunhofer_title),
            FadeOut(solar_frame),
            run_time=1.4
        )

        self.play(
            LaggedStart(*[FadeIn(hl) for hl in line_highlights], lag_ratio=0.15),
            run_time=1.1
        )

        show_caption(
            "These dark lines are not random imperfections. They mark precise wavelengths where matter has absorbed light, leaving a recognizable pattern behind.",
            run_time=5.3
        )

        info_box = RoundedRectangle(
            corner_radius=0.16,
            width=4.2,
            height=1.05,
            stroke_color=BLUE_D,
            stroke_width=1.8,
            fill_color="#10131c",
            fill_opacity=0.88
        ).to_edge(LEFT, buff=0.25).shift(UP * 2)

        info_text = VGroup(
            Text("Pattern in light → composition", font_size=16, color=WHITE),
            Text("Pattern position → motion", font_size=16, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(info_box.get_center())

        self.play(FadeIn(info_box), FadeIn(info_text), run_time=0.9)

        show_caption(
            "So hidden inside light, there is information. The pattern of the lines can tell us what is there, and their position can tell us how that source is moving.",
            run_time=5.2
        )

        # =================================================
        # Section 6 — Redshift / Blueshift
        # =================================================
        shift_img = ImageMobject("Rednadblueshift.png")
        shift_img.scale_to_fit_width(9.8)
        shift_img.scale_to_fit_height(2.4)
        shift_img.move_to(DOWN * 0.1)

        shift_frame = RoundedRectangle(
            corner_radius=0.10,
            width=shift_img.width + 0.14,
            height=shift_img.height + 0.14,
            stroke_color=GREY_B,
            stroke_width=1.0
        ).move_to(shift_img)

        ref_bar = Rectangle(
            width=7.4,
            height=0.42,
            stroke_color=WHITE,
            stroke_width=1.2,
            fill_opacity=1
        ).set_fill(color=[PURPLE, BLUE, TEAL, GREEN, YELLOW, ORANGE, RED])
        ref_bar.move_to(UP * 2.0)

        ref_label = Text("Reference pattern", font_size=22, color=WHITE).next_to(ref_bar, UP, buff=0.14)

        self.play(
            FadeOut(fraunhofer_img),
            FadeOut(line_highlights),
            FadeOut(info_box),
            FadeOut(info_text),
            FadeOut(solar_title),
            run_time=0.8
        )

        self.play(
            FadeIn(ref_bar),
            FadeIn(ref_label),
            FadeIn(shift_img, shift=UP * 0.2),
            Create(shift_frame),
            run_time=1.5
        )

        show_caption(
            "And now comes the next crucial step. If the same spectral pattern appears shifted toward red or toward blue, that shift carries physical meaning.",
            run_time=5.2
        )

        red_arrow = Arrow(
            start=UP * 1.35 + RIGHT * 0.4,
            end=UP * 1.35 + LEFT * 1.2,
            buff=0,
            color=RED_B,
            stroke_width=8
        )

        blue_arrow = Arrow(
            start=DOWN * 1.75 + LEFT * 0.4,
            end=DOWN * 1.75 + RIGHT * 1.2,
            buff=0,
            color=BLUE_B,
            stroke_width=8
        )

        red_text = Text("shift toward red", font_size=16, color=RED_B).next_to(red_arrow, UP, buff=0.02)
        blue_text = Text("shift toward blue", font_size=16, color=BLUE_B).next_to(blue_arrow, DOWN, buff=0.02)

        self.play(
            GrowArrow(red_arrow),
            FadeIn(red_text),
            GrowArrow(blue_arrow),
            FadeIn(blue_text),
            run_time=1.3
        )

        show_caption(
            "A shift toward longer wavelengths is called redshift. A shift toward shorter wavelengths is called blueshift. With light alone, we begin to detect motion.",
            run_time=5.4
        )

        show_caption(
            "So the same idea returns again: behind what first looks like complexity, there is pattern. And with the right mathematical tools, pattern becomes knowledge.",
            run_time=5.0
        )

        # =================================================
        # Final summary
        # =================================================
        remove_caption()

        summary_box = RoundedRectangle(
            corner_radius=0.18,
            width=8.8,
            height=1.25,
            stroke_color=BLUE_D,
            fill_color="#10131c",
            fill_opacity=0.84
        ).to_edge(DOWN, buff=0.55)

        summary_text = Text(
            "Fourier teaches us to look for hidden structure.\nAstronomy teaches us that light is full of it.",
            font_size=22,
            color=WHITE,
            line_spacing=1.0,
            weight=BOLD,
            font="DejaVu Sans"
        ).move_to(summary_box.get_center())

        self.play(FadeIn(summary_box), Write(summary_text), run_time=1.5)
        self.wait(2.0)

        final_text = Text(
            "Next: how spectral shifts reveal\nmotion, stars, and the expanding universe.",
            font_size=30,
            color=BLUE_B,
            line_spacing=1.08,
            weight=BOLD,
            font="DejaVu Sans"
        ).move_to(ORIGIN)

        self.play(
            FadeOut(ref_bar),
            FadeOut(ref_label),
            FadeOut(shift_img),
            FadeOut(shift_frame),
            FadeOut(red_arrow),
            FadeOut(red_text),
            FadeOut(blue_arrow),
            FadeOut(blue_text),
            FadeOut(summary_box),
            FadeOut(summary_text),
            FadeOut(title_group),
            run_time=1.8
        )

        self.play(FadeIn(final_text, shift=DOWN * 0.2), run_time=1.8)
        self.wait(2.5)
        self.play(FadeOut(final_text), run_time=1.2)
        self.wait(0.5)
