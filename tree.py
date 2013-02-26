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


def compute_tree(pos, direction=vec(-0.1, SEG_HEIGHT, 0), weight=1.0):
    points = [(pos)]

    direction += vec(random.random() - 0.5, random.random() - 0.5, random.random() - 0.5)
    direction = direction.normalize()

    pos2 = pos + (direction * weight * SEG_HEIGHT)
    points.append(pos2)

    if weight > 0.05:
        branch_direction = direction + vec(random.random() - 0.5, random.random() - 0.5, random.random() - 0.5)
        points.extend(
            compute_tree(pos2, direction, weight - 0.1))
        points.extend(
            compute_tree(pos2, branch_direction, weight - 0.1)
        )

    return points


tree = compute_tree(vec(0, 0, 0))


def draw_tree():
    glColor3f(0.8, 0.2, 0)
    glBegin(GL_LINES)
    for p in tree:
        glVertex3f(*p)
    glEnd()


@window.event
def on_draw():
    glClearColor(0.3, 0.4, 1.0, 1.0)
    window.clear()

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

    draw_floor()
    draw_tree()


def on_update(dt):
    global angle
    angle += ORBIT_SPEED * dt

pyglet.clock.schedule(on_update)
pyglet.app.run()
