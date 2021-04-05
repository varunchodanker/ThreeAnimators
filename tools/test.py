from manim import *

class Test(Scene):
    def construct(self):
        d1 = Dot(RIGHT).rotate_about_origin(1.57+0.1)
        l1 = Line().rotate(1.57+0.1)
        print(l1.get_angle())
        print(l1.get_end() == d1.get_center())
        self.add(l1,d1)
        self.wait()