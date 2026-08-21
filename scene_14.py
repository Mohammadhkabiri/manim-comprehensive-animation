from manim import *
import numpy as np

class FourierSignalProcessor(Scene):
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
        # PART 1 — Introduction & Theoretical Transition
        # ================================================================
        show_caption("We have seen the theoretical beauty of Fourier in the roots of the Heat Equation.", run_time=3.5)
        show_caption("But in the practical world of trading, he plays a much more hands-on role.", run_time=3.5)
        remove_caption()

        # Centered mathematical context requirement (Not a subtitle)
        vol_text_base = Text("To use the Black-Scholes model, we need one crucial input: Volatility", font_size=24, color=WHITE)
        sigma_symbol = MathTex(r"(\sigma)", font_size=32, color=BLUE_B)
        vol_statement_group = VGroup(vol_text_base, sigma_symbol).arrange(RIGHT, buff=0.15).move_to(ORIGIN)

        self.play(FadeIn(vol_statement_group, shift=UP * 0.2))
        self.wait(2.5)
        self.play(FadeOut(vol_statement_group, shift=DOWN * 0.2))

        # ================================================================
        # PART 2 — Volatility & The Noisy VIX Charts (Images 7 & 8)
        # ================================================================
        # Top-of-screen context title label
        vix_header = Text("VIX; Chicago Board Options Exchange's CBOE Volatility Index", font_size=18, color=GRAY_A)
        vix_header.to_edge(UP, buff=0.4)
        self.play(Write(vix_header))

        # Load and set up asset image 7 & 8
        img7 = ImageMobject("7.jpg").scale_to_fit_height(4.2).move_to(UP * 0.3)
        img8 = ImageMobject("8.jpg").scale_to_fit_height(4.2).move_to(UP * 0.3)

        show_caption("Volatility is extracted from past price behavior. But here is the problem: a raw price chart is a mess.", run_time=4.5)
        self.play(FadeIn(img7, shift=UP * 0.1))
        
        show_caption("It is a chaotic mix of noise, news shocks, and short-term emotional spikes. If you feed 'noise' into a model, you get 'noise' out.", run_time=5.5)
        # Cross-fade cleanly from image 7 to image 8
        self.play(FadeOut(img7, run_time=0.4), FadeIn(img8, run_time=0.4))
        self.wait(2.0)

        # Clean up chart view before procedural section
        remove_caption()
        self.play(FadeOut(img8), FadeOut(vix_header))

        # ================================================================
        # PART 3 — High-Precision Signal Filter & Fourier Decomposition
        # ================================================================
        show_caption("This where the Fourier Transform enters the stage—as a High-Precision Signal Filter.", run_time=4.0)
        show_caption("Think of the market like a complex audio track. There is the loud, distracting 'static' of day-to-day noise...", run_time=4.5)

        # Minimalist Procedural Signal Processing Graph Representation
        signal_axis = Axes(x_range=[0, 3.2, 0.5], y_range=[-1.5, 1.5, 1], x_length=7, y_length=2.2, axis_config={"stroke_opacity": 0.2}).move_to(UP * 1.5)
        
        # Generator for clean vs noisy composite cycles
        def macro_cycle(x): return 0.6 * np.sin(2 * np.pi * x)
        def noisy_signal(x): return macro_cycle(x) + 0.25 * np.cos(8 * np.pi * x) + 0.12 * np.sin(22 * np.pi * x)

        graph_noisy = signal_axis.plot(noisy_signal, color=RED_B, stroke_width=2.5)
        graph_clean = signal_axis.plot(macro_cycle, color=GREEN_C, stroke_width=3.5)

        
        label_noisy = Text("Raw Complex Signal (Noise Included)", font_size=14, color=RED_B).next_to(signal_axis, UP, buff=0.1)

        self.play(Create(signal_axis), run_time=0.5)
        self.play(Create(graph_noisy), FadeIn(label_noisy), run_time=2.0)
        
        show_caption("...and then there are the deep, underlying 'rhythms' or structural cycles.", run_time=4.0)
        show_caption("Fourier allows us to decompose this complex price signal into its constituent frequencies.", run_time=4.5)

        # Decomposed Frequencies (Spectrum breakdown view below)
        decomp_axis = Axes(
    x_range=[0, 3.2, 0.5],
    y_range=[-1, 1, 1],
    x_length=7,
    y_length=1.4,
    axis_config={"stroke_opacity": 0.15}
).move_to(DOWN * 1.55)

        label_clean = Text("Extracted Dominant Underling Rhythm", font_size=14, color=GREEN_C).next_to(decomp_axis, UP, buff=0.22)

        down_arrow = Arrow(start=signal_axis.get_bottom(), end=label_clean.get_top(), color=BLUE_D, stroke_width=3, max_tip_length_to_length_ratio=0.15)

        graph_clean2 = decomp_axis.plot(macro_cycle, color=GREEN_C, stroke_width=3.5)
        self.play(
            Create(decomp_axis),
            GrowArrow(down_arrow),
            Create(graph_clean),
            Create(graph_clean2),
            FadeIn(label_clean),
            run_time=2.5
        )

        
        show_caption("By doing this, we can isolate the dominant cycles and filter out the high-frequency noise.", run_time=4.5)
        self.wait(1.5)

        # Clear procedural graph elements
        remove_caption()
        self.play(
            FadeOut(signal_axis), FadeOut(graph_noisy), FadeOut(graph_clean),FadeOut(graph_clean2),
            FadeOut(label_noisy), FadeOut(decomp_axis), FadeOut(down_arrow), FadeOut(label_clean)
        )

        # ================================================================
        # PART 4 — Next Gen Indicators Slide Sequence (Images 9 to 13)
        # ================================================================
        show_caption("This is exactly how the next generation of Technical Indicators is born.", run_time=3.5)

        # Array configuration to step through indicator figures one-by-one safely
        indicator_files = ["9.jpg", "10.jpg", "11.jpg", "12.jpg", "13.jpg"]
        active_image = [None]

        show_caption("Unlike traditional indicators that often lag behind the market, Fourier-based Indicators are designed to adapt to the market’s current frequency.", run_time=6.0)
        
        # Load and present first indicator plot (9.jpg)
        active_image[0] = ImageMobject(indicator_files[0]).scale_to_fit_height(4.2).move_to(UP * 0.3)
        self.play(FadeIn(active_image[0], shift=UP * 0.1))
        self.wait(1.0)

        show_caption("They don’t just smooth the data; they reveal the underlying 'heartbeat' of the price action.", run_time=5.0)
        
        # Sequentially loop through the remaining images like turning a slide page
        for file_name in indicator_files[1:]:
            next_image = ImageMobject(file_name).scale_to_fit_height(4.2).move_to(UP * 0.3)
            self.play(
                FadeOut(active_image[0], shift=LEFT * 0.4),
                FadeIn(next_image, shift=RIGHT * 0.4),
                run_time=0.9,
                rate_func=smooth,
            )

            active_image[0] = next_image
            self.wait(1.2)

        # ================================================================
        # PART 5 — Grounded Reality & Feature Extraction Conclusion
        # ================================================================
        show_caption("However, we must remain grounded. Fourier is a powerful tool, but it is not a Crystal Ball.", run_time=4.5)
        
        # Dim the final image slightly to emphasize ground truth thoughts
        self.play(active_image[0].animate.set_opacity(0.25), run_time=0.8)

        show_caption("It does not predict the future. Instead, it acts as a Feature Extractor.", run_time=4.0)
        show_caption("It clarifies the current structure of the data, identifies the dominant cycles, and reduces the noise.", run_time=5.0)
        show_caption("It tells us where we are and what the 'market rhythm' looks like right now, providing the clean features we need for better analysis.", run_time=6.0)

        # Final smooth exit transition
        remove_caption()
        self.play(FadeOut(active_image[0], shift=DOWN * 0.2), run_time=0.8)
        self.wait(1.0)