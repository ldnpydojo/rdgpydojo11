#!/usr/bin/env python

import pyglet
from pyglet.gl import *

import random
import math
from euclid import Vector3 as vec

F_SIZE = 20
SEG_HEIGHT = 1.5
ORBIT_DIST = 15
ORBIT_SPEED = 0.5

angle = 0

window = pyglet.window.Window()


def draw_floor():
    glColor3f(0, 0.5, 0)
    glBegin(GL_QUADS)
    glVertex3f(F_SIZE, 0, F_SIZE)
    glVertex3f(F_SIZE, 0, -F_SIZE)
    glVertex3f(-F_SIZE, 0, -F_SIZE)
    glVertex3f(-F_SIZE, 0, F_SIZE)
    glEnd()

WEIGHT_FACTOR = 0.87
RANDOMNESS = 1.3
UPWARD_BIAS = 0.2
BULK = 0.4


def draw_tree(pos, direction=vec(-0.1, SEG_HEIGHT, 0), weight=1.0):

    direction += RANDOMNESS * vec(random.random() - 0.5, random.random() - 0.5, random.random() - 0.5) + UPWARD_BIAS * vec(0, 1.0, 0)
    direction = direction.normalize()

    pos2 = pos + (direction * weight * SEG_HEIGHT)
    next_weight = weight * WEIGHT_FACTOR
    color = (0.5, 0.2, 0) if weight > 0.2 else (0.2, 0.6, 0.1)
    points = [(pos, pos2, color)]
    base_hex_list = [vec(math.sin(math.radians(a)),
        0,
        math.cos(math.radians(a))) for a in range(0, 361, 60)]
    bottom_hex_list = [pos + v * weight * BULK for v in base_hex_list]
    top_hex_list = [pos2 + v * next_weight * BULK for v in base_hex_list]
    glBegin(GL_TRIANGLE_STRIP)
    glColor3f(*color)
    for n, v1, v2 in zip(base_hex_list, bottom_hex_list, top_hex_list):
        glNormal3f(*n)
        glVertex3f(*v1)
        glVertex3f(*v2)
    glEnd()

    if weight > 0.2:
        branch = random.random() > (weight ** 2 - 0.5)
        if branch:
            rvec = vec(random.random() - 0.5, random.random() - 0.5, random.random() - 0.5)
            branch_direction = direction + rvec * (weight + 0.2)
            points.extend(
                draw_tree(pos2, branch_direction, next_weight)
            )
        points.extend(
            draw_tree(pos2, direction, next_weight))

    return points


dlist = glGenLists(1)
glNewList(dlist, GL_COMPILE)
draw_tree(vec(0, 0, 0))
glEndList()


@window.event
def on_draw():
    glClearColor(0.3, 0.4, 1.0, 1.0)
    window.clear()

    def v(*args):
        return (GLfloat * len(args))(*args)

    glLightfv(GL_LIGHT0, GL_POSITION,  v(-40, 50, 60, 0.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, v(0.7, 0.7, 0.7, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, v(0.1, 0.1, 0.1, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, window.width / float(window.height), 0.05, 100)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    eye = math.sin(angle) * ORBIT_DIST, 1.3, math.cos(angle) * ORBIT_DIST
    look_at = 0, 1.3, 0
    up = 0, 1, 0
    gluLookAt(*(eye + look_at + up))

    glDisable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)

    draw_floor()
    glCallList(dlist)


def on_update(dt):
    global angle
    angle += ORBIT_SPEED * dt

pyglet.clock.schedule(on_update)
pyglet.app.run()
