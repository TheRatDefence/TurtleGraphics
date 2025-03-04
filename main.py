import turtle
import time
import numpy as np
import random as r
from bra import *

def turt_init():
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.screen.colormode(255)
    t.color(face.colour)
    turtle.hideturtle()
    turtle.tracer(0)
    return t
#3D Face
class Face:
    def __init__(self, A: Vec3, B: Vec3, C: Vec3):
        #Asign verts
        self.verts = [A,B,C]
        self.colour = (r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))

    def Translate(self, X, Y, Z):
        for point in self.verts:
            point.x += X
            point.y += Y
            point.z += Z

#3D Camera
class Camera:
    def __init__(self, focal_length, x, y, z):
        self.focal_length = focal_length
        self.x = x
        self.y = y
        self.z = z
#2D Triangle
class Triange:
    def __init__(self, face, A: Vec2, B: Vec2, C: Vec2):
        #Create Turtle and colour
        self.turtle = turt_init()

        #Asign verts
        self.verts = [A,B,C]

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

def draw_triangle(tri, face):
    #Assign vars
    t = tri.turtle
    verts = tri.verts

    #Lift pen and begin fill
    t.clear()
    t.up()
    t.begin_fill()

    t.teleport(verts[-1].x,verts[-1].y)
    i = 0
    for vert in verts:
        wX = int(face.verts[i].x)
        wY = int(face.verts[i].y)
        wZ = int(face.verts[i].z)


        t.goto(vert.x,vert.y)

        colour = face.colour
        t.color(0, 0, 0)

        t.write(f"{wX}, {wY}, {wZ}")

        t.color(colour)

        i += 1

    #End fill
    t.end_fill()



points = [
        Vec3(-100, -100, 5),
        Vec3(0, 1000, 5 ),
        Vec3(1000, 1000, 5)
    ]

face = Face(points[0], points[1], points[2])
camera = Camera(2.5005, 0,0,0)

frames = []

print('#' * 5)


fps = 60
i = int(0)
dance = int(0)
running = True
while running:
    i += 1


    if i < 1500:
        dance += 1
        face.Translate(0, 0, dance * 0.00001)
    elif i < 2000:
        dance += 1
        dance = i - dance
        face.Translate(0, 0, dance * -0.00001)
    elif i < 6000:
        face.Translate(r.randint(-1,1),r.randint(-1,1),r.randint(-1,1))

    #Stores, draws, clears and removes frames
    frames.append(flatten_face(face, camera))


    if i > 3:
        frames[2].turtle.clear()
        draw_triangle(frames[3], face)
        frames.pop(1)


    turtle.update()
    if i % 60 == 0:
        end_time = time.time()
        try:
            fps = round((fps + (60 / (end_time - start_time))) / 2, 1)
            print(f"FPS: {fps}")
        except:
            print("Loading FPS")
        start_time = time.time()



turtle.mainloop()