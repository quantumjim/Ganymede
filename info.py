from ganymede import Engine

import random
import time


L = 16

colours = ['grey','red','blue','green','orange',None]

message = [
    'Press ↓ to scroll through this text.',
    '',
    'Ganymede is a lo-fi fantasy console. Designed for the',
    'Raspberry Pi with 4 colours, 2 brightnesses, a bit of text',
    'and not many pixels.',
    '',
    'You can play the games included, or even try making your',
    'own with the simple Ganymede game engine.',
    '',
    'See',
    'github.com/quantumjim',
    'for more info.',
    ''
    ]

def random_star():
    if random.random()<2/3:
        return ''
    else:
        return random.choice(['.','·','˙'])

def start(engine):
    
    engine.music.load('assets/Space_Fighter_Loop.mp3')
    engine.music.play(-1)
    
    engine.t0 = time.time()
    engine.scroll = 0

    # get save image
    with open('assets/controllers.py','r') as file:
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
    
    text = [
     ['','↑','','','','','','','','','Y'],
     ['←','','→','','>I','','','II','','X','','B'],
     ['','↓','','','','','','','','','A'],
     [],[],[],[],
     ['Q','W','E','R','T','Y','U','I','O','P'],
     ['A','S','D','F','G','H','J','K','L'],
     ['','Z','X','C','V','B','N','M','','II','↑'],
     ['','','','','','>I','','','','←','↓','→']
     ]
    for k,line in enumerate(text):
        for j,char in enumerate(line):
            engine.screen.pixel[2+j,3+k].set_text( char )
        
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
                
    for j,char in enumerate(['C','O','N','T','R','O','L','S']):
        engine.screen.pixel[4+j,0].set_text( char )
    
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
        
    if engine.controller['down'].value:
        engine.scroll = min(engine.scroll+1,len(message)-3)
    elif engine.controller['up'].value:
        engine.scroll = max(engine.scroll-1,0)
        
    text = '\n'.join(message[engine.scroll:engine.scroll+3])
    if engine.scroll<len(message)-3:
        text += '\n...'
    else:
        text += '\nNow press Esc on your keyboard to return to the menu!'
    engine.screen.pixel['text'].set_text( text )
            
# run     
engine = Engine(start,next_frame,L=L,continuous=True)
engine.music.stop()
