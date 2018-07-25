from tkinter import *
from Game import Game, Agent
from geometry import Point2D, Vector2D
import math
import random
import time

class Paddle(Agent):
    START_X   = 0.01
    START_Y   = 0.02
    WIDTH     = 1.0
    LENGTH    = 5.0
    AGILITY   = 0.2

    def __init__(self,world):
        self.in_middle = True
        self.length = self.LENGTH
        self.width  = self.WIDTH
        xoffset = -self.START_X 
        position = world.bounds.point_at((xoffset+1.0)/2.0,self.START_Y)
        Agent.__init__(self,position,world)
        
    def keep_within_bounds(self):
        if self.position.x - self.length/2.0 < self.world.bounds.xmin:
            self.position.x = self.world.bounds.xmin + self.length/2.0
        if self.position.x + self.length/2.0 > self.world.bounds.xmax:
            self.position.x = self.world.bounds.xmax - self.length/2.0

    def hits_paddle(self,ball):

        if ball.position.y <= self.position.y + self.width:
            if ball.position.x >= self.position.x - self.length/2.0 and ball.position.x <= self.position.x + self.length/2.0:
                return True
        else:
            return False
        
    def color(self):
        return "#FF8040"

    def shape(self):
        p1 = self.position + Vector2D( -self.length/2.0, -self.width/2.0)       
        p2 = self.position + Vector2D( self.length/2.0, -self.width/2.0)        
        p3 = self.position + Vector2D(self.length/2.0,self.width/2.0)       
        p4 = self.position + Vector2D( -self.length/2.0,self.width/2.0)       
        return [p1,p2,p3,p4]
        
    def move_left(self):
        self.position.x -= self.length * self.AGILITY
        self.keep_within_bounds()

    def move_right(self):
        self.position.x += self.length * self.AGILITY
        self.keep_within_bounds()

    def update(self):
        if self.world.use_mouse:
            if self.world.ball == None:
                return
            
            else:
                if self.world.ball.heading.dx < 0.0 and (not self.in_middle):
                    return

            self.position.x = self.world.mouse_position.x
            self.keep_within_bounds()

class Brick(Agent):
    WIDTH     = 1.5
    LENGTH    = 3.5
#Keep track of sides of the sides of the brick, not the width.
    def __init__(self,world, health, START_X, START_Y):
        self.in_middle = True
        self.length = self.LENGTH
        self.width  = self.WIDTH
        xoffset = -START_X 
        position = world.bounds.point_at((xoffset+1.0)/2.0,START_Y)
        self.health = health
        Agent.__init__(self,position,world)
        self.world.brick_list.append(self)
    '''
    def explode(self, ball):
        if self.hits_brick(ball):
            self.health -=1 
            print("hello")
        if self.health <= 0:
            self.leave()
    '''
#CHECK:
    def hits_brick(self,ball):

        if ball.position.y >= self.position.y - self.width/2.0 and ball.position.y <= self.position.y + self.width/2.0:
            if ball.position.x >= self.position.x - self.length/2.0 and ball.position.x <= self.position.x + self.length/2.0:
                self.health -= 1    
                self.world.score += 5
                self.world.power_count += 1
                self.world.report()
                self.world.report()
                self.world.report()
                self.world.report()
                self.world.report("SCORE: " + str(self.world.score))
                return True
                return True
        else:
            return False

    def color(self):
        if self.health > 4:
            return "#7fef84"
        elif self.health == 4 or self.health == 3 or self.health == 2:
            return "#edef7f"
        elif self.health == 1:
            return "#fc0000"
            
       

    def shape(self):
        p1 = self.position + Vector2D( -self.length/2.0, -self.width/2.0)       
        p2 = self.position + Vector2D( self.length/2.0, -self.width/2.0)        
        p3 = self.position + Vector2D(self.length/2.0,self.width/2.0)       
        p4 = self.position + Vector2D( -self.length/2.0,self.width/2.0)       
        return [p1,p2,p3,p4]

    def update(self):
        if self.health <= 0:
            self.world.remove(self)
            self.world.brick_list.remove(self)
            self.world.score += 5

