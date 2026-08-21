from manim import *
import numpy as np


class FourierScene4(Scene):
    def construct(self):
        self.camera.background_color = "#0f1117"

        # ---------------------------------------------------------------
        # Subtitle System
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

        def build_caption(text, font_size=22, max_chars=62):
            words = text.split()
            lines = wrap_words(words, max_chars)
            full_str = "\n".join(lines)

            full_text = Text(
                full_str,
                font_size=font_size,
                color=WHITE,
                line_spacing=1.0,
                font="DejaVu Sans",
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
            VGroup(caption_bg, full_text).to_edge(DOWN, buff=0.4)
            accent.next_to(caption_bg.get_left(), RIGHT, buff=0.12)

            word_groups, idx = [], 0
            for w in words:
                n = len(w)
                word_groups.append(VGroup(*full_text[idx: idx + n]))
                idx += n

            return caption_bg, accent, full_text, word_groups

        def show_caption(text, run_time=3.5, wait_time=0.25, font_size=22):
            new_bg, new_accent, full_text, word_groups = build_caption(text, font_size)

            if not bg_on[0]:
                self.play(
                    FadeIn(new_bg, shift=UP * 0.18),
                    FadeIn(new_accent, shift=UP * 0.18),
                    run_time=0.5,
                )
                cap_bg[0], cap_accent[0], bg_on[0] = new_bg, new_accent, True
            else:
                anims = [
                    Transform(cap_bg[0], new_bg),
                    Transform(cap_accent[0], new_accent),
                ]
                if cap_words[0] is not None:
                    anims.append(FadeOut(cap_words[0], shift=DOWN * 0.08))
                self.play(*anims, run_time=0.5)

            words_vgroup = VGroup(*word_groups)
            self.play(
                LaggedStart(
                    *[FadeIn(g, shift=UP * 0.14) for g in word_groups],
                    lag_ratio=0.38,
                ),
                run_time=run_time,
            )
            cap_words[0] = words_vgroup
            self.wait(wait_time)

        def remove_caption():
            if bg_on[0]:
                anims = [
                    FadeOut(cap_bg[0], shift=DOWN * 0.18),
                    FadeOut(cap_accent[0], shift=DOWN * 0.18),
                ]
                if cap_words[0] is not None:
                    anims.append(FadeOut(cap_words[0], shift=DOWN * 0.1))
                self.play(*anims, run_time=0.5)
                bg_on[0] = False

        # ---------------------------------------------------------------
        # Helpers
        # ---------------------------------------------------------------
        def make_glow_dot(point, color, radius=0.08):
            outer = Dot(point, radius=radius * 2.2, color=color, fill_opacity=0.15, stroke_opacity=0)
            inner = Dot(point, radius=radius, color=color)
            return VGroup(outer, inner)

        def create_option_panel():
            panel = RoundedRectangle(
                width=11.1,
                height=3.55,
                corner_radius=0.25,
                stroke_color=BLUE_D,
                stroke_width=1.5,
                fill_color="#111522",
                fill_opacity=0.55,
            ).shift(UP * 1.10)


            title = Text(
                "Call & Put Options",
                font_size=32,
                color=YELLOW,
                weight=BOLD,
                font="DejaVu Sans",
            ).move_to(panel.get_top() + DOWN * 0.26)

            divider = Line(
                panel.get_left() + RIGHT * 0.4 + DOWN * 0.50,
                panel.get_right() + LEFT * 0.4 + DOWN * 0.5,
                color=GREY_B,
                stroke_width=1.8,
            )



            # Left: Call
            left_origin = panel.get_left() + RIGHT * 1.05 + DOWN * 1.62
            left_x_axis = Arrow(
                left_origin,
                left_origin + RIGHT * 4.0,
                buff=0,
                color=WHITE,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.12,
            )
            left_y_axis = Arrow(
                left_origin,
                left_origin + UP * 1.95,
                buff=0,
                color=WHITE,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.12,
            )



            left_curve_points = [
                left_origin + RIGHT * 0.00 + UP * 0.05,
                left_origin + RIGHT * 0.55 + UP * 0.75,
                left_origin + RIGHT * 1.10 + UP * 0.58,
                left_origin + RIGHT * 1.55 + UP * 1.35,
                left_origin + RIGHT * 2.12 + UP * 1.12,
                left_origin + RIGHT * 2.55 + UP * 1.82,
                left_origin + RIGHT * 3.12 + UP * 1.58,
                left_origin + RIGHT * 3.55 + UP * 2.18,
                left_origin + RIGHT * 3.82 + UP * 2.18,
            ]
            call_curve = VMobject(color="#39ff14", stroke_width=4)
            call_curve.set_points_as_corners(left_curve_points)
            call_arrow = Arrow(
                left_curve_points[-2],
                left_curve_points[-1],
                buff=0,
                color="#39ff14",
                stroke_width=0,
                max_tip_length_to_length_ratio=0.35,
            )

            call_box = RoundedRectangle(
                width=2.0,
                height=0.62,
                corner_radius=0.12,
                stroke_color=BLUE,
                stroke_width=2.4,
                fill_color="#0d1320",
                fill_opacity=0.92,
            ).move_to(left_origin + RIGHT * 2.20 + UP * 2.28)


            call_text = Text(
                "Call Option",
                font_size=20,
                color=WHITE,
                font="DejaVu Sans",
            ).move_to(call_box.get_center())



            left_price = Text("Price", font_size=20, color=WHITE, font="DejaVu Sans").next_to(
                left_y_axis, LEFT, buff=0.16
            )
            left_time = Text("Time", font_size=20, color=WHITE, font="DejaVu Sans").next_to(
                left_x_axis, DOWN, buff=0.08
            )


            # Right: Put
            right_origin = panel.get_left() + RIGHT * 6.25 + DOWN * 1.62
            right_x_axis = Arrow(
                right_origin,
                right_origin + RIGHT * 4.0,
                buff=0,
                color=WHITE,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.12,
            )
            right_y_axis = Arrow(
                right_origin,
                right_origin + UP * 2.00,
                buff=0,
                color=WHITE,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.12,
            )


            right_curve_points = [
                right_origin + RIGHT * 0.10 + UP * 2.15,
                right_origin + RIGHT * 0.55 + UP * 1.95,
                right_origin + RIGHT * 1.05 + UP * 1.62,
                right_origin + RIGHT * 1.48 + UP * 1.78,
                right_origin + RIGHT * 1.95 + UP * 1.12,
                right_origin + RIGHT * 2.42 + UP * 1.28,
                right_origin + RIGHT * 2.88 + UP * 0.72,
                right_origin + RIGHT * 3.38 + UP * 0.95,
                right_origin + RIGHT * 3.72 + UP * 0.42,
            ]
            put_curve = VMobject(color=RED, stroke_width=4)
            put_curve.set_points_as_corners(right_curve_points)
            put_arrow = Arrow(
                right_curve_points[-2],
                right_curve_points[-1],
                buff=0,
                color=RED,
                stroke_width=0,
                max_tip_length_to_length_ratio=0.35,
            )
            put_box = RoundedRectangle(
                width=2.0,
                height=0.62,
                corner_radius=0.12,
                stroke_color=BLUE,
                stroke_width=2.4,
                fill_color="#0d1320",
                fill_opacity=0.92,
            ).move_to(right_origin + RIGHT * 2.35 + UP * 2.28)


            put_text = Text(
                "Put Option",
                font_size=20,
                color=WHITE,
                font="DejaVu Sans",
            ).move_to(put_box.get_center())



            right_price = Text("Price", font_size=20, color=WHITE, font="DejaVu Sans").next_to(
                right_y_axis, LEFT, buff=0.16
            )
            right_time = Text("Time", font_size=20, color=WHITE, font="DejaVu Sans").next_to(
                right_x_axis, DOWN, buff=0.08
            )


            group = VGroup(
                panel, title, divider,
                left_x_axis, left_y_axis, left_price, left_time, call_curve, call_arrow, call_box, call_text,
                right_x_axis, right_y_axis, right_price, right_time, put_curve, put_arrow, put_box, put_text,
            )
            return {
                "group": group,
                "panel": panel,
                "title": title,
                "divider": divider,
                "left_axes": VGroup(left_x_axis, left_y_axis, left_price, left_time),
                "right_axes": VGroup(right_x_axis, right_y_axis, right_price, right_time),
                "call_curve": VGroup(call_curve, call_arrow),
                "put_curve": VGroup(put_curve, put_arrow),
                "call_box": VGroup(call_box, call_text),
                "put_box": VGroup(put_box, put_text),
            }

        def create_monte_carlo_group():
            axes = Axes(
                x_range=[0, 100, 20],
                y_range=[60, 180, 20],
                x_length=9.4,
                y_length=3.0,
                axis_config={
                    "color": GREY_B,
                    "stroke_width": 1.4,
                    "include_ticks": True,
                    "font_size": 18,
                },
                tips=False,
            ).shift(UP * 0.42)

            title = Text(
                "Monte Carlo Simulation for Stock Price",
                font_size=26,
                color=WHITE,
                font="DejaVu Sans",
            ).next_to(axes, UP, buff=0.28)


            x_label = Text(
                "Numbers of steps",
                font_size=20,
                color=GREY_A,
                font="DejaVu Sans",
            ).next_to(axes, DOWN, buff=0.2)

            y_label = Text(
                "Stock price",
                font_size=20,
                color=GREY_A,
                font="DejaVu Sans",
            ).rotate(PI / 2).next_to(axes, LEFT, buff=0.25)

            grid_lines = VGroup()
            for x in [20, 40, 60, 80]:
                grid_lines.add(
                    DashedLine(
                        axes.c2p(x, 60),
                        axes.c2p(x, 180),
                        dash_length=0.08,
                        color=GREY_E,
                        stroke_opacity=0.35,
                        stroke_width=1,
                    )
                )
            for y in [80, 100, 120, 140, 160]:
                grid_lines.add(
                    DashedLine(
                        axes.c2p(0, y),
                        axes.c2p(100, y),
                        dash_length=0.08,
                        color=GREY_E,
                        stroke_opacity=0.35,
                        stroke_width=1,
                    )
                )

            np.random.seed(7)
            colors = [
                BLUE_B, GREEN_B, YELLOW, RED_B, TEAL_B,
                ORANGE, PURPLE_B, MAROON_B, GOLD_B, LIGHT_PINK,
                "#3ddbd9", "#f72585", "#90be6d", "#577590", "#f8961e"
            ]

            paths = VGroup()
            for i in range(26):
                start_price = 100.0
                mu = 0.06
                sigma = 0.20 + 0.025 * np.sin(i * 0.7)
                dt = 1 / 100
                prices = [start_price]

                for _ in range(100):
                    z = np.random.normal()
                    next_price = prices[-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)
                    prices.append(next_price)

                prices = np.clip(prices, 55, 178)

                curve = VMobject(color=colors[i % len(colors)], stroke_width=1.6, stroke_opacity=0.68)
                points = [axes.c2p(step, price) for step, price in enumerate(prices)]
                curve.set_points_as_corners(points)
                paths.add(curve)

            envelope_upper = axes.plot(
                lambda x: 100 + 7.0 * np.sqrt(x),
                x_range=[0, 100],
                color=BLUE_E,
                stroke_width=1.5,
                stroke_opacity=0.35,
            )
            envelope_lower = axes.plot(
                lambda x: 100 - 4.2 * np.sqrt(x),
                x_range=[0, 100],
                color=BLUE_E,
                stroke_width=1.5,
                stroke_opacity=0.35,
            )

            mc_group = VGroup(
                grid_lines, axes, title, x_label, y_label,
                envelope_upper, envelope_lower, paths
            )

            return {
                "group": mc_group,
                "axes": axes,
                "title": title,
                "x_label": x_label,
                "y_label": y_label,
                "grid": grid_lines,
                "paths": paths,
                "upper": envelope_upper,
                "lower": envelope_lower,
            }

        # ---------------------------------------------------------------
        # Scene Start: linked to previous scene
        # ---------------------------------------------------------------
        transition = Text(
            "From market behavior to financial instruments",
            font_size=34,
            color=BLUE_B,
            weight=BOLD,
            font="DejaVu Sans",
        ).move_to(ORIGIN)

        self.play(FadeIn(transition, shift=UP * 0.2), run_time=1.2)
        self.wait(1.0)
        self.play(FadeOut(transition, shift=UP * 0.2), run_time=0.8)

        section_title = Text(
            "From Trading to Option Pricing",
            font_size=38,
            color=YELLOW,
            weight=BOLD,
            font="DejaVu Sans",
        ).to_edge(UP, buff=0.35)

        self.play(FadeIn(section_title, shift=DOWN * 0.2), run_time=1.0)

        # ---------------------------------------------------------------
        # Part 1: Market dealing image
        # ---------------------------------------------------------------
        show_caption(
            "Most of us are familiar with the concept of trading assets in financial markets; for example, buying and selling stocks, commodities, currencies, or even CFD contracts.",
            run_time=7.2,
            wait_time=0.3,
        )

        trading_frame = RoundedRectangle(
            width=10.2,
            height=4.45,
            corner_radius=0.18,
            stroke_color=BLUE_D,
            stroke_width=1.8,
            fill_color="#0b0f18",
            fill_opacity=0.35,
        ).shift(UP * 0.50)

        trading_image = ImageMobject("price-deal.jpg")
        trading_image.set_width(6.6)
        trading_image.move_to(trading_frame.get_center() + UP * 0.08)


        trading_glow = trading_frame.copy().set_stroke(color=BLUE_E, width=8, opacity=0.12)
        trading_label = Text(
            "Asset Trading",
            font_size=22,
            color=GREY_A,
            font="DejaVu Sans",
        ).next_to(trading_frame, UP, buff=0.08)


        self.play(
            FadeIn(trading_glow),
            FadeIn(trading_frame),
            FadeIn(trading_image, scale=1.03),
            FadeIn(trading_label, shift=DOWN * 0.08),
            run_time=1.4,
        )
        self.wait(0.6)

        show_caption(
            "But one of the most important instruments in this environment is something that most of us are not very familiar with: the option contract, or simply, the Option.",
            run_time=7.0,
            wait_time=0.3,
        )

        option_hint = Text(
            "A more advanced financial instrument",
            font_size=24,
            color=BLUE_B,
            weight=BOLD,
            font="DejaVu Sans",
        ).next_to(trading_frame, DOWN, buff=0.35).shift(UP * 0.9)

        self.play(FadeIn(option_hint, shift=UP * 0.12), run_time=0.8)
        self.wait(0.3)

        # Transition from image to option structure
        self.play(
            FadeOut(trading_image, scale=0.96),
            FadeOut(trading_label, shift=UP * 0.08),
            FadeOut(option_hint, shift=DOWN * 0.08),
            run_time=0.9,
        )

        # ---------------------------------------------------------------
        # Part 2: Option panel built with Manim
        # ---------------------------------------------------------------
        option_scene = create_option_panel()

        self.play(
            FadeOut(trading_glow, shift=UP * 0.04),
            Transform(trading_frame, option_scene["panel"]),
            FadeIn(option_scene["title"], shift=DOWN * 0.08),
            FadeIn(option_scene["divider"]),
            run_time=1.1,
        )




        self.play(
            FadeIn(option_scene["left_axes"]),
            FadeIn(option_scene["right_axes"]),
            run_time=0.9,
        )

        self.play(
            Create(option_scene["call_curve"]),
            Create(option_scene["put_curve"]),
            run_time=1.8,
        )

        self.play(
            FadeIn(option_scene["call_box"], scale=0.95),
            FadeIn(option_scene["put_box"], scale=0.95),
            run_time=1.0,
        )

        show_caption(
            "An option is, in fact, a contract; a contract that gives you the right to buy or sell an asset in the future at a specified price, but does not obligate you to do so.",
            run_time=8.0,
            wait_time=0.35,
        )

        contract_box = RoundedRectangle(
            width=3.2,
            height=1.0,
            corner_radius=0.15,
            stroke_color=YELLOW,
            stroke_width=2.2,
            fill_color="#1b1820",
            fill_opacity=0.88,
        ).shift(DOWN * 1.2)

        contract_title = Text(
            "OPTION CONTRACT",
            font_size=22,
            color=YELLOW,
            weight=BOLD,
            font="DejaVu Sans",
        ).move_to(contract_box.get_center() + UP * 0.15)

        contract_sub = Text(
            "Right, not obligation",
            font_size=18,
            color=WHITE,
            font="DejaVu Sans",
        ).move_to(contract_box.get_center() + DOWN * 0.2)

        link_left = Arrow(
            contract_box.get_left() + LEFT * 0.05,
            option_scene["call_box"].get_right() + LEFT * 0.15,
            buff=0.08,
            color=BLUE_B,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.16,
        )
        link_right = Arrow(
            contract_box.get_right() + RIGHT * 0.05,
            option_scene["put_box"].get_left() + RIGHT * 0.15,
            buff=0.08,
            color=BLUE_B,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.16,
        )

        self.play(
            FadeIn(contract_box, scale=0.92),
            Write(contract_title),
            FadeIn(contract_sub, shift=UP * 0.05),
            GrowArrow(link_left),
            GrowArrow(link_right),
            run_time=1.6,
        )
        self.wait(0.5)

        # ---------------------------------------------------------------
        # Part 3: Engineering question
        # ---------------------------------------------------------------
        self.play(
            FadeOut(
                VGroup(
                    option_scene["title"],
                    option_scene["divider"],
                    option_scene["left_axes"],
                    option_scene["right_axes"],
                    option_scene["call_curve"],
                    option_scene["put_curve"],
                    option_scene["call_box"],
                    option_scene["put_box"],
                    contract_box,
                    contract_title,
                    contract_sub,
                    link_left,
                    link_right,
                )
            ),
            run_time=1.0,
        )

        question_panel = RoundedRectangle(
            width=10.8,
            height=3.5,
            corner_radius=0.2,
            stroke_color=BLUE_D,
            stroke_width=1.8,
            fill_color="#111522",
            fill_opacity=0.55,
        ).move_to(trading_frame.get_center())

        q1 = Text(
            "When the future price of an asset is",
            font_size=30,
            color=WHITE,
            font="DejaVu Sans",
        ).move_to(question_panel.get_center() + UP * 0.7)

        q2 = Text(
            "uncertain and random,",
            font_size=32,
            color=YELLOW,
            weight=BOLD,
            font="DejaVu Sans",
        ).move_to(question_panel.get_center() + UP * 0.15)

        q3 = Text(
            "what value does this trading right have today?",
            font_size=30,
            color=WHITE,
            font="DejaVu Sans",
        ).move_to(question_panel.get_center() + DOWN * 0.55)

        self.play(
            Transform(trading_frame, question_panel),
            FadeIn(q1, shift=UP * 0.08),
            FadeIn(q2, shift=UP * 0.08),
            FadeIn(q3, shift=UP * 0.08),
            run_time=1.3,
        )

        show_caption(
            "But then, an engineering question arises:",
            run_time=2.4,
            wait_time=0.2,
        )

        show_caption(
            "When the future price of an asset is uncertain and random, what value does this trading right have today?",
            run_time=6.4,
            wait_time=0.35,
        )

        self.wait(0.5)

        # ---------------------------------------------------------------
        # Part 4: Dynamic system -> Monte Carlo
        # ---------------------------------------------------------------
        self.play(
            FadeOut(VGroup(q1, q2, q3), shift=UP * 0.15),
            run_time=0.7,
        )

        mc = create_monte_carlo_group()

        self.play(
            Transform(trading_frame, mc["axes"].copy().surround(mc["axes"], buff=0.35).set_opacity(0)),
            run_time=0.2,
        )

        self.play(
            FadeOut(trading_frame),
            FadeIn(mc["grid"]),
            FadeIn(mc["axes"]),
            FadeIn(mc["title"]),
            FadeIn(mc["x_label"]),
            FadeIn(mc["y_label"]),
            run_time=1.0,
        )

        self.play(
            FadeIn(mc["upper"]),
            FadeIn(mc["lower"]),
            run_time=0.6,
        )

        self.play(
            LaggedStart(
                *[Create(path) for path in mc["paths"]],
                lag_ratio=0.03,
            ),
            run_time=4.0,
        )

        center_focus = make_glow_dot(mc["axes"].c2p(0, 100), BLUE_B, radius=0.09)
        spread_focus_top = make_glow_dot(mc["axes"].c2p(98, 165), GREEN_B, radius=0.09)
        spread_focus_bottom = make_glow_dot(mc["axes"].c2p(98, 68), RED_B, radius=0.09)

        self.play(
            FadeIn(center_focus, scale=0.9),
            FadeIn(spread_focus_top, scale=0.9),
            FadeIn(spread_focus_bottom, scale=0.9),
            run_time=0.9,
        )

        dynamic_text = Text(
            "Uncertainty evolves through time",
            font_size=24,
            color="#6ec1ff",
            weight=BOLD,
            font="DejaVu Sans",
        ).next_to(mc["title"], UP, buff=0.16)



        self.play(FadeIn(dynamic_text, shift=UP * 0.08), run_time=0.8)

        show_caption(
            "We are no longer dealing with a static problem; rather, we are dealing with a completely dynamic system.",
            run_time=6.0,
            wait_time=0.35,
        )

        # ---------------------------------------------------------------
        # Ending transition
        # ---------------------------------------------------------------
        remove_caption()

        end_group = VGroup(
            mc["grid"], mc["axes"], mc["title"], mc["x_label"], mc["y_label"],
            mc["upper"], mc["lower"], mc["paths"],
            center_focus, spread_focus_top, spread_focus_bottom, dynamic_text,
            section_title,
        )

        conclusion = Text(
            "Option pricing begins\nwith uncertainty, time,\nand dynamics.",
            font_size=34,
            line_spacing=1.25,
            color=WHITE,
            font="DejaVu Sans",
        ).move_to(ORIGIN)

        self.play(FadeOut(end_group, shift=UP * 0.15), run_time=1.2)
        self.play(Write(conclusion), run_time=2.4)
        self.wait(2.0)
        self.play(FadeOut(conclusion), run_time=1.0)
        self.wait(0.8)
