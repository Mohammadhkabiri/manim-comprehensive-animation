from manim import *
import numpy as np

class BlackScholesToHeatScene(Scene):
    def construct(self):
        # ==========================================
        # Theme & Styling Setup
        # ==========================================
        self.camera.background_color = "#0f1117"

        # --- Subtitle System ---
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
                             line_spacing=1.1, font="sans-serif")
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
        # PART 1: The Black-Scholes Equation
        # ================================================================
        show_caption("In the 1970s, Black, Scholes, and Merton introduced a model that became the foundation of modern financial markets.", run_time=5)
        show_caption("This model shows that the price of an option is described by a partial differential equation:", run_time=5)

        bs_eq = MathTex(
            r"\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + rS \frac{\partial V}{\partial S} - rV = 0"
        ).scale(1.1).move_to(UP * 1)
        
        self.play(Write(bs_eq), run_time=2)
        
        vars_text = VGroup(
            Text("V: Option price", font_size=20),
            Text("S: Asset price", font_size=20),
            Text("t: Time", font_size=20),
            Text("r: Risk-free rate", font_size=20),
            Text("σ: Market volatility", font_size=20, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(bs_eq, DOWN, buff=0.5)

        self.play(FadeIn(vars_text, shift=UP * 0.2), run_time=1.5)
        show_caption("In this equation, V is the option price, S is the asset price, t is time, r is the risk-free rate, and σ is volatility.", run_time=6)
        show_caption("Do not worry about the formula; we are not going to solve it. We just want to focus on one parameter: σ.", run_time=5)
        
        self.play(FadeOut(vars_text))

        # ================================================================
        # PART 2: Why is it difficult? (Non-constant coefficients)
        # ================================================================
        show_caption("Why does a financial equation become exactly the same equation used in physics for heat diffusion?", run_time=5)
        show_caption("First, why is this equation difficult? Because its coefficients are not constant.", run_time=5)

        # Highlight S^2 and S
        s2_box = SurroundingRectangle(bs_eq[0][9:11], color=RED, buff=0.1)
        s_box = SurroundingRectangle(bs_eq[0][17], color=RED, buff=0.1)
        
        self.play(Create(s2_box), Create(s_box))
        show_caption("The asset price itself appears inside the coefficients (S and S²). Let us change variables.", run_time=5)
        
        self.play(FadeOut(s2_box), FadeOut(s_box), bs_eq.animate.to_edge(UP).scale(0.8))

        # ================================================================
        # PART 3: Step 1 - Logarithmic Space
        # ================================================================
        step1_title = Text("Step 1: Logarithmic Space", font_size=24, color=BLUE_B).move_to(UP*1.5 + LEFT*3)
        log_sub = MathTex(r"x = \ln\left(\frac{S}{K}\right) \implies S = K e^x").next_to(step1_title, DOWN, aligned_edge=LEFT, buff=0.3)
        
        self.play(FadeIn(step1_title), Write(log_sub))
        show_caption("Step One: Instead of the absolute price, we use the logarithm of relative price changes.", run_time=5)

        derivs = MathTex(
            r"\frac{\partial V}{\partial S} &= \frac{1}{S}\frac{\partial V}{\partial x} \\",
            r"\frac{\partial^2 V}{\partial S^2} &= \frac{1}{S^2}\left(\frac{\partial^2 V}{\partial x^2} - \frac{\partial V}{\partial x}\right)"
        ).scale(0.8).next_to(log_sub, DOWN, aligned_edge=LEFT, buff=0.5)

        self.play(FadeIn(derivs, shift=UP*0.2))
        show_caption("By applying the chain rule, we compute the new first and second derivatives.", run_time=4)

        eq_step1 = MathTex(
            r"\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 \frac{\partial^2 V}{\partial x^2} + \left(r - \frac{1}{2}\sigma^2\right)\frac{\partial V}{\partial x} - rV = 0"
        ).scale(0.9).move_to(DOWN*1)

        self.play(Transform(bs_eq, eq_step1), FadeOut(derivs), FadeOut(log_sub), FadeOut(step1_title))
        show_caption("Substituting these back, the troublesome dependencies disappear. Everything has become constant!", run_time=5)

        # ================================================================
        # PART 4: Step 2 & 3 - Time Reversal & Normalization
        # ================================================================
# ================================================================
# PART 4: Step 2 & 3 - Time Reversal & Normalization
# ================================================================
        step23_title = Text("Steps 2 & 3: Reversing & Normalizing Time", font_size=24, color=BLUE_B).move_to(UP*1.5 + LEFT*2)
        time_sub = MathTex(r"\tau = \frac{1}{2}\sigma^2(T - t), \quad k = \frac{2r}{\sigma^2}").next_to(step23_title, DOWN, aligned_edge=LEFT, buff=0.3)

        self.play(FadeIn(step23_title), Write(time_sub), bs_eq.animate.move_to(UP*3))
        show_caption("Step Two and Three: We reverse time to create an initial-value problem and normalize it to simplify the diffusion coefficient.", run_time=6)

        eq_step3 = MathTex(
            r"\frac{\partial v}{\partial \tau} = \frac{\partial^2 v}{\partial x^2} + (k-1)\frac{\partial v}{\partial x} - kv"
        ).scale(1).move_to(DOWN*0.5)

        self.play(
            Transform(bs_eq, eq_step3),
            FadeOut(step23_title),
            FadeOut(time_sub),
            run_time=1.2
        )
        show_caption("This looks closer, but we still have extra terms: the first-order derivative and the zero-order term.", run_time=5)

        # ================================================================
        # PART 5: Step 4 - Exponential Change of Variables
        # ================================================================
# ================================================================
# PART 5: Step 4 - Exponential Change of Variables
# ================================================================
        step4_title = Text("Step 4: Removing Extra Terms", font_size=24, color=BLUE_B).move_to(UP*1.5 + LEFT*3)
        exp_sub = MathTex(r"v(x,\tau) = e^{ax+b\tau}u(x,\tau)").next_to(step4_title, DOWN, aligned_edge=LEFT, buff=0.3)

        self.play(
            FadeOut(bs_eq),
            FadeIn(step4_title),
            Write(exp_sub),
            run_time=1
        )
        show_caption("Step Four: We multiply by an exponential factor to cancel out the extra terms.", run_time=4)


        ab_conditions = MathTex(
            r"a = \frac{1-k}{2}, \quad b = -\frac{(k+1)^2}{4}"
        ).next_to(exp_sub, DOWN, aligned_edge=LEFT, buff=0.4)

        self.play(FadeIn(ab_conditions, shift=UP*0.2))
        show_caption("By choosing specific values for 'a' and 'b', the extra drift and discounting terms vanish completely.", run_time=5)

        # ================================================================
        # PART 6: The Final Equation (Heat Equation)
        # ================================================================
        self.play(
            FadeOut(step4_title),
            FadeOut(exp_sub),
            FadeOut(ab_conditions),
            run_time=1
        )

        final_eq = MathTex(
            r"\frac{\partial u}{\partial \tau} = \alpha \frac{\partial^2 u}{\partial x^2}"
        ).scale(2).set_color(ORANGE).move_to(ORIGIN)

        show_caption("But this is where the beauty of mathematics appears...", run_time=3)
        self.play(FadeIn(final_eq, scale=0.5))

        show_caption("If we make a suitable change of variables, this equation turns into the heat equation.", run_time=5)

        heat_text = Text("The Heat Equation", font_size=36, color=RED_B).next_to(final_eq, UP, buff=0.8)
        self.play(FadeIn(heat_text, shift=DOWN*0.2))
