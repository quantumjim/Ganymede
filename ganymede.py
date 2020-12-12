import pygame
pygame.init()

try:
    pygame.joystick.init()
except:
    pass

th_desc = 20
margin = 32

class Pixel():
    def __init__(self,pos,size,surface,description=False):
        x,y = pos[0]+margin,pos[1]+margin
        dx,dy = size
        self.description = description
        self.rect = pygame.Rect(x,y,dx+1,dy+1)
        self.surface = surface
        self.set_color('grey',draw=False)
        self.set_brightness(True,draw=False)
        self.set_text('',draw=False)
        self._draw()
        
    def _draw(self):
        if self.color in ['grey','gray']:
            if self.bright:
                color = (255,255,255)
            else:
                color = (0,0,0)
        elif self.color=='green':
            if self.bright:
                color = (64,255,64)
            else:
                color = (0,128,0)
        elif self.color=='blue':
            if self.bright:
                color = (135, 206, 235)
            else:
                color = (0,0,255)
        elif self.color=='orange':
            if self.bright:
                color = (255,192,96)
            else:
                color = (192,128,64)
        elif self.color=='red':
            if self.bright:
                color = (255,0,0)
            else:
                color = (128,32,64)
        pygame.draw.rect(self.surface,color,self.rect)
        
        if self.description:
            th = th_desc
            tx = self.rect.x + th_desc/8
            ty = self.rect.y
            font = pygame.font.SysFont('liberationsans',th,bold=True)
        else:
            th = int(0.9*self.rect.height)
            font = pygame.font.SysFont('liberationsans',th)
            tx = self.rect.x + int((self.rect.width-font.size(self.text)[0])/2)
            ty = self.rect.y + int((self.rect.height-font.size(self.text)[1])/2)
            
        for j,line in enumerate(self.text.split('\n')):
            self.surface.blit(font.render(line,False,(128,128,128)),(tx,ty+j*th))
                
    def set_color(self,color,draw=True):
        self.color = color
        if draw:
            self._draw()
        
    def set_brightness(self,bright,draw=True):
        self.bright = bright
        if draw:
            self._draw()
            
    def set_text(self,text,draw=True):
        self.text = text
        if draw:
            self._draw()
        

class Screen():

    def __init__ (self,size,L=8):
            
        self.width = size
        if type(L)==tuple:
            self.L = L
        else:
            self.L = (L,L)
            
        self.surface = pygame.display.set_mode((int(size[0]+2*margin),int( (L+1)*size[1]/L+5*th_desc )+2*margin))
        self.surface.fill((128,128,128))
        pygame.display.update()
        
        dx = int(size[0]/self.L[0])
        dy = int(size[1]/self.L[1])
        self.pixel = {}
        for x in range(self.L[0]):
            for y in range(self.L[1]):
                self.pixel[x,y] = Pixel( (x*dx,y*dy), (dx,dy), self.surface)
                
        ddx = size[0]
        ddy = 5*th_desc
        self.pixel['text'] = Pixel( (0,(self.L[1]+1)*dx), (ddx,ddy), self.surface, description=True)
        self.pixel['text'].set_text('')


class Button():
    def __init__(self,value):
        self.value = value
        

class Engine():

    def __init__(self,start,next_frame,L=8,continuous=False,dt=0,size=(600,600)):
        

    
        self.L = L
        self.screen = Screen(size,L=L)
        self.music = pygame.mixer.music
        self.running = True
        
        self.start = start
        self.next_frame = next_frame
        
        self.controller = {}
        for button in ['up','down','left','right','X','Y','A','B','next']:
            self.controller[button] = Button(False)
    
        start(self)
        pygame.display.flip()
    
        last_press = None
        while self.running:
            
            pressed = None
            events = pygame.event.get()  
            # look to the controller for an input
            try:
                # check buttons
                joystick = pygame.joystick.Joystick(0)
                joystick.init()
                buttons = joystick.get_numbuttons()
                for j in range(buttons):
                    button = joystick.get_button(j)
                    if button:
                        if j==0:
                            pressed = 'A'
                        if j==1:
                            pressed = 'B'
                        if j==2:
                            pressed = 'X'
                        if j==3:
                            pressed = 'Y'
                        if j==6:
                            pressed = 'next'
                        if j==7:
                            pressed = 'start'
                # check d pad
                for hat_index in range(joystick.get_numhats()):
                    hat_status = joystick.get_hat(hat_index)
                    if hat_status[0] < -.5:
                        pressed = 'left'
                    elif hat_status[0] > .5:
                        pressed = 'right'
                    if hat_status[1] < -.5:
                        pressed = 'down'
                    elif hat_status[1] > .5:
                        pressed = 'up'     
            except:
                pass
                
            # if none from the controller, look to the keyboard
            if pressed==None:
                if events:
                    for event in events:
                        if event.type==pygame.QUIT:
                            self.running = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key in [pygame.K_LEFT]:#,pygame.K_a]:
                                pressed = 'left'
                            elif event.key in [pygame.K_RIGHT]:#,pygame.K_d]:
                                pressed = 'right'
                            elif event.key in [pygame.K_UP]:#,pygame.K_w]:
                                pressed = 'up'
                            elif event.key in [pygame.K_DOWN]:#,pygame.K_s]:
                                pressed = 'down'
                            elif event.key in [pygame.K_x]:#,pygame.K_j]:
                                pressed = 'X'
                            elif event.key in [pygame.K_y]:#,pygame.K_i]:
                                pressed = 'Y'
                            elif event.key in [pygame.K_a]:#,pygame.K_k]:
                                pressed = 'A'
                            elif event.key in [pygame.K_b]:#,pygame.K_l]:
                                pressed = 'B'
                            elif event.key in [pygame.K_SPACE]:
                                pressed = 'next'
                            elif event.key in [pygame.K_RETURN]:
                                pressed = 'start'
                            elif event.key==pygame.K_ESCAPE:
                                self.running = False
            
            
            # if the pressed button is the same one pressed in the last frame, ignore it
            # otherwise, register it
            if pressed!=last_press:
                last_press = pressed
                if pressed=='start':
                    continuous = not continuous
                    pressed = None
                if pressed:
                    self.controller[pressed].value = True

            if pressed or continuous:
                self.message = next_frame(self)
                pygame.display.flip()
                
            for button in self.controller:
                self.controller[button].value = False
                        
            pygame.time.wait(dt)

    
                
