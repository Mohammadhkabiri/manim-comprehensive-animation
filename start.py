from manim import *
import numpy as np

class FourierIntroScene(Scene):
    def construct(self):
        self.camera.background_color = "#0f1117"

        # ---------------------------------------------------------------
        # Subtitle System (Maintained from previous scenes)
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
                             line_spacing=1.0, font="sans-serif")
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
        # INTRO TITLE
        # ================================================================
        main_title = Text("The Universal Language of Fourier",
                     font_size=34, weight=BOLD, color=BLUE_B,
                     font="sans-serif").to_edge(UP, buff=0.4)
        
        self.play(FadeIn(main_title, shift=DOWN * 0.2), run_time=1.2)

        show_caption("In this journey, we will explore how the Fourier Transform acts as a master key to the universe.", run_time=4.5)

        # ================================================================
        # PART 1: Nature & Galaxies (Order in the cosmos)
        # ================================================================
        show_caption("We will begin by discovering the hidden mathematical harmonies in nature and the vastness of galaxies.", run_time=5.5)

        # Creating a beautiful minimal spiral galaxy
        galaxy = VGroup()
        for offset, color in zip([0, np.pi], [BLUE_C, TEAL_C]):
            spiral_arm = ParametricFunction(
                lambda t: np.array([
                    (0.1 + 0.3 * t) * np.cos(t + offset),
                    (0.1 + 0.3 * t) * np.sin(t + offset),
                    0
                ]),
                t_range=[0, 4 * np.pi],
                color=color, stroke_width=3
            )
            galaxy.add(spiral_arm)
        
        galaxy.shift(UP * 0.3).scale(0.6)
        
        # Add a starry glow in the center
        core = Dot(galaxy.get_center(), radius=0.1, color=WHITE).set_opacity(0.8)
        galaxy.add(core)

        self.play(Create(galaxy, run_time=3.0, rate_func=smooth))
        self.play(Rotate(galaxy, angle=PI/2, run_time=4.0, rate_func=linear))

        # ================================================================
        # PART 2: Human Behavior & Economic Markets
        # ================================================================
        show_caption("Then, we will shift our focus to the complex and collective behavior of humanity...", run_time=4.5)
        
        # Prepare financial chart components
        axes = Axes(
            x_range=[0, 10, 1], y_range=[-3, 3, 1],
            x_length=6.0, y_length=2.5,
            axis_config={"color": GREY_B, "stroke_width": 1.4},
        ).shift(UP * 0.6)

        # A volatile, seemingly random market chart
        np.random.seed(42)
        market_data = [np.sin(x) + np.sin(3*x)*0.3 + np.random.uniform(-0.6, 0.6) for x in np.linspace(0, 10, 60)]
        market_chart = axes.plot_line_graph(
            x_values=np.linspace(0, 10, 60),
            y_values=market_data,
            line_color=RED_C,
            add_vertex_dots=False,
            stroke_width=2.5
        )

        # Morphing Galaxy into the Axes (smooth visual transition)
        self.play(ReplacementTransform(galaxy, axes), run_time=1.5)
        self.play(Create(market_chart), run_time=2.0)

        show_caption("...revealing how we can uncover underlying order within seemingly chaotic economic markets.", run_time=5.0)

        # Extracting the "order" (smooth sine wave) from the chaos
        smooth_trend = axes.plot(lambda x: np.sin(x), x_range=[0, 10], color=GREEN_C, stroke_width=4)
        trend_label = Text("Fundamental Pattern", font_size=18, color=GREEN_C).next_to(smooth_trend, UP, buff=0.2)

        self.play(market_chart.animate.set_opacity(0.3), Create(smooth_trend), run_time=2.0)
        self.play(FadeIn(trend_label, shift=UP*0.1))
        self.wait(1.5)

        # ================================================================
        # PART 3: Technology, AI, and Audio Processing
        # ================================================================
        show_caption("Finally, we will bridge the gap to modern technology and Artificial Intelligence.", run_time=4.5)

        self.play(
            FadeOut(trend_label),
            FadeOut(market_chart),
            FadeOut(smooth_trend),
            FadeOut(axes),
            run_time=1.0
        )

        # Creating a digital/AI audio waveform
        audio_bars = VGroup()
        for i, x in enumerate(np.linspace(-4.5, 4.5, 55)):
            # Math formula for a cool symmetric waveform shape
            height = (np.sin(x*4)**2 + np.cos(x*1.5)) * np.exp(-x**2/6) * 1.3
            color_val = interpolate_color(TEAL_C, BLUE_D, abs(x)/4.5)
            bar = Line([x, -abs(height), 0], [x, abs(height), 0], color=color_val, stroke_width=4.5)
            audio_bars.add(bar)
        
        audio_bars.shift(UP * 0.4)

        self.play(LaggedStart(*[GrowFromCenter(bar) for bar in audio_bars], lag_ratio=0.03), run_time=2.0)

        show_caption("We will see how Fourier analysis enables machines to perceive, understand, and generate human voice.", run_time=5.5)

        # Morphing audio bars to represent "AI Nodes/Data"
        ai_nodes = VGroup()
        for bar in audio_bars:
            dot_top = Dot(bar.get_end(), radius=0.04, color=YELLOW)
            dot_bottom = Dot(bar.get_start(), radius=0.04, color=YELLOW)
            ai_nodes.add(dot_top, dot_bottom)

        self.play(
            audio_bars.animate.set_stroke(opacity=0.3),
            FadeIn(ai_nodes),
            run_time=1.5
        )
        
        # A subtle glowing animation
        self.play(ai_nodes.animate.set_color(WHITE), run_time=1.5)

        # ================================================================
        # OUTRO / TRANSITION
        # ================================================================
        remove_caption()

        self.play(
            FadeOut(main_title, shift=UP * 0.2),
            FadeOut(audio_bars, shift=DOWN * 0.2),
            FadeOut(ai_nodes, scale=1.2),
            run_time=1.5
        )

        # Final hook text
        hook = Text("Let's dive in.", font_size=32, color=WHITE, font="sans-serif", weight=BOLD)
        self.play(FadeIn(hook, scale=0.9))
        self.wait(1.5)
        self.play(FadeOut(hook))
        self.wait(0.5)
