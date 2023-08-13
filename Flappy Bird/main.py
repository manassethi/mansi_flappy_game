import random #For generating random numbers
import sys # we will use sys.exit to exit the game
import pygame
from pygame.locals import * #Basic pygame imports


#Global variables for the game
FPS= 32 #frames per second
SCREENWIDTH=387
SCREENHEIGHT=511
SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT)) #display surface bana deta. pygame mein 
GROUNDY= SCREENHEIGHT*0.8
GAME_SPRITES={}
GAME_SOUNDS={}
PLAYER='gallery/sprites/bird.png'
BACKGROUND='gallery/sprites/background.png'
PIPE='gallery/sprites/pipe.png'






def welcomeScreen():
    #shows my welcome screen
    playerx=int(SCREENWIDTH/5)
    playery=int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    messagex=int((SCREENWIDTH-GAME_SPRITES['message'].get_width())/2)
    messagey=int(SCREENHEIGHT*0.12)
    basex=0
    while True:
        for event in pygame.event.get():
            #if user clicks on cross button, close the game
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            #if the user presses the space or up arrow key, start the game for them
            elif event.type==KEYDOWN and (event.type==K_SPACE or event.key==K_UP):
                return 
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                
                pygame.display.update()
                FPSCLOCK.tick(FPS)
'''def isCollide(playerx,playery,upperPipes,lowerPipes):
    if playery>GROUNDY-25 or playery<0:
        return True
    for pipe in upperPipes:
        pipeheight=GAME_SPRITES['pipe'][0].get_height
        if (playery<(pipeHeight+pipe['y'])) and abs(playerx-pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            return True
    for pipe in lowerPipes:
        if(playery+GAME_SPRITES['player'].get_height()>pipe['y']) and abs(playerx-pipe['x'])< GAME_SPRITES['pipe'][0].get_width():
            return True '''
            

def getRandomPipe():
    #two pipes. ek seedha . upar wala ulta
    pipeHeight=GAME_SPRITES['pipe'][0].get_height()
    offset=SCREENHEIGHT/3
    y2=offset+random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES['base'].get_height()-1.2*offset))
    pipeX=SCREENWIDTH+10
    y1=pipeHeight-y2+offset
    pipe=[
        
        {'x':pipeX,'y':(-1)*y1},#upper pipe
        {'x':pipeX,'y':y2}
        
        
    ]
    return pipe
def isCollide(playerx,playery,upperPipes,lowerPipes):
    
    if playery>GROUNDY-50 or playery<0:
        return True
    for pipe in upperPipes:
        pipeheight=GAME_SPRITES['pipe'][0].get_height()
        if (playery<pipeheight+pipe['y'] and abs(playerx-pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            return True
    for pipe in lowerPipes:
        if(playery+GAME_SPRITES['player'].get_height()>pipe['y'] and abs(playerx-pipe['x'])< GAME_SPRITES['pipe'][0].get_width()):
            return True 
def mainGame():
    score=0
    playerx=int(SCREENWIDTH/5)
    playery=int(SCREENHEIGHT/2)
    basex=0
    #create 2 pipes for blitting on the screen
    newPipe1=getRandomPipe()
    newPipe2=getRandomPipe()
    
    
    # my list of upper pipes
    
    upperPipes=[
        {'x':SCREENWIDTH+200,'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newPipe2[0]['y']}
        
    ]
    #my list of lower pipes
    lowerPipes=[
        {'x':SCREENWIDTH+200,'y':newPipe1[1]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newPipe2[1]['y']}
        
    ]
    pipeVelX=-4
    
    playerVelY=-9
    playerMaxVelY=5
    playerMinVelY=-8
    playerAccY=1
    
    playerFlapv=-8  #velocity while flapping
    playerFlapped= False #true only when bird is flapping
    
    
    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.type==K_UP):
                if playery>0:
                    playerVelY=playerFlapv
                    playerFlapped=True
            
        crashTest=isCollide(playerx,playery,upperPipes,lowerPipes)    
        #this function returns true if player is crashed
        if crashTest:
            return
        #check for score
        
        playerMidPos=playerx+GAME_SPRITES['player'].get_width()/2   
        for pipe in upperPipes:
            pipeMidPos=pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2 # pipe ka center
            if pipeMidPos<=playerMidPos<pipeMidPos+4:#########
                score+=1
                print(f'your score is {score}')
        if playerVelY<playerMaxVelY and not playerFlapped:
            playerVelY+=playerAccY
        if playerFlapped:
            
            playerFlapped=False
            
        playerHeight=GAME_SPRITES['player'].get_height()
        playery=playery+min(playerVelY,GROUNDY-playery-playerHeight)
        #move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x']+=pipeVelX
            lowerPipe['x']+=pipeVelX
        
        #add a new pipe when the first pipe about to cross the leftmost part of screen
        if 0<upperPipes[0]['x']<5:
            newpipe=getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])
            
        
        #if the pipe is out of the screen  
        if upperPipes[0]['x']< (-1)*GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        #Let's blit our sprites
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'],lowerPipe['y']))
            
            
        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
        myDigits=[int(x) for x in list(str(score))]
        width=0
        for digit in myDigits:
            width+=GAME_SPRITES['numbers'][digit].get_width()
        Xoffset=int((SCREENWIDTH-width)/2)
        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(Xoffset,SCREENHEIGHT*0.12))
            Xoffset+=GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
            
        
            
            
                
            
    
    
    
    
                
                
                
                
                
                
                


if __name__=="__main__":
    #This will be the main point from where our game will start
    pygame.init()#initializes all pygame modules
    
    FPSCLOCK=pygame.time.Clock() # ek clock banadi jo tick karti rahegi . clock.tick() mein jitne denge
    #utne frames run honge ek baar mein
    pygame.display.set_caption('Flappy Bird by Mansi Sethi')
    GAME_SPRITES['numbers']=(
        
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),#image processing mein help karta h
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
        
        
    )
    GAME_SPRITES['message']=pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base']=pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe']=(
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
         pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert_alpha()
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()
    
    while True:
        
        welcomeScreen()#shows welcome screen to user until he presses a button
            
        mainGame()#main game function 
        
    
     
        
    
    

    

    
