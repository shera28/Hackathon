import pygame
import sys
import random
import time

#Инициализация
pygame.init()
fps=pygame.time.Clock()
icon=pygame.image.load("images/icon.jpg")
pygame.display.set_icon(icon)

block_size = 40
left_margin = 3 * block_size
upper_margin =1.5* block_size
 
font1=pygame.font.Font("Fonts/hot-pizza6.ttf", block_size)
size = (left_margin + 28 * block_size, upper_margin + 18 * block_size)
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
pic=pygame.image.load('images/s.png')
picture=pygame.transform.scale(pic,(2*block_size,2*block_size))
screen = pygame.display.set_mode(size)
pygame.display.set_caption("SEA BATTLE!!!")
new_font=pygame.font.Font("Fonts/ds-eraser-cyr1.ttf", block_size)
font_size = int(block_size / 2)
font = pygame.font.Font("Fonts/ds-eraser-cyr1.ttf", font_size)
game_over_font_size = 2 * block_size
game_over_font = pygame.font.Font("Fonts/ds-eraser-cyr1.ttf", game_over_font_size)



class Grid:
    def __init__(self, title, offset):
        self.title = title
        self.offset = offset
        self.__draw_grid()
        self.__add_nums_letters_to_grid()
        self.__sign_grid()

    def __draw_grid(self):
        for i in range(11):
            # Horizontal lines
            pygame.draw.line(screen, 'black', (left_margin + self.offset * block_size, upper_margin + i * block_size),
                             (left_margin + (10 + self.offset) * block_size, upper_margin + i * block_size), 1)
            # Vertical lines
            pygame.draw.line(screen, 'black', (left_margin + (i + self.offset) * block_size, upper_margin),
                             (left_margin + (i + self.offset) * block_size, upper_margin + 10 * block_size), 1)

    def __add_nums_letters_to_grid(self):      
        for i in range(10):
            num_ver = font.render(str(i + 1), True, 'black')
            letters_hor = font.render(LETTERS[i], True, 'black')
            num_ver_width = num_ver.get_width()
            num_ver_height = num_ver.get_height()
            letters_hor_width = letters_hor.get_width()

            # Numbers (vertical)
            screen.blit(num_ver, (left_margin - (block_size // 2 + num_ver_width // 2) + self.offset * block_size,
                                  upper_margin + i * block_size + (block_size // 2 - num_ver_height // 2)))
            # Letters (horizontal)
            screen.blit(letters_hor, (left_margin + i * block_size + (block_size // 2 -letters_hor_width // 2) + self.offset * block_size, 
                                  upper_margin + 10 * block_size))

    def __sign_grid(self):
        player = font.render(self.title, True, 'black')
        sign_width = player.get_width()
        screen.blit(player, (left_margin + 5 * block_size - sign_width // 2 + self.offset * block_size, upper_margin - block_size // 2 - font_size))


class AutoShips:

    def __init__(self, offset):
        self.offset = offset
        self.available_blocks = {(x, y) for x in range(
            1 + self.offset, 11 + self.offset) for y in range(1, 11)}
        self.ships_set = set()
        self.ships = self.__populate_grid()
        self.orientation = None
        self.direction = None

    def __create_start_block(self, available_blocks):
        self.orientation = random.randint(0, 1)
        # -1 is left or down, 1 is right or up
        self.direction = random.choice((-1, 1))
        x, y = random.choice(tuple(available_blocks))
        return x, y, self.orientation, self.direction

    def __create_ship(self, number_of_blocks, available_blocks):
        ship_coordinates = []
        x, y, self.orientation, self.direction = self.__create_start_block(available_blocks)
        for _ in range(number_of_blocks):
            ship_coordinates.append((x, y))
            if self.orientation==0:
                self.direction, x = self.__get_new_block_for_ship(x, self.direction, self.orientation, ship_coordinates)
            else:
                self.direction, y = self.__get_new_block_for_ship(y, self.direction, self.orientation, ship_coordinates)
        if self.__is_ship_valid(ship_coordinates):
            return ship_coordinates
        return self.__create_ship(number_of_blocks, available_blocks)

    def __get_new_block_for_ship(self, coordinate, direction, orientation, ship_coordinates):
        self.direction = direction
        self.orientation = orientation
        if (coordinate <= 1 - self.offset * (self.orientation - 1) and self.direction == -1) or (coordinate >= 10 - self.offset * (self.orientation - 1) and self.direction == 1):
            self.direction *= -1
            return self.direction, ship_coordinates[0][self.orientation] + self.direction
        else:
            return self.direction, ship_coordinates[-1][self.orientation] + self.direction

    def __is_ship_valid(self, new_ship):
        ship = set(new_ship)
        return ship.issubset(self.available_blocks)

    def __add_new_ship_to_set(self, new_ship):
        self.ships_set.update(new_ship)

    def __update_available_blocks_for_creating_ships(self, new_ship):
        for elem in new_ship:
            for k in range(-1, 2):
                for m in range(-1, 2):
                    if self.offset < (elem[0] + k) < 11 + self.offset and 0 < (elem[1] + m) < 11:
                        self.available_blocks.discard((elem[0] + k, elem[1] + m))

    def __populate_grid(self):
        ships_coordinates_list = []
        for number_of_blocks in range(4, 0, -1):
            for _ in range(5 - number_of_blocks):
                new_ship = self.__create_ship(number_of_blocks, self.available_blocks)
                ships_coordinates_list.append(new_ship)
                self.__add_new_ship_to_set(new_ship)
                self.__update_available_blocks_for_creating_ships(new_ship)
        return ships_coordinates_list


def draw_ships(ships_coordinates_list,color=None):
    if not color:
     for elem in ships_coordinates_list:
        ship = sorted(elem)
        x_start = ship[0][0]
        y_start = ship[0][1]
        # Horizontal and 1block ships
        ship_width = block_size * len(ship)
        ship_height = block_size
        # Vertical ships
        if len(ship) > 1 and ship[0][0] == ship[1][0]:
            ship_width, ship_height = ship_height, ship_width
        x = block_size * (x_start - 1) + left_margin
        y = block_size * (y_start - 1) + upper_margin
        pygame.draw.rect(screen, 'black', ((x, y), (ship_width, ship_height)), width=block_size // 10)
    else:
        for elem in ships_coordinates_list:
          ship = sorted(elem)
          x_start = ship[0][0]
          y_start = ship[0][1]
          ship_width = block_size * len(ship)
          ship_height = block_size
          if len(ship) > 1 and ship[0][0] == ship[1][0]:
              ship_width, ship_height = ship_height, ship_width
          x = block_size * (x_start - 1) + left_margin
          y = block_size * (y_start - 1) + upper_margin
          pygame.draw.rect(screen, color, ((x, y), (ship_width, ship_height)))


player1auto=AutoShips(0)
player2auto=AutoShips(15)
player1wins=0
player2wins=0
pl1score=font1.render(str(player1wins),False,'black')
pl2score=font1.render(str(player2wins),False,'black')
grid1=Grid("PLAYER 1",0)
grid2=Grid("PLAYER 2",15)
x_st=0
y_st=0
new_ship=[] 
c=0
k=0
player1_ships_list=[]
b=[1,1,1,1,2,2,2,3,3,4]
d=[1,1,1,1,2,2,2,3,3,4]
player2_ships_list=[]
first_player_ships_unfinished=True
second_player_ships_unfinished=False
move_first=random.randint(0,2)
Game=False
Game2=False
player1moveout=False
player2moveout=False
hitted_blocks1 = []
hitted=[]
drawing=False
hitted_blocks2 = []
locked_blocks1 = []
locked_blocks2 = []
mina1=[]
min1draw=[]
min2draw=[]
mina2=[]
mining1=False
mining2=False
undestroyed_player1_ships = []
undestroyed_player2_ships = []
destroyed_player1_ships = []
destroyed_player2_ships = []
destroyed_blocks1 = []
destroyed_blocks2 = []
alredy=False
draw_own=False
colorh='black'
color1='black'
color2='black'
color3='black'
color4='black'
color5='black'
color6='black'
av=True
min2boom=[]
min1boom=[]
available1=[]
player1lose=False
player2lose=False
choose_mode=False
classic=False
timegame=False
startfree=0
timer=0
Gaming=False
bgsound=pygame.mixer.Sound("sounds/bg.mp3")
bgsound.set_volume(0.1)
bgr=pygame.USEREVENT+1
winsound=pygame.mixer.Sound("sounds/win.mp3")
misssound=pygame.mixer.Sound("sounds/miss.mp3")
hitsound=pygame.mixer.Sound("sounds/hit.mp3")
breaksound=pygame.mixer.Sound("sounds/break.mp3")
winsound.set_volume(0.5)
breaksound.set_volume(0.1)
hitsound.set_volume(0.5)
misssound.set_volume(0.5)
miss=False
hit=False
breaked=False
for i in range(10):
    for j in range(10):
        available1.append((i,j))

available2=[]
for i in range(15,25):
    for j in range(10):
        available2.append((i,j))
while True:
    screen.fill('white')
    screen.blit(picture,(size[0]/2-block_size,0))
    screen.blit(pl1score,(size[0]/2-1.8*block_size,block_size/2))
    screen.blit(pl2score,(size[0]/2+1.1*block_size,block_size/2))
    grid1._Grid__draw_grid()
    grid1._Grid__add_nums_letters_to_grid()
    grid1._Grid__sign_grid()
    grid2._Grid__draw_grid()
    grid2._Grid__add_nums_letters_to_grid()
    grid2._Grid__sign_grid()
    pl1score=font1.render(str(player1wins),False,'black')
    pl2score=font1.render(str(player2wins),False,'black')
    for a in hitted_blocks1:
        pygame.draw.rect(screen,'gray',(left_margin+a[0]*block_size+1,upper_margin+a[1]*block_size+1,block_size-1,block_size-1))
    for a in destroyed_blocks1:
        pygame.draw.rect(screen,'brown',(left_margin+a[0]*block_size+1,upper_margin+a[1]*block_size+1,block_size-1,block_size-1))
    for a in hitted_blocks2:
        pygame.draw.rect(screen,'gray',(left_margin+a[0]*block_size+1,upper_margin+a[1]*block_size+1,block_size-1,block_size-1))
    for a in destroyed_blocks2:
        pygame.draw.rect(screen,'brown',(left_margin+a[0]*block_size+1,upper_margin+a[1]*block_size+1,block_size-1,block_size-1))
    if first_player_ships_unfinished:
       draw_ships(player1_ships_list)
       player1auto=AutoShips(0)
       autobutton=pygame.draw.rect(screen,color1,(left_margin+block_size,upper_margin+11*block_size, 3*block_size, block_size))
       auto=font.render('AUTO',True,"White")
       nad=new_font.render('Locate ships!',True,'black')
       w1=auto.get_width()
       screen.blit(nad,(left_margin+block_size,upper_margin+13*block_size))
       screen.blit(auto,(left_margin+block_size-w1/2+3*block_size/2, upper_margin+11*block_size+block_size/2-font_size/2))
       save=font.render('SAVE',True,"White")
       w2=save.get_width()
       savebutton=pygame.draw.rect(screen,color2,(left_margin+3.5*block_size,upper_margin+15*block_size, 3*block_size, block_size))
       screen.blit(save,(left_margin+3.5*block_size-w2/2+3*block_size/2, upper_margin+15*block_size+block_size/2-font_size/2))
       pos=pygame.mouse.get_pos()
       own=font.render('OWN',True,"white")
       ownbutton=pygame.draw.rect(screen,color5,(left_margin+6*block_size,upper_margin+11*block_size, 3*block_size, block_size))
       w3=own.get_width()
       screen.blit(own,(left_margin+6*block_size-w3/2+3*block_size/2, upper_margin+11*block_size+block_size/2-font_size/2))
       if autobutton.collidepoint(pos):
                  color1="gray"
       else:
                  color1='black'
       if savebutton.collidepoint(pos):
                  color2="gray"
       else:
                  color2='black'
       if ownbutton.collidepoint(pos):
                  color5="gray"
       else:
                  color5='black'
       for event in pygame.event.get():
          if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

          if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and autobutton.collidepoint(pos):
               player1_ships_list.clear()
               player1_ships_list=player1auto.ships
               draw_own=False
          if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and ownbutton.collidepoint(pos):
              player1_ships_list.clear()
              b=[1,1,1,1,2,2,2,3,3,4]
              locked_blocks1.clear()
              draw_own=True
          if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and savebutton.collidepoint(pos):
             if len(player1_ships_list)==10:
                  first_player_ships_unfinished=False
                  mining1=True
                  draw_own=False
          if draw_own:
        
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and ((left_margin<pos[0]<left_margin+10*block_size) and (upper_margin<pos[1]<upper_margin+10*block_size)):
               x_st=pos[0]
               y_st=pos[1]
               drawing=True
            if event.type == pygame.MOUSEMOTION:
              if drawing:
                pos=event.pos
                wid=pos[0]-x_st
                heig=pos[1]-y_st

                pygame.draw.rect(screen,'red',(x_st,y_st,wid,heig), width=block_size//10)
            if event.type == pygame.MOUSEBUTTONUP and event.button==1 and drawing:
                   drawing=False
                   pos=event.pos
                   if pos[0]<x_st or pos[1]<y_st or pos[0]>left_margin+10*block_size or pos[1]>upper_margin+10*block_size:
                       pass
                   else:
                       st_x_y=(int((x_st - left_margin) // block_size),int((y_st - upper_margin) // block_size))
                       f_x_y=(int((pos[0] - left_margin) // block_size),int((pos[1] - upper_margin) // block_size))
                
                       if f_x_y[0]==st_x_y[0] and f_x_y[1]-st_x_y[1]<4 and f_x_y not in locked_blocks1 and st_x_y not in locked_blocks1:
                           for i in range(f_x_y[1]-st_x_y[1]+1):
                               new_ship.append((f_x_y[0]+1,st_x_y[1]+i+1))
                           
                           if len(new_ship) in b:
                             for el in new_ship:
                               for i in range(-2,1):
                                  for j in range(-2,1):
                                    locked_blocks1.append((el[0]+i,el[1]+j))
                             player1_ships_list.append(new_ship)
                             b.remove(len(new_ship))
                           new_ship=[]
                       elif f_x_y[1]==st_x_y[1] and f_x_y[0]-st_x_y[0]<4 and f_x_y not in locked_blocks1 and st_x_y not in locked_blocks1:
                           for i in range(f_x_y[0]-st_x_y[0]+1):
                               new_ship.append((st_x_y[0]+i+1,st_x_y[1]+1))
                           if len(new_ship) in b:
                             for el in new_ship:
                               for i in range(-2,1):
                                  for j in range(-2,1):
                                    locked_blocks1.append((el[0]+i,el[1]+j))
                             player1_ships_list.append(new_ship)
                             b.remove(len(new_ship))
                           new_ship=[]





    if mining1:
        draw_ships(player1_ships_list)
        draw_ships(min1draw,'red')
        minloc=game_over_font.render("Locate 3 BOMBS!",True,"black")
        w1=minloc.get_width()
        screen.blit(minloc,(size[0]/2-w1/2, upper_margin+12*block_size))
        save=font.render('SAVE',True,"White")
        w2=save.get_width()
        savebutton=pygame.draw.rect(screen,color6,(size[0]/2-1.5*block_size,upper_margin+15*block_size, 3*block_size, block_size))
        screen.blit(save,(size[0]/2-w2/2, upper_margin+15*block_size+block_size/2-font_size/2))
        pos=pygame.mouse.get_pos()
        if savebutton.collidepoint(pos):
                  color6="gray"
        else:
                  color6='black'
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
          if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and savebutton.collidepoint(pos):
             if len(mina1)==3:
                  second_player_ships_unfinished=True
                  mining1=False
          if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and (left_margin<pos[0]<left_margin+10*block_size) and (upper_margin<pos[1]<upper_margin+10*block_size) and len(mina1)<3:
                x_y=(int((pos[0] - left_margin) // block_size),int((pos[1] - upper_margin) // block_size))
                for elem in player1_ships_list:
                    for el in elem:
                        e=(el[0]-1,el[1]-1)
                        for i in range(-1,2):
                            for j in range(-1,2):
                                if 0<=e[0]+i<10 and 0<=e[1]+j<10:
                                    if (e[0]+i,e[1]+j)==x_y:
                                        av=False
                if x_y in mina1:
                    av=False
                if av:
                    list=[(x_y[0]+1,x_y[1]+1)]
                    min1draw.append(list)
                    mina1.append(x_y)
                else:
                    av=True
    


    if mining2:
        draw_ships(player2_ships_list)
        draw_ships(min2draw,'red')
        minloc=game_over_font.render("Locate 3 BOMBS!",True,"black")
        w1=minloc.get_width()
        screen.blit(minloc,(size[0]/2-w1/2, upper_margin+12*block_size))
        save=font.render('SAVE',True,"White")
        w2=save.get_width()
        savebutton=pygame.draw.rect(screen,color6,(size[0]/2-1.5*block_size,upper_margin+15*block_size, 3*block_size, block_size))
        screen.blit(save,(size[0]/2-w2/2, upper_margin+15*block_size+block_size/2-font_size/2))
        pos=pygame.mouse.get_pos()
        if savebutton.collidepoint(pos):
                  color6="gray"
        else:
                  color6='black'
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
          if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and savebutton.collidepoint(pos):
             if len(mina2)==3:
                  mining2=False
                  choose_mode=True
          if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and (left_margin+15*block_size<pos[0]<left_margin+25*block_size) and (upper_margin<pos[1]<upper_margin+10*block_size) and len(mina2)<3:
                x_y=(int((pos[0] - left_margin) // block_size),int((pos[1] - upper_margin) // block_size))
                for elem in player2_ships_list:
                    for el in elem:
                        e=(el[0]-1,el[1]-1)
                        for i in range(-1,2):
                            for j in range(-1,2):
                                if 15<=e[0]+i<25 and 0<=e[1]+j<10:
                                    if (e[0]+i,e[1]+j)==x_y:
                                        av=False
                if x_y in mina2:
                    av=False
                if av:
                    list=[(x_y[0]+1,x_y[1]+1)]
                    min2draw.append(list)
                    mina2.append(x_y)
                else:
                    av=True

    



    if second_player_ships_unfinished:
       draw_ships(player2_ships_list)
       player2auto=AutoShips(15)
       autobutton=pygame.draw.rect(screen,color3,(left_margin+16*block_size,upper_margin+11*block_size, 3*block_size, block_size))
       auto=font.render('AUTO',True,"White")
       nad=new_font.render('Locate ships!',True,'black')
       w1=auto.get_width()
       screen.blit(nad,(left_margin+16*block_size,upper_margin+13*block_size))
       screen.blit(auto,(left_margin+16*block_size-w1/2+3*block_size/2, upper_margin+11*block_size+block_size/2-font_size/2))
       save=font.render('SAVE',True,"White")
       w2=save.get_width()
       savebutton=pygame.draw.rect(screen,color4,(left_margin+18.5*block_size,upper_margin+15*block_size, 3*block_size, block_size))
       screen.blit(save,(left_margin+18.5*block_size-w2/2+3*block_size/2, upper_margin+15*block_size+block_size/2-font_size/2))
       pos=pygame.mouse.get_pos()
       own=font.render('OWN',True,"white")
       ownbutton=pygame.draw.rect(screen,color5,(left_margin+21*block_size,upper_margin+11*block_size, 3*block_size, block_size))
       w3=own.get_width()
       screen.blit(own,(left_margin+21*block_size-w3/2+3*block_size/2, upper_margin+11*block_size+block_size/2-font_size/2))
       if autobutton.collidepoint(pos):
                  color3="gray"
       else:
                  color3='black'
       if savebutton.collidepoint(pos):
                  color4="gray"
       else:
                  color4='black'
       if ownbutton.collidepoint(pos):
                  color5="gray"
       else:
                  color5='black'
       for event in pygame.event.get():
          if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

          if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and autobutton.collidepoint(pos):
               player2_ships_list.clear()
               player2_ships_list=player2auto.ships
               draw_own=False
          if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and ownbutton.collidepoint(pos):
              player2_ships_list.clear()
              d=[1,1,1,1,2,2,2,3,3,4]
              locked_blocks2.clear()
              draw_own=True
          if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and savebutton.collidepoint(pos):
             if len(player2_ships_list)==10:
                  second_player_ships_unfinished=False
                  mining2=True
                  draw_own=False
          if draw_own:
        
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and ((left_margin+15*block_size<pos[0]<left_margin+25*block_size) and (upper_margin<pos[1]<upper_margin+10*block_size)):
               x_st=pos[0]
               y_st=pos[1]
               drawing=True
            if event.type == pygame.MOUSEMOTION:
              if drawing:
                pos=event.pos
                wid=pos[0]-x_st
                heig=pos[1]-y_st

                pygame.draw.rect(screen,'red',(x_st,y_st,wid,heig), width=block_size//10)
            if event.type == pygame.MOUSEBUTTONUP and event.button==1 and drawing:
                   drawing=False
                   pos=event.pos
                   if pos[0]<x_st or pos[1]<y_st or pos[0]>left_margin+25*block_size or pos[1]>upper_margin+10*block_size:
                       pass
                   else:
                       st_x_y=(int((x_st - left_margin) // block_size),int((y_st - upper_margin) // block_size))
               
                       f_x_y=(int((pos[0] - left_margin) // block_size),int((pos[1] - upper_margin) // block_size))
                
                       if f_x_y[0]==st_x_y[0] and f_x_y[1]-st_x_y[1]<4 and f_x_y not in locked_blocks2 and st_x_y not in locked_blocks2:
                         
                           for i in range(f_x_y[1]-st_x_y[1]+1):
                               new_ship.append((f_x_y[0]+1,st_x_y[1]+i+1))
                           
                           if len(new_ship) in d:
                             for el in new_ship:
                               for i in range(-2,1):
                                  for j in range(-2,1):
                                    locked_blocks2.append((el[0]+i,el[1]+j))
                             player2_ships_list.append(new_ship)
                             d.remove(len(new_ship))
                           new_ship=[]
                       elif f_x_y[1]==st_x_y[1] and f_x_y[0]-st_x_y[0]<4 and f_x_y not in locked_blocks2 and st_x_y not in locked_blocks2:
                           for i in range(f_x_y[0]-st_x_y[0]+1):
                               new_ship.append((st_x_y[0]+i+1,st_x_y[1]+1))
                           if len(new_ship) in d:
                             for el in new_ship:
                               for i in range(-2,1):
                                  for j in range(-2,1):
                                    locked_blocks2.append((el[0]+i,el[1]+j))
                             player2_ships_list.append(new_ship)
                             d.remove(len(new_ship))
                           new_ship=[]


    if choose_mode:
        co=game_over_font.render("Choose MODE!",True,"black")
        w1=co.get_width()
        screen.blit(co,(size[0]/2-w1/2, upper_margin+11*block_size))
        classicmode=font.render('Classic',True,"White")
        timemode=font.render('5s for move',True,"White")
        w2=classicmode.get_width()
        w3=timemode.get_width()
        button1=pygame.draw.rect(screen,color6,(size[0]/2-8*block_size,upper_margin+16*block_size, 4*block_size, 1.5*block_size))
        button2=pygame.draw.rect(screen,color5,(size[0]/2+4*block_size,upper_margin+16*block_size, 4*block_size, 1.5*block_size))
        screen.blit(classicmode,(size[0]/2-6*block_size-w2/2, upper_margin+16*block_size+0.75*block_size-font_size/2))
        screen.blit(timemode,(size[0]/2+6*block_size-w3/2, upper_margin+16*block_size+0.75*block_size-font_size/2))
        pos=pygame.mouse.get_pos()
        if button1.collidepoint(pos):
                  color6="gray"
        else:
                  color6='black'
        if button2.collidepoint(pos):
                  color5="gray"
        else:
                  color5='black'
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
          if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and button1.collidepoint(pos):
                  Game=True
                  choose_mode=False
                  Gaming=True
                  bgsound.play()
                  pygame.time.set_timer(bgr,193450)
          if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and button2.collidepoint(pos):
                  Game2=True
                  choose_mode=False
                  Gaming=True
                  bgsound.play()
                  pygame.time.set_timer(bgr,193450)

    if Gaming:
        for elem in hitted_blocks1:
          if elem in available1:
              available1.remove(elem)
        for elem in hitted_blocks2:
          if elem in available2:
              available2.remove(elem)
        for elem in mina1:
          if elem in available1:
              available1.remove(elem)
        for elem in mina2:
          if elem in available2:
              available2.remove(elem)
        
    
    if Game:
        # draw_ships(player1_ships_list)
        # draw_ships(player2_ships_list)
        draw_ships(destroyed_player1_ships,'black')
        draw_ships(destroyed_player2_ships,'black')
        draw_ships(min1boom,'red')

        draw_ships(min2boom,'red')
        # count=font1.render(str(5-timer),False,'red')
        # screen.blit(count,(left_margin+12*block_size,upper_margin+3*block_size))
        if move_first:
           turn=font.render("YOUR TURN!",False,'red')
           screen.blit(turn,(left_margin+3.3*block_size,upper_margin+11*block_size))
           pos=pygame.mouse.get_pos()
           if alredy:
               na =font.render("Already fired!",False,'red')
               w=na.get_width()
               screen.blit(na,(left_margin+12.5*block_size-w/2,upper_margin+14*block_size))
           if player1moveout:
               out =font.render("Out of Grid!",False,'red')
               w=out.get_width()
               screen.blit(out,(left_margin+12.5*block_size-w/2,upper_margin+14*block_size))
           for event in pygame.event.get():
              if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
              if event.type == bgr:
                  bgsound.play()
              if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and (left_margin+15*block_size<pos[0]<left_margin+25*block_size and upper_margin<pos[1]<upper_margin+10*block_size):
                 hitted=((pos[0] - left_margin) // block_size,(pos[1] - upper_margin) // block_size)
                #  if hitted in available2:
                #     available2.remove(hitted)
                 if hitted in hitted_blocks2 :
                     alredy=True
                 else:
                     hitted=((pos[0] - left_margin) // block_size+1,(pos[1] - upper_margin) // block_size+1)
                     alredy=False
                     miss=True
                     for elem in player2_ships_list:
                         if hitted in elem:
                             miss=False
                             hit=True
                             hitted=((pos[0] - left_margin) // block_size ,(pos[1] - upper_margin) // block_size)
                             destroyed_blocks2.append(hitted)
                             for el in elem:
                                 e=(el[0]-1,el[1]-1)
                                 if e in destroyed_blocks2:
                                     k+=1
                             c+=1
                           
                         if k==len(elem):
                             k=0
                             hit=False
                             breaked=True
                             destroyed_player2_ships.append(elem)
                             for el in elem:
                                 e=(el[0]-1,el[1]-1)
                                 for i in range(-1,2):
                                     for j in range(-1,2):
                                         if 15<=e[0]+i<25 and 0<=e[1]+j<10:
                                            hitted_blocks2.append((e[0]+i,e[1]+j))
                                            # if (e[0]+i,e[1]+j) in available2:
                                            #     available2.remove((e[0]+i,e[1]+j))

                         else:
                             k=0
                     if c==0:
                        move_first=0
                     c=0
                     hitted=((pos[0] - left_margin) // block_size,(pos[1] - upper_margin) // block_size )
                     if hitted in mina2:
                         miss=False
                         breaked=True
                         list=[((pos[0] - left_margin) // block_size+1,(pos[1] - upper_margin) // block_size+1 )]
                         min2boom.append(list)
                         l=random.randint(0,len(available1))
                         if l>=len(available1):
                                    l=0
                         hitted_blocks1.append(available1[l])
                         for elem in player1_ships_list:
                          k=0
                          if (available1[l][0]+1,available1[l][1]+1) in elem:
                             destroyed_blocks1.append(available1[l])
                             for el in elem:
                                 e=(el[0]-1,el[1]-1)
                                 if e in destroyed_blocks1:
                                     k+=1
                          
                          if k==len(elem):
                             k=0
                             destroyed_player1_ships.append(elem)
                             for el in elem:
                                 e=(el[0]-1,el[1]-1)
                                 for i in range(-1,2):
                                     for j in range(-1,2):
                                         if 0<=e[0]+i<10 and 0<=e[1]+j<10:
                                            hitted_blocks1.append((e[0]+i,e[1]+j))
                                            # if (e[0]+i,e[1]+j) in available1:
                                            #     available1.remove((e[0]+i,e[1]+j))

                          else:
                             k=0
                        #  available1.remove(available1[l])
                     hitted_blocks2.append(hitted)
                 player1moveout=False
              elif event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and (pos[0]<left_margin+15*block_size or pos[0]>left_margin+25*block_size or pos[1]<upper_margin or pos[1]>upper_margin+10*block_size):
                 player1moveout=True
                 alredy=False
           if breaked:
               breaksound.play()
               breaked=False
           elif miss:
               misssound.play()
               miss=False
           elif hit:
               hitsound.play()
               hit=False
               

              
        else:
            turn=font.render("YOUR TURN!",False,'red')
            screen.blit(turn,(left_margin+18.3*block_size,upper_margin+11*block_size))
            pos=pygame.mouse.get_pos()
            if alredy:
               na =font.render("Already fired!",False,'red')
               w=na.get_width()
               screen.blit(na,(left_margin+12.5*block_size-w/2,upper_margin+14*block_size))
            if player2moveout:
               out =font.render("Out of Grid!",False,'red')
               w=out.get_width()
               screen.blit(out,(left_margin+12.5*block_size-w/2,upper_margin+14*block_size))
            for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  pygame.quit()
                  sys.exit() 
              if event.type == bgr:
                  bgsound.play()  
              if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and (left_margin<pos[0]<left_margin+10*block_size and upper_margin<pos[1]<upper_margin+10*block_size):
                 hitted=((pos[0] - left_margin) // block_size ,(pos[1] - upper_margin) // block_size)
                #  if hitted in available1:
                #     available1.remove(hitted)
                 if hitted in hitted_blocks1:
                     alredy=True
                 else:
                     hitted=((pos[0] - left_margin) // block_size+1,(pos[1] - upper_margin) // block_size+1)
                     alredy=False
                     miss=True
                     for elem in player1_ships_list:
                         if hitted in elem:
                             miss=False
                             hit=True
                             hitted=((pos[0] - left_margin) // block_size ,(pos[1] - upper_margin) // block_size)
                             destroyed_blocks1.append(hitted)
                             for el in elem:
                                 e=(el[0]-1,el[1]-1)
                                 if e in destroyed_blocks1:
                                     k+=1
                             c+=1
                            
                         if k==len(elem):
                             k=0
                             hit=False
                             breaked=True
                             destroyed_player1_ships.append(elem)
                             for el in elem:
                                 e=(el[0]-1,el[1]-1)
                                 for i in range(-1,2):
                                     for j in range(-1,2):
                                         if 0<=e[0]+i<10 and 0<=e[1]+j<10:
                                            hitted_blocks1.append((e[0]+i,e[1]+j))
                                        #  if (e[0]+i,e[1]+j) in available1:
                                        #         available1.remove((e[0]+i,e[1]+j))
                         else:
                             k=0
                     if c==0:
                        move_first=1
                     c=0
                     hitted=((pos[0] - left_margin) // block_size ,(pos[1] - upper_margin) // block_size)
                     if hitted in mina1:
                         miss=False
                         breaked=True
                         list=[((pos[0] - left_margin) // block_size+1,(pos[1] - upper_margin) // block_size+1 )]
                         min1boom.append(list)
                         l=random.randint(0,len(available2))
                         if l>=len(available2):
                                    l=0
                         hitted_blocks2.append(available2[l])
                         for elem in player2_ships_list:
                          k=0
                          if (available2[l][0]+1,available2[l][1]+1) in elem:
                             destroyed_blocks2.append(available2[l])
                             for el in elem:
                                 e=(el[0]-1,el[1]-1)
                                 if e in destroyed_blocks2:
                                     k+=1
                            
                          if k==len(elem):
                             k=0
                             destroyed_player2_ships.append(elem)
                             for el in elem:
                                 e=(el[0]-1,el[1]-1)
                                 for i in range(-1,2):
                                     for j in range(-1,2):
                                         if 15<=e[0]+i<25 and 0<=e[1]+j<10:
                                            hitted_blocks2.append((e[0]+i,e[1]+j))
                                            # if (e[0]+i,e[1]+j) in available2:
                                            #     available2.remove((e[0]+i,e[1]+j))
                           
                          else:
                             k=0
                        #  available2.remove(available2[l])  
                     hitted_blocks1.append(hitted)
                 player2moveout=False
              elif event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and (pos[0]<left_margin or pos[0]>left_margin+10*block_size or pos[1]<upper_margin or pos[1]>upper_margin+10*block_size):
                 alredy=False
                 player2moveout=True 
            if breaked:
               breaksound.play()
               breaked=False
            elif miss:
               misssound.play()
               miss=False
            elif hit:
               hitsound.play()
               hit=False


    if Game2:
        # draw_ships(player1_ships_list)
        # draw_ships(player2_ships_list)
        draw_ships(destroyed_player1_ships,'black')
        draw_ships(destroyed_player2_ships,'black')
        draw_ships(min1boom,'red')
        draw_ships(min2boom,'red')
        count=font1.render(str(5-timer),False,'red')
        screen.blit(count,(left_margin+12*block_size,upper_margin+3*block_size))
        if move_first:
           if startfree==1:
               pygame.time.set_timer(pygame.USEREVENT,1000)

           turn=font.render("YOUR TURN!",False,'red')
           screen.blit(turn,(left_margin+3.3*block_size,upper_margin+11*block_size))
           pos=pygame.mouse.get_pos()
           if alredy:
               na =font.render("Already fired!",False,'red')
               w=na.get_width()
               screen.blit(na,(left_margin+12.5*block_size-w/2,upper_margin+14*block_size))
           if player1moveout:
               out =font.render("Out of Grid!",False,'red')
               w=out.get_width()
               screen.blit(out,(left_margin+12.5*block_size-w/2,upper_margin+14*block_size))
           for event in pygame.event.get():
              if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
              if event.type == bgr:
                  bgsound.play()
              if event.type==pygame.USEREVENT:
                  timer+=1
                  if timer==5:
                      pygame.time.set_timer(pygame.USEREVENT,1000)
                      timer=0
                      move_first=0
                      startfree+=1
              if move_first:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and (left_margin+15*block_size<pos[0]<left_margin+25*block_size and upper_margin<pos[1]<upper_margin+10*block_size):
                        hitted=((pos[0] - left_margin) // block_size,(pos[1] - upper_margin) // block_size)
                        # if hitted in available2:
                        #     available2.remove(hitted)
                        if hitted in hitted_blocks2 :
                            alredy=True
                        else:
                            hitted=((pos[0] - left_margin) // block_size+1,(pos[1] - upper_margin) // block_size+1)
                            alredy=False
                            miss=True
                            for elem in player2_ships_list:
                                if hitted in elem:
                                    miss=False
                                    hit=True
                                    hitted=((pos[0] - left_margin) // block_size ,(pos[1] - upper_margin) // block_size)
                                    destroyed_blocks2.append(hitted)
                                    for el in elem:
                                        e=(el[0]-1,el[1]-1)
                                        if e in destroyed_blocks2:
                                            k+=1
                                    c+=1
                                    #  hitted=((pos[0] - left_margin) // block_size ,(pos[1] - upper_margin) // block_size)
                                    #  destroyed_blocks2.append(hitted)
                                if k==len(elem):
                                    hit=False
                                    breaked=True
                                    k=0
                                    destroyed_player2_ships.append(elem)
                                    for el in elem:
                                        e=(el[0]-1,el[1]-1)
                                        for i in range(-1,2):
                                            for j in range(-1,2):
                                                if 15<=e[0]+i<25 and 0<=e[1]+j<10:
                                                    hitted_blocks2.append((e[0]+i,e[1]+j))
                                                    # if (e[0]+i,e[1]+j) in available2:
                                                    #     available2.remove((e[0]+i,e[1]+j))

                                else:
                                    k=0
                            if c==0:
                                pygame.time.set_timer(pygame.USEREVENT,0)
                                move_first=0
                                startfree+=1
                                timer=0
                                pygame.time.set_timer(pygame.USEREVENT,1000)
                            else:
                                pygame.time.set_timer(pygame.USEREVENT,0)
                                timer=0
                                startfree+=2
                                pygame.time.set_timer(pygame.USEREVENT,1000)
                            c=0
                            hitted=((pos[0] - left_margin) // block_size,(pos[1] - upper_margin) // block_size )
                            if hitted in mina2:
                                miss=False
                                breaked=True
                                list=[((pos[0] - left_margin) // block_size+1,(pos[1] - upper_margin) // block_size+1 )]
                                min2boom.append(list)
                                l=random.randint(0,len(available1))
                                if l>=len(available1):
                                    l=0
                                hitted_blocks1.append(available1[l])
                                for elem in player1_ships_list:
                                 if (available1[l][0]+1,available1[l][1]+1) in elem:
                                    destroyed_blocks1.append(available1[l])
                                    for el in elem:
                                        e=(el[0]-1,el[1]-1)
                                        if e in destroyed_blocks1:
                                            k+=1
                                    #  hitted=((pos[0] - left_margin) // block_size ,(pos[1] - upper_margin) // block_size)
                                    #  destroyed_blocks2.append(hitted)
                                 if k==len(elem):
                                    k=0
                                    destroyed_player1_ships.append(elem)
                                    for el in elem:
                                        e=(el[0]-1,el[1]-1)
                                        for i in range(-1,2):
                                            for j in range(-1,2):
                                                if 0<=e[0]+i<10 and 0<=e[1]+j<10:
                                                    hitted_blocks1.append((e[0]+i,e[1]+j))
                                                    # if (e[0]+i,e[1]+j) in available1:
                                                    #     available1.remove((e[0]+i,e[1]+j))

                                 else:
                                    k=0
                                # available1.remove(available1[l])
                            hitted_blocks2.append(hitted)
                        player1moveout=False

                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and (pos[0]<left_margin+15*block_size or pos[0]>left_margin+25*block_size or pos[1]<upper_margin or pos[1]>upper_margin+10*block_size):
                        player1moveout=True
                        alredy=False
           if breaked:
               breaksound.play()
               breaked=False
           elif miss:
               misssound.play()
               miss=False
           elif hit:
               hitsound.play()
               hit=False


              
        else:
            if startfree==1:
               pygame.time.set_timer(pygame.USEREVENT,1000)
            turn=font.render("YOUR TURN!",False,'red')
            screen.blit(turn,(left_margin+18.3*block_size,upper_margin+11*block_size))
            pos=pygame.mouse.get_pos()
            if alredy:
               na =font.render("Already fired!",False,'red')
               w=na.get_width()
               screen.blit(na,(left_margin+12.5*block_size-w/2,upper_margin+14*block_size))
            if player2moveout:
               out =font.render("Out of Grid!",False,'red')
               w=out.get_width()
               screen.blit(out,(left_margin+12.5*block_size-w/2,upper_margin+14*block_size))
            for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  pygame.quit()
                  sys.exit()
              if event.type == bgr:
                  bgsound.play()
              if event.type==pygame.USEREVENT:
                  timer+=1
                  if timer==5:
                      pygame.time.set_timer(pygame.USEREVENT,0)
                      timer=0
                      pygame.time.set_timer(pygame.USEREVENT,1000)
                      move_first=1 
                      startfree+=1
              if move_first==0:  
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and (left_margin<pos[0]<left_margin+10*block_size and upper_margin<pos[1]<upper_margin+10*block_size):
                        hitted=((pos[0] - left_margin) // block_size ,(pos[1] - upper_margin) // block_size)
                        # if hitted in available1:
                        #     available1.remove(hitted)
                        if hitted in hitted_blocks1:
                            alredy=True
                        else:
                            hitted=((pos[0] - left_margin) // block_size+1,(pos[1] - upper_margin) // block_size+1)
                            alredy=False
                            miss=True
                            for elem in player1_ships_list:
                                if hitted in elem:
                                    miss=False
                                    hit=True
                                    hitted=((pos[0] - left_margin) // block_size ,(pos[1] - upper_margin) // block_size)
                                    destroyed_blocks1.append(hitted)
                                    for el in elem:
                                        e=(el[0]-1,el[1]-1)
                                        if e in destroyed_blocks1:
                                            k+=1
                                    c+=1
                                    #  hitted=((pos[0] - left_margin) // block_size ,(pos[1] - upper_margin) // block_size)
                                    #  destroyed_blocks1.append(hitted)
                                if k==len(elem):
                                    hit=False
                                    breaked=True
                                    k=0
                                    destroyed_player1_ships.append(elem)
                                    for el in elem:
                                        e=(el[0]-1,el[1]-1)
                                        for i in range(-1,2):
                                            for j in range(-1,2):
                                                if 0<=e[0]+i<10 and 0<=e[1]+j<10:
                                                    hitted_blocks1.append((e[0]+i,e[1]+j))
                                                # if (e[0]+i,e[1]+j) in available1:
                                                #         available1.remove((e[0]+i,e[1]+j))
                                else:
                                    k=0
                            if c==0:
                                pygame.time.set_timer(pygame.USEREVENT,0)
                                move_first=1
                                startfree+=1
                                timer=0
                                pygame.time.set_timer(pygame.USEREVENT,1000)
                            else:
                                pygame.time.set_timer(pygame.USEREVENT,0)
                                timer=0
                                startfree+=2
                                pygame.time.set_timer(pygame.USEREVENT,1000)
                            c=0
                            hitted=((pos[0] - left_margin) // block_size ,(pos[1] - upper_margin) // block_size)
                            if hitted in mina1:
                                miss=False
                                breaked=True
                                list=[((pos[0] - left_margin) // block_size+1,(pos[1] - upper_margin) // block_size+1 )]
                                min1boom.append(list)
                                l=random.randint(0,len(available2))
                                if l>=len(available2):
                                    l=0
                                hitted_blocks2.append(available2[l])
                                for elem in player2_ships_list:
                                  if (available2[l][0]+1,available2[l][1]+1) in elem:
                                    destroyed_blocks2.append(available2[l])
                                    for el in elem:
                                        e=(el[0]-1,el[1]-1)
                                        if e in destroyed_blocks2:
                                            k+=1
                                    
                                  if k==len(elem):
                                    k=0
                                    destroyed_player2_ships.append(elem)
                                    for el in elem:
                                        e=(el[0]-1,el[1]-1)
                                        for i in range(-1,2):
                                            for j in range(-1,2):
                                                if 15<=e[0]+i<25 and 0<=e[1]+j<10:
                                                    hitted_blocks2.append((e[0]+i,e[1]+j))
                                                    # if (e[0]+i,e[1]+j) in available2:
                                                    #     available2.remove((e[0]+i,e[1]+j))
                                
                                  else:
                                    k=0
                                # available2.remove(available2[l])  
                            hitted_blocks1.append(hitted)
                        player2moveout=False
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and (pos[0]<left_margin or pos[0]>left_margin+10*block_size or pos[1]<upper_margin or pos[1]>upper_margin+10*block_size):
                        alredy=False
                        player2moveout=True 
            if breaked:
               breaksound.play()
               breaked=False
            elif miss:
               misssound.play()
               miss=False
            elif hit:
               hitsound.play()
               hit=False


    if len(destroyed_player1_ships)==10:
        player1lose=True
        destroyed_player1_ships=[]
        Game2=False
        Game=False
        Gaming=False
        player2wins+=1
        pygame.mixer.pause()
        winsound.play()
        pygame.time.set_timer(bgr,0)
    elif len(destroyed_player2_ships)==10:
        player2lose=True
        destroyed_player2_ships.clear()
        Game2=False
        Game=False
        Gaming=False
        pygame.mixer.pause()
        winsound.play()
        pygame.time.set_timer(bgr,0)
        player1wins+=1
    if player2lose:
        screen.fill('red')
        win=game_over_font.render('PLAYER 1 WIN!!!',False,'white')
        w=win.get_width()
        restart=font.render('RESTART',True,"White")
        w2=restart.get_width()
        restartbutton=pygame.draw.rect(screen,'black',(size[0]/2-2*block_size,upper_margin+15*block_size, 4*block_size, block_size))
        screen.blit(restart,(size[0]/2-w2/2, upper_margin+15*block_size+block_size/2-font_size/2))
        screen.blit(win,(size[0]/2-w/2, size[1]/2-game_over_font_size/2))
        pos=pygame.mouse.get_pos()
        for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  pygame.quit()
                  sys.exit()   
              if event.type == pygame.MOUSEBUTTONUP and event.button==1 and restartbutton.collidepoint(pos):
                        x_st=0
                        y_st=0
                        new_ship=[] 
                        c=0
                        k=0
                        player1_ships_list=[]
                        b=[1,1,1,1,2,2,2,3,3,4]
                        d=[1,1,1,1,2,2,2,3,3,4]
                        player2_ships_list=[]
                        first_player_ships_unfinished=True
                        second_player_ships_unfinished=False
                        move_first=random.randint(0,2)
                        Game=False
                        player1moveout=False
                        player2moveout=False
                        hitted_blocks1 = []
                        hitted=[]
                        drawing=False
                        hitted_blocks2 = []
                        locked_blocks1 = []
                        locked_blocks2 = []
                        mina1=[]
                        min1draw=[]
                        min2draw=[]
                        mina2=[]
                        mining1=False
                        mining2=False
                        undestroyed_player1_ships = []
                        undestroyed_player2_ships = []
                        destroyed_player1_ships.clear()
                        destroyed_player2_ships.clear()
                        destroyed_blocks1 = []
                        destroyed_blocks2 = []
                        alredy=False
                        draw_own=False
                        colorh='black'
                        color1='black'
                        color2='black'
                        color3='black'
                        color4='black'
                        color5='black'
                        color6='black'
                        av=True
                        min2boom=[]
                        min1boom=[]
                        available1=[]
                        player1lose=False
                        player2lose=False
                        choose_mode=False
                        classic=False
                        timegame=False
                        startfree=0
                        timer=0
                        for i in range(10):
                          for j in range(10):
                            available1.append((i,j))

                        available2=[]
                        for i in range(15,25):
                            for j in range(10):
                                available2.append((i,j))
    if player1lose:
        screen.fill('red')
        win=game_over_font.render('PLAYER 2 WIN!!!',False,'white')
        w=win.get_width()
        restart=font.render('RESTART',True,"White")
        w2=restart.get_width()
        restartbutton=pygame.draw.rect(screen,'black',(size[0]/2-2*block_size,upper_margin+15*block_size, 4*block_size, block_size))
        screen.blit(restart,(size[0]/2-w2/2, upper_margin+15*block_size+block_size/2-font_size/2))
        screen.blit(win,(size[0]/2-w/2, size[1]/2-game_over_font_size/2))
        pos=pygame.mouse.get_pos()
        for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  pygame.quit()
                  sys.exit()   
              if event.type == pygame.MOUSEBUTTONUP and event.button==1 and restartbutton.collidepoint(pos):
                        x_st=0
                        y_st=0
                        new_ship=[] 
                        c=0
                        k=0
                        player1_ships_list=[]
                        b=[1,1,1,1,2,2,2,3,3,4]
                        d=[1,1,1,1,2,2,2,3,3,4]
                        player2_ships_list=[]
                        first_player_ships_unfinished=True
                        second_player_ships_unfinished=False
                        move_first=random.randint(0,2)
                        Game=False
                        player1moveout=False
                        player2moveout=False
                        hitted_blocks1 = []
                        hitted=[]
                        drawing=False
                        hitted_blocks2 = []
                        locked_blocks1 = []
                        locked_blocks2 = []
                        mina1=[]
                        min1draw=[]
                        min2draw=[]
                        mina2=[]
                        mining1=False
                        mining2=False
                        undestroyed_player1_ships = []
                        undestroyed_player2_ships = []
                        destroyed_player1_ships.clear()
                        destroyed_player2_ships.clear()
                        destroyed_blocks1 = []
                        destroyed_blocks2 = []
                        alredy=False
                        draw_own=False
                        colorh='black'
                        color1='black'
                        color2='black'
                        color3='black'
                        color4='black'
                        color5='black'
                        color6='black'
                        av=True
                        min2boom=[]
                        min1boom=[]
                        available1=[]
                        player2lose=False
                        player1lose=False
                        choose_mode=False
                        classic=False
                        timegame=False
                        startfree=0
                        timer=0
                        for i in range(10):
                            for j in range(10):
                               available1.append((i,j))

                        available2=[]
                        for i in range(15,25):
                            for j in range(10):
                                available2.append((i,j))
    fps.tick(30)
    pygame.display.update()