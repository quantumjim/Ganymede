from ganymede import Engine

import random
import time


L = 16

colours = ['grey','red','blue','green','orange',None]

def random_star():
    if random.random()<2/3:
        return ''
    else:
        return random.choice(['.','·','˙'])

def start(engine):
    
    engine.music.load('assets/Space_Fighter_Loop.mp3')
    engine.music.play(-1)
    
    engine.t0 = time.time()

    # get saved image
    with open('assets/ganymede.py','r') as file:
        engine.image = eval(file.read())
        
    engine.stars = {}
    for X in range(engine.L):
        for Y in range(engine.L):
            engine.stars[X,Y] = random_star()
                
    # draw moon
    for X in range(engine.L):
        for Y in range(engine.L):
            colour = colours[engine.image[X,Y][0]]
            if colour:
                engine.screen.pixel[X,Y].set_color( colour )
                engine.screen.pixel[X,Y].set_text( ' ' )
                engine.screen.pixel[X,Y].set_brightness( engine.image[X,Y][1] )
            else:
                engine.screen.pixel[X,Y].set_brightness( False )
                
    for j,char in enumerate(['G','A','N','Y','M','E','D','E']):
        engine.screen.pixel[6+j,11].set_text( char )
        
    # initialize with `next_frame`
    engine.next_frame(engine)
    
def next_frame (engine):
    
    # draw stars
    for X in range(engine.L):
        for Y in range(engine.L):
            colour = colours[engine.image[X,Y][0]]
            if not colour:
                engine.screen.pixel[X,Y].set_color( 'grey' )
                engine.screen.pixel[X,Y].set_text( engine.stars[X,Y] )
    
    t = time.time()
    if t-engine.t0>0.1:
        # move stars
        new_stars = {}
        for Y in range(engine.L):
            new_stars[0,Y] = random_star()
            for X in range(1,engine.L):
                new_stars[X,Y] = engine.stars[X-1,Y]
        engine.stars = new_stars
        engine.t0 = t
        
    if engine.controller['A'].value:
        engine.running = False
        engine.music.stop()
        return 'info'
     
running = True
while running:
    # run title screen     
    engine = Engine(start,next_frame,L=L,continuous=True)
    # run selected game
    try:
        exec('import '+engine.message)
    except:
        running = False
        
engine.music.stop()
