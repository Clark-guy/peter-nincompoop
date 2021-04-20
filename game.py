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
bg = pygame.image.load("resources/bg4.png")
text = "hello"
font = pygame.font.Font(None, 24)
#curMessage = font.render(text,True, WHITE)

#clock initialize
clock = pygame.time.Clock()

#start music, initialize sounds
pygame.mixer.init()
music = pygame.mixer.music
music.load("music16.wav")
music.set_volume(.02)
music.play(loops=-1)
#foot = [pygame.mixer.Sound("sounds/footstep.wav"), pygame.mixer.Sound("sounds/footstep0.wav")]
#this keeps crashing the game. maybe an issue with initialization or some shit i cant tell. try and get it to play slower
foot = pygame.mixer.Sound("sounds/footstep.wav")



#make guy
pSpeed = 30
counter = 0
friendSprites = ["resources/friendWalkCycle300/friend.png", "resources/friendWalkCycle300/friend1.png", "resources/friendWalkCycle300/friend.png", "resources/friendWalkCycle300/friend2.png"]

playerPos = [0,0]
friend = player("friend", False, 10, 8, friendSprites[0],True, playerPos)
friendView = pygame.image.load(friend.get_sprite())
friendRect = friendView.get_rect()
friendAll = (friend, friendView)
playerPos = [width/2-(friendRect[2]/2), height/2-(friendRect[3]/2)]
friend.set_pos(playerPos)

friendWalk1 = pygame.image.load(friendSprites[1])
friendWalk2 = pygame.image.load(friendSprites[2])
screenPos = [-100,-100]


#make new guy
quackPos = [300, 300]
quack = person("quackers", False, 10, 8, "resources/guy0.png", True, quackPos)
quackView = pygame.image.load(quack.get_sprite())
quackAll = (quack, quackView)

charList = [friendAll, quackAll]

#animation change stuff
initTime = 0
#making a single variable for main character would make it hard to have other people walk around too. maybe put the delta
# time in the person object and then retrieve that? i could probably streamline this by having a universal checker for
# all movement, but that might make the game look weird.

#i think it would make sense to put a last updated value on every person, initialized to when they are blit'd
#this way i could keep one big clock going and just check that against the individual


########## Game Functions ########## 

def orderChars(charList):
    #go through list, find smallest item. swap with index 0, check again from next item in list
    #can't use sort function, need to sort by get_pos()[1] charList.sort(key=charList)
    smallest = 42
    for char1 in charList:
        for char2 in charList:
            if(char2[0].get_pos()[1] < char1[0].get_pos()[1]):
                char1, char2 = char2, char1
                print("SWAP")
    for char in charList:
        if isinstance(char[0], player):
            screen.blit(char[1], char[0].get_pos())
        else:
            #this code currently subtracts character position from background. to fix, change character position
            # with respect to background
            screen.blit(char[1],(char[0].get_pos()[0] + screenPos[0],char[0].get_pos()[1]+screenPos[1]))
        
def orderCharsNew(charList):
    for char1 in range (len(charList)):
        for char2 in range (len(charList)-char1-1):
            print("char2 pos ", charList[char2][0].get_pos())
            print("char2+1 pos ", charList[char2+1][0].get_pos())
            print("background")
            if charList[char2][0].get_pos() > charList[char2+1][0].get_pos():
                print("oooooooooo")
                charList[char2], charList[char2+1] = charList[char2+1], charList[char2]
    for char in charList:
        if isinstance(char[0], player):
            screen.blit(char[1], char[0].get_pos())
        else:
            screen.blit(char[1],(char[0].get_pos()[0] + screenPos[0],char[0].get_pos()[1]+screenPos[1]))

########## Main game loop ########## 

while True:
    #clear screen
    screen.fill(0)
    #draw screen things
    #bg = pygame.transform.scale(bg, (1000, 1000))
    screen.blit(bg,screenPos)
    
    #blit all guys. make a method that gets all their y positions, and blits them in order from highest to lowest. blit only if they are within screen bounds based on map position
    #screen.blit(friendView,(playerPos))
    #screen.blit(quackView,(quackPos[0]+screenPos[0],quackPos[1]+screenPos[1]))
    orderCharsNew(charList)
    friend.set_pos(playerPos)
    print(screenPos)
    
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
    #things that the keys actually do
    if keys[5]:
        pSpeed = 3
    else:
        pSpeed = 1
    if keys[0] or keys[1] or keys[2] or keys[3]:
        if friend.get_facing() == True:
            # how to make counter update after certain change in time
            # better way: just do if gameCounter % num == 0, where num increases for larger increments. game counter
            # starts at 0, this way i can keep track of everything with one counter rather than several. look into
            # pygame game counter
            if (friend.get_last_updated() >= 10):
                counter = (counter + 1) % len(friendSprites)
                friend.set_last_updated(0)
            else:
                friend.set_last_updated(friend.get_last_updated()+1)
            friendView = pygame.image.load(friendSprites[counter])
            #friendView = pygame.transform.scale(friendView, (20,40))
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
            screen.blit(curMessage, (playerPos[0]+friendRect[0],playerPos[1]+friendRect[1]))
            curMessage = font.render(text,True, WHITE)
            screen.blit(curMessage, (playerPos[0]+friendRect[0]+1,playerPos[1]+friendRect[1]+1))
            pygame.display.flip()
            time.sleep(1)
    #if clock.get_time()
        #print(clock.get_fps())
    #print(clock.get_time())
    print(pygame.time.get_ticks())
    clock.tick(30)

