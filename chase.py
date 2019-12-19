#! python3
# chase.py

# Coding the Chase sequence of the game.

# Create a map, preferably a maze, make three exits, it does not need to perfectly match the text game.

# The player must chase and hit the runaway to catch them.

# Make sure there are enough places to go so that the player has a chance to catch the runaway.

# Create a mini AI for the runaway so that he isn’t just moving in relation to the player.

import pygame
import escape

pygame.init()

# CONSTANTS --------
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
WINDOW_TITLE = "Chase"
REFRESH_RATE = 60
BGCOLOUR = (16, 16, 16)
WHITE =    (0xFF, 0xFF, 0xFF)
BLACK =    ( 0x0,  0x0,  0x0)
RED =      (0xFF,  0x0,  0x0)
GREEN =    ( 0x0, 0xFF,  0x0)
BLUE =     ( 0x0,  0x0, 0xFF)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.walls = None

        self.vel_x = 0
        self.vel_y = 0

        

    def update(self):
       
        self.rect.x += self.vel_x
        wall_hit_list = pygame.sprite.spritecollide(
            self, self.walls, False
        )

        for wall in wall_hit_list:
            
            if self.vel_x > 0:
                self.rect.right = wall.rect.left
            else:
                self.rect.left = wall.rect.right

        self.rect.y += self.vel_y

        wall_hit_list = pygame.sprite.spritecollide(
            self, self.walls, False
        )

        for wall in wall_hit_list:
            if self.vel_y > 0:
                self.rect.bottom = wall.rect.top
            else:
                self.rect.top = wall.rect.bottom

    def change_vel(self, x, y):
        self.vel_x += x
        self.vel_y += y

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    
    # where the enemy code will be placed.
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([20, 20])
        self.image.fill(WHITE)
        self.velocity = 3
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.wall = None

        self.direction = "right"

        self.velx = 0
        self.vely = 0

    


    # def update(self):
    
        # define the way the enemy moves in the world.
        # set out a path system to give the enemy a list of choices 
        # so that it can select one of the paths to choose
    def update(self):
        self.rect.x += self.velx
        wall_hit = pygame.sprite.spritecollide(
            self, self.wall, False
        )

        for walls in wall_hit:

            if self.velx > 0:
                self.rect.right = walls.rect.left
                self.direction = "up"
            else:
                self.rect.left = self.rect.right
                self.direction = "right"
                
        self.rect.y += self.vely
        wall_hit = pygame.sprite.spritecollide(
            self, self.wall, False
        )

        for walls in wall_hit:
            if self.vely > 0:
                self.rect.bottom = walls.rect.top
                self.direction = "left"
            else:
                self.rect.top = walls.rect.bottom
                self.direction = "down"

        if self.direction == "up":
            self.vely =  -self.velocity
            

        elif self.direction == "down":
            self.vely = self.velocity
           

        elif self.direction == "right":
            self.velx = self.velocity


        elif self.direction == "left":
            self.velx = -self.velocity
            
    def change_velocity(self, x, y):
        self.vely += y
        self.velx += x
   



def mains():

    PLAYER_SPEED = 5
    # LOCAL variables ----------
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    done = False
    pygame.display.set_caption(WINDOW_TITLE)

    map_sprite_list = pygame.sprite.Group()
    all_sprite_list = pygame.sprite.Group()
    enemy_list = pygame.sprite.Group()

    wall_top = Wall(10, SCREEN_HEIGHT-10, SCREEN_WIDTH-20, 10)
    wall_bottom = Wall(0, 0, 10, 600)
    wall_side = Wall(10, 0, 790, 10)
    wall_side2 = Wall(SCREEN_WIDTH-10, 0, 10, SCREEN_HEIGHT)

    
    

    map_sprite_list.add(wall_top, wall_bottom, wall_side, wall_side2)
    all_sprite_list.add(wall_top, wall_bottom, wall_side, wall_side2)

    player = Player(50, 50)

    player.walls = map_sprite_list
    all_sprite_list.add(player)

    enemy = Enemy(20, 20)
    
    enemy.wall = map_sprite_list
    enemy_list.add(enemy)
    all_sprite_list.add(enemy)

    # main loop
    while not done:
        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.change_vel(0, -PLAYER_SPEED)
                    
                elif event.key == pygame.K_s:
                    player.change_vel(0, PLAYER_SPEED)
                elif event.key == pygame.K_a:
                    player.change_vel(-PLAYER_SPEED, 0)
                elif event.key == pygame.K_d:
                    player.change_vel(PLAYER_SPEED, 0)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.change_vel(0, PLAYER_SPEED)
                elif event.key == pygame.K_s:
                    player.change_vel(0, -PLAYER_SPEED)
                elif event.key == pygame.K_a:
                    player.change_vel(PLAYER_SPEED, 0)
                elif event.key == pygame.K_d:
                    player.change_vel(-PLAYER_SPEED, 0)
        
        # game logic -------------

        # get the player's position in relation to 
        # "left" "right" "up" and "down" in relation to the enemy,
        # remove the direction the player occupies from the enemy's 
        # movement list at that time.

        #for enemy in enemy_list:
            #for mapped_area in map_sprite_list:
                #if pygame.sprite.collide_rect(enemy, mapped_area):
                    #if enemy.direction == "right": enemy.direction == "up"
                    #elif enemy.direction == "up": enemy.direction == "down"
                    #elif enemy.direction == "down": enemy.direction == "left"
                    #else: enemy.direction == "right"

        all_sprite_list.update()

        # drawing --------------
        screen.fill(BGCOLOUR)
        all_sprite_list.draw(screen)
        pygame.display.flip()

        # clock tick -------------
        clock.tick(REFRESH_RATE)

