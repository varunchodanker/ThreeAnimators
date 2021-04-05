from manim import *
import numpy as np


class CircleTheorems(Scene):
    def construct(self):
        self.theorem_1()

    def theorem_2(self):
        d = Dot().set_color(BLUE).move_to(3 * UP)
        dL = Dot().set_color(BLUE).move_to(3 * LEFT)
        dR = Dot().set_color(BLUE).move_to(3 * RIGHT)
        base = VGroup(
            Circle().scale(3).set_color(WHITE),
            Dot().set_color(BLUE),
            Line(dL.get_center(), dR.get_center())
        )

        moving_line1 = always_redraw(
            lambda: Line(d.get_center(), dL.get_center()).set_color(BLUE)
            .set_stroke(width=6)
        )

        moving_line2 = always_redraw(
            lambda: Line(d.get_center(), dR.get_center()).set_color(BLUE)
            .set_stroke(width=6)
        )

        moving_lines = VGroup(moving_line1, moving_line2)

        # the nested if else statements are used to flip the right angle
        # when dL and dR pass d to the other side
        right_angle = always_redraw(
            lambda: Square()
            # moving the right angle as the points move
            .move_to(
                d.get_center(),
                aligned_edge=(
                    DOWN + LEFT if d.get_center()[1] < 0 else UP + LEFT)
            )
            # rotating the right angle as the points move
            .rotate(
                (-1 if d.get_center()[1] < 0 else 1) *
                -np.arctan(
                    abs(
                        (d.get_center()[0] - dL.get_center()[0]) /
                        (d.get_center()[1] - dL.get_center()[1])
                    )
                ),
                about_point=d.get_center()
            )
            .scale(
                0.20,
                about_point=d.get_center()
            )
        )

        self.play(
            Write(base),
            Write(moving_lines),
            Write(dL),
            Write(dR),
            Write(right_angle)
        )
        self.play(
            Rotate(d, 45 * DEGREES, about_point=ORIGIN),
            run_time=1.7
        )
        self.wait(0.7)
        self.play(
            Rotate(d, -70 * DEGREES, about_point=ORIGIN),
            run_time=1.7
        )
        self.wait(0.7)
        self.play(
            Rotate(d, -40 * DEGREES, about_point=ORIGIN),
            run_time=1.7
        )
        self.wait(0.7)
        self.play(
            Rotate(d, -60 * DEGREES, about_point=ORIGIN),
            run_time=1.7
        )
        self.wait(0.7)
        self.play(
            Rotate(d, 65 * DEGREES, about_point=ORIGIN),
            run_time=1.7
        )
        self.wait(0.7)
        self.play(
            Rotate(d, -200 * DEGREES, about_point=ORIGIN),
            run_time=5.1
        )

    def generate_mv1(self, fed, rd): 
                        return Line(fed.get_center(), rd.get_center())

    def theorem_1(self):
            circle = Circle().scale(3).set_color(WHITE) #default circle with radius 3 in the manim grid
            centerDot = Dot()
            fixedEdgeDot = Dot().shift(3*UP)

            base = VGroup(
                circle, centerDot, fixedEdgeDot
            )

            leftDot = Dot().shift(3*DOWN)
            rightDot = Dot().shift(3*DOWN)

            moving_line1 = always_redraw(
                lambda: self.generate_mv1(fixedEdgeDot,rightDot)
            )
            moving_line2 = always_redraw(
                lambda: Line(fixedEdgeDot.get_center(), leftDot.get_center())
            )
            moving_line3 = always_redraw(
                lambda: Line(centerDot.get_center(), leftDot.get_center())
            )
            moving_line4 = always_redraw(
                lambda: Line(centerDot.get_center(), rightDot.get_center())
            )
            moving_lines = VGroup(moving_line1, moving_line2, moving_line3, moving_line4)

            updating_angle1 = always_redraw(
                lambda :
                    VGroup (
                    Arc(
                    arc_center=fixedEdgeDot.get_center(), 
                    radius=0.5, 
                    start_angle= moving_line1.get_angle(), 
                    angle = (moving_line2.get_angle()-moving_line1.get_angle())/2
                    ),
                    Arc(
                    arc_center=fixedEdgeDot.get_center(), 
                    radius=0.5, 
                    start_angle= moving_line2.get_angle()-((moving_line2.get_angle()-moving_line1.get_angle())/2), 
                    angle = (moving_line2.get_angle()-moving_line1.get_angle())/2
                    )
                    )
            )
            updating_angle2 = always_redraw(
                lambda :
                    VGroup ( 
                    Arc (
                        arc_center=centerDot.get_center(),
                        radius=0.5,
                        start_angle= moving_line4.get_angle(),
                        angle= (moving_line3.get_angle() - moving_line4.get_angle())/2
                    ),
                    Arc (
                        arc_center=centerDot.get_center(),
                        radius=0.5,
                        start_angle= moving_line3.get_angle() - ((moving_line3.get_angle() - moving_line4.get_angle())/2),
                        angle= (moving_line3.get_angle() - moving_line4.get_angle())/2
                    )
                    )
            )

            updating_angles = VGroup(updating_angle1, updating_angle2)

            self.play(Write(base), Write(moving_lines), Write(leftDot), Write(rightDot), Write(updating_angles))
            self.wait(0.7)
            self.play(
                Rotate(leftDot, 90 * DEGREES, about_point=ORIGIN),
                Rotate(rightDot, -90 * DEGREES, about_point=ORIGIN),
                run_time=2.8
            )
            self.wait(0.7)

            #(-pi,pi]
            #once working, replace arcs with sectors so can shade the region