class Power(Agent):
    WIDTH     = 1.5
    LENGTH    = 3.5
    def __init__(self,world, health, START_X, START_Y):
        self.in_middle = True
        self.length = self.LENGTH
        self.width  = self.WIDTH
        xoffset = -START_X 
        if  START_X <= 1.0 and START_X >= -1.0:
            position = world.bounds.point_at(START_X,START_Y)
        else:
            START_X = (-1 + rand())*2
            position = world.bounds.point_at(START_X,START_Y)
        self.health = health
        Agent.__init__(self,position,world)
        self.world.brick_list.append(self)

    def hits_brick(self,ball):

        if ball.position.y >= self.position.y - self.width/2.0 and ball.position.y <= self.position.y + self.width/2.0:
            if ball.position.x >= self.position.x - self.length/2.0 and ball.position.x <= self.position.x + self.length/2.0:
                self.health -= 1
                self.world.score += 1
                return True
        else:
            return False

    def color(self):
        return "#ffffff"

    def shape(self):
        p1 = self.position + Vector2D( -self.length/2.0, -self.width/2.0)       
        p2 = self.position + Vector2D( self.length/2.0, -self.width/2.0)        
        p3 = self.position + Vector2D(self.length/2.0,self.width/2.0)       
        p4 = self.position + Vector2D( -self.length/2.0,self.width/2.0)       
        return [p1,p2,p3,p4]

    def update(self):
        if self.health <= 0:
            self.world.remove(self)
            self.world.brick_list.remove(self)
            self.world.score += 10

class Shield(Agent):
    WIDTH     = 1.5
    LENGTH    = 3.5
    def __init__(self,world, health, START_X, START_Y):
        self.in_middle = True
        self.length = self.LENGTH
        self.width  = self.WIDTH
        xoffset = -START_X 
        if  START_X <= 1.0 and START_X >= -1.0:
            position = world.bounds.point_at(START_X,START_Y)
        else:
            START_X = (-1 + rand())*2
            position = world.bounds.point_at(START_X,START_Y)
        self.health = health
        Agent.__init__(self,position,world)
        self.world.brick_list.append(self)

    def hits_brick(self,ball):

        if ball.position.y >= self.position.y - self.width/2.0 and ball.position.y <= self.position.y + self.width/2.0:
            if ball.position.x >= self.position.x - self.length/2.0 and ball.position.x <= self.position.x + self.length/2.0:
                self.health -= 1
                self.world.score += 1
                return True
        else:
            return False

    def color(self):
        return "#a1fcf3"

    def shape(self):
        p1 = self.position + Vector2D( -self.length/2.0, -self.width/2.0)       
        p2 = self.position + Vector2D( self.length/2.0, -self.width/2.0)        
        p3 = self.position + Vector2D(self.length/2.0,self.width/2.0)       
        p4 = self.position + Vector2D( -self.length/2.0,self.width/2.0)       
        return [p1,p2,p3,p4]

    def update(self):
        if self.health <= 0:
            self.world.remove(self)
            self.world.brick_list.remove(self)
            self.world.score += 10

class Damage(Agent):
    WIDTH     = 1.5
    LENGTH    = 3.5
    def __init__(self,world, health, START_X, START_Y):
        self.in_middle = True
        self.length = self.LENGTH
        self.width  = self.WIDTH
        xoffset = -START_X 
        position = world.bounds.point_at((xoffset+1.0)/2.0,START_Y)
        self.health = health
        Agent.__init__(self,position,world)
        self.world.brick_list.append(self)

    def hits_brick(self,ball):

        if ball.position.y >= self.position.y - self.width/2.0 and ball.position.y <= self.position.y + self.width/2.0:
            if ball.position.x >= self.position.x - self.length/2.0 and ball.position.x <= self.position.x + self.length/2.0:
                self.health -= 1
                self.world.score += 1
                return True
        else:
            return False

    def color(self):
        return "#ef7f7f"

    def shape(self):
        p1 = self.position + Vector2D( -self.length/2.0, -self.width/2.0)       
        p2 = self.position + Vector2D( self.length/2.0, -self.width/2.0)        
        p3 = self.position + Vector2D(self.length/2.0,self.width/2.0)       
        p4 = self.position + Vector2D( -self.length/2.0,self.width/2.0)       
        return [p1,p2,p3,p4]

    def update(self):
        if self.health <= 0:
            self.world.remove(self)
            self.world.brick_list.remove(self)
            self.world.score += 10
