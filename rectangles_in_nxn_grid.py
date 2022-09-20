import numpy as np
from manim import *

# BOTTOM = -3
# TOP = 3
# LEFT = -6
# RIGHT = 6

class nxn_grid(ThreeDScene):
    def construct(self):
        size = 6
        speed = 1
        square_size = 0.5
        cube_size = 0.25
        total_num = ((size * (size + 1)) // 2) ** 2

        squares = [[Square(side_length=square_size, stroke_width=0.5, stroke_color=BLACK, fill_color=PURE_GREEN, fill_opacity=0.1).shift(i*square_size*RIGHT + j*square_size*UP + -0.5*size*square_size*DL) for i in range(size)] for j in range(size)]
        cubes = []
        for n in range(1, size+1):
            cubes.append([Cube(side_length=cube_size, fill_color=BLUE, stroke_width=0.3, stroke_opacity=1, stroke_color=BLACK).shift(i*cube_size*RIGHT+j*cube_size*UP+k*cube_size*OUT) for i in range(n) for j in range(n) for k in range(n)])
        vcubes = []
        for big_cube in cubes:
            vcubes.append(VGroup(*big_cube).rotate(90*DEGREES, RIGHT).rotate(45*DEGREES, UL).rotate(-90*DEGREES, UP))
        grid = VGroup(*[s for slist in squares for s in slist])

        counter = Text(f"0 / {total_num}").move_to(np.array((-3,3,0)))
        self.add(counter)
        self.add(grid.move_to(np.array((-3,0,0))))
        self.wait(1)

        def light_rectangles():
            for x1 in range(size):
                for y1 in range(size):
                    for x2 in range(x1, size):
                        for y2 in range(y1, size):
                            for x in range(x1, x2+1):
                                for y in range(y1, y2+1):
                                    squares[x][y].set_fill(opacity=1)
                            self.wait(0.1 * speed)
                            yield
                            for x in range(x1, x2+1):
                                for y in range(y1, y2+1):
                                    squares[x][y].set_fill(opacity=0.1)
                            self.wait(0.02 * speed)


        def show_cubes():
            new_cube = np.array((3, 3.8, 0))
            for i in range(size):
                for cube in cubes[i]:
                    self.add(cube)
                    yield new_cube
                for cube in cubes[i]:
                    self.remove(cube)
                old_cube = new_cube
                new_cube=Cube(side_length=cube_size*(i+1), fill_color=BLUE, stroke_width=0.3, stroke_opacity=1, stroke_color=BLACK).rotate(90*DEGREES, RIGHT).rotate(45*DEGREES, UL).rotate(-90*DEGREES, UP)
                self.play(new_cube.animate.next_to(old_cube, DOWN))


        lr = light_rectangles()
        sc = show_cubes()

        for num in range(1, total_num+1):
            f_cube = next(sc)
            next(lr)
            self.remove(counter)
            counter = Text(f"{num} / {total_num}").move_to(np.array((-3, 3, 0)))
            self.add(counter)

        for cube in cubes[-1]:
            self.remove(cube)
        self.play(Cube(side_length=cube_size * (size), fill_color=BLUE, stroke_width=0.3, stroke_opacity=1,
                       stroke_color=BLACK).rotate(90 * DEGREES, RIGHT).rotate(45 * DEGREES, UL).rotate(-90 * DEGREES,
                                                                                                       UP).animate.next_to(f_cube, DOWN))