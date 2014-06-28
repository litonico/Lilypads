import sys
sys.path.append("..")

from graphics import Circle, Point, GraphWin
from random import random
from v2d import vadd, vsub, vmag, vnorm, vscale


def points(lilypads):
    return list(map(lambda x: x[:2],  lilypads))


def nearest_two(point, ptslist):  # nearest two points to given pt
    nearest_to_point = lambda x: vmag(vsub(x, point))
    ptslist.sort(key=nearest_to_point)
    return ptslist[:2]


def generate(generations):  # approx_pads_per_gen
    # lilypads: [[x, y, rad], [x1, y1, rad1], ...]
    center = [0.5, 0.5]
    print(center)
    lilypads = [center.append(1)]  # The middle lilypad
    print(lilypads)
    constraints = []
    genscale = lambda y: -y/generations + 1

    for i in range(generations):
        index = len(lilypads)
        rad = genscale(i)
        startingpos = [center[0] + random(), center[1] + random()]

        # Create constraints between the current point and center and
        # nearest two points
        if len(lilypads) > 1:
            nearests = nearest_two(startingpos, points(lilypads))
            print(nearests)
                
            constraints.append([[0, index],
                            [index, nearests[0]],
                            [index, nearests[1]]]
                            )
        else:
            constraints += [0, index]

        lilypads.append([startingpos[0], startingpos[1], rad])

        # Avoid collision with other lilypads
        satisfy_constraints(lilypads, constraints, 1)

        # jitter?

    return lilypads


def satisfy_constraints(verts, edges, iterations):
    print(edges)
    print(verts)
    for i in range(iterations):  # could be animated
        for edge in edges:
            restlen = verts[edge[0]][2] + verts[edge[1]][2]
            # Brain: melted by brackets.
            x1 = [verts[edge[0]][0], verts[edge[0]][1]]
            x2 = [verts[edge[1]][0], verts[edge[1]][1]]
            current_len = vmag(vsub(x2, x1))
            difference = vscale(
                            vnorm(vsub(x2, x1)),
                            ((restlen-current_len)/2)
                         )

            verts[edge[1]] = vadd(x2, difference)
            edge[0] = vadd(x1, difference)


def scale(lilypads, scalar, offset):
    for k in lilypads:
        k[0] = k[0] * scalar + offset
        k[1] = k[1] * scalar + offset
        k[2] = k[2] * scalar


def draw(lilypads, win):
    for pad in lilypads:
        Circle(Point(pad[0], pad[1]), pad[2]).draw(win)

lilypads = generate(6)
window = GraphWin("Lilypad Circles", 800, 800)
scale(lilypads, 5, 50)
draw(lilypads, window)
