from pathlib import Path

from manim import *


config.background_color = "#05060A"
config.frame_width = 16
config.frame_height = 9
config.pixel_width = 1920
config.pixel_height = 1080


ASSET_DIRS = [
    Path("."),
    Path("assets"),
    Path("images"),
    Path("media"),
]


def find_asset(*names: str) -> str:
    for directory in ASSET_DIRS:
        for name in names:
            candidate = directory / name
            if candidate.exists():
                return str(candidate)
    raise FileNotFoundError(f"None of these assets were found: {names}")


class Scene08EvidenceInTheSky(Scene):
    def construct(self):
        self.font = "DejaVu Sans"
        
        self.caption_visible = False
        self.cap_bg = None
        self.cap_accent = None
        self.cap_words = None


        self.survey_path = find_asset(
            "2df_slice_blue_big.gif",
            "2df_slice_blue_big.png",
            "sdss_redshift_survey.jpg",
            "Sdss_slice.jpg",
        )
        self.cmb_path = find_asset(
            "Planck_CMB_pillars.jpg",
            "planck_cmb_map.png",
            "cmb_full_sky_map.jpg",
        )
        self.blackbody_path = find_asset(
            "unnamed.gif",
            "cobe_firas_spectrum.png",
            "cmb_blackbody_spectrum.jpg",
            "Cosmic_microwave_background_spectrum_percent.jpg",
        )

        self.opening()
        self.hubble_evidence()
        self.redshift_survey()
        self.expanding_space()
        self.cmb_relic()
        self.blackbody_signal()
        self.closing_bridge()

    def make_text(self, text, size=34, color=WHITE, weight=NORMAL):
        return Text(
            text,
            font=self.font,
            font_size=size,
            color=color,
            weight=weight,
        )

    def wrap_words(self, words, max_chars):
        lines = []
        cur = []
        cur_len = 0

        for w in words:
            add = len(w) + (1 if cur else 0)
            if cur_len + add <= max_chars:
                cur.append(w)
                cur_len += add
            else:
                lines.append(" ".join(cur))
                cur = [w]
                cur_len = len(w)

        if cur:
            lines.append(" ".join(cur))

        return lines
    
    def build_caption(self, text, font_size=20, max_chars=64):
        words = text.split()
        lines = self.wrap_words(words, max_chars)
        full_str = "\n".join(lines)

        full_text = Text(
            full_str,
            font_size=font_size,
            color=WHITE,
            line_spacing=1.0,
            font=self.font,
        )
        caption_bg = RoundedRectangle(
            corner_radius=0.18,
            height=full_text.height + 0.5,
            width=min(full_text.width + 0.9, 12.8),
            stroke_color=BLUE_D,
            stroke_width=1.4,
            fill_color="#0a0c14",
            fill_opacity=0.82,
        ) 
        accent = RoundedRectangle(
            corner_radius=0.05,
            height=caption_bg.height - 0.22,
            width=0.08,
            fill_color=BLUE_B,
            fill_opacity=0.9,
             stroke_opacity=0,
             )
        full_text.move_to(caption_bg.get_center())
        VGroup(caption_bg, full_text).to_edge(DOWN, buff=0.22)
        accent.next_to(caption_bg.get_left(), RIGHT, buff=0.12)
        word_groups = []
        idx = 0
        for w in words:
            n = len(w)
            word_groups.append(VGroup(*full_text[idx:idx + n]))
            idx += n
        return caption_bg, accent, full_text, word_groups
    def show_caption(self, text, run_time=3.8, wait_time=0.25, font_size=20):
        new_bg, new_accent, full_text, word_groups = self.build_caption(text, font_size)

        if not self.caption_visible:
            self.play(
                FadeIn(new_bg, shift=UP * 0.18),
                FadeIn(new_accent, shift=UP * 0.18),
                run_time=0.5,
            )
            self.cap_bg = new_bg
            self.cap_accent = new_accent
            self.caption_visible = True
        else:
            anims = [
                Transform(self.cap_bg, new_bg),
                Transform(self.cap_accent, new_accent),
            ]
            if self.cap_words is not None:
                anims.append(FadeOut(self.cap_words, shift=DOWN * 0.08))
            self.play(*anims, run_time=0.5)

        words_vgroup = VGroup(*word_groups)
        if len(word_groups) > 0:
            self.play(
                LaggedStart(
                    *[FadeIn(g, shift=UP * 0.14) for g in word_groups],
                    lag_ratio=0.38,
                ),
                run_time=run_time,
            )

        self.cap_words = words_vgroup
        self.wait(wait_time)

    def remove_caption(self):
        if self.caption_visible:
            anims = [
                FadeOut(self.cap_bg, shift=DOWN * 0.18),
                FadeOut(self.cap_accent, shift=DOWN * 0.18),
            ]
            if self.cap_words is not None:
                anims.append(FadeOut(self.cap_words, shift=DOWN * 0.1))

            self.play(*anims, run_time=0.5)

            self.caption_visible = False
            self.cap_bg = None
            self.cap_accent = None
            self.cap_words = None
    def image_card(self, path, width=6.4, height=None, stroke_color="#FFFFFF"):
        image = ImageMobject(path)
        image.set_width(width)
        if height is not None and image.height > height:
            image.set_height(height)

        frame = RoundedRectangle(
            corner_radius=0.16,
            width=image.width + 0.18,
            height=image.height + 0.18,
            stroke_color=stroke_color,
            stroke_opacity=0.45,
            stroke_width=1.4,
            fill_color=BLACK,
            fill_opacity=0.18,
        )
        frame.move_to(image)

        return Group(frame, image)

    def title_bar(self, title, subtitle=None):
        title_text = self.make_text(title, size=40, color="#FFFFFF", weight=BOLD)
        title_text.to_edge(UP, buff=0.34)

        if subtitle:
            subtitle_text = self.make_text(subtitle, size=24, color="#B8C7FF")
            subtitle_text.next_to(title_text, DOWN, buff=0.13)
            return VGroup(title_text, subtitle_text)

        return VGroup(title_text)

    def opening(self):
        title = self.title_bar(
            "Evidence in the Sky",
            "Expansion became measurable — and the early universe left a signal",
        )

        left = Circle(radius=1.15, stroke_color="#6EA8FF", stroke_width=3)
        left.set_fill("#10233F", opacity=0.25)
        left_label = self.make_text("Redshift", size=25, color="#B7D3FF")
        left_label.move_to(left)

        right = Circle(radius=1.15, stroke_color="#FFB14E", stroke_width=3)
        right.set_fill("#3A1B08", opacity=0.25)
        right_label = self.make_text("CMB", size=25, color="#FFD9A2")
        right_label.move_to(right)

        bridge = Arrow(
            left.get_right(),
            right.get_left(),
            buff=0.28,
            stroke_width=4,
            color="#DDE6FF",
        )
        bridge_label = self.make_text("observations", size=24, color="#E8E8E8")
        bridge_label.next_to(bridge, UP, buff=0.22)

        evidence_group = VGroup(left, left_label, bridge, bridge_label, right, right_label)
        evidence_group.arrange(RIGHT, buff=0.75)
        evidence_group.move_to(ORIGIN + DOWN * 0.1)

        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.8)
        self.play(
            LaggedStart(
                GrowFromCenter(left),
                FadeIn(left_label),
                GrowArrow(bridge),
                FadeIn(bridge_label),
                GrowFromCenter(right),
                FadeIn(right_label),
                lag_ratio=0.18,
            ),
            run_time=1.8,
        )
        self.show_caption(
            "In the last scene, redshift became a measurement. Now it becomes evidence.",
            wait_time=2.2,
        )
        self.play(FadeOut(title), FadeOut(evidence_group), run_time=0.75)

    def hubble_evidence(self):
        title = self.title_bar("Many galaxies, one pattern")

        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            x_length=7.0,
            y_length=4.65,
            axis_config={
                "color": "#9EA7B8",
                "stroke_width": 2,
                "include_tip": False,
            },
            tips=False,
        )
        axes.move_to(LEFT * 1.15)

        x_label = self.make_text("distance", size=24, color="#D7DCE8")
        y_label = self.make_text("recession speed", size=24, color="#D7DCE8")
        x_label.next_to(axes.x_axis, DOWN, buff=0.35)
        y_label.rotate(PI / 2)
        y_label.next_to(axes.y_axis, LEFT, buff=0.35)

        data = [
            (0.8, 0.9),
            (1.4, 1.8),
            (2.1, 2.2),
            (2.7, 3.0),
            (3.3, 3.7),
            (4.2, 4.1),
            (5.1, 5.6),
            (6.0, 6.2),
            (6.8, 7.1),
            (7.6, 7.7),
            (8.7, 8.8),
        ]

        dots = VGroup(
            *[
                Dot(
                    axes.c2p(x, y),
                    radius=0.06,
                    color="#70B7FF",
                )
                for x, y in data
            ]
        )

        trend = Line(
            axes.c2p(0.55, 0.55),
            axes.c2p(9.05, 9.05),
            color="#FF5C7A",
            stroke_width=4,
        )

        equation_box = RoundedRectangle(
            corner_radius=0.18,
            width=3.9,
            height=1.35,
            stroke_color="#FF5C7A",
            stroke_opacity=0.55,
            fill_color="#16070C",
            fill_opacity=0.72,
        )
        equation = MathTex("v", "=", "H_0", "d", font_size=44)
        equation.set_color_by_tex("v", "#70B7FF")
        equation.set_color_by_tex("H_0", "#FFCF66")
        equation.set_color_by_tex("d", "#70B7FF")
        equation.move_to(equation_box)

        note = self.make_text(
            "The farther a galaxy is,\nthe faster its light is redshifted.",
            size=25,
            color="#E8E8E8",
        )
        note_box = RoundedRectangle(
            corner_radius=0.18,
            width=5.55,
            height=1.55,
            stroke_color="#FFFFFF",
            stroke_opacity=0.18,
            fill_color="#0B0E16",
            fill_opacity=0.82,
        )
        note.move_to(note_box)

        equation_group = VGroup(equation_box, equation)
        note_group = VGroup(note_box, note)

        right_group = VGroup(equation_group, note_group)
        right_group.arrange(DOWN, buff=0.45)
        right_group.move_to(RIGHT * 5.0 + DOWN * 0.05)


        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.65)
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1.0)
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in dots], lag_ratio=0.08), run_time=1.55)
        self.play(Create(trend), run_time=0.9)
        self.play(FadeIn(right_group, shift=LEFT * 0.15), run_time=0.8)
        self.show_caption(
            "A single redshift is a measurement. Many redshifts reveal a law.",
            wait_time=2.0,
        )

        self.play(
            FadeOut(title),
            FadeOut(axes),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(dots),
            FadeOut(trend),
            FadeOut(right_group),
            run_time=0.8,
        )

    def redshift_survey(self):
        title = self.title_bar("Redshift surveys map structure")

        survey = self.image_card(self.survey_path, width=9.0, height=3.7, stroke_color="#719CFF")
        survey.move_to(ORIGIN + DOWN * 0.2)

        label_box = RoundedRectangle(
            corner_radius=0.16,
            width=8.8,
            height=0.60,
            stroke_color="#719CFF",
            stroke_opacity=0.5,
            fill_color="#071022",
            fill_opacity=0.82,
        )
        label = self.make_text("Each point is a galaxy measured by its redshift", size=25, color="#DDE8FF")
        label.move_to(label_box)
        label_group = VGroup(label_box, label)
        label_group.next_to(survey, DOWN, buff=0.22)

        filaments = self.make_text("filaments", size=24, color="#5F7CFF")
        voids = self.make_text("voids", size=24, color="#5F7CFF")
        observer = self.make_text("us", size=24, color="#F1BC3F")

        filaments.move_to(LEFT * 4.5 + UP * 0.1)
        voids.move_to(RIGHT * 4 + UP *0.1)
        observer.move_to(ORIGIN + DOWN * 0.55)

        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.65)
        self.play(FadeIn(survey, scale=0.98), run_time=1.0)
        self.play(FadeIn(label_group), run_time=0.55)
        self.play(
            LaggedStart(
                FadeIn(filaments, shift=UP * 0.1),
                FadeIn(voids, shift=UP * 0.1),
                FadeIn(observer, shift=UP * 0.1),
                lag_ratio=0.2,
            ),
            run_time=0.9,
        )
        self.show_caption(
            "Redshift turns the sky into a three-dimensional map of the universe.",
            wait_time=2.2,
        )

        self.play(
            FadeOut(title),
            FadeOut(survey),
            FadeOut(label_group),
            FadeOut(filaments),
            FadeOut(voids),
            FadeOut(observer),
            run_time=0.85,
        )

    def expanding_space(self):
        title = self.title_bar("Not motion through space — expansion of space")

        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            x_length=9.8,
            y_length=5.8,
            background_line_style={
                "stroke_color": "#38506F",
                "stroke_width": 1.2,
                "stroke_opacity": 0.55,
            },
            faded_line_style={
                "stroke_color": "#1B2C43",
                "stroke_width": 0.8,
                "stroke_opacity": 0.32,
            },
        )
        plane.move_to(ORIGIN + DOWN * 0.05)

        coords = [
            (-3, -1),
            (-2, 1),
            (-1, -2),
            (1, 1),
            (2, -1),
            (3, 2),
            (0, -0.3),
        ]

        galaxies = VGroup()
        for x, y in coords:
            dot = Dot(plane.c2p(x, y), radius=0.095, color="#FFD166")
            halo = Circle(radius=0.18, stroke_color="#FFD166", stroke_width=1.2, stroke_opacity=0.6)
            halo.move_to(dot)
            galaxies.add(VGroup(halo, dot))

        same_label = self.make_text("same galaxies", size=24, color="#FFE6A8")
        larger_label = self.make_text("larger separations", size=24, color="#B7D3FF")

        same_label.move_to(LEFT * 4.2 + UP * 2.65)
        larger_label.move_to(RIGHT * 4.2 + UP * 2.65)

        labels_before = VGroup(same_label, larger_label)


        expansion_arrows = VGroup()
        for angle in [0, PI / 4, PI / 2, 3 * PI / 4, PI, 5 * PI / 4, 3 * PI / 2, 7 * PI / 4]:
            start = np.array([0.45 * np.cos(angle), 0.45 * np.sin(angle), 0])
            end = np.array([1.2 * np.cos(angle), 1.2 * np.sin(angle), 0])
            expansion_arrows.add(
                Arrow(
                    start,
                    end,
                    buff=0,
                    color="#72A8FF",
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.22,
                )
            )

        expansion_arrows.move_to(ORIGIN + UP * 0.1)

        expanded_plane = plane.copy().scale(1.55)
        expanded_galaxies = VGroup()
        center = plane.get_center()
        for galaxy in galaxies:
            new_galaxy = galaxy.copy()
            vector = galaxy.get_center() - center
            new_galaxy.move_to(center + vector * 1.55)
            expanded_galaxies.add(new_galaxy)

        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.65)
        self.play(Create(plane), LaggedStart(*[FadeIn(g) for g in galaxies], lag_ratio=0.08), run_time=1.2)
        self.play(FadeIn(labels_before[0]), run_time=0.45)
        self.show_caption(
            "The galaxies are not flying through a fixed grid.",
            wait_time=1.45,
        )
        self.play(FadeIn(expansion_arrows, scale=0.7), run_time=0.55)
        self.play(
            Transform(plane, expanded_plane),
            Transform(galaxies, expanded_galaxies),
            FadeIn(labels_before[1]),
            expansion_arrows.animate.scale(1.25).set_opacity(0.35),
            run_time=2.0,
            rate_func=smooth,
        )
        self.show_caption(
            "The grid itself stretches, so distant galaxies separate faster.",
            wait_time=2.0,
        )

        self.play(
            FadeOut(title),
            FadeOut(plane),
            FadeOut(galaxies),
            FadeOut(labels_before),
            FadeOut(expansion_arrows),
            run_time=0.85,
        )

    def cmb_relic(self):
        title = self.title_bar("A relic from the early universe")

        cmb = self.image_card(self.cmb_path, width=9.2, height=3.3, stroke_color="#FFB14E")
        cmb.move_to(ORIGIN + DOWN * 0.08)

        age_tag_box = RoundedRectangle(
            corner_radius=0.16,
            width=7.65,
            height=0.62,
            stroke_color="#FFB14E",
            stroke_opacity=0.55,
            fill_color="#1A0E05",
            fill_opacity=0.82,
        )
        age_tag = self.make_text("light from ~380,000 years after the Big Bang", size=23, color="#FFE0B3")
        age_tag.move_to(age_tag_box)
        age_group = VGroup(age_tag_box, age_tag)
        age_group.next_to(cmb, DOWN, buff=0.2)

        fluctuation_box = RoundedRectangle(
            corner_radius=0.18,
            width=4.5,
            height=1.25,
            stroke_color="#FFFFFF",
            stroke_opacity=0.22,
            fill_color="#081018",
            fill_opacity=0.83,
        )
        fluctuation_text = self.make_text(
            "tiny temperature differences\nencoded early structure",
            size=24,
            color="#EAF2FF",
        )
        fluctuation_text.move_to(fluctuation_box)
        fluctuation_group = VGroup(fluctuation_box, fluctuation_text)
        fluctuation_group.move_to(RIGHT * 5.25 + UP * 2.45)

        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.65)
        self.play(FadeIn(cmb, scale=0.98), run_time=1.15)
        self.play(FadeIn(age_group, shift=UP * 0.08), run_time=0.55)
        self.play(FadeIn(fluctuation_group, shift=LEFT * 0.1), run_time=0.65)
        self.show_caption(
            "If the universe was once hot and dense, a cooled afterglow should remain.",
            wait_time=2.1,
        )
        self.show_caption(
            "The cosmic microwave background is that afterglow — mapped across the sky.",
            wait_time=2.1,
        )

        self.play(
            FadeOut(title),
            FadeOut(cmb),
            FadeOut(age_group),
            FadeOut(fluctuation_group),
            run_time=0.85,
        )

    def blackbody_signal(self):
        title = self.title_bar("A measurable thermal signal")

        spectrum = self.image_card(self.blackbody_path, width=7.5, height=5.4, stroke_color="#DDE8FF")
        spectrum.move_to(LEFT * 3.8 + DOWN * 0.1)

        formula_box = RoundedRectangle(
            corner_radius=0.18,
            width=4.75,
            height=1.25,
            stroke_color="#FFCF66",
            stroke_opacity=0.55,
            fill_color="#171004",
            fill_opacity=0.78,
        )
        formula = MathTex("T", "\\approx", "2.725", "\\,K", font_size=46)
        formula.set_color_by_tex("T", "#FFCF66")
        formula.set_color_by_tex("2.725", "#FFFFFF")
        formula.move_to(formula_box)

        signal_box = RoundedRectangle(
            corner_radius=0.18,
            width=5.35,
            height=2.1,
            stroke_color="#FFFFFF",
            stroke_opacity=0.18,
            fill_color="#0B0E16",
            fill_opacity=0.82,
        )
        signal_text = self.make_text(
            "The measured points fall almost\nperfectly on a blackbody curve.",
            size=25,
            color="#E8E8E8",
        )
        signal_text.move_to(signal_box)

        fourier_box = RoundedRectangle(
            corner_radius=0.18,
            width=5.05,
            height=1.65,
            stroke_color="#6EA8FF",
            stroke_opacity=0.45,
            fill_color="#071022",
            fill_opacity=0.78,
        )
        fourier_text = self.make_text(
            "Again, the universe speaks\nthrough a spectrum.",
            size=25,
            color="#DDE8FF",
        )
        fourier_text.move_to(fourier_box)

        right_group = VGroup(
            VGroup(formula_box, formula),
            VGroup(signal_box, signal_text),
            VGroup(fourier_box, fourier_text),
        )
        right_group.arrange(DOWN, buff=0.42)
        right_group.move_to(RIGHT * 4.25 + DOWN * 0.05)

        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.65)
        self.play(FadeIn(spectrum, scale=0.98), run_time=1.05)
        self.play(FadeIn(right_group[0], shift=LEFT * 0.1), run_time=0.55)
        self.play(FadeIn(right_group[1], shift=LEFT * 0.1), run_time=0.65)
        self.show_caption(
            "The CMB is not just an image. It is a precisely measured spectrum.",
            wait_time=2.0,
        )
        self.play(FadeIn(right_group[2], shift=LEFT * 0.1), run_time=0.65)
        self.show_caption(
            "From light to redshift to the CMB, hidden order appears in measured signals.",
            wait_time=2.25,
        )

        self.play(
            FadeOut(title),
            FadeOut(spectrum),
            FadeOut(right_group),
            run_time=0.85,
        )

    def closing_bridge(self):
        title = self.title_bar("From evidence to synthesis")

        chain_items = [
            ("sound", "#9AD0FF"),
            ("light", "#FFE08A"),
            ("spectrum", "#FF9F6E"),
            ("redshift", "#FF5C7A"),
            ("CMB", "#72A8FF"),
            ("structure", "#B9FBC0"),
        ]

        nodes = VGroup()
        for label, color in chain_items:
            circle = Circle(radius=0.62, stroke_color=color, stroke_width=2.6)
            circle.set_fill(color, opacity=0.13)
            text = self.make_text(label, size=18, color=color)
            text.move_to(circle)
            nodes.add(VGroup(circle, text))

        nodes.arrange(RIGHT, buff=0.42)
        nodes.move_to(UP * 0.25)

        arrows = VGroup()
        for left_node, right_node in zip(nodes[:-1], nodes[1:]):
            arrows.add(
                Arrow(
                    left_node.get_right(),
                    right_node.get_left(),
                    buff=0.12,
                    color="#E8E8E8",
                    stroke_width=2.4,
                    max_tip_length_to_length_ratio=0.24,
                )
            )

        final_box = RoundedRectangle(
            corner_radius=0.2,
            width=10.5,
            height=1.35,
            stroke_color="#FFFFFF",
            stroke_opacity=0.2,
            fill_color="#090B12",
            fill_opacity=0.84,
        )
        final_text = self.make_text(
            "Next: Fourier as a language for reading hidden order",
            size=30,
            color="#FFFFFF",
        )
        final_text.move_to(final_box)
        final_group = VGroup(final_box, final_text)
        final_group.next_to(nodes, DOWN, buff=0.7)

        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.65)
        self.play(
            LaggedStart(*[FadeIn(node, scale=0.92) for node in nodes], lag_ratio=0.1),
            run_time=1.25,
        )
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.08), run_time=1.0)
        self.play(FadeIn(final_group, shift=UP * 0.12), run_time=0.75)
        self.show_caption(
            "The final step is to connect the whole journey: Fourier, signals, and cosmic order.",
            wait_time=2.4,
        )
        self.remove_caption()
        self.wait(0.4)
        self.play(FadeOut(title), FadeOut(nodes), FadeOut(arrows), FadeOut(final_group), run_time=1.0)
