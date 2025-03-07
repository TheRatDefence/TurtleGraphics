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

class Screen:
    def __init__(self, width, height):
        turtle.screensize(width,height)
        self.width = width
        self.height = height
        self.aspect = width/height

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
    def __init__(self, focal_point: Vec3, near, far, fov, screen):
        self.focal_point = focal_point
        self.near = near
        self.far = far
        self.fov = fov


        #Creating screen plane
        self.A = Vec3(focal_point.x + ((screen.width/2)/(np.tan(fov/2))),(focal_point.y + ((screen.height/2)/(np.tan(fov/2)))),focal_point.z + (screen.height/2))
        self.B = Vec3(focal_point.x + ((screen.width / 2) / (np.tan(fov / 2))),(focal_point.y + ((screen.height / 2) / (np.tan(fov / 2)))), focal_point.z)
        self.C = Vec3(focal_point.x + ((screen.width / 2) / (np.tan(fov / 2))) * -1,(focal_point.y + ((screen.height / 2) / (np.tan(fov / 2)))), focal_point.z)

        self.focal_length = Vec3()


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
        #print("Started def Triangle: ")
        #Create Turtle and colour
        self.turtle = turtle_init()

        #Asign verts
        self.verts = [A,B,C]
        #print(f"\t|Triangle created with\nA = [{A.x},{A.y}]\nB = [{B.x},{B.y}]\nC = [{C.x},{C.y}]")

def calculate_vert(vert, camera, screen):
    #print(f"Started def calculate_vert:")
    n = camera.near
    far = camera.far
    fov = camera.fov
    point_prime = Vec3(0,0,0)

    #Y and Z

    #Get the camera angle
    offset_angle = fov/2 - np.arctan((camera.A.z - camera.focal_point.z)/camera.A.y - camera.focal_point.y)

    #Rotate point
    rotated_point = rotate_point(offset_angle, vert.y, vert.z)
    point_prime.y =





    Zprime = dZ * (far/(far - n)) - ((far * n)/(far - n))


    #print(f"\t| screen-space X,Y = {Xprime, Yprime}")
    return point_prime

def rotate_point(angle, x,y):
    final_x = (x * np.cos(angle)) + (y * np.sin(angle) * -1)
    final_y = (x * np.sin(angle)) + (y * np.cos(angle))

    return (final_x,final_y)

def flatten_face(face: Face, camera: Camera, screen): #Returns a Triangle which is sceenspace equivalent of the face
    #print("Started def flatten_face:")
    v = face.verts

    #Calculate each vert's screenspace equivalent
    points = [calculate_vert((v[0,0],v[0,1],v[0,2]), camera, screen),
              calculate_vert((v[1,0],v[1,1],v[1,2]), camera, screen),
              calculate_vert((v[2,0],v[2,1],v[2,2]), camera, screen)]



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



screen = Screen(1000,1000)

camera = Camera(Vec3(0,0,0),1,2000, 90, screen)
#print(f"\t| Camera at {camera.x},{camera.y},{camera.z}")

points = Mat3([
        0, 10, 0,
        0, 10, 1000,
        1000, 10, 1000
    ])

face = Face(points)
#print(f"\t| World space points = \n{face.verts}")







def on_motion(event):
    global mouse_x, mouse_y
    mouse_x = event.x - turtle.window_width() / 2
    mouse_y = -event.y + turtle.window_height() / 2
def move_face(face, frame, lastframe):
    x,y = frame
    lx, ly = lastframe
    dx,dy = x - lx, y - ly
    face.Translate(dx, 0, dy)
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
#print("Started mainloop:")
running = True
while running:
    i += 1

    cords.append((mouse_x, mouse_y))
    if i > 2:
        cords.remove(cords[0])
        #rotate_face(face, cords[-1], cords[-2])

    #Stores, draws, clears and removes frames
    frames.append(flatten_face(face, camera, screen))
    if i > 2:
        frames[1].turtle.clear()
        draw_triangle(frames[2], face)
        turtle.turtles().remove(frames[1].turtle)
        frames.pop(1)



    turtle.update()
    if i % 60 == 0:
        face.Rotate('y', 1)
        #camera.Translate(100,0,0)
        #print(camera.x)
        #camera.Rotate('y', 20)
        end_time = time.time()
        try:
            fps = round((fps + (60 / (end_time - start_time))) / 2, 1)
            #print(f"\t| FPS: {fps}")
        except:
            print("\t| Loading FPS")
        start_time = time.time()



turtle.mainloop()