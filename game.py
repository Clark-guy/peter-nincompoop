import pygame
import math
import time
from person import person, player, npc
from settings import Settings



#constants
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)


#initialize
pygame.init()
settings = Settings()
width, height = settings.screen_width, settings.screen_height
# keys: w     a     s     d     e     Lshft
keys = [False,False,False,False,False,False]
paused = False
screen = pygame.display.set_mode((width, height))
bg = pygame.image.load("resources/bg.png")
text = "hello"
font = pygame.font.Font(None, 24)
#curMessage = font.render(text,True, WHITE)

#clock initialize
clock = pygame.time.Clock()

#start music, initialize sounds
pygame.mixer.init()
music = pygame.mixer.music
music.load("music16.wav")
music.set_volume(.2)
music.play(loops=1)
#foot = [pygame.mixer.Sound("sounds/footstep.wav"), pygame.mixer.Sound("sounds/footstep0.wav")]
#this keeps crashing the game. maybe an issue with initialization or some shit i cant tell. try and get it to play slower
foot = pygame.mixer.Sound("sounds/footstep.wav")



#make guy
pSpeed = 3
counter = 0
friendSprites = ["resources/friend.png", "resources/friend1.png", "resources/friend.png", "resources/friend2.png"]
friend = player("friend", False, 10, 8, friendSprites[0],True)
friendView = pygame.image.load(friend.get_sprite())
friendWalk1 = pygame.image.load(friendSprites[1])
friendWalk2 = pygame.image.load(friendSprites[2])
friendRect = friendView.get_rect()
playerPos = [100-(friendRect[2]/2), 100-(friendRect[3]/2)]
screenPos = [0,0]

#animation change stuff
initTime = 0
#making a single variable for main character would make it hard to have other people walk around too. maybe put the delta
# time in the person object and then retrieve that? i could probably streamline this by having a universal checker for
# all movement, but that might make the game look weird.

#i think it would make sense to put a last updated value on every person, initialized to when they are blit'd
#this way i could keep one big clock going and just check that against the individual



#friend = pygame.transform.scale(friend, (20,40))

#game loop
while True:
    #clear screen
    screen.fill(0)
    #draw screen things
    screen.blit(bg,screenPos)
    screen.blit(friendView,(100-(friendRect[2]/2),100-(friendRect[3]/2)))
    #update screen
    pygame.display.flip()
    #events
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_w:
                keys[0]=True
            elif event.key==pygame.K_a:
                keys[1]=True
                friend.set_facing(True)
            elif event.key==pygame.K_s:
                keys[2]=True
            elif event.key==pygame.K_d:
                keys[3]=True
                friend.set_facing(False)
            elif event.key==pygame.K_e:
                keys[4]=True
            elif event.key==pygame.K_LSHIFT:
                keys[5]=True
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_w:
                keys[0]=False
            elif event.key==pygame.K_a:
                keys[1]=False
            elif event.key==pygame.K_s:
                keys[2]=False
            elif event.key==pygame.K_d:
                keys[3]=False
            elif event.key==pygame.K_e:
                keys[4]=False
            elif event.key==pygame.K_LSHIFT:
                keys[5]=False
    if keys[5]:
        pSpeed = 1
    else:
        pSpeed = .5
    if keys[0] or keys[1] or keys[2] or keys[3]:
        if friend.get_facing() == True:
            #how to make counter update after certain change in time
            if (friend.get_last_updated() >= 10):
                counter = (counter + 1) % len(friendSprites)
                friend.set_last_updated(0)
            else:
                friend.set_last_updated(friend.get_last_updated()+1)
            friendView = pygame.image.load(friendSprites[counter])
            #time.sleep(.1)
        else:
            if (friend.get_last_updated() >= 10):
                counter = (counter + 1) % len(friendSprites)
                friend.set_last_updated(0)
            else:
                friend.set_last_updated(friend.get_last_updated()+1)
            friendView = pygame.transform.flip(pygame.image.load(friendSprites[counter]), True, False)
            #time.sleep(.1)
    if not keys[0] and not keys[1] and not keys[2] and not keys[3]:
        counter = 0
        pygame.mixer.Sound.stop(foot)
        if friend.get_facing() == True:
            friendView = pygame.image.load(friendSprites[counter])
        else:
            friendView = pygame.transform.flip(pygame.image.load(friendSprites[counter]), True, False)
    if keys[0] and keys[1]:
        screenPos[1]+=0.66*pSpeed
        screenPos[0]+=0.66*pSpeed
    elif keys[0] and keys[3]:
        screenPos[1]+=0.66*pSpeed
        screenPos[0]-=0.66*pSpeed
    elif keys[2] and keys[1]:
        screenPos[1]-=0.66*pSpeed
        screenPos[0]+=0.66*pSpeed
    elif keys[2] and keys[3]:
        screenPos[1]-=0.66*pSpeed
        screenPos[0]-=0.66*pSpeed
    elif keys[0]:
        screenPos[1]+=1*pSpeed
    elif keys[2]:
        screenPos[1]-=1*pSpeed
    elif keys[1]:
        screenPos[0]+=1*pSpeed
    elif keys[3]:
        screenPos[0]-=1*pSpeed
    if keys[4]:
        if paused==True:
            paused=False
        else:
            paused=True
            #rect = curMessage.getRect()
            curMessage = font.render(text,True, BLACK)
            screen.blit(curMessage, (playerPos[0]+10,playerPos[1]-10))
            curMessage = font.render(text,True, WHITE)
            screen.blit(curMessage, (playerPos[0]+11,playerPos[1]-9))
            pygame.display.flip()
            time.sleep(1)
    #pygame.time.Clock().tick(500) 

