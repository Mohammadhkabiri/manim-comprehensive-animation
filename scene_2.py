from manim import *
import numpy as np

class FourierScene2(Scene):
    def construct(self):
        self.camera.background_color = "#0f1117"

        # --- سیستم زیرنویس (دقیقاً مشابه سکانس ۱ برای حفظ یکدستی) ---
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
            if cur: lines.append(" ".join(cur))
            return lines

        def build_caption(text, font_size=28, max_chars=52):
            words = text.split()
            lines = wrap_words(words, max_chars)
            full_str = "\n".join(lines)
            full_text = Text(full_str, font_size=font_size, color=WHITE, line_spacing=1.0, font="DejaVu Sans")
            caption_bg = RoundedRectangle(corner_radius=0.18, height=full_text.height + 0.5, 
                                          width=min(full_text.width + 0.9, 12.8), stroke_color=BLUE_D, 
                                          stroke_width=1.4, fill_color="#0a0c14", fill_opacity=0.82)
            accent = RoundedRectangle(corner_radius=0.05, height=caption_bg.height - 0.22, width=0.08, 
                                      fill_color=BLUE_B, fill_opacity=0.9, stroke_opacity=0)
            full_text.move_to(caption_bg.get_center())
            VGroup(caption_bg, full_text).to_edge(DOWN, buff=0.4)
            accent.next_to(caption_bg.get_left(), RIGHT, buff=0.12)
            word_groups, idx = [], 0
            for w in words:
                n = len(w)
                word_groups.append(VGroup(*full_text[idx:idx + n]))
                idx += n
            return caption_bg, accent, full_text, word_groups

        def show_caption(text, run_time=3.5, wait_time=0.25, font_size=28):
            new_bg, new_accent, full_text, word_groups = build_caption(text, font_size)
            if not bg_on[0]:
                self.play(FadeIn(new_bg, shift=UP*0.18), FadeIn(new_accent, shift=UP*0.18), run_time=0.5)
                cap_bg[0], cap_accent[0], bg_on[0] = new_bg, new_accent, True
            else:
                anims = [Transform(cap_bg[0], new_bg), Transform(cap_accent[0], new_accent)]
                if cap_words[0] is not None: anims.append(FadeOut(cap_words[0], shift=DOWN*0.08))
                self.play(*anims, run_time=0.5)
            words_vgroup = VGroup(*word_groups)
            self.play(LaggedStart(*[FadeIn(g, shift=UP*0.14) for g in word_groups], lag_ratio=0.38), run_time=run_time)
            cap_words[0] = words_vgroup
            self.wait(wait_time)

        def remove_caption():
            if bg_on[0]:
                anims = [FadeOut(cap_bg[0], shift=DOWN*0.18), FadeOut(cap_accent[0], shift=DOWN*0.18)]
                if cap_words[0] is not None: anims.append(FadeOut(cap_words[0], shift=DOWN*0.1))
                self.play(*anims, run_time=0.5)
                bg_on[0] = False

        # -------------------------------------------------
        # شروع سکانس ۲
        # -------------------------------------------------
        title = Text("The Power of Combination", font_size=40, weight=BOLD, color=BLUE_B).to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.2))

        show_caption("In the previous part, we saw that a single sine wave is simple and pure.")

        # ایجاد محورها
        axes = Axes(x_range=[0, 2*PI, PI/2], y_range=[-2.2, 2.2, 1], x_length=10, y_length=4.5,
                    axis_config={"color": GREY_A}).shift(DOWN*0.2)
        
        # تعریف دو موج مختلف
        wave1 = axes.plot(lambda x: np.sin(x), x_range=[0, 2*PI], color=YELLOW)
        wave2 = axes.plot(lambda x: 0.5 * np.sin(3*x), x_range=[0, 2*PI], color=RED_B)
        
        self.play(Create(axes), run_time=1)
        self.play(Create(wave1), run_time=1.5)
        
        show_caption("But the real magic happens when we start adding these waves together.")

        self.play(Create(wave2), run_time=1.5)
        show_caption("Imagine two different sounds or signals overlapping in the same space.")

        # فرمول ترکیب
        sum_formula = MathTex(r"f(x) = \sin(x) + 0.5\sin(3x)", font_size=38).to_corner(UR, buff=0.7).shift(DOWN*0.8)
        self.play(Write(sum_formula))

        # موج حاصل‌جمع
        combined_wave = axes.plot(lambda x: np.sin(x) + 0.5 * np.sin(3*x), x_range=[0, 2*PI], color=WHITE, stroke_width=6)
        
        show_caption("By adding their values at every point, a new, more complex shape emerges.")

        # انیمیشن تبدیل (موج‌ها کمرنگ شوند و موج جدید ظاهر شود)
        self.play(
            wave1.animate.set_stroke(opacity=0.3),
            wave2.animate.set_stroke(opacity=0.3),
            Create(combined_wave),
            run_time=2.5
        )

        show_caption("This is no longer a simple sine wave, yet it is entirely made of them.")

        # یک مرحله پیچیده‌تر: اضافه کردن موج سوم
        wave3 = axes.plot(lambda x: 0.3 * np.sin(7*x), x_range=[0, 2*PI], color=GREEN_B, stroke_opacity=0.3)
        combined_wave_2 = axes.plot(lambda x: np.sin(x) + 0.5*np.sin(3*x) + 0.3*np.sin(7*x), 
                                     x_range=[0, 2*PI], color=BLUE_B, stroke_width=6)

        self.play(Create(wave3), run_time=1)
        self.play(
            Transform(combined_wave, combined_wave_2),
            FadeOut(sum_formula),
            run_time=2
        )

        show_caption("As we add more frequencies, the resulting signal becomes increasingly intricate.")

        show_caption("This is the core intuition of Joseph Fourier's groundbreaking discovery.")

        # پیام نهایی سکانس ۲
        remove_caption()
        self.play(FadeOut(VGroup(axes, wave1, wave2, wave3, combined_wave, title)))

        final_msg = Text("Any complex signal, no matter how irregular,\ncan be broken down into simple sine waves.",
                         font_size=32, line_spacing=1.2).move_to(ORIGIN)
        
        self.play(Write(final_msg), run_time=3)
        self.wait(2)
        
        transition_text = Text("But how do we find these hidden ingredients?", 
                               color=YELLOW, font_size=34).move_to(ORIGIN)
        
        self.play(FadeOut(final_msg, shift=UP*0.3))
        self.play(FadeIn(transition_text, shift=DOWN*0.2))
        self.wait(2.5)

        self.play(FadeOut(transition_text))
        self.wait(1)
