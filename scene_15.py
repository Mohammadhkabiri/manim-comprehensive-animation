from manim import *
import numpy as np
import random

class SimonsAndEvolutionScene(Scene):
    def construct(self):
        # ==========================================
        # Theme & Styling Setup
        # ==========================================
        self.camera.background_color = "#0f1117"

        # --- Helper functions for modern minimalist subtitles ---
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

        def build_caption(text, font_size=19, max_chars=65):
            words = text.split()
            lines = wrap_words(words, max_chars)
            full_str = "\n".join(lines)
            full_text = Text(full_str, font_size=font_size, color=WHITE,
                             line_spacing=1.1, font="DejaVu Sans")
            caption_bg = RoundedRectangle(
                corner_radius=0.15, height=full_text.height + 0.4,
                width=min(full_text.width + 0.8, 12.5),
                stroke_color=BLUE_E, stroke_width=1.2,
                fill_color="#070911", fill_opacity=0.85)
            accent = RoundedRectangle(
                corner_radius=0.04, height=caption_bg.height - 0.2,
                width=0.06, fill_color=BLUE_B, fill_opacity=0.9, stroke_opacity=0)
            
            full_text.move_to(caption_bg.get_center())
            VGroup(caption_bg, full_text).to_edge(DOWN, buff=0.3)
            accent.next_to(caption_bg.get_left(), RIGHT, buff=0.1)
            
            word_groups, idx = [], 0
            for w in words:
                n = len(w)
                word_groups.append(VGroup(*full_text[idx: idx + n]))
                idx += n
            return caption_bg, accent, full_text, word_groups

        def show_caption(text, run_time=4.0, wait_time=0.3, font_size=19):
            new_bg, new_accent, full_text, word_groups = build_caption(text, font_size)
            if not bg_on[0]:
                self.play(FadeIn(new_bg, shift=UP * 0.15),
                          FadeIn(new_accent, shift=UP * 0.15), run_time=0.4)
                cap_bg[0], cap_accent[0], bg_on[0] = new_bg, new_accent, True
            else:
                anims = [Transform(cap_bg[0], new_bg), Transform(cap_accent[0], new_accent)]
                if cap_words[0] is not None:
                    anims.append(FadeOut(cap_words[0], shift=DOWN * 0.05))
                self.play(*anims, run_time=0.4)
            words_vgroup = VGroup(*word_groups)
            self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.1) for g in word_groups],
                                  lag_ratio=0.25), run_time=run_time * 0.8)
            cap_words[0] = words_vgroup
            self.wait(wait_time)

        def remove_caption():
            if bg_on[0]:
                anims = [FadeOut(cap_bg[0], shift=DOWN * 0.15),
                         FadeOut(cap_accent[0], shift=DOWN * 0.15)]
                if cap_words[0] is not None:
                    anims.append(FadeOut(cap_words[0], shift=DOWN * 0.08))
                self.play(*anims, run_time=0.4)
                bg_on[0] = False

        # ================================================================
        # PART 1 — James Simons Photo
        # ================================================================
        try:
            simons_img = ImageMobject("20.jpg").scale_to_fit_height(5.5).move_to(UP * 0.2)
        except:
            # Fallback if image not found
            simons_img = RoundedRectangle(width=8, height=5).set_fill(GRAY, 0.5)
            simons_img.add(Text("20.jpg\n(James Simons)", color=WHITE).move_to(simons_img))

        self.play(FadeIn(simons_img, shift=UP * 0.1))
        
        show_caption("This is where James Simons chose a different path.", run_time=3.5)
        show_caption("American mathematician, billionaire hedge fund manager, and philanthropist regarded as the 'Quant King'.", run_time=5.5)
        show_caption("He earned his MIT bachelor's and a UC Berkeley PhD at age 23, later working as an NSA codebreaker.", run_time=5.5)
        
        remove_caption()
        self.play(FadeOut(simons_img))

        # ================================================================
        # PART 2 — Medallion vs S&P 500 Bar Chart
        # ================================================================
        show_caption("Jim Simons set up the Medallion Investment Fund...", run_time=3.5)
        
        returns_axes = Axes(
            x_range=[0, 15, 1], y_range=[-0.4, 1.0, 0.2], 
            x_length=10, y_length=4.5,
            axis_config={"color": GRAY, "include_numbers": False}
        ).move_to(UP * 0.7)
        
        returns_title = Text("Annual Returns: S&P 500 vs. Medallion Fund", font_size=28, color=WHITE).next_to(returns_axes, UP, buff=0.2)

        sp_data = [0.18, -0.05, 0.3, 0.08, 0.1, 0.38, 0.25, 0.22, 0.35, 0.28, -0.1, -0.22, -0.38, 0.05, 0.15]
        med_data = [0.1, 0.55, 0.4, 0.38, 0.7, 0.39, 0.32, 0.42, 0.99, 0.35, 0.28, 0.3, 0.45, 0.75, 0.8]
        
        bars = VGroup()
        for i in range(15):
            x_pos = returns_axes.c2p(i + 0.5, 0)[0]
            sp_bar = Rectangle(width=0.25, height=abs(returns_axes.c2p(0, sp_data[i])[1] - returns_axes.c2p(0, 0)[1]))
            sp_bar.set_fill(BLUE_D, 1).set_stroke(width=0)
            sp_bar.move_to([x_pos - 0.15, returns_axes.c2p(0, sp_data[i]/2)[1], 0])
            
            med_bar = Rectangle(width=0.25, height=abs(returns_axes.c2p(0, med_data[i])[1] - returns_axes.c2p(0, 0)[1]))
            med_bar.set_fill(LIGHT_GRAY, 1).set_stroke(width=0)
            med_bar.move_to([x_pos + 0.15, returns_axes.c2p(0, med_data[i]/2)[1], 0])
            
            bars.add(sp_bar, med_bar)

        zero_line = Line(returns_axes.c2p(0, 0), returns_axes.c2p(15, 0), color=WHITE, stroke_width=2)
        
        legend = VGroup(
            VGroup(Square(side_length=0.2, fill_color=LIGHT_GRAY, fill_opacity=1, stroke_width=0), Text("Medallion", font_size=20)).arrange(RIGHT),
            VGroup(Square(side_length=0.2, fill_color=BLUE_D, fill_opacity=1, stroke_width=0), Text("S&P 500", font_size=20, color=BLUE_D)).arrange(RIGHT)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(returns_axes, RIGHT, buff=0.3).shift(UP*0.5)

        ret_y_labels = VGroup(
            Text("0%", font_size=16).next_to(returns_axes.c2p(0, 0), LEFT, buff=0.15),
            Text("50%", font_size=16).next_to(returns_axes.c2p(0, 0.5), LEFT, buff=0.15),
            Text("100%", font_size=16).next_to(returns_axes.c2p(0, 1.0), LEFT, buff=0.15),
        )
        ret_x_labels = VGroup(
            Text("1990", font_size=16).next_to(returns_axes.c2p(2, -0.4), DOWN, buff=0.2),
            Text("2000", font_size=16).next_to(returns_axes.c2p(7, -0.4), DOWN, buff=0.2),
            Text("2010", font_size=16).next_to(returns_axes.c2p(12, -0.4), DOWN, buff=0.2),
        )
        ret_y_title = Text("Annual Return", font_size=20).rotate(PI/2).next_to(returns_axes, LEFT, buff=0.8)
        ret_x_title = Text("Year", font_size=20).next_to(returns_axes, DOWN, buff=0.6)
        
        returns_group = VGroup(returns_title, returns_axes, zero_line, legend, ret_y_labels, ret_x_labels, ret_y_title, ret_x_title)

        self.play(FadeIn(returns_group))
        self.play(LaggedStart(*[GrowFromCenter(bar) for bar in bars], lag_ratio=0.05), run_time=2.5)

        show_caption("...and every year for the next 30 years, the Medallion Fund delivered higher returns than the market average.", run_time=5.5)
        show_caption("And not just by a little bit. They returned 66% per year.", run_time=4.5)
        
        self.play(FadeOut(returns_group), FadeOut(bars))

        # ================================================================
        # PART 3 — Cumulative Profits Bar Chart
        # ================================================================
        cum_axes = Axes(
            x_range=[0, 20, 1], y_range=[0, 110, 20], 
            x_length=9, y_length=4.5,
            axis_config={"color": GRAY, "include_numbers": False}
        ).move_to(UP * 0.3)
        cum_title = Text("The Medallion Fund Cumulative Profits, $Bn", font_size=28, color=WHITE).next_to(cum_axes, UP, buff=0.2)

        exp_data = [0.1, 0.2, 0.5, 0.8, 1.2, 1.8, 2.5, 4.0, 6.0, 9.0, 13.0, 18.0, 25.0, 35.0, 48.0, 62.0, 78.0, 92.0, 105.0]
        cum_bars = VGroup()
        for i, val in enumerate(exp_data):
            x_pos = cum_axes.c2p(i + 0.8, 0)[0]
            bar = Rectangle(width=0.25, height=abs(cum_axes.c2p(0, val)[1] - cum_axes.c2p(0, 0)[1]))
            bar.set_fill(WHITE, 1).set_stroke(width=0)
            bar.move_to([x_pos, cum_axes.c2p(0, val/2)[1], 0])
            cum_bars.add(bar)

        cum_y_labels = VGroup(*[
            Text(str(i), font_size=16).next_to(cum_axes.c2p(0, i), LEFT, buff=0.15) 
            for i in range(0, 120, 20)
        ])
        
        years_list = range(1988, 2019, 2)
        cum_x_labels = VGroup(*[
            Text(str(year), font_size=14).next_to(cum_axes.c2p(idx * (20/15.0), 0), DOWN, buff=0.15).rotate(-PI/6)
            for idx, year in enumerate(years_list)
        ])
        
        cum_y_title = Text("$ Billions", font_size=20).rotate(PI/2).next_to(cum_axes, LEFT, buff=0.8)
        cum_x_title = Text("Year", font_size=20).next_to(cum_axes, DOWN, buff=0.7)

        cum_group = VGroup(cum_title, cum_axes, cum_y_labels, cum_x_labels, cum_y_title, cum_x_title)
        
        self.play(FadeIn(cum_group))
        self.play(LaggedStart(*[FadeIn(bar, shift=UP*0.2) for bar in cum_bars], lag_ratio=0.1), run_time=3)

        show_caption("At that rate of growth, $100 invested in 1988 would be worth $23.141 Billion today.", run_time=5.0)
        show_caption("This made Jim Simons easily the richest mathematician of all time.", run_time=4.5)

        self.play(FadeOut(cum_group), FadeOut(cum_bars))

        # ================================================================
        # PART 4A — Generic Neural Networks Diagram
        # ================================================================
        show_caption("He did not remove humans; his team was full of mathematicians, physicists, and data scientists.", run_time=5.5)
        show_caption("What was removed was emotional, moment-to-moment judgment in the execution of trades.", run_time=5.5)
        
        layers = [4, 7, 7, 1]
        nodes = VGroup()
        edges = VGroup()
        
        x_spacing = 2.5
        y_spacing = 0.6
        
        node_positions = []
        for i, num_nodes in enumerate(layers):
            layer_positions = []
            x = (i - len(layers)/2 + 0.5) * x_spacing
            for j in range(num_nodes):
                y = (j - num_nodes/2 + 0.5) * y_spacing
                pos = np.array([x, y, 0]) + UP * 0.5
                layer_positions.append(pos)
                nodes.add(Dot(pos, radius=0.08, color=WHITE))
            node_positions.append(layer_positions)
            
        colors = [TEAL_C, MAROON_C, PURPLE, BLUE_D]
        for i in range(len(layers) - 1):
            for p1 in node_positions[i]:
                for p2 in node_positions[i+1]:
                    color = random.choice(colors)
                    stroke_w = random.uniform(0.5, 2.5)
                    edge = Line(p1, p2, color=color, stroke_width=stroke_w, stroke_opacity=0.6)
                    edges.add(edge)

        nn_group = VGroup(edges, nodes)
        
        self.play(Create(nodes, lag_ratio=0.1), run_time=1)
        self.play(Create(edges, lag_ratio=0.01), run_time=2.5)
        self.wait(1)
        self.play(FadeOut(nn_group))

        # ================================================================
        # PART 4B — CNN Architecture Diagram (Sync with remaining captions)
        # ================================================================
        def build_feature_maps(num_layers, size, dx, dy):
            stack = VGroup()
            for i in range(num_layers - 1, -1, -1):
                sq = Square(side_length=size, stroke_color="#5A3A29", stroke_width=1.5)
                if i % 2 == 1:
                    sq.set_fill("#B86F52", 1)
                else:
                    sq.set_fill("#EAC3B0", 1)
                sq.shift(RIGHT * i * dx + UP * i * dy)
                stack.add(sq)
            return stack

        input_sq = Square(side_length=1.6, stroke_color="#5A3A29", stroke_width=1.5).set_fill("#EAC3B0", 1)
        input_sq.move_to(LEFT * 5.8 + UP * 0.2)

        c1 = build_feature_maps(6, 1.2, 0.15, 0.15).next_to(input_sq, RIGHT, buff=1.2).shift(DOWN * 0.2)
        s1 = build_feature_maps(6, 1.2, 0.15, 0.15).next_to(c1, RIGHT, buff=0.6)
        
        c2 = build_feature_maps(8, 0.8, 0.15, 0.15).next_to(s1, RIGHT, buff=1).shift(UP * 0.2)
        s2 = build_feature_maps(8, 0.8, 0.15, 0.15).next_to(c2, RIGHT, buff=0.6)

        dots = VGroup(*[Dot(radius=0.06, color="#A86A4A") for _ in range(8)])
        dots.arrange(DOWN + RIGHT, buff=0.15)
        dots.next_to(s2, RIGHT, buff=0.8).shift(UP * 0.5)

        out_0 = Text("0", font_size=20, color=WHITE).next_to(dots[0], RIGHT, buff=1)
        out_1 = Text("1", font_size=20, color=WHITE).next_to(out_0, DOWN, buff=0.3)
        out_dots = VGroup(Dot(radius=0.06, color="#A86A4A").next_to(out_0, LEFT, buff=0.15),
                          Dot(radius=0.06, color="#A86A4A").next_to(out_1, LEFT, buff=0.15))

        l_color = WHITE
        l_stroke = 1.2
        
        l1 = Line(input_sq.get_right(), c1[-1].get_corner(UL), color=l_color, stroke_width=l_stroke)
        l2 = Line(input_sq.get_right(), c1[-1].get_left(), color=l_color, stroke_width=l_stroke)
        l3 = Line(input_sq.get_right(), c1[-1].get_corner(DL), color=l_color, stroke_width=l_stroke)
        
        l4 = Line(c1[0].get_corner(UR), s1[0].get_corner(UL), color=l_color, stroke_width=l_stroke)
        l5 = Line(c1[-1].get_corner(DR), s1[-1].get_corner(DL), color=l_color, stroke_width=l_stroke)

        l6 = Line(s1[-1].get_right(), c2[-1].get_corner(UL), color=l_color, stroke_width=l_stroke)
        l7 = Line(s1[-1].get_right(), c2[-1].get_corner(DL), color=l_color, stroke_width=l_stroke)
        
        l8 = Line(c2[0].get_corner(UR), s2[0].get_corner(UL), color=l_color, stroke_width=l_stroke)
        l9 = Line(c2[-1].get_corner(DR), s2[-1].get_corner(DL), color=l_color, stroke_width=l_stroke)

        l10 = Line(s2[0].get_corner(UR), dots[0].get_center(), color=l_color, stroke_width=l_stroke)
        l11 = Line(s2[-1].get_corner(DR), dots[-1].get_center(), color=l_color, stroke_width=l_stroke)
        
        l12 = Line(dots[0].get_center(), out_dots[0].get_center(), color=l_color, stroke_width=l_stroke)
        l13 = Line(dots[-1].get_center(), out_dots[1].get_center(), color=l_color, stroke_width=l_stroke)

        lbl_font = 14
        t_in = Text("Input 51X51", font_size=lbl_font, color=WHITE).next_to(input_sq, DOWN, buff=0.8)
        t_c1 = Text("C1 feature\nmaps 28X28", font_size=lbl_font, line_spacing=1, color=WHITE).next_to(c1, UP, buff=0.5)
        t_s1 = Text("S1 feature\nmaps 28X28", font_size=lbl_font, line_spacing=1, color=WHITE).next_to(s1, UP, buff=0.5)
        t_c2 = Text("C2 feature\nmaps 28X28", font_size=lbl_font, line_spacing=1, color=WHITE).next_to(c2, UP, buff=0.3)
        t_s2 = Text("S2 feature\nmaps 28X28", font_size=lbl_font, line_spacing=1, color=WHITE).next_to(s2, UP, buff=0.3)

        brace_y = s2.get_bottom()[1] - 0.7
        brace_feat = BraceBetweenPoints([input_sq.get_left()[0] + 0.2, brace_y, 0], 
                                        [s2.get_right()[0], brace_y, 0], 
                                        direction=DOWN, buff=0.1, color=BLUE_B)
        t_feat = brace_feat.get_text("Feature Extraction").set_color(WHITE).scale(0.7)
        
        brace_class = BraceBetweenPoints([dots.get_left()[0], brace_y, 0], 
                                         [out_1.get_right()[0], brace_y, 0], 
                                         direction=DOWN, buff=0.1, color=BLUE_B)
        t_class = brace_class.get_text("Classification").set_color(WHITE).scale(0.7)

        cnn_diagram = VGroup(
            input_sq, c1, s1, c2, s2, dots, out_dots, out_0, out_1,
            l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13,
            t_in, t_c1, t_s1, t_c2, t_s2,
            brace_feat, t_feat, brace_class, t_class
        ).scale(0.9).move_to(UP * 0.7)

        # Draw first part of CNN
        self.play(FadeIn(input_sq), Write(t_in), run_time=1)
        self.play(Create(VGroup(l1, l2, l3)), FadeIn(c1), Write(t_c1), run_time=0.8)
        self.play(Create(VGroup(l4, l5)), FadeIn(s1), Write(t_s1), run_time=0.8)

        show_caption("From this perspective, the output of the Fourier transform is not a definite prediction; rather, it is a feature extractor.", run_time=6.5)

        # Draw second part of CNN
        self.play(Create(VGroup(l6, l7)), FadeIn(c2), Write(t_c2), run_time=0.8)
        self.play(Create(VGroup(l8, l9)), FadeIn(s2), Write(t_s2), run_time=0.8)
        self.play(FadeIn(brace_feat), Write(t_feat), run_time=0.8)

        show_caption("In fact, the Fourier transform can be considered a first generation of hand-crafted feature engineering.", run_time=6.0)

        # Draw final part of CNN
        self.play(Create(VGroup(l10, l11)), FadeIn(dots), run_time=0.8)
        self.play(Create(VGroup(l12, l13)), FadeIn(out_dots), Write(out_0), Write(out_1), run_time=0.8)
        self.play(FadeIn(brace_class), Write(t_class), run_time=0.8)

        show_caption("The engineer analyzes the data, extracts the important features, and then gives them to the model.", run_time=5.5)
        show_caption("But in deep learning, neural networks learn many of these features automatically from raw data.", run_time=6.0)

        remove_caption()
        self.play(FadeOut(cnn_diagram))

        # ================================================================
        # PART 5 — Evolution Flowchart
        # ================================================================
        show_caption("So, the path of evolution can be summarized like this:", run_time=4.0)

        steps = [
            ("Classical\nMathematics", r"\int f(x) dx"),
            ("Signal\nAnalysis", r"\sin(\omega t)"),
            ("Feature\nEngineering", "Engine"),
            ("Machine\nLearning", "Weights"),
            ("Deep\nLearning", "Network")
        ]

        boxes = VGroup()
        for text, _ in steps:
            bg = RoundedRectangle(width=2.2, height=1.5, corner_radius=0.2, stroke_color=BLUE_C, stroke_width=2, fill_color="#121520", fill_opacity=1)
            lbl = Text(text, font_size=16, color=WHITE, line_spacing=1.2).move_to(bg)
            boxes.add(VGroup(bg, lbl))

        boxes.arrange(RIGHT, buff=0.6).move_to(UP * 0.5)

        arrows = VGroup()
        for i in range(len(boxes) - 1):
            arrow = Arrow(boxes[i].get_right(), boxes[i+1].get_left(), buff=0.1, color=GRAY, max_tip_length_to_length_ratio=0.15)
            arrows.add(arrow)

        flowchart = VGroup(boxes, arrows).scale(0.9)

        for i in range(len(boxes)):
            self.play(FadeIn(boxes[i], shift=UP * 0.2), run_time=0.6)
            if i < len(arrows):
                self.play(GrowArrow(arrows[i]), run_time=0.4)
        
        self.wait(2.5)

        remove_caption()
        self.play(FadeOut(flowchart, shift=DOWN * 0.3))

        # ================================================================
        # PART 6 — Centered Text (The Question)
        # ================================================================
        question_text = Text(
            "And now the next question is this:\n\n"
            "How does the machine learn these features,\n"
            "and how does it make decisions in a space full of uncertainty?",
            font_size=34,
            color=WHITE,
            line_spacing=1.3
        ).move_to(ORIGIN)
        
        self.play(Write(question_text), run_time=4.5)
        self.wait(2)
        self.play(FadeOut(question_text))

        final_text = Text(
            "That is exactly the subject of the next part of the presentation.",
            font_size=28, color=GRAY_B
        )
        self.play(FadeIn(final_text, shift=UP * 0.2))
        self.wait(3)
        self.play(FadeOut(final_text))
