from manim import *
import numpy as np

class TeamIntroScene(Scene):
    def construct(self):
        self.camera.background_color = "#0f1117"

        # ---------------------------------------------------------------
        # Subtitle System (Maintained exactly from your structure)
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
        # SCENE ANIMATIONS
        # ================================================================
        
        # Text Objects for Names
        name1 = Text("Mohammad Hossein Kabiri", font_size=28, color=TEAL_C).shift(UP * 1.5)
        name2 = Text("Mohammad Reza Izadi", font_size=28, color=TEAL_C).next_to(name1, DOWN, buff=0.4)
        name3 = Text("Seyed Amin Esmaeili", font_size=28, color=TEAL_C).next_to(name2, DOWN, buff=0.4)
        
        mentor_title = Text("Esteemed Mentor", font_size=24, color=GREY_B).next_to(name3, DOWN, buff=0.8)
        mentor_name = Text("Professor Ali Haghi", font_size=36, weight=BOLD, color=GOLD).next_to(mentor_title, DOWN, buff=0.2)
        
        students_group = VGroup(name1, name2, name3)
        mentor_group = VGroup(mentor_title, mentor_name)

        # 1. Introduce First Student
        show_caption("I’m Mohammad Hossein Kabiri, and alongside me are two of my university companions,", run_time=4.0)
        self.play(Write(name1), run_time=1.5)
        
        # 2. Introduce Other Students
        show_caption("Mohammad Reza Izadi and Seyed Amin Esmaeili,", run_time=3.5)
        self.play(
            FadeIn(name2, shift=UP * 0.2),
            FadeIn(name3, shift=UP * 0.2),
            run_time=1.5, lag_ratio=0.3
        )

        # 3. Introduce Mentor
        show_caption("as well as our esteemed mentor, Professor Ali Haghi.", run_time=3.5)
        self.play(
            FadeIn(mentor_title, shift=UP * 0.2),
            Write(mentor_name),
            run_time=2.0
        )
        
        # Add a subtle glowing effect to the mentor's name
        self.play(mentor_name.animate.set_color(YELLOW), run_time=1.0)
        self.play(mentor_name.animate.set_color(GOLD), run_time=1.0)

        # 4. Purpose Statement
        show_caption("Together, we’ve crafted this production with one purpose:", run_time=3.5)
        
        # Fade out names to focus on the message
        self.play(
            FadeOut(students_group, shift=UP * 0.2),
            FadeOut(mentor_group, shift=DOWN * 0.2),
            run_time=1.5
        )

        show_caption("to explore the quiet elegance and profound logic woven into the fabric of engineering mathematics.", run_time=5.0)
        show_caption("This isn’t just a lecture, it’s a narrative. A journey through the equations that shape our world,", run_time=5.0)
        show_caption("told through the lens of those who live and breathe them. Let us begin!", run_time=4.5)

        remove_caption()

        # ================================================================
        # FINAL HOOK: The main topic (Fourier & Cosmic Order)
        # ================================================================
        
        # You can change this to Persian if your Manim environment supports it
        final_topic_1 = Text("Discovering the Applications of Fourier", font_size=36, color=WHITE)
        final_topic_2 = Text("in the Cosmic Order", font_size=42, weight=BOLD, color=BLUE_C).next_to(final_topic_1, DOWN, buff=0.3)
        final_group = VGroup(final_topic_1, final_topic_2).move_to(ORIGIN)

        # Grand reveal with scaling and glowing
        self.play(
            FadeIn(final_group, scale=0.8),
            run_time=2.5, rate_func=rate_functions.ease_out_sine
        )
        
        # A beautiful lighting/shimmer effect across the text
        self.play(
            final_topic_2.animate.set_color(TEAL_A).scale(1.05),
            run_time=1.5, rate_func=rate_functions.there_and_back

        )
        
        self.wait(2.0)
        
        # Fade out to end scene
        self.play(FadeOut(final_group, scale=1.1), run_time=1.5)
        self.wait(1.0)