class Unbreakable(Agent):
    WIDTH     = 1.5
    LENGTH    = 10.0
    def __init__(self,world, health, START_X, START_Y):
        self.in_middle = True
        self.length = self.LENGTH
        self.width  = self.WIDTH
        xoffset = -START_X 
        position = world.bounds.point_at((xoffset+1.0)/2.0,START_Y)
        self.health = health
        Agent.__init__(self,position,world)
        self.world.brick_list.append(self)

    def hits_brick(self,ball):

        if ball.position.y >= self.position.y - self.width/2.0 and ball.position.y <= self.position.y + self.width/2.0:
            if ball.position.x >= self.position.x - self.length/2.0 and ball.position.x <= self.position.x + self.length/2.0:
                self.health -= 1
                self.world.score += 1
                return True
        else:
            return False

    def color(self):
        return "#56259b"

    def shape(self):
        p1 = self.position + Vector2D( -self.length/2.0, -self.width/2.0)       
        p2 = self.position + Vector2D( self.length/2.0, -self.width/2.0)        
        p3 = self.position + Vector2D(self.length/2.0,self.width/2.0)       
        p4 = self.position + Vector2D( -self.length/2.0,self.width/2.0)       
        return [p1,p2,p3,p4]

    def update(self):
        if self.health <= 0:
            self.world.remove(self)
            self.world.brick_list.remove(self)
            self.world.score += 10

class Prize(Agent):
    WIDTH     = 1.5
    LENGTH    = 3.5
    def __init__(self,world, health, START_X, START_Y):
        self.in_middle = True
        self.length = self.LENGTH
        self.width  = self.WIDTH
        xoffset = -START_X 
        position = world.bounds.point_at((xoffset+1.0)/2.0,START_Y)
        self.health = health
        Agent.__init__(self,position,world)
        self.world.brick_list.append(self)

    def hits_brick(self,ball):

        if ball.position.y >= self.position.y - self.width/2.0 and ball.position.y <= self.position.y + self.width/2.0:
            if ball.position.x >= self.position.x - self.length/2.0 and ball.position.x <= self.position.x + self.length/2.0:
                self.health -= 1
                self.world.score += 1
                return True
        else:
            return False

    def color(self):
        return "#f902e5"

    def shape(self):
        p1 = self.position + Vector2D( -self.length/2.0, -self.width/2.0)       
        p2 = self.position + Vector2D( self.length/2.0, -self.width/2.0)        
        p3 = self.position + Vector2D(self.length/2.0,self.width/2.0)       
        p4 = self.position + Vector2D( -self.length/2.0,self.width/2.0)       
        return [p1,p2,p3,p4]

    def update(self):
        if self.health <= 0:
            self.world.remove(self)
            self.world.brick_list.remove(self)
            self.world.score += 10

class Wormhole(Agent):
    WIDTH     = 2
    LENGTH    = 2
    def __init__(self,world, health, START_X, START_Y):
        self.in_middle = True
        self.length = self.LENGTH
        self.width  = self.WIDTH
        xoffset = -START_X 
        position = world.bounds.point_at((xoffset+1.0)/2.0,START_Y)
        self.health = health
        Agent.__init__(self,position,world)
        self.world.brick_list.append(self)

    def hits_brick(self,ball):

        if ball.position.y >= self.position.y - self.width/2.0 and ball.position.y <= self.position.y + self.width/2.0:
            if ball.position.x >= self.position.x - self.length/2.0 and ball.position.x <= self.position.x + self.length/2.0:
                self.health -= 1
                self.world.score += 1
                return True
        else:
            return False

    def color(self):
        return "#ff9d00"

    def shape(self):
        p1 = self.position + Vector2D( -self.length/2.0, -self.width/2.0)       
        p2 = self.position + Vector2D( self.length/2.0, -self.width/2.0)        
        p3 = self.position + Vector2D(self.length/2.0,self.width/2.0)       
        p4 = self.position + Vector2D( -self.length/2.0,self.width/2.0)       
        return [p1,p2,p3,p4]

    def update(self):
        if self.health <= 0:
            self.world.remove(self)
            self.world.brick_list.remove(self)
            self.world.score += 10


