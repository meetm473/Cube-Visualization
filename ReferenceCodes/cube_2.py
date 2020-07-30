import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
    (1,-1,-1),
    (1,1,-1),
    (-1,1,-1),
    (-1,-1,-1),
    (1,-1,1),
    (1,1,1),
    (-1,1,1),
    (-1,-1,1)
    )

"""
0 - Front(Red)
1 - Back(Cyan)   
2 - Top(Blue)
3 - Bottom(Yellow)
4 - Right(Magenta)
5 - Left(Green)
"""
faces = (
    (4,5,6,7),
    (0,1,2,3),
    (5,1,2,6),
    (4,0,3,7),
    (3,2,6,7),
    (0,1,5,4)
    )

colors = (
    (1,0,0),
    (0,1,1),
    (0,0,1),
    (1,1,0),
    (1,0,1),
    (0,1,0)
    )

def drawCube():
    glBegin(GL_QUADS)
    c_idx = 0;
    for face in faces:
        glColor3fv(colors[c_idx])
        for vertex in face:
            glVertex3fv(vertices[vertex])
        c_idx += 1
    glEnd()

def displayFrame():
    """
    glClear:
    sets the bitplane area of the window to values previously selected by
    glClearColor, glClearDepthf, and glClearStencil.
    Input param: Bitwise OR of GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_STENCIL_BUFFER_BIT
    """
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)    
	
    drawCube()
    

def cubeInit():
    """
    glClearColor:
    specifies the red, green, blue,
    and alpha values used by glClear to clear the color buffers.
    Values specified by glClearColor are clamped to the range 0:1.
    This can be used to set the background.
    """
    glClearColor(0,0,0,0)

    """
    glEnable:
    Enables various capabilites.
    """
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)

    """
    glMatrixMode:
    Specifies which matrix stack is the target for subsequent
    matrix operations. Initial value is model_view
    Values accepted -
        - GL_MODELVIEW
        - GL_PROJECTION
        - GL_TEXTURE
        - GL_COLOR

    glLoadIdentity:
    Replaces current matrix with identity matrix

    glOrtho:
    Describes a transformation that produces a parallel projection.
    Parameters: left, right, bottom, top, nearVal, farVal
    left, right - coordinates for left and right vertical clipping planes
    bottom, top - coordinates for bottom and top horizontal clipping planes
    nearVal, farVal - distances to the nearer and farther depth clipping planes
    """

    # Setting orthographic projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-4,4,-4,4,-10,10)

    # Setting matrix mode to model
    glMatrixMode(GL_MODELVIEW)


def windowInit():
    pygame.init()                          
    display = (400,400)

    # This sets the display mode to the required width, height, and OpenGL display.
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption('Cube Rotate - Key')

def main():

    windowInit()
    cubeInit()
    
    while True:        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glRotatef(-10,0,0,1)
                if event.key == pygame.K_RIGHT:
                    glRotatef(10,0,0,1)
                    
                if event.key == pygame.K_UP:
                    glRotatef(-10,1,0,0)
                if event.key == pygame.K_DOWN:
                    glRotatef(10,1,0,0)

                if event.key == pygame.K_r:
                    glLoadIdentity()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glRotatef(-10,0,1,0)
                if event.button == 5:
                    glRotatef(10,0,1,0)
        
        displayFrame()
        pygame.display.flip()
        pygame.time.wait(1)

main()
