#Minimax vs. minimax
#Alpha-beta vs. alpha-beta
#Minimax vs. alpha-beta (minimax goes first)
#Alpha-beta vs. minimax (alpha-beta goes first)

#offensive(1st) vs Defensive
#defensive(1st) vs offensive
#Offensive vs offensive
#Defensive vs Defensive
import pyglet
import numpy as np
import copy
import time
import os
'''
window = pyglet.window.Window()

@window.event
def on_key_press(symbol, modifiers):
    print ('A key was pressed')

@window.event
def on_draw():
    window.clear()

pyglet.app.run()'''

pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
    [0, 1, 2, 0, 2, 3],
    ('v2i', (100, 100,
             150, 100,
             150, 150,
             100, 150))
)

@window.event
def on_draw():
    window.clear()
    image.blit(0, 0)

pyglet.app.run()
