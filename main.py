import turtle
import numpy as np
import random as r
from bra import *


#3D Face
class Face:
    def __init__(self, A: Vec3, B: Vec3, C: Vec3):
        #Asign verts
        self.verts = [A,B,C]

#3D Camera
class Camera:
    def __init__(self, focal_length, x, y):
        self.focal_length = focal_length
        self.x = x
        self.y = y

def calculate_vert(vert, camera, f):
    wX, wY, wZ = vert

    #calculate relative
    wX = wX - camera.x
    wY = wY - camera.y
    wZ = wZ - camera.z

    #calculate screenspace x



def flatten_face(face: Face, camera: Camera): #Returns a Triangle which is sceenspace equivalent of the face
    #Calculate each vert's screenspace equivalent



    finalA = 0
    finalB = 0
    finalC = 0
    triangle = Triange(finalA, finalB, finalC)


#2D Triangle
class Triange:
    def __init__(self, A: Vec2, B: Vec2, C: Vec2):
        #Create Turtle and colour
        self.turtle = turtle.Turtle()
        self.turtle.screen.colormode(255)
        self.turtle.color(r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
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
    Vec2(0,0),
    Vec2(0,100),
    Vec2(100,100)
]

triangle = Triange(points[0],points[1],points[2])

draw_triangle(triangle)

turtle.mainloop()