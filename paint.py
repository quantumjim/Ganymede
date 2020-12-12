from ganymede import Engine

import random


L = 16

colours = ['grey','red','blue','green','orange',None]

def draw_pixel(engine,pos):
    X,Y = pos
    colour = colours[engine.image[X,Y][0]]
    if colour:
        engine.screen.pixel[X,Y].set_color( colour )
        engine.screen.pixel[X,Y].set_text( '' )
    else:
        engine.screen.pixel[X,Y].set_color( 'grey' )
        engine.screen.pixel[X,Y].set_text('·')
    engine.screen.pixel[X,Y].set_brightness( engine.image[X,Y][1] )

def start(engine):
    
    engine.music.load('assets/bit-quest.mp3')
    engine.music.play(-1)

    try:
        # get save image
        with open('assets/paint/image.py','r') as file:
           engine.image = eval(file.read())
    except:
        # otherwise, start with blank image
        engine.image = {}
        for X in range(engine.L):
            for Y in range(engine.L):
                engine.image[X,Y] = [-1,True]
                
    # draw image
    for X in range(engine.L):
        for Y in range(engine.L):
            draw_pixel(engine,(X,Y))
                
    # cursor position
    engine.x = int(engine.L/2-1)
    engine.y = int(engine.L/2-1)
    
    engine.screen.pixel['text'].set_text( 'Draw a picture!\nSave with A' )
        
    # initialize with `next_frame`
    engine.next_frame(engine)
    
def next_frame (engine):

    # set old cursor position to correct text
    for dx,dy in [(+1,0),(-1,0),(0,+1),(0,-1)]:
        X = engine.x+dx
        Y = engine.y+dy
        if X in range(engine.L) and Y in range(engine.L):
            if colours[engine.image[X,Y][0]]:
                engine.screen.pixel[X,Y].set_text('')
            else:
                engine.screen.pixel[X,Y].set_text('·')
    
    # change cursor position based on controller input
    if engine.controller['up'].value:
        engine.y = max(engine.y-1,0)
    if engine.controller['down'].value:
        engine.y = min(engine.y+1,engine.L-1)
    if engine.controller['left'].value:
        engine.x = max(engine.x-1,0)
    if engine.controller['right'].value:
        engine.x = min(engine.x+1,engine.L-1)
          
    X,Y = engine.x,engine.y
         
    # change colour and brightness of active pixel based on controller input
    if engine.controller['X'].value:
        engine.image[X,Y][0] = (engine.image[X,Y][0]+1)%6
    if engine.controller['Y'].value:
        engine.image[X,Y][0] = (engine.image[X,Y][0]-1)%6
    if engine.controller['B'].value:
        engine.image[X,Y][1] = not engine.image[X,Y][1]
        
    # set active pixel to new colour and brightness
    draw_pixel(engine,(X,Y))
    
    # set current cursor position
    for dx,dy,char in [(+1,0,'←'),(-1,0,'→'),(0,+1,'↑'),(0,-1,'↓')]:
        X = engine.x+dx
        Y = engine.y+dy
        if X in range(engine.L) and Y in range(engine.L):
            engine.screen.pixel[X,Y].set_text( char )
    
    # save if A is pressed
    if engine.controller['A'].value:
        with open('assets/paint/image.py','w') as file:
            file.write(str(engine.image))

        
engine = Engine(start,next_frame,L=L)
engine.music.stop()