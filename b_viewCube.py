"""
Takes care of the visualization thread
"""

import threading
import pygame
from pygame.locals import *
from OpenGL.GL import *
from d_sensorFusion import Rpy


class ViewCube(threading.Thread):
    """
    Defining the cube. Faces are of the following colors:
    0 - Front(Red)
    1 - Back(Cyan)
    2 - Top(Blue)
    3 - Bottom(Yellow)
    4 - Right(Magenta)
    5 - Left(Green)
    """
    vertices = (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, 1, 1),
        (-1, -1, 1)
    )
    faces = (
        (4, 5, 6, 7),
        (0, 1, 2, 3),
        (5, 1, 2, 6),
        (4, 0, 3, 7),
        (3, 2, 6, 7),
        (0, 1, 5, 4)
    )
    colors = (
        (1, 0, 0),
        (0, 1, 1),
        (0, 0, 1),
        (1, 1, 0),
        (1, 0, 1),
        (0, 1, 0)
    )

    def drawCube(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBegin(GL_QUADS)
        c_idx = 0;
        for face in self.faces:
            glColor3fv(self.colors[c_idx])
            for vertex in face:
                glVertex3fv(self.vertices[vertex])
            c_idx += 1
        glEnd()

    @staticmethod
    def cubeInit():
        glClearColor(0, 0, 0, 0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_COLOR_MATERIAL)

        # Setting orthographic projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-4, 4, -4, 4, -10, 10)

        # Setting matrix mode to model
        glMatrixMode(GL_MODELVIEW)

    def __init__(self):
        threading.Thread.__init__(self)
        self.show_cube = False

    def run(self):
        print('Opening Cube...')
        pygame.init()
        display = (400, 400)

        # This sets the display mode to the required width, height, and OpenGL display.
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption('Cube Rotate - Key')

        self.cubeInit()
        
        rpy = [0,0,0]
        
        while self.show_cube:
            # Acquiring data from sensor fusion
            Rpy.lock.acquire()
            try:
                Rpy.lock.wait(0.1)
                rpy = [Rpy.rotateX, Rpy.rotateY, Rpy.rotateZ]
            except:
                print('Some prob')
            finally:
                Rpy.lock.release()
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    print('Cube Closed')
                    quit()
                            
            glLoadIdentity()
            glRotatef(rpy[0], 1,0,0)
            glRotatef(rpy[1], 0,1,0)
            glRotatef(rpy[2], 0,0,1)
            self.drawCube()
            pygame.display.flip()
            pygame.time.wait(1)

        if not self.show_cube:
            pygame.display.quit()
            pygame.quit()
        print('Cube Closed')
