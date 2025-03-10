import turtle
import time
from os import system, name
from math import radians

import numpy as np
import random as r
from bra import *

def turtle_init(colour):
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.screen.colormode(255)
    t.color(colour)
    turtle.hideturtle()
    turtle.tracer(0)
    return t

class Screen:
    def __init__(self, width, height):
        turtle.setup(width,height)
        self.width = width / 2
        self.height = height / 2
        self.aspect = width/height
        #turtle.setworldcoordinates(-1, -1, 1, 1)
        Screen.border(self)
    def border(self):
        t = turtle_init((0,0,0))
        thick = 3
        t.pensize(thick * 2)
        h = self.height + thick
        w = self.width + thick

        t.teleport(-1 * w, -1 * h)
        t.seth(90)
        for i in range(2):
            t.fd(h * 2)
            t.right(90)
            t.fd(w * 2)
            t.right(90)

#3D Face
class Face:
    def __init__(self, p: Mat3):
        #Asign verts
        self.verts = p
        self.colour = (r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
        self.midpoint = Face.get_mid_point(self)

    def Translate(self, X, Y, Z):
        v = self.verts
        self.verts = Mat3([
            v[0,0] + X,v[0,1] + Y,v[0,2] + Z,
            v[1, 0] + X, v[1, 1] + Y, v[1, 2] + Z,
            v[2, 0] + X, v[2, 1] + Y, v[2, 2] + Z
        ])

    def Rotate(self, axis: str, radians, origin: Vec3):
        angle = np.radians(radians)

        A = Vec3(self.verts[0, 0], self.verts[0, 1], self.verts[0, 2])
        B = Vec3(self.verts[1, 0], self.verts[1, 1], self.verts[1, 2])
        C = Vec3(self.verts[2, 0], self.verts[2, 1], self.verts[2, 2])

        #print(f"Before: {A}, {B}, {C}")

        #T = Mat3([
        #    1,0,normX,
        #    0,1,normY,
        #    0,0,1+normZ
        #])

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


        #invT = Mat3([
        #    1,0,-1*normX,
        #    0,1,-1*normY,
        #    0,0,-1*normZ
        #])


        #A = Vec3(A.x - origin.x,A.y - origin.y,A.z - origin.z)
        #B = Vec3(B.x - origin.x,B.y - origin.y,B.z - origin.z)
        #C = Vec3(C.x - origin.x,C.y - origin.y,C.z - origin.z)

        A = R * A
        B = R * B
        C = R * C

        A = Vec3(A.x + origin.x, A.y + origin.y, A.z + origin.z)
        B = Vec3(B.x + origin.x, B.y + origin.y, B.z + origin.z)
        C = Vec3(C.x + origin.x, C.y + origin.y, C.z + origin.z)



        self.verts = Mat3([A.x,A.y,A.z,
                           B.x,B.y,B.z,
                           C.x,C.y,C.z])

        #print(f"After: {A}, {B}, {C}")


    def get_mid_point(self):
        x = self.verts[0,0] + self.verts[1,0] + self.verts[2,0]
        y = self.verts[0,1] + self.verts[1,1] + self.verts[2,1]
        z = self.verts[0,2] + self.verts[1,2] + self.verts[2,2]
        return Vec3(x/3,y/3,z/3)



#3D Camera
class Camera:
    def __init__(self, focal_point: Vec3, near, far, fov, screen):
        self.focal_point = focal_point
        self.near = near
        self.far = far
        self.fov = np.radians(180 - fov)
        self.hfov = np.radians((180 - fov)/2)
        w = screen.width
        h = screen.height
        self.offsetxy = 0
        self.offsetzy = 0


        #Creating screen plane
        A = Vec3(focal_point.x + w, focal_point.y + (h/np.tan(self.hfov)), focal_point.z + h)
        B = Vec3(focal_point.x + w, focal_point.y + (h / np.tan(self.hfov)), focal_point.z - h)
        C = Vec3(focal_point.x - w, focal_point.y + (h / np.tan(self.hfov)), focal_point.z - h)

        self.A = A
        self.B = B
        self.C = C



        self.verts = Mat3([A.x, A.y, A.z,
                           B.x, B.y, B.z,
                           C.x, C.y, C.z])

        self.focal_length = (screen.height)/(np.tan(self.hfov))
        print(f"Camera init:\n\t|Focal length = {self.focal_length}\n\t|Tan(fov/2) = {np.tan(self.hfov)}")


    def Translate(self, X, Y, Z):
        c = self
        c.focal_point.x += X
        c.focal_point.y += Y
        c.focal_point.z += Z

        c.A.x += X
        c.B.x += X
        c.C.x += X

        c.A.y += Y
        c.B.y += Y
        c.C.y += Y

        c.A.z += Z
        c.B.z += Z
        c.C.z += Z


    def Rotate(self, axis, radians):
        angle = np.radians(radians)

        origin = camera.focal_point



        A = Vec3(self.verts[0, 0], self.verts[0, 1], self.verts[0, 2])
        B = Vec3(self.verts[1, 0], self.verts[1, 1], self.verts[1, 2])
        C = Vec3(self.verts[2, 0], self.verts[2, 1], self.verts[2, 2])

        # print(f"Before: {A}, {B}, {C}")

        # T = Mat3([
        #    1,0,normX,
        #    0,1,normY,
        #    0,0,1+normZ
        # ])

        if axis == 'x':
            R = Mat3([
                1, 0, 0,
                0, np.cos(angle), -1 * np.sin(angle),
                0, np.sin(angle), np.cos(angle)
            ])
            self.offsetzy += radians
        elif axis == 'y':
            R = Mat3([
                np.cos(angle), 0, np.sin(angle),
                0, 1, 0,
                np.sin(angle) * -1, 0, np.cos(angle)
            ])

        elif axis == 'z':
            R = Mat3([
                np.cos(angle), np.sin(angle) * -1, 0,
                np.sin(angle), np.cos(angle), 0,
                0, 0, 1
            ])

        # invT = Mat3([
        #    1,0,-1*normX,
        #    0,1,-1*normY,
        #    0,0,-1*normZ
        # ])

        #A = Vec3(A.x - origin.x, A.y - origin.y, A.z - origin.z)
        #B = Vec3(B.x - origin.x, B.y - origin.y, B.z - origin.z)
        #C = Vec3(C.x - origin.x, C.y - origin.y, C.z - origin.z)

        A = R * A
        B = R * B
        C = R * C

        #A = Vec3(A.x + origin.x, A.y + origin.y, A.z + origin.z)
        #B = Vec3(B.x + origin.x, B.y + origin.y, B.z + origin.z)
        #C = Vec3(C.x + origin.x, C.y + origin.y, C.z + origin.z)

        A = Vec3(A.x, A.y, A.z)
        B = Vec3(B.x, B.y, B.z)
        C = Vec3(C.x, C.y, C.z)

        self.A = A
        self.B = B
        self.C = C

        self.verts = Mat3([A.x, A.y, A.z,
                           B.x, B.y, B.z,
                           C.x, C.y, C.z])


        # print(f"After: {A}, {B}, {C}")


#2D Triangle
class Triangle:
    def __init__(self, face, A: Vec2, B: Vec2, C: Vec2):
        #print("Started def Triangle: ")
        #Create Turtle and colour
        self.colour = (r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
        self.turtle = turtle_init(self.colour)

        #Asign verts
        self.verts = [A,B,C]
        #print(f"\t|Triangle created with\nA = [{A.x},{A.y}]\nB = [{B.x},{B.y}]\nC = [{C.x},{C.y}]")

def calculate_vert(vert: Vec3, camera, screen):

    system('clear')
    point = vert
    n = camera.near
    far = camera.far
    fov = camera.hfov
    point_prime = Vec3(0,0,0)
    f = camera.focal_length
    focal_point = camera.focal_point

    normZ = camera.A.z - camera.focal_point.z
    normY = camera.A.y - camera.focal_point.y
    normX = camera.A.x - focal_point.x

    #Y and Z
    #Get the camera angle
    offset_angle = fov - np.arctan(normZ/normY)
    print(f"Offset angle YZ: {np.degrees(offset_angle)}")

    #Rotate point
    rotated_y,rotated_z = rotate_point(offset_angle, point.y, point.z)
    print(f"Rotated Y,Z = \n\t{round(rotated_y,0)}\n\t{round(rotated_z,0)}")

    #Calculate angle
    riseZ = (rotated_z - focal_point.z)
    runZ = (rotated_y - focal_point.y)
    if rotated_y != 0 and rotated_z != 0:
        angleZ = (riseZ/runZ)
    else:
        angleZ = ((riseZ + 1)/ (runZ + 1))

    #Calculate screenspace equivalent
    point_prime.z = f * angleZ

    #X and Y
    #Get the camera angle
    offset_angle = fov - np.arctan(normX/normY)
    print(f"Offset angle XY: {np.degrees(offset_angle)}")

    #Rotate point
    rotated_x,rotated_y = rotate_point(offset_angle, point.x, point.y)
    print(f"Rotated X,Y = \n\t{round(rotated_x,0)}\n\t{round(rotated_y,0)}")

    #Calculate angle
    riseX = (rotated_x - focal_point.x)
    runX = (rotated_y - focal_point.y)
    if rotated_x != 0 and rotated_y != 0:
        angleX = (riseX/runX)
    else:
        angleX = (riseX + 1)/(runX + 1)
    #Calculate screenspace equivalent
    point_prime.x = f * angleX


    point_prime.y = (rotated_y * (far/(far - n)) - ((far * n)/(far - n))) - camera.focal_point.y

    #if point_prime.x != 0:
    point_prime.x = (point_prime.x / screen.width)
    #if point_prime.z != 0:
    point_prime.z = (point_prime.z / screen.height)

    #print(f"\t| Camera: {camera.A}, {camera.B}, {camera.C}")
    #print(f"\t| screen-space X,Z = {point_prime.x}, {point_prime.z}")
    return point_prime

def rotate_point(angle, x,y):
    final_x = (x * np.cos(angle)) + (y * np.sin(angle) * -1)
    final_y = (x * np.sin(angle)) + (y * np.cos(angle))

    return (final_x,final_y)

def flatten_face(face: Face, camera: Camera, screen): #Returns a Triangle which is sceenspace equivalent of the face
    #print("Started def flatten_face:")
    v = face.verts

    #Calculate each vert's screenspace equivalent
    points = [calculate_vert(Vec3(v[0,0],v[0,1],v[0,2]), camera, screen),
              calculate_vert(Vec3(v[1,0],v[1,1],v[1,2]), camera, screen),
              calculate_vert(Vec3(v[2,0],v[2,1],v[2,2]), camera, screen)]



    return Triangle(face, points[0], points[1], points[2])

def check_if_in_cameraspace(vert, screen):
    if vert.y > 0:
        if (vert.x < 1) and (vert.x > -1):
            x = (vert.x * screen.width)

            # print(f"({vert.x}),({vert.z})")

            write_x = round(x, 1)

        else:
            if vert.x > 1:
                x = 1 * screen.width
                write_x = ' '
            elif vert.x < -1:
                x = -1 * screen.width
                write_x = ' '

            print("Off screen")
        if (vert.z < 1) and (vert.z > -1):
            z = vert.z * screen.height
            write_z = round(z, 1)
        else:
            if vert.z > 1:
                z = 1 * screen.height
                write_z = ' '
            elif vert.z < -1:
                z = -1 * screen.height
                write_z = ' '
            print("Off screen")

    else:
        x = 0
        write_x = ' '
        z = 1 * screen.height
        write_z = ' '
        print("Off screen")
    return x,z,write_x,write_z

def draw_triangle(tri, face):
    #Assign vars
    t = tri.turtle
    verts = tri.verts
    #Lift pen and begin fill
    t.clear()
    t.up()
    t.begin_fill()

    tempx,tempz,_,_ = check_if_in_cameraspace(verts[-1], screen)

    t.teleport(tempx,tempz)
    i = 0
    for vert in verts:
        wX = face.verts[i,0]
        wY = face.verts[i,1]
        wZ = face.verts[i,2]





        x,z,write_x,write_z = check_if_in_cameraspace(vert, screen)

        t.goto(x, z)

        colour = face.colour
        t.color(0, 0, 0)

        t.write(f"{write_x}, {round(wY,1)}, {write_z}")

        t.color(colour)

        i += 1

    #End fill
    t.end_fill()



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
    face.Rotate('z', dx, face.midpoint)
    face.Rotate('x', dy, face.midpoint)
def rotate_camera(camera, frame, lastframe):
    x, y = frame
    lx, ly = lastframe
    dx, dy = x - lx, y - ly
    camera.Rotate('y', dx)
def move_camera(camera, frame, lastframe):
    x,y = frame
    lx, ly = lastframe
    dx,dy = x - lx, y - ly
    camera.Translate(dx * 0.01, dy * 0.01, 0)



print("Running mainloop:")



screen = Screen(800,800)

camera = Camera(Vec3(0,-30,0),1,2000, 90, screen)
#print(f"\t| Camera at {camera.x},{camera.y},{camera.z}")

points = Mat3([
        0, 0, 0,
        0, 0, 10,
        10, 0, 10
    ])

face = Face(points)
#print(f"\t| World space points = \n{face.verts}")


mouse_x, mouse_y = 0,0
cords = []
turtle.getcanvas().bind("<Motion>", on_motion)

face.Translate(0,30,0)
#camera.Rotate('z', 180)

#cameraFace = Face(Mat3([camera.A.x, camera.A.y, camera.A.z,camera.B.x, camera.B.y, camera.B.z,camera.C.x, camera.C.y, camera.C.z]))
#cameraFace.Translate(0,10,0)
#face.verts = Mat3([camera.A.x, camera.A.y, camera.A.z,camera.B.x, camera.B.y, camera.B.z,camera.C.x, camera.C.y, camera.C.z,])

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
        #rotate_camera(camera, cords[-1], cords[-2])

    #Stores, draws, clears and removes frames
    frames.append(flatten_face(face, camera, screen))
    if i > 2:
        frames[1].turtle.clear()
        draw_triangle(frames[2], face)
        turtle.turtles().remove(frames[1].turtle)
        frames.pop(1)
    midpoint = face.midpoint
    #face.Rotate('x', 360,midpoint)
    #face.Translate(0, -0.1, 0)
    #camera.Rotate('x', 1)
    #camera.Rotate('z', 2)
    #cameraFace.verts = Mat3([camera.A.x, camera.A.y, camera.A.z,camera.B.x, camera.B.y, camera.B.z,camera.C.x, camera.C.y, camera.C.z,])
    #cameraFace.Translate(0,10,0)
    #midpoint = face.midpoint
    #face.Rotate('y', -1,midpoint)
    turtle.update()
    if i % 60 == 0:


        #print(camera.x)

        end_time = time.time()
        try:
            fps = round((fps + (60 / (end_time - start_time))) / 2, 1)
            #print(f"\t| FPS: {fps}")
        except:
            print("\t| Loading FPS")
        start_time = time.time()



turtle.mainloop()