class Ball(Agent):

    START_Y   = 0.1
    SPEED     = 0.55

    def __init__(self,world):
        dy = 1.0 
        dx = random.uniform(-3.0,3.0)
        self.heading = Vector2D(dx,dy)
        offset = -self.START_Y 
        position = world.bounds.point_at(random.random(), (1.0+offset)/2.0)
        Agent.__init__(self,position,world)

    def check_bounce_horizontal(self,y_value,from_above=True):
        if from_above:
            if self.position.y >= y_value:
                self.position.y = y_value - abs(self.position.y-y_value)
                self.heading.dy = -self.heading.dy
        else:
            if self.position.y <= y_value:
                self.position.y = y_value + abs(self.position.y-y_value)
                self.heading.dy = -self.heading.dy

    def check_bounce_vertical(self,x_value,from_left=True):
        if from_left:
            if self.position.x >= x_value:
                self.position.x = x_value - abs(self.position.x-x_value)
                self.heading.dx = -self.heading.dx
        else:
            if self.position.x <= x_value:
                self.position.x = x_value + abs(self.position.x-x_value)
                self.heading.dx = -self.heading.dx
       
    def update(self):
        if not self.world.serving:
            old_position = self.position
            new_position = self.position + self.heading * self.SPEED
            self.position = new_position
            if self.world.paddle.hits_paddle(self):
                self.check_bounce_horizontal(self.world.paddle.position.y+self.world.paddle.width/2.0,from_above=False)
            for k in self.world.brick_list:
                if Ball.SPEED == 0.22:
                    if self.world.power_count >= 3:
                        Ball.SPEED = 0.55
                elif Ball.SPEED == 0.85 and self.world.score > 180:
                    if self.world.power_count >= 3:
                        Ball.SPEED = 0.75
                elif Ball.SPEED == 0.85 and self.world.score <= 180:
                    if self.world.power_count >= 3:
                        Ball.SPEED = 0.55
                if self.world.paddle.length == 15.0:
                    if self.world.power_count >= 5:
                        self.world.paddle.length = 5.0
                if k.hits_brick(self):
                    if type(k) is Power:
                        Ball.SPEED = 0.22
                        self.world.power_count = 0
                    if type(k) is Damage:
                        Ball.SPEED = 0.85
                        self.world.power_count = 0
                    if type(k) is Shield:
                        self.world.paddle.length = 15.0
                        self.world.power_count = 0
                    if type(k) is Unbreakable:
                        self.check_bounce_horizontal(k.position.y-k.width/2.0,from_above=True)
                    if type(k) is Prize:
                        self.world.score += 25
                    if type(k) is Wormhole:
                        self.position.x,self.position.y = 0 + random.uniform(-0.3,0.3), 0.5+ random.uniform(-0.3,0.3)
                    if self.position.y <= k.position.y + k.width/2.0 and self.position.y>k.position.y:
                        self.check_bounce_horizontal(k.position.y+k.width/2.0,from_above=False)
                    elif self.position.y >= k.position.y - k.width/2.0 and self.position.y<k.position.y:
                        self.check_bounce_horizontal(k.position.y-k.width/2.0,from_above=True)
                    elif self.position.x == k.position.x + k.length/2.0:
                        self.check_bounce_vertical(k.position.x + k.length/2.0,from_left=True)
                    elif self.position.x == k.position.x - k.length/2.0:
                        self.check_bounce_vertical(k.position.x - k.length/2.0,from_left=False)

                    
            self.check_bounce_horizontal(self.world.bounds.ymax,from_above=True)
            self.check_bounce_vertical(self.world.bounds.xmin,from_left=False)
            self.check_bounce_vertical(self.world.bounds.xmax,from_left=True)
        else:
            paddle = self.world.paddle
            self.position = Point2D(paddle.position.x,paddle.position.y)

    def color(self):
        return "#cd0de2"

    def shape(self):
        p1 = self.position + Vector2D( 0.5, 0.5)       
        p2 = self.position + Vector2D(-0.5, 0.5)        
        p3 = self.position + Vector2D(-0.5,-0.5)        
        p4 = self.position + Vector2D( 0.5,-0.5)
        return [p1,p2,p3,p4]

