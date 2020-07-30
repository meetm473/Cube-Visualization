import pygame
from pygame.locals import *

import tkinter as tk

import threading

stop_openGL = False
stop_notif = False

def show_openGL():
    global stop_openGL
    
    pygame.init()
    display = (800,800)

    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption('Window 1')

    while not stop_openGL:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                stop_openGL = True
                
        pygame.display.flip()
        pygame.time.wait(1)

    print('Closed OpenGL')

def show_notif():
    global stop_openGL
    
    window = tk.Tk()
    window.geometry("200x200")

    main_frame = tk.Frame(master=window, width=200, height=200, bg="red")
    main_frame.pack(fill=tk.BOTH, expand=True)

    greeting = tk.Label(master=main_frame,text="Hey there!")

    greeting.pack()
    window.mainloop()
    stop_openGL = True
    print('closed')
    

thread_opengl = threading.Thread(target=show_openGL)
thread_notif = threading.Thread(target=show_notif)

thread_opengl.start()
thread_notif.start()

thread_opengl.join()
thread_notif.join()

print('DONE!')
 

    
    
    
