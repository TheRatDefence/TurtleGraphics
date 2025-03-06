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
        #Create Turtle and colour
        self.turtle = turtle_init()

        #Asign verts
        self.verts = [A,B,C]
        print(f"Triangle created with\nA = [{A.x},{A.y}]\nB = [{B.x},{B.y}]\nC = [{C.x},{C.y}]")

def calculate_vert(vert, camera):
    near = camera.near
    far = camera.far
    fov = camera.fov
    x, y, z = vert
    Rfov = 1 / np.tan(fov * 0.5 * 3.1459 / 180 )
    screenX, screenY = turtle.screensize()
    aspect_ratio = screenX/screenY

    S = 1 / (np.tan((fov/2)*(3.1415926/180)))

    print(f"Far = {far}, near = {near} \n {far/(far - near)}")

    matProj = Mat4([
        S, 0,0,0,
        0, S, 0,0,
        0,0,(far * -1) / (far - near),-1,
        0,0,((-1 * far) * near) / (far - near),0
    ])
    print(f"1{matProj[0,0]},{matProj[0,1]},{matProj[0,2]},{matProj[0,3]}\n"
          f"2{matProj[1,0]},{matProj[1,1]},{matProj[1,2]},{matProj[1,3]}\n"
          f"3{matProj[2,0]},{matProj[2,1]},{matProj[2,2]},{matProj[2,3]}\n"
          f"4{matProj[3,0]},{matProj[3,1]},{matProj[3,2]},{matProj[3,3]}\n")

    projFace = multmat4(Vec3(x,z,y), matProj)

    print(f"2D Y = {projFace.y * 0.5 * screenY}")

    return Vec2(projFace.x * 0.5 * screenX,projFace.y * 0.5 * screenY)

def multmat4(i, m):
    o = Vec3(0,0,0)
    o.x = i.x * m[0,0] + i.y * m[1,0] + i.z * m[2,0] + m[3,0]
    o.y = i.x * m[0,1] + i.y * m[1,1] + i.z * m[2,1] + m[3,1]
    o.z = i.x * m[0,2] + i.y * m[1,2] + i.z * m[2,2] + m[3,2]
    w =   i.x * m[0,3] + i.y * m[1,3] + i.z * m[2,3] + m[3,3]
    if (w != 0):
        o.x /= w
        o.y /= w
        o.z /= w
        print("Dividing")

    return (o)

def flatten_face(face: Face, camera: Camera): #Returns a Triangle which is sceenspace equivalent of the face
    points = []
    v = face.verts
    vmat = [0,0,0,
         0,0,0,
         0,0,0,]
    n = camera.near
    f = camera.far

    #for i in range(3):
        #y = verts[i,2]
        #vmat[i * 3 + 0] = (verts[i,0] * n)
        #vmat[i * 3 + 2] = (verts[i,2] * n)
        #vmat[i * 3 + 1] = (verts[i,1] * ((f + n) * verts[i,1] - (f * n)))
        #print(f"{i} succeeded")

    #v = Mat3([vmat[0], vmat[1], vmat[2],
              #vmat[3], vmat[4], vmat[5],
              #vmat[6], vmat[7], vmat[8],])

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



points = Mat3([
        0, 10, 0,
        0, 10, 50,
        50, 10, 50
    ])



face = Face(points)
print(f"World space points = \n{face.verts}")
camera = Camera(0,0,0, 1, 2000, 90)
print(f"Camera at {camera.x},{camera.y},{camera.z}")

frames = []

fps = 60
i = int(0)
dance = int(0)


print(f"World space points after translation = \n{face.verts}")


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
        #camera.Translate(100,0,0)
        #print(camera.x)
        #camera.Rotate('y', 20)
        end_time = time.time()
        try:
            fps = round((fps + (60 / (end_time - start_time))) / 2, 1)
            print(f"FPS: {fps}")
        except:
            print("Loading FPS")
        start_time = time.time()



turtle.mainloop()