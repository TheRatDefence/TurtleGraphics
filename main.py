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
    def __init__(self, points):
        #Asign verts
        self.verts = points
        self.colour = (r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))

    def Translate(self, X, Y, Z):
        v = self.verts
        self.verts = Mat3([
            v[0,0] + X,v[0,1] + Y,v[0,2] + Z,
            v[1, 0] + X, v[1, 1] + Y, v[1, 2] + Z,
            v[2, 0] + X, v[2, 1] + Y, v[2, 2] + Z
        ])
    def Rotate(self, axis, angle):
        if axis == 'x':
            R = Mat3([
                1,          0,          0,
                0,          np.cos(angle),  -1 * np.sin(angle),
                0,          np.sin(angle),  np.cos(angle)
            ])
        elif axis == 'y':
            R = Mat3([
                np.cos(angle), 0, np.sin(angle),
                0, 1, 0,
                np.sin(angle) * -1, 0, np.cos(angle)
            ])
        elif axis == 'z':
            R = Mat3([
                np.arccos(angle), np.arcsin(angle) * -1, 0,
                np.arcsin(angle), np.arccos(angle), 0,
                0, 0, 1
            ])
            print(f"cos angle = {np.arccos(angle)}, sin anle = {np.arcsin(angle)}")
        A = R * Vec3(self.verts[0,0],self.verts[0,1],self.verts[0,2],)
        B = R * Vec3(self.verts[1,0],self.verts[1,1],self.verts[1,2],)
        C = R * Vec3(self.verts[2,0],self.verts[2,1],self.verts[2,2],)

        self.verts = Mat3([ A.x,A.y,A.z,
                            B.x,B.y,B.z,
                            C.x,C.y,C.z])


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
    wX, wY, wZ = vert
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
    v = face.verts
    #Calculate each vert's screenspace equivalent

    points = [calculate_vert((v[0,0],v[0,1],v[0,2]), camera),
              calculate_vert((v[1,0],v[1,1],v[1,2]), camera),
              calculate_vert((v[2,0],v[2,1],v[2,2]), camera)]

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
        wX = int(face.verts[i,0])
        wY = int(face.verts[i, 1])
        wZ = int(face.verts[i, 2])


        t.goto(vert.x,vert.y)

        colour = face.colour
        t.color(0, 0, 0)

        t.write(f"{wX}, {wY}, {wZ}")

        t.color(colour)

        i += 1

    #End fill
    t.end_fill()



points = Mat3([
        0, 0, 5,
        0, 1000, 5 ,
        1000, 1000, 5
    ])

face = Face(points)
camera = Camera(2.5005, 0,0,0)

frames = []

print('#' * 5)

matrix = Mat3([
    1,2,3,
    4,5,6,
    7,8,9,
])

print(matrix * matrix)

fps = 60
i = int(0)
dance = int(0)

face.Translate(0,0,10)

face.Rotate('z', 90)

running = True
while running:
    i += 1

    #face.Rotate('y', i * 0.00001)

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