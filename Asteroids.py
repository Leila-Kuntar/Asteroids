# Asteroids by Leila Kuntar
# You can try it on
# http://www.codeskulptor.org/#user42_OuOMkvK6Tv_0.py

import simplegui
import math
import random

# globals for user interface
width = 800
height = 600
time = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center
 
    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
 
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris1_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 500, 10)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 50, 1500) 
asteroid_images = [simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_brown.png"),
                   simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png"),
                   simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")]

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
soundtrack.set_volume(.5)
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
ship_thrust_sound.set_volume(.7)
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
explosion_sound.set_volume(.10)

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def vector_len(p1, p2):
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
    
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, 
                              self.pos, self.image_size, self.angle)
      
    def do_thrust(self, bOn):
        if bOn:
            ship_thrust_sound.play()
            self.image_center = [135, 45] 
        else:
            ship_thrust_sound.rewind() 
            self.image_center = [45, 45]  
            
        self.thrust = bOn
        
    def inc_angle_velocity(self):
        self.angle_vel += 0.06
        
    def dec_angle_velocity(self):
        self.angle_vel -= 0.06
        
    def reset_angle_velocity(self):
        self.angle_vel = 0
    
    def get_pos(self):
        return self.pos
        
    def shoot(self):
        global a_missile_set
        forward = angle_to_vector(self.angle) 
        pos = [self.pos[0]+(35 * math.cos(self.angle)), self.pos[1]+(35*math.sin(self.angle))] 
        vel = [self.vel[0] + forward[0]*10,self.vel[1] + forward[1]*10]
        a_missile_set.add(Sprite(pos,vel, 0, 0, missile_image, missile_info, missile_sound))
        
    def update(self):
        self.angle += self.angle_vel 
        self.pos[0] = (self.pos[0] + self.vel[0]) % width
        self.pos[1] = (self.pos[1] + self.vel[1]) % height
        forward = angle_to_vector(self.angle)
        if (self.thrust):
            self.vel[0] += forward[0]*0.3
            self.vel[1] += forward[1]*0.3
        '''update the velocity vector by a small fraction of the 
           forward acceleration vector so that the ship does not accelerate too fast''' 
        fraction = 1 - 0.025
        self.vel[0] *=  fraction
        self.vel[1] *=  fraction

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.bExplosion = False 
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        global bLastExplosion 
        if self.bExplosion == True:
            index = self.t//1 
            size = explosion_info.get_size() 
            center = [explosion_info.get_center()[0] + size[0]*index, explosion_info.get_center()[1]]
            canvas.draw_image(explosion_image, center, size, self.pos, size)
            self.t += 0.5 
            if self.t >= 25:
                explosion_sound.rewind() 
                if self.bLastExp == True:
                    bLastExplosion = False
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]  
        self.age += 1 
            
        return self.age<self.lifespan and self.pos[0]<=width and self.pos[1]<=height
    
    def get_pos(self):
        return self.pos
        
    def start_explosion(self, bLast = False):
        explosion_sound.play() 
        self.lifespan = 50
        self.age = 0 
        self.bExplosion = True 
        self.bLastExp = bLast
        self.t = 0
        
    def collide(self, other_sprite):
        return  (self.bExplosion == False) and (vector_len(self.pos, other_sprite.get_pos()) <= self.radius) 
     
def draw(canvas):
    global time, g_bonus, g_score, g_lives, bInGame, g_rocks_count, t, bLastExplosion, g_best_score, g_max_rocks_count
 
    # animate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8.0) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [width/2, height/2], [width, height])
    canvas.draw_image(debris_image, [center[0]-wtime, center[1]], [size[0]-2*wtime, size[1]], 
                                [width/2+1.25*wtime, height/2], [width-2.5*wtime, height])
    canvas.draw_image(debris_image, [size[0]-wtime, center[1]], [0.1 + 2*wtime, size[1]], 
                                [1.25*wtime, height/2], [0.1 + 2.5*wtime, height])
    
    canvas.draw_text("Lives: "+str(g_lives), (20, 30), 20, "White")
    canvas.draw_text("Score: "+str(g_score), (660, 30), 20, "White")
    canvas.draw_text("Best score: "+str(g_best_score), (660, 50), 15, "White")

    if bInGame or bLastExplosion:
        for a_rock in set(a_rock_set):
            a_rock.draw(canvas)
            if (a_rock.update() == False):
                a_rock_set.remove(a_rock)
                g_rocks_count -= 1 
                
        for a_missile in set(a_missile_set):
            a_missile.draw(canvas)
            if (a_missile.update() == False):
                a_missile_set.remove(a_missile) 
                
        if bLastExplosion == False:
            my_ship.draw(canvas)
            my_ship.update()
        
            for a_rock in a_rock_set:
                if a_rock.collide(my_ship):
                    g_lives -= 1
                    if g_lives == 0:
                        finish_game() 
                        a_rock.start_explosion(True)
                        break 
                    else:
                        a_rock.start_explosion()
                for a_missile in set(a_missile_set):
                    if a_rock.collide(a_missile):
                       a_rock.start_explosion()
                       a_missile_set.remove(a_missile) 
                       g_score += 5 
                       if g_score > g_best_score:
                            g_best_score = g_score
                       if g_score >= g_bonus:
                            g_lives += 1
                            g_max_rocks_count += 5
                            g_bonus += g_bonus
    else:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), 
                                [width/2, height/2], splash_info.get_size())
        
