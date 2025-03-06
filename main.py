import turtle
import time
from math import radians

import numpy as np
import random as r
from bra import *

def turtle_init():
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
    def __init__(self, p):
        #Asign verts
        self.verts = p
        self.colour = (r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))

    def Translate(self, X, Y, Z):
        v = self.verts
        self.verts = Mat3([
            v[0,0] + X,v[0,1] + Y,v[0,2] + Z,
            v[1, 0] + X, v[1, 1] + Y, v[1, 2] + Z,
            v[2, 0] + X, v[2, 1] + Y, v[2, 2] + Z
        ])

    def Rotate(self, axis, radians):
        angle = np.radians(radians)
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
                np.cos(angle),   np.sin(angle) * -1,  0,
                np.sin(angle),   np.cos(angle),       0,
                0,                  0,                      1
            ])

        A = R * Vec3(self.verts[0,0],self.verts[0,1],self.verts[0,2],)
        B = R * Vec3(self.verts[1,0],self.verts[1,1],self.verts[1,2],)
        C = R * Vec3(self.verts[2,0],self.verts[2,1],self.verts[2,2],)

        self.verts = Mat3([ A.x,A.y,A.z,
                            B.x,B.y,B.z,
                            C.x,C.y,C.z])


#3D Camera
class Camera:
    def __init__(self, x, y, z, near, far, fov):
        self.x = x
        self.y = y
        self.z = z
        self.near = near
        self.far = far
        self.fov = fov

    def Translate(self, X, Y, Z):
        v = self
        v.x += X
        v.y += Y
        v.z += Z


    def Rotate(self, axis, radians):
        angle = np.radians(radians)
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
                np.cos(angle),   np.sin(angle) * -1,  0,
                np.sin(angle),   np.cos(angle),       0,
                0,                  0,                      1
            ])

        verts = R * Vec3(self.x,self.y,self.x)
        self.x,self.y,self.z = verts.x,verts.y,verts.z

#2D Triangle
class Triangle:
    def __init__(self, face, A: Vec2, B: Vec2, C: Vec2):
        print("Started def Triangle: ")
        #Create Turtle and colour
        self.turtle = turtle_init()

        #Asign verts
        self.verts = [A,B,C]
        print(f"\t|Triangle created with\nA = [{A.x},{A.y}]\nB = [{B.x},{B.y}]\nC = [{C.x},{C.y}]")

def calculate_vert(vert, camera):
    print(f"Started def calculate_vert:")
    Px, Py, Pz = vert

    dX, dY, dZ = 1,1,1
    print(f"\t| Vert: {vert}")
    print(f"\t| Camera cords: {camera.x}, {camera.y}, {camera.z}")


    dZ = Pz - camera.z
    dY = Py - camera.y
    dX = Px - camera.x


    if dY != 0:
        Yprime = round(camera.near * (dZ / dY),1)
        Xprime = round(camera.near * (dX / dY),1)
        #Xprime = 0
    else:
        Yprime = camera.near
        Xprime = camera.near


    print(f"\t| screen-space X,Y = {Xprime, Yprime}")
    return Vec2(Xprime, Yprime)


def flatten_face(face: Face, camera: Camera): #Returns a Triangle which is sceenspace equivalent of the face
    points = []
    v = face.verts
    #Calculate each vert's screenspace equivalent
    points = [calculate_vert((v[0,0],v[0,1],v[0,2]), camera),
              calculate_vert((v[1,0],v[1,1],v[1,2]), camera),
              calculate_vert((v[2,0],v[2,1],v[2,2]), camera)]

    return Triangle(face, points[0], points[1], points[2])

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
        wX = face.verts[i,0]
        wY = face.verts[i,1]
        wZ = face.verts[i,2]


        t.goto(vert.x,vert.y)

        colour = face.colour
        t.color(0, 0, 0)

        t.write(f"{round(wX)}, {round(wY)}, {round(wZ)}")

        t.color(colour)

        i += 1

    #End fill
    t.end_fill()







print("Running mainloop:")


points = Mat3([
        0, 10, 0,
        0, 10, 1000,
        1000, 10, 1000
    ])



face = Face(points)
print(f"\t| World space points = \n{face.verts}")


camera = Camera(0,0,0, 1, 2000, 90)
print(f"\t| Camera at {camera.x},{camera.y},{camera.z}")






def on_motion(event):
    global mouse_x, mouse_y
    mouse_x = event.x - turtle.window_width() / 2
    mouse_y = -event.y + turtle.window_height() / 2
def move_face(face, frame, lastframe):
    x,y = frame
    lx, ly = lastframe
    dx,dy = x - lx, y - ly
    face.Translate(dx * 0.01, dy * 0.01, 0)
def rotate_face(face, frame, lastframe):
    x, y = frame
    lx, ly = lastframe
    dx, dy = x - lx, y - ly
    face.Rotate('z', dx)
def rotate_camera(camera, frame, lastframe):
    x, y = frame
    lx, ly = lastframe
    dx, dy = x - lx, y - ly
    face.Rotate('z', dx)
def move_camera(camera, frame, lastframe):
    x,y = frame
    lx, ly = lastframe
    dx,dy = x - lx, y - ly
    camera.Translate(dx * 0.01, dy * 0.01, 0)


mouse_x, mouse_y = 0,0
cords = []
turtle.getcanvas().bind("<Motion>", on_motion)

frames = []
fps = 60
i = int(0)
print("Started mainloop:")
running = True
while running:
    i += 1

    cords.append((mouse_x, mouse_y))
    if i > 2:
        cords.remove(cords[0])
        #move_face(face, cords[-1], cords[-2])

    #Stores, draws, clears and removes frames
    frames.append(flatten_face(face, camera))
    if i > 2:
        frames[1].turtle.clear()
        draw_triangle(frames[2], face)
        turtle.turtles().remove(frames[1].turtle)
        frames.pop(1)



    turtle.update()
    if i % 60 == 0:
        #face.Rotate('y', 1)
        camera.Translate(0,0,0)
        #print(camera.x)
        #camera.Rotate('y', 20)
        end_time = time.time()
        try:
            fps = round((fps + (60 / (end_time - start_time))) / 2, 1)
            print(f"\t| FPS: {fps}")
        except:
            print("\t| Loading FPS")
        start_time = time.time()



turtle.mainloop()