class BrickBreaker(Game):

    def __init__(self):
        Game.__init__(self,"BRICKBREAKER",60.0,45.0,800,600,topology='bound',console_lines=6)

        self.report("Hit 'z' or '/' to move.")
        self.report("Hit 'q' to quit.")
        self.report("Hit 'p' to pause.")
        self.report("Hit SPACE to switch mouse mode on/off.")
        self.report("Mac users will want to make this window full screen.")

        self.score  = 0
        self.use_mouse   = False
        self.reset()

        self.ball = Ball(self)
        self.paddle  = Paddle(self)
        self.serving = False

        self.brick_list = []
        self.power_count = 0
        self.UNCount = 0
        self.speedcount = 0
        self.brick_checker = 1
        
        
        for j in range(5,11, 2):
            if j/10 == 0.5 or j/10 == 0.9:
                for i in range(-8,10, 2):
                    Brick(self,5, i/10, j/10)
            elif j/10 == 0.7:
                for i in range(-9,10, 2):
                    Brick(self,5, i/10, j/10)
        
        Shield(self,1, 0.7, 0.85)  
        Shield(self, 1, 0.55, 0.75)
        Shield(self, 1, 0.6, 0.65)
        Power(self, 1, 0.3, 0.83)
        Power(self, 1, 0.88, 0.65)
        Power(self, 1, 0.2, 0.86)
        Damage(self,1, 0.1, 0.75)
        Damage(self,1, 0.7, 0.6)
        Damage(self,1, -0.5, 0.58)
        Prize(self,1, 0, 0.97)
        Prize(self,1, -0.5, 0.97)
        Prize(self, 1, 0.5, 0.97 )
        Wormhole(self,float('inf'), 0.9, 0.3)
        Wormhole(self, float('inf'), -0.9, 0.3)
        Wormhole(self, float('inf'), 0.9, 0.8)
        Wormhole(self, float('inf'), -0.9, 0.8)       
        
    def handle_keypress(self,event):
        Game.handle_keypress(self,event)
        if event.char == ' ':
            self.use_mouse = not self.use_mouse
        elif event.char == 'z' and not self.use_mouse:
            self.paddle.move_left()
        elif event.char == '/' and not self.use_mouse:
            self.paddle.move_right()
        
        elif event.char == 'x' and not self.use_mouse:
            if self.serving:
                self.serving = False
    
        
    def handle_mouse_release(self,event):
        Game.handle_mouse_release(self,event)
        if self.use_mouse:
            self.serving = False

    def reset(self):
        self.ticks_before_start = 100
        self.ball = None

    def serve(self):
        self.ball = Ball(self)
        if self.use_mouse:
            self.report("Hit space, then 'x' to start.")
        else:
            self.report("Hit 'x' to start.")
        self.serving = True

    def display_score(self):
        self.report("SCORE:"+str(self.score))

    def update(self):
        if self.ball == None:
            self.ticks_before_start -= 1
            if self.ticks_before_start <= 0:
                self.serve()


        Game.update(self)
        if self.score > 250 and self.UNCount!=1:
            Unbreakable(self, float('inf'), 0.7, 0.4)
            Unbreakable(self, float('inf'), -0.7, 0.4)
            Unbreakable(self, float('inf'), 0, 0.4)
            self.UNCount = 1
    
            
        if self.score > 180 and self.speedcount!=1:
            self.ball.SPEED = 0.75
            self.report()
            self.report()
            self.report()
            self.report()
            self.report('SPEED UP!')
            self.speedcount = 1
        if self.ball != None:
            if self.ball.position.y <= self.bounds.ymin:
                self.ball.leave()
                if self.score <=5:
                    self.score -= 1
                if self.score > 5 and self.score < 20:
                    self.score -= 10
                if self.score > 20 and self.score < 50:
                    self.score -= 20
                if self.score > 50 and self.score < 100:
                    self.score -= 50
                if self.score > 100:
                    self.score -= 100
                if self.score <= 0:
                    self.report()
                    self.report()
                    self.report()
                    self.report()
                    self.report("YOU LOSE!")
                    self.display_score()
                    self.report()
                    time.sleep(1)
                    self.GAME_OVER = True
                else:
                    self.report()
                    self.report()
                    self.report()
                    self.report()
                    self.report("YOU LOSE POINTS!")
                    self.display_score()
                    self.reset()
        
        if len(self.brick_list) == 5:
                for k in self.brick_list:
                    if type(k) is Unbreakable:
                        self.brick_checker = 0
                if self.brick_checker == 0:
                    self.canvas.create_text(30,20,fill="white",font="Times 20 italic bold",
                        text="YOU WIN")
                    time.sleep(1)
                    self.GAME_OVER = True


game = BrickBreaker()
while not game.GAME_OVER:
    time.sleep(1.0/60.0)
    game.update()
