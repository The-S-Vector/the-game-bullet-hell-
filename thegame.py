# IMPORTS 
import pygame
import numpy
import time

#INITIALISATION 
pygame.init()

clock = pygame.time.Clock()

screen_width = pygame.display.Info().current_w 
screen_height = pygame.display.Info().current_h

screen = pygame.display.set_mode((screen_width, screen_height - 60))
pygame.display.set_caption("Platformer Game")


#OBJECTS 
class Player():
    def __init__(self):
        #the image...
        self.maoScaleX = 100
        self.maoScaleY = 150
        self.mao = pygame.image.load("mao.jpg")
        self.mao = pygame.transform.scale(self.mao, (self.maoScaleX ,self.maoScaleY))
        
        #the behaviour of the image
        self.Yforce = 29                    #the upwards acceleration when jumping
        self.XComponent = 0                 #the x velocity, momentum kind of
        self.XForce = 10                    #the horizontal acceleration when running
        
        #the starting XY coordinates
        self.x = 0                          
        self.y = 720                        
        
class Platform():
    def __init__(self, x = 0, y = screen_height - 40 ,length = 40, width = screen_width): # default is the floor
        self.length = length
        self.width = width +10
        self.x = x
        self.y = y - self.length
        self.recta = pygame.Rect(self.x,self.y, self.width, self.length)
        self.colour = ("#9400ff")        
            	
class Asteroids():
    def __init__(self):
        self.size = numpy.random.randint(20, 60)
        self.speed = numpy.random.randint(1, 10)
        self.xval = numpy.random.randint(0, screen_width)
        self.yval = -numpy.random.randint(0, screen_height)
        self.colour = (numpy.random.randint(10,255),numpy.random.randint(10,255),numpy.random.randint(10,255))

class Score():
    def __init__(self, score):
        self.value = score
    def increase(self):
        self.value += 1
 
class Objects():
    def __init__(self):
        #the image...
        self.elonScaleX = 180
        self.elonScaleY = 150
        self.elon = pygame.image.load("elon.jpg")
        self.elon = pygame.transform.scale(self.elon, (self.elonScaleX ,self.elonScaleY))
        
    def generate(self):
        self.x = 250 * numpy.random.randint(0,6) + 125 - self.elonScaleX/2
        self.y = 240 * numpy.random.randint(0,4)
        

#FUNCTIONS 
def HitBox():
    #creates the hit box coordinate parameters by taking the coordinates of the image
    rectangle = pygame.Rect(player.x,player.y, player.maoScaleX, player.maoScaleY)
    
    #draws the Hitbox in Red...
    # pygame.draw.rect(screen, Red, pygame.Rect(player.x,player.y, player.maoScaleX, player.maoScaleY))
    
    return pygame.Rect(player.x,player.y, player.maoScaleX, player.maoScaleY)

def HitBoxObject():
    rectangle = pygame.Rect(object.x,object.y, object.elonScaleX, object.elonScaleY)
    return pygame.Rect(object.x,object.y, object.elonScaleX, object.elonScaleY)

def gravity():
    #hitbox coalision
    if onfloor() == True:
        gravity = 0
    else:
        gravity = 10 
        
    player.y += gravity
   
def jump():

    jumpFactor = player.Yforce  

    jumping = True
    while jumping == True:
        
        #maintain the momentum
        player.x += player.XComponent
        
        #change the upwards acceleration
        player.y -= jumpFactor
        jumpFactor -= 1.5
        
        #continue rendering everything else
        renderPlayerAndObject()
        render_score_board()
        rocks()   
        bonus_muliplier()     
        
        
        #if it touches a platform stop the jumping
        if onfloor() == True:
            jumping = False
        
        clock.tick(tick_rate)
        
    #0 the xcomponent when back on the floor
    player.XComponent = 0
        
def exit_func():#pointless...
    print("good day...bye...whyyyyy...nooooo...I'm...aliveee")
    pygame.display.quit()
    exit()

def onfloor():
    #for everyplatform check for collisions with the player
    for pl in GeneratePlatform(): 
        if pygame.Rect.colliderect(HitBox(),pl.recta) == True: 
            return True
    return False
        
def GeneratePlatform():
    Platforms = []
    
    #floor
    Platforms.append(Platform())  
    
    #default platform
    width = 250
    length = 30
    
    create_platform = lambda chunk_x, chunk_y: Platform(chunk_x*width,chunk_y*240,length,width)
    
    #turning the screen into a grid...y maximum of 4 platforms and x maximum of 5 platforms
    # max_chunks_y  1 - 3    #(screen_height-40)/(player.maoScaleY+30) 
    # max_chunks_x  0 - 5     #(screen_width/250)
    #create_platform(x_grid, y_grid) #coordinates to place on the grid
    
    Platforms.append(create_platform(0, 3))
    # Platforms.append(create_platform(1, 3))
    # Platforms.append(create_platform(2, 3))
    Platforms.append(create_platform(3, 3))
    # Platforms.append(create_platform(4, 3))
    # Platforms.append(create_platform(5, 3))
    
    # Platforms.append(create_platform(0, 2))
    Platforms.append(create_platform(1, 2))
    # Platforms.append(create_platform(2, 2))
    # # Platforms.append(create_platform(3, 2))
    # Platforms.append(create_platform(4, 2))
    Platforms.append(create_platform(5, 2))
    
    Platforms.append(create_platform(0, 1))
    # Platforms.append(create_platform(1, 1))
    # Platforms.append(create_platform(2, 1))
    Platforms.append(create_platform(3, 1))
    # Platforms.append(create_platform(4, 1))
    # Platforms.append(create_platform(5, 1))
    
    #renders all the platforms
    for plats in Platforms:
        pygame.draw.rect(screen, plats.colour,plats.recta)   
    return Platforms