# timer handler that spawns a rock    
def rock_spawner():   
    global a_rock_set, g_rocks_count, g_max_rocks_count 
    if bInGame and (g_rocks_count<g_max_rocks_count):
        pos = [random.randrange(0, width), random.randrange(0, height)]
        horizontal_vel = vertical_vel = 0 
        while (horizontal_vel == 0):
            horizontal_vel = random.randrange(-28,28)/10
        while (vertical_vel == 0):
            vertical_vel = random.randrange(-8,8)/10 
        vel = [horizontal_vel, vertical_vel] 
        angle_vel = random.randrange(-1, 1)*0.01
        asteroid_image = asteroid_images[random.randrange(0, 3)] 
        a_rock_set.add(Sprite(pos, vel, 0, angle_vel, asteroid_image, asteroid_info))
        g_rocks_count+=1 
        

def keydown(key):
    global bShoot
    if bInGame:
        if key == 38: #up arrow key
            my_ship.do_thrust(True)
        elif key == 37: #left arrow key
            my_ship.dec_angle_velocity()
        elif key == 39: #right arrow key
            my_ship.inc_angle_velocity()
        elif key == 32: #space key
            my_ship.shoot()
            bShoot = True
        
def keyup(key):
    if bInGame:
        if key == 39 or key == 37: 
            my_ship.reset_angle_velocity()  
        elif key == 38: 
            my_ship.do_thrust(False)
            
def mouseclick(pos):
    global bInGame
    size = splash_info.get_size()
    center = [width / 2, height / 2]
    if ( (pos[0] <= center [0] + size[0]/2) and (pos[0] >= center [0] - size[0]/2)
        and (pos[1] <= center [1] + size[1]/2) and (pos[1] >= center [1] - size[1]/2)):
        start_game()
    
def finish_game():
    global bInGame, bLastExplosion
    bInGame = False
    bLastExplosion = True
    ship_thrust_sound.rewind()
    soundtrack.rewind() 
    missile_sound.rewind()
        
def start_game():
    global g_bonus, a_rock_set, a_missile_set, g_lives, g_score, bInGame, g_rocks_count, my_ship, t, bLastExplosion, g_max_rocks_count
    if bInGame == False and bLastExplosion == False:
        # initialize ship and sprite's sets
        a_rock_set = set([])
        a_missile_set = set([])
        my_ship = Ship([width / 2, height / 2], [0,0.01], 0, ship_image, ship_info)
        g_lives = 3 
        g_score = 0 
        g_bonus = 100 
        g_rocks_count = 0
        g_max_rocks_count = 15
        bLastExplosion = False
        rock_spawner()
        bInGame = True 
        soundtrack.play() 
    
# initialize frame
frame = simplegui.create_frame("Asteroids", width, height)


bInGame = False
bLastExplosion = False
g_lives = 3
g_score = 0 
g_best_score = 0 
g_rocks_count = 0 
g_max_rocks_count = 0
# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(mouseclick)
frame.add_label("**************************")
frame.add_label("Welcome to RiceRocks!")
frame.add_label("**************************")
frame.add_label("")
frame.add_label("**************************")
frame.add_label("Available keys")
frame.add_label("**************************")
frame.add_label("Right arrow: to turn  clockwise")
frame.add_label("Left arrow: to turn counterclockwise")
frame.add_label("Up arrow: to accelerate")
frame.add_label("Space: to shoot")


timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()