from matplotlib import pyplot as plt
import random
import numpy as np
from matplotlib.animation import FuncAnimation
import math

speed = 1/50 # 1/50, How far each particle will go per update
accuracy = 0.97 # 0.97, How reliably each particle will move in the right direction
energy_loss = 0.005 # 0.005, How fast the velocity decreases
show_centers = False # False, Show centers of each group

point_num = 10000

fig, ax = plt.subplots()

bx=[]
by=[]
bsize = 100
bcenter = (500, 500)
rx=[]
ry=[]
rsize = 100
rcenter = (-500, -500)

for _ in range(point_num):
    _bx = random.uniform(bcenter[0]-bsize/2, bcenter[0]+bsize/2)
    _by = random.uniform(bcenter[1]-bsize/2, bcenter[1]+bsize/2)
    while (_bx-bcenter[0])**2 + (_by-bcenter[1])**2 > (bsize/2)**2:
        _bx = random.uniform(bcenter[0] - bsize / 2, bcenter[0] + bsize / 2)
        _by = random.uniform(bcenter[1] - bsize / 2, bcenter[1] + bsize / 2)
    bx.append([_bx, 0])
    by.append([_by, 0])
    _rx = random.uniform(rcenter[0]-rsize/2, rcenter[0]+rsize/2)
    _ry = random.uniform(rcenter[1]-rsize/2, rcenter[1]+rsize/2)
    while (_rx-rcenter[0])**2 + (_ry-rcenter[1])**2 > (rsize/2)**2:
        _rx = random.uniform(rcenter[0] - rsize / 2, rcenter[0] + rsize / 2)
        _ry = random.uniform(rcenter[1] - rsize / 2, rcenter[1] + rsize / 2)
    rx.append([_rx, 0])
    ry.append([_ry, 0])

bxavg = sum([i[0] for i in bx]) / len(bx)
byavg = sum([i[0] for i in by]) / len(by)
rxavg = sum([i[0] for i in rx]) / len(rx)
ryavg = sum([i[0] for i in ry]) / len(ry)

xavg = (bxavg + rxavg) / 2
yavg = (byavg + ryavg) / 2

for i in range(point_num):
    bx[i][1] = (rxavg - bx[i][0])
    by[i][1] = (ryavg - by[i][0])
    rx[i][1] = (bxavg - rx[i][0])
    ry[i][1] = (byavg - ry[i][0])

plt.xlim(-2000, 2000)
plt.ylim(-2000, 2000)
ax.set_aspect(1.0/ax.get_data_ratio())

blue = ax.scatter([i[0] for i in bx], [i[0] for i in by], s=1, color='#1495cc')
red = ax.scatter([i[0] for i in rx], [i[0] for i in ry], s=1, color='#d62728')
if show_centers:
    center = ax.scatter([xavg, bxavg, rxavg], [yavg, byavg, ryavg], s=20, c=['#000000', '#0d5370', '#7a1515'])
    plot = [blue, red, center]
else:
    plot = [blue, red]

def init():
    blue.set_offsets([])
    red.set_offsets([])
    if show_centers: center.set_offsets([])

    return plot

def update(iteration):
    rxavg = sum([i[0] for i in rx]) / len(rx)
    ryavg = sum([i[0] for i in ry]) / len(ry)
    for i in range(point_num):
        move_dist = random.uniform(-(1-accuracy), 1)
        bxmove = move_dist * random.uniform(0, 1) * speed * bx[i][1]
        bymove = move_dist * random.uniform(0, 1) * speed * by[i][1]
        bx[i][0] += bxmove
        by[i][0] += bymove
    blue.set_offsets(np.c_[[i[0] for i in bx], [i[0] for i in by]])

    bxavg = sum([i[0] for i in bx]) / len(bx)
    byavg = sum([i[0] for i in by]) / len(by)
    for i in range(point_num):
        move_dist = random.uniform(-(1-accuracy), 1)
        rxmove = move_dist * random.uniform(0, 1) * speed * rx[i][1]
        rymove = move_dist * random.uniform(0, 1) * speed * ry[i][1]
        rx[i][0] += rxmove
        ry[i][0] += rymove
    red.set_offsets(np.c_[[i[0] for i in rx], [i[0] for i in ry]])

    xavg = (bxavg + rxavg) / 2
    yavg = (byavg + ryavg) / 2
    if show_centers: center.set_offsets(np.c_[[xavg, bxavg, rxavg], [yavg, byavg, ryavg]])

    for i in range(point_num):
        bx[i][1] = bx[i][1]/(1 + energy_loss) + (rxavg - bx[i][0])
        by[i][1] = by[i][1]/(1 + energy_loss) + (ryavg - by[i][0])
        rx[i][1] = rx[i][1]/(1 + energy_loss) + (bxavg - rx[i][0])
        ry[i][1] = ry[i][1]/(1 + energy_loss) + (byavg - ry[i][0])

    # ax.set_xlim(min([i[0] for i in bx] + [i[0] for i in rx]), max([i[0] for i in bx] + [i[0] for i in rx]))
    # ax.set_ylim(min([i[0] for i in by] + [i[0] for i in ry]), max([i[0] for i in by] + [i[0] for i in ry]))
    return plot

anim = FuncAnimation(fig, update, init_func=init, interval=1, blit=False)

plt.show()