from manim import *
import numpy as np


class FourierScene9(Scene):
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
        # Subtitle system — same style continuity
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
        # Title bar
        # =================================================
        def title_bar(title_str, subtitle_str=None):
            title = Text(
                title_str,
                font_size=34,
                weight=BOLD,
                color=BLUE_B,
                font="DejaVu Sans"
            )
            if subtitle_str is not None:
                subtitle = Text(
                    subtitle_str,
                    font_size=20,
                    color=GREY_B,
                    font="DejaVu Sans"
                ).next_to(title, DOWN, buff=0.10)
                group = VGroup(title, subtitle)
            else:
                group = VGroup(title)
            group.to_edge(UP, buff=0.50)
            return group

        # =================================================
        # Helpers
        # =================================================
        def make_panel(width, height, stroke=BLUE_D, fill="#10131c", opacity=0.86):
            return RoundedRectangle(
                corner_radius=0.18,
                width=width,
                height=height,
                stroke_color=stroke,
                stroke_width=1.5,
                fill_color=fill,
                fill_opacity=opacity
            )

        def make_section_label(text, y=1.95, color=YELLOW):
            return Text(
                text,
                font_size=24,
                color=color,
                font="DejaVu Sans"
            ).move_to([0, y, 0])

        def spectrum_bar(width=3.8, height=0.42):
            colors = [RED, ORANGE, YELLOW, GREEN, BLUE]
            bars = VGroup()
            seg_w = width / len(colors)
            for i, c in enumerate(colors):
                rect = Rectangle(
                    width=seg_w,
                    height=height,
                    stroke_opacity=0,
                    fill_color=c,
                    fill_opacity=1
                )
                rect.move_to([-width/2 + seg_w*(i+0.5), 0, 0])
                bars.add(rect)
            return bars

        def fourier_sum(x, amps, freqs, phases):
            y = np.zeros_like(x)
            for a, f, p in zip(amps, freqs, phases):
                y += a * np.sin(f * x + p)
            return y

        # =================================================
        # Opening
        # =================================================
        header = title_bar(
            "Fourier: Reading Hidden Order",
            "From simple waves to the structure hidden inside nature"
        )
        self.play(FadeIn(header, shift=DOWN * 0.2), run_time=1.2)

        show_caption(
            "We have now seen light, redshift, spectra, galaxies, and the early universe as signals. This scene brings those ideas together under one question: how do we read hidden order inside complex patterns?",
            run_time=5.2
        )

        # =================================================
        # Section 1 — Simple sine wave
        # =================================================
        sec1 = make_section_label("1. A simple wave")
        self.play(FadeIn(sec1), run_time=0.7)

        axes1 = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=8.8,
            y_length=2.8,
            axis_config={"color": GREY_B, "stroke_width": 2},
            tips=False
        ).move_to([0, 0.05, 0])

        amp_line_top = DashedLine(
            axes1.c2p(PI / 2, 0),
            axes1.c2p(PI / 2, 1),
            color=BLUE_C,
            stroke_width=2
        )
        amp_line_bottom = DashedLine(
            axes1.c2p(PI / 2, -1),
            axes1.c2p(PI / 2, 0),
            color=BLUE_C,
            stroke_width=2
        )

        wave1 = axes1.plot(lambda x: np.sin(x), x_range=[0, 2 * PI], color=BLUE_B, stroke_width=4)

        amp_label = Text("amplitude", font_size=20, color=BLUE_B, font="DejaVu Sans").next_to(amp_line_top, RIGHT, buff=0.15)
        freq_label = Text("frequency", font_size=20, color=YELLOW, font="DejaVu Sans").next_to(axes1, DOWN, buff=0.18)

        self.play(Create(axes1), run_time=1.0)
        self.play(Create(wave1), run_time=1.6)
        self.play(Create(amp_line_top), Create(amp_line_bottom), FadeIn(amp_label), FadeIn(freq_label), run_time=1.0)

        show_caption(
            "We began with the simplest building block: a repeating wave. With only a few parameters, a sine wave already carries rhythm, scale, and structure.",
            run_time=4.8
        )

        # =================================================
        # Section 2 — Build complexity from simple waves
        # =================================================
        sec2 = make_section_label("2. Complexity from simple waves")
        self.play(
            FadeOut(sec1),
            FadeIn(sec2),
            run_time=0.7
        )

        self.play(
            FadeOut(amp_line_top),
            FadeOut(amp_line_bottom),
            FadeOut(amp_label),
            FadeOut(freq_label),
            run_time=0.5
        )

        left_axes = Axes(
            x_range=[0, 2 * PI, PI],
            y_range=[-1.8, 1.8, 1],
            x_length=4.5,
            y_length=1.8,
            axis_config={"color": GREY_C, "stroke_width": 1.8},
            tips=False
        )

        wave_a = left_axes.plot(lambda x: 1.0 * np.sin(x), color=BLUE_B, stroke_width=3)
        wave_b = left_axes.plot(lambda x: 0.55 * np.sin(2*x + 0.4), color=GREEN_B, stroke_width=3)
        wave_c = left_axes.plot(lambda x: 0.35 * np.sin(3*x - 0.7), color=YELLOW, stroke_width=3)

        row1 = VGroup(left_axes.copy(), wave_a).move_to([-3.7, 0.95, 0])
        row2 = VGroup(left_axes.copy(), wave_b).move_to([-3.7, -0.35, 0])
        row3 = VGroup(left_axes.copy(), wave_c).move_to([-3.7, -1.55, 0])

        plus1 = MathTex("+", color=WHITE).scale(1.0).move_to([-2.15, 0.20, 0])
        plus2 = MathTex("+", color=WHITE).scale(1.0).move_to([-2.15, -0.90, 0])
        equal = MathTex("=", color=WHITE).scale(1.0).move_to([-0.95, -0.15, 0])

        right_axes = Axes(
            x_range=[0, 2 * PI, PI],
            y_range=[-2.2, 2.2, 1],
            x_length=5.1,
            y_length=3.2,
            axis_config={"color": GREY_B, "stroke_width": 2},
            tips=False
        ).move_to([2.45, -0.15, 0])

        complex_wave = right_axes.plot(
            lambda x: np.sin(x) + 0.55*np.sin(2*x + 0.4) + 0.35*np.sin(3*x - 0.7),
            color="#FF7A59",
            stroke_width=4
        )

        comp_label = Text(
            "complex pattern",
            font_size=20,
            color="#FFB18A",
            font="DejaVu Sans"
        )
        comp_label.move_to(right_axes.get_top() + DOWN * 0.10 + RIGHT * 1.35)


        self.play(
            FadeOut(axes1),
            FadeOut(wave1),
            run_time=0.7
        )

        self.play(FadeIn(row1), FadeIn(row2), FadeIn(row3), run_time=1.2)
        self.play(FadeIn(plus1), FadeIn(plus2), FadeIn(equal), run_time=0.7)
        self.play(Create(right_axes), run_time=0.8)
        self.play(Create(complex_wave), FadeIn(comp_label), run_time=1.6)

        show_caption(
            "Then we saw something deeper: a complicated pattern does not have to come from complicated ingredients. Several simple waves can combine to produce a much richer signal.",
            run_time=5.0
        )

        # =================================================
        # Section 3 — Fourier view
        # =================================================
        # =================================================
        # Section 3 — Fourier view
        # =================================================
        sec3 = make_section_label("3. Fourier reveals the components", y=1.86)
        self.play(FadeOut(sec2), FadeIn(sec3), run_time=0.7)

        freq_axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 1.3, 0.5],
            x_length=4.5,
            y_length=3.2,
            axis_config={"color": GREY_B, "stroke_width": 2},
            tips=False
        ).move_to([2.75, -0.22, 0])

        bars = VGroup(
            Line(freq_axes.c2p(1, 0), freq_axes.c2p(1, 1.0), color=BLUE_B, stroke_width=8),
            Line(freq_axes.c2p(2, 0), freq_axes.c2p(2, 0.55), color=GREEN_B, stroke_width=8),
            Line(freq_axes.c2p(3, 0), freq_axes.c2p(3, 0.35), color=YELLOW, stroke_width=8),
        )

        self.play(
            FadeOut(row1), FadeOut(row2), FadeOut(row3),
            FadeOut(plus1), FadeOut(plus2), FadeOut(equal),
            FadeOut(comp_label),
            right_axes.animate.move_to([-2.15, -0.22, 0]).scale(0.95),
            complex_wave.animate.shift(LEFT * 4.6 + DOWN * 0.07),
            run_time=1.0
        )

        # Rebuild the plotted wave against the final axes position.
        right_axes_left = right_axes.copy().move_to([-2.15, -0.22, 0]).scale(0.95)
        complex_wave_left = right_axes_left.plot(
            lambda x: np.sin(x) + 0.55*np.sin(2*x + 0.4) + 0.35*np.sin(3*x - 0.7),
            color="#FF7A59",
            stroke_width=4
        )
        self.remove(complex_wave)
        self.remove(right_axes)
        right_axes = right_axes_left
        complex_wave = complex_wave_left
        self.add(right_axes, complex_wave)

        signal_title = Text(
            "signal view",
            font_size=18,
            color=WHITE,
            font="DejaVu Sans"
        )
        freq_title = Text(
            "frequency view",
            font_size=18,
            color=WHITE,
            font="DejaVu Sans"
        )

        signal_title.move_to(right_axes.get_top() + UP * 0.12 + LEFT * 1.10)
        freq_title.move_to(freq_axes.get_top() + UP * 0.12 + RIGHT * 0.95)

        arrow_start = right_axes.get_right() + RIGHT * 0.10 + UP * 0.18
        arrow_end = freq_axes.get_left() + LEFT * 0.10 + UP * 0.18

        arrow_fourier = Arrow(
            arrow_start,
            arrow_end,
            buff=0.0,
            color=BLUE_B,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.16
        )

        arrow_label = Text(
            "Fourier",
            font_size=19,
            color=BLUE_B,
            font="DejaVu Sans"
        )
        arrow_label.move_to(arrow_fourier.get_center() + UP * 0.82 + LEFT * 0.5)

        self.play(
            FadeIn(signal_title),
            Create(freq_axes),
            FadeIn(freq_title),
            GrowArrow(arrow_fourier),
            FadeIn(arrow_label),
            run_time=1.2
        )
        self.play(
            LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2),
            run_time=1.2
        )


        # =================================================
        # Section 4 — Light and Doppler / redshift
        # =================================================
        sec4 = make_section_label("4. Waves, light, and redshift")
        self.play(FadeOut(sec3), FadeIn(sec4), run_time=0.7)

        self.play(
            FadeOut(signal_title),
            FadeOut(freq_title),
            FadeOut(arrow_fourier),
            FadeOut(arrow_label),
            FadeOut(right_axes),
            FadeOut(complex_wave),
            FadeOut(freq_axes),
            FadeOut(bars),
            run_time=0.9
        )

        top_axes = Axes(
            x_range=[0, 8, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=8.0,
            y_length=1.7,
            axis_config={"color": GREY_C, "stroke_width": 2},
            tips=False
        ).move_to([0, 0.75, 0])

        base_wave = top_axes.plot(lambda x: np.sin(2.8*x), x_range=[0, 8], color=WHITE, stroke_width=3)
        blue_wave = top_axes.plot(lambda x: np.sin(3.6*x), x_range=[0, 8], color=BLUE_B, stroke_width=3)
        red_wave = top_axes.plot(lambda x: np.sin(2.1*x), x_range=[0, 8], color=RED_B, stroke_width=3)

        rest_text = Text("rest", font_size=18, color=WHITE, font="DejaVu Sans").next_to(top_axes, LEFT, buff=0.20).shift(UP*0.15)
        blue_text = Text("blueshift", font_size=18, color=BLUE_B, font="DejaVu Sans").move_to([3.55, 0.1, 0])
        red_text = Text("redshift", font_size=18, color=RED_B, font="DejaVu Sans").move_to([3.45, 2.15, 0])

        spec_panel = make_panel(7.8, 0.7, stroke=GREY_B, fill="#0b0e16", opacity=0.92).move_to([0, -0.60, 0])
        spec_bar = spectrum_bar(width=6.6, height=0.34).move_to(spec_panel.get_center() + UP*0.12)

        line_xs_rest = [-2.1, -0.55, 1.35]
        line_xs_red = [x + 0.55 for x in line_xs_rest]

        rest_lines = VGroup(*[
            Line([x, -0.30, 0], [x, 0.02, 0], color=WHITE, stroke_width=5)
            for x in line_xs_rest
        ]).shift(DOWN*0.42)

        red_lines = VGroup(*[
            Line([x, -0.30, 0], [x, 0.02, 0], color=RED_B, stroke_width=5)
            for x in line_xs_red
        ]).shift(DOWN*0.42)

        shift_arrow = Arrow(
            [line_xs_rest[1], -1.05, 0],
            [line_xs_red[1], -1.05, 0],
            buff=0,
            color=YELLOW,
            stroke_width=5
        )
        shift_label = MathTex(r"\Delta \lambda", color=YELLOW).scale(0.85).next_to(shift_arrow, DOWN, buff=0.12)

        self.play(Create(top_axes), FadeIn(rest_text), run_time=0.8)
        self.play(Create(base_wave), run_time=1.0)
        self.play(TransformFromCopy(base_wave, blue_wave), FadeIn(blue_text), run_time=1.0)
        self.play(TransformFromCopy(base_wave, red_wave), FadeIn(red_text), run_time=1.0)

        self.play(FadeIn(spec_panel), FadeIn(spec_bar), run_time=0.8)
        self.play(LaggedStart(*[GrowFromCenter(l) for l in rest_lines], lag_ratio=0.15), run_time=0.8)
        self.play(
            LaggedStart(*[GrowFromCenter(l) for l in red_lines], lag_ratio=0.12),
            run_time=1.0
        )
        self.play(GrowArrow(shift_arrow), FadeIn(shift_label), run_time=0.8)

        show_caption(
            "This is why light became so important. Once treated as a wave, its changes can be measured. Stretching and compression are no longer just visual metaphors; they become readable shifts inside a signal.",
            run_time=5.1
        )

        # =================================================
        # Section 5 — Real evidence cards: spectrum / CMB / structure
        # =================================================
        sec5 = make_section_label("5. The same logic across nature")
        self.play(FadeOut(sec4), FadeIn(sec5), run_time=0.7)

        self.play(
            FadeOut(top_axes), FadeOut(base_wave), FadeOut(blue_wave), FadeOut(red_wave),
            FadeOut(rest_text), FadeOut(blue_text), FadeOut(red_text),
            FadeOut(spec_panel), FadeOut(spec_bar), FadeOut(rest_lines), FadeOut(red_lines),
            FadeOut(shift_arrow), FadeOut(shift_label),
            run_time=0.9
        )

        # Three evidence cards
        card_w = 3.25
        card_h = 2.55

        card1 = make_panel(card_w, card_h, stroke=BLUE_D, fill="#111723", opacity=0.92).move_to([-4.0, 0.05, 0])
        card2 = make_panel(card_w, card_h, stroke=BLUE_D, fill="#111723", opacity=0.92).move_to([0.0, 0.05, 0])
        card3 = make_panel(card_w, card_h, stroke=BLUE_D, fill="#111723", opacity=0.92).move_to([4.0, 0.05, 0])

        img1 = ImageMobject("Fraunhofer_lines.svg.png")
        img1.scale_to_fit_width(2.15)
        img1.move_to(card1.get_center() + UP*0.38)


        img2 = ImageMobject("Planck_CMB_pillars.jpg")
        img2.scale_to_fit_width(2.95)
        img2.scale_to_fit_height(1.45)
        img2.move_to(card2.get_center() + UP*0.25)

        img3 = ImageMobject("sdss_pie2.jpg")
        img3.scale_to_fit_width(2.85)
        img3.scale_to_fit_height(1.50)
        img3.move_to(card3.get_center() + UP*0.25)

        t1 = Text("stellar spectrum", font_size=18, color=WHITE, font="DejaVu Sans").move_to(card1.get_center() + DOWN*0.82)
        t2 = Text("CMB fluctuations", font_size=18, color=WHITE, font="DejaVu Sans").move_to(card2.get_center() + DOWN*0.82)
        t3 = Text("galaxy structure", font_size=18, color=WHITE, font="DejaVu Sans").move_to(card3.get_center() + DOWN*0.82)

        s1 = Text("light carries measurable structure", font_size=14, color=GREY_B, font="DejaVu Sans").move_to(card1.get_center() + DOWN*1.12)
        s2 = Text("tiny variations reveal early order", font_size=14, color=GREY_B, font="DejaVu Sans").move_to(card2.get_center() + DOWN*1.12)
        s3 = Text("many objects form collective patterns", font_size=14, color=GREY_B, font="DejaVu Sans").move_to(card3.get_center() + DOWN*1.12)

        self.play(FadeIn(card1), FadeIn(card2), FadeIn(card3), run_time=0.9)
        self.play(
            FadeIn(img1, shift=UP*0.1), FadeIn(img2, shift=UP*0.1), FadeIn(img3, shift=UP*0.1),
            FadeIn(t1), FadeIn(t2), FadeIn(t3),
            FadeIn(s1), FadeIn(s2), FadeIn(s3),
            run_time=1.3
        )



        show_caption(
            "By now the pattern is unmistakable. In spectra, in the microwave background, and in the large-scale distribution of galaxies, nature keeps presenting structure through signals.",
            run_time=5.0
        )

        show_caption(
            "What changes from case to case is the physical setting. What remains constant is the logic: detect a pattern, separate its components, and read the order hidden inside.",
            run_time=5.2
        )

        # =================================================
        # Section 6 — Final synthesis
        # =================================================
        sec6 = make_section_label("6. We found order in nature", color=BLUE_B)
        self.play(FadeOut(sec5), FadeIn(sec6), run_time=0.7)

        self.play(
            FadeOut(img1), FadeOut(img2), FadeOut(img3),
            FadeOut(t1), FadeOut(t2), FadeOut(t3),
            FadeOut(s1), FadeOut(s2), FadeOut(s3),
            FadeOut(card1), FadeOut(card2), FadeOut(card3),
            run_time=1.0
        )


        center_wave_panel = make_panel(7.8, 1.65, stroke=BLUE_D, fill="#0d1320", opacity=0.92).move_to([0, -0.85, 0])

        center_axes = Axes(
            x_range=[0, 2*PI, PI],
            y_range=[-2.2, 2.2, 1],
            x_length=6.6,
            y_length=1.7,
            axis_config={"color": GREY_C, "stroke_width": 1.8},
            tips=False
        ).move_to(center_wave_panel.get_center())

        center_wave = center_axes.plot(
            lambda x: np.sin(x) + 0.45*np.sin(2*x + 0.5) + 0.28*np.sin(4*x - 0.3),
            color=BLUE_B,
            stroke_width=3.5
        )

        synthesis_text = Text(
            "Nature reveals order through waves, patterns, and signals.\nFourier gives us a way to study that order.",
            font_size=24,
            color=WHITE,
            line_spacing=1.12,
            font="DejaVu Sans",
            weight=BOLD
        ).move_to([0, 1.10, 0])

        self.play(FadeIn(center_wave_panel), Create(center_axes), Create(center_wave), run_time=1.3)
        self.play(Write(synthesis_text), run_time=1.5)

        show_caption(
            "This is the real conclusion of the whole journey so far: we found order in nature, and we learned that waves and Fourier analysis let us investigate that order in a precise way.",
            run_time=5.4
        )

        # =================================================
        # Section 7 — Bridge to collective human behavior
        # =================================================
# =================================================
# Section 7 — Bridge to collective human behavior
# =================================================
        remove_caption()

        sec7 = make_section_label("7. A new question", color=YELLOW)
        question_box = make_panel(9.4, 2.45, stroke=YELLOW_D, fill="#14120b", opacity=0.90).move_to([0, -0.05, 0])

        q1 = Text(
            "If hidden order exists in nature...",
            font_size=28,
            color=WHITE,
            font="DejaVu Sans",
            weight=BOLD
        ).move_to(question_box.get_center() + UP*0.48)

        q2 = Text(
            "could collective human behavior also contain patterns?",
            font_size=24,
            color=BLUE_B,
            font="DejaVu Sans"
        ).move_to(question_box.get_center() + UP*0.02)

        q3 = Text(
            "Could those patterns also be studied as signals?",
            font_size=22,
            color=GREY_B,
            font="DejaVu Sans"
        ).move_to(question_box.get_center() + DOWN*0.42)

        self.play(
            FadeOut(sec6),
            FadeOut(center_wave_panel),
            FadeOut(center_axes),
            FadeOut(center_wave),
            FadeOut(synthesis_text),
            FadeIn(sec7),
            run_time=0.9
        )

        self.play(
            FadeIn(question_box),
            FadeIn(q1),
            FadeIn(q2),
            FadeIn(q3),
            run_time=1.5
        )


        # =================================================
        # End
        # =================================================
        remove_caption()

        final_line = Text(
            "Next: from cosmic signals to collective human behavior",
            font_size=28,
            color=BLUE_B,
            font="DejaVu Sans",
            weight=BOLD
        ).move_to([0, -2.55, 0])

        self.play(FadeIn(final_line, shift=UP*0.12), run_time=1.0)
        self.wait(2.2)

        self.play(
            FadeOut(question_box),
            FadeOut(q1), FadeOut(q2), FadeOut(q3),
            FadeOut(final_line),
            FadeOut(sec7),
            FadeOut(header),
            run_time=1.4
        )
        self.wait(0.4)