def renderPlayerAndObject():
    
    player.x = max(0, min(screen_width-player.maoScaleX, player.x))
    player.y = max(0, min(screen_height, player.y))  

    
    screen.blit(object.elon,(object.x, object.y))
    screen.blit(player.mao,(player.x,player.y))
    pygame.display.flip()
    screen.fill(Black)
    
def userInputs():
    for event in pygame.event.get():  # gets the registered keys of the events stack
        if event == pygame.QUIT:
            exit_func()  # if the event is the close button than exit

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        return exit_func()  

    elif pygame.key.get_pressed()[pygame.K_a] and onfloor() == True:
        player.XComponent = -5 
        player.x -= player.XForce 
        
    elif pygame.key.get_pressed()[pygame.K_d] and onfloor() == True:
        player.XComponent = 5
        player.x += player.XForce 
        
    if pygame.key.get_pressed()[pygame.K_SPACE] and onfloor() == True:
        jump()
        
    player.XComponent = 0  
    return  # returning nothing, theif!

def main():
    userInputs()
    HitBox()
    GeneratePlatform()
    gravity()
    renderPlayerAndObject()
    rocks()
    render_score_board()
    bonus_muliplier()
    
    clock.tick(tick_rate)
   
def generate(number_of_asteroids):
    rock_field_array = []
    for i in range(0,number_of_asteroids): 
        rock_field_array.append(Asteroids())
    return rock_field_array

def rocks():

    #for every rock that exist
    for rock in rock_field: 
        rock.yval += rock.speed #move square down
        
        if rock.yval > screen_height + 10:  # if it reaches the bottom
            rock.xval = numpy.random.randint(0, screen_width)  # ramdom x coordinate bassed off the width of the screen
            rock.yval = numpy.random.randint(-20, -5)  # random height 20 to 5 pixels above the screen
            score.increase()
        
        #render the rocks
        square = pygame.draw.rect(screen,rock.colour, pygame.Rect(rock.xval-rock.size/2,rock.yval,rock.size,rock.size)) 


        #this checks if the player hitbox hits one of the square
        collide = pygame.Rect.colliderect(square, HitBox())
        if collide == True:
            unalived()
            

    clock.tick(tick_rate)  # caps their speed fps

def unalived(): 
  
    #generate the 3 lines of text
    over_board = pygame.font.SysFont("couriernew", 100).render(f"you have lost", True, Purple) 
    over_board_2 = pygame.font.SysFont("couriernew", 80).render(f"score: {score.value}", True, Purple)
    over_board_escape = pygame.font.SysFont("couriernew", 80).render(f"|esc| or wait", True, Purple) 
    
    #endlessly check for the escape button and render the text 
    x = 0 
    while x <= 10:
        
        for event in pygame.event.get():  # gets the registered keys of the events stack
            if pygame.key.get_pressed()[pygame.K_ESCAPE]: 
                exit_func()
        
        screen.fill(Black)       
        screen.blit(over_board, (screen_width/2 - over_board.get_width()/2  , screen_height/2 - over_board.get_height()))
        screen.blit(over_board_2, (screen_width/2 - over_board_2.get_width()/2  , screen_height/2 + over_board_2.get_height()))
        screen.blit(over_board_escape, (screen_width/2 - over_board_escape.get_width()/2  , screen_height/2  + over_board_2.get_height() + over_board_escape.get_height()))
        pygame.display.flip()
        
        time.sleep(0.5)
        x += 1        
    exit()    
     
def bonus_muliplier():
    if pygame.Rect.colliderect(HitBox(),HitBoxObject()) == True:
        if object.y == 0:
            score.value = score.value * 10
        elif object.y == 1:
            score.value = score.value * 5
        elif object.y >= 2:
            score.value = score.value * 2
        object.generate()
        
def render_score_board():   
    score_board = pygame.font.SysFont("couriernew", 200).render(f"{score.value}", True, Purple)        
    screen.blit(score_board, (screen_width/2 - score_board.get_width() / 2  , 10))   

#Gloabl Variables
global tick_rate, rock_field

#VARIABLES
player = Player()
object = Objects()
object.generate()
score = Score(0)
rock_field = generate(8)
tick_rate = 120

#colours
White = ("#ffffff")
Black = ("#000000")
Purple = ("#9400ff")
Red = ("#ff3131")


#MAIN 
while True:
    main()
    
    
    
