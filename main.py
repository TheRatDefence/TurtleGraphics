import turtle
import numpy as np
import random as r
from bra import *


#3D Face
class Face:
    def __init__(self, A: Vec3, B: Vec3, C: Vec3):
        #Asign verts
        self.verts = [A,B,C]
        self.colour = (r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))

#3D Camera
class Camera:
    def __init__(self, focal_length, x, y, z):
        self.focal_length = focal_length
        self.x = x
        self.y = y
        self.z = z

def calculate_vert(vert, camera):
    wX = vert.x
    wY = vert.y
    wZ = vert.z
    f = camera.focal_length

    #calculate relative
    wX = wX - camera.x
    wY = wY - camera.y
    wZ = wZ - (camera.z - f)

    #calculate screenspace y
    Yangle = np.arctan(wY/wZ)
    sY = f * np.tan(Yangle)

    #calculate screenspace x
    Xangle = np.arctan(wX / wZ)
    sX = f * np.tan(Xangle)

    return Vec2(sX,sY)


def flatten_face(face: Face, camera: Camera): #Returns a Triangle which is sceenspace equivalent of the face
    points = []
    #Calculate each vert's screenspace equivalent
    for vert in face.verts:
        points.append(calculate_vert(vert, camera))

    return Triange(face, points[0], points[1], points[2])


#2D Triangle
class Triange:
    def __init__(self, face, A: Vec2, B: Vec2, C: Vec2):
        #Create Turtle and colour
        self.turtle = turtle.Turtle()
        self.turtle.speed(100000)
        self.turtle.screen.colormode(255)
        self.turtle.color(face.colour)
        self.turtle.hideturtle()

        #Asign verts
        self.verts = [A,B,C]

def draw_triangle(tri):
    #Assign vars
    t = tri.turtle
    verts = tri.verts

    #Lift pen and beguin fill
    t.up()
    t.begin_fill()

    t.goto(verts[-1].x,verts[-1].y)
    for vert in verts:
        t.goto(vert.x,vert.y)

    #End fill
    t.end_fill()

points = [
        Vec3(0, 0, 0),
        Vec3(0, 100, 0),
        Vec3(100, 100, 0)
    ]
face = Face(points[0], points[1], points[2])
camera = Camera(1, 0,0,0)

i = 0
running = True
while running:
    i += 1
    newpoints = [
        Vec3(0, 0, 0),
        Vec3(0, 100, i * -2),
        Vec3(100, 100, 0)
    ]
    face.verts = newpoints
    triangle = flatten_face(face, camera)
    draw_triangle(triangle)
    turtle.clearscreen()


turtle.mainloop()