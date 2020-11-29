#Import the turtle module
import turtle
import os
import random
import time

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space War By @Aaryan Sarda")
wn.setup(width=800, height=700)
#CChange the background image
wn.bgpic("starfield1.gif")
turtle.setundobuffer(1)
wn.tracer(0)
turtle.ht()

player_vertices = ((0, 15), (-15, 0), (-18, 5), (-18, -5), (0, 0), (18, -5), (18, 5), (15, 0))
wn.register_shape("player", player_vertices)

class Sprite(turtle.Turtle):
    def __init__(self, shape, color, startx, starty):
        turtle.Turtle.__init__(self, shape=shape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)

        self.speed = 1

    def move(self):
        self.fd(self.speed)

        #Boundary Detection
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)
        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

    def is_collision(self, other):
        if (self.xcor() >= (other.xcor() - 20)) and\
        (self.xcor() <= (other.xcor() + 20)) and\
        (self.ycor() >= (other.ycor() - 20)) and\
        (self.ycor() <= (other.ycor() + 20)):
            return True
        else:
            return False



class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 2
        self.lives = 10

    def turn_left(self):
        self.lt(45)

    def turn_right(self):
        self.rt(45)

    def accelerate(self):
        self.speed += 0.1

    def decelerate(self):
        self.speed -= 0.1
        if self.speed <= 0:
            self.speed = 0

class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 6
        self.setheading(random.randint(0, 360))

class Particles(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.goto(-1000, -1000)
        self.speed = 10
        self.frame = 0
    
    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0, 360))
        self.frame = 1

    def move(self):
        if self.frame > 0:
            self.fd(self.speed)
            self.frame += 1
        
        if self.frame > 10:
            self.frame = 0
            self.goto(-1000, -1000)


class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 8
        self.setheading(random.randint(0, 360))
    
    def move(self):
        self.fd(self.speed)

        #Boundary Detection
        if self.xcor() > 290:
            self.setx(290)
            self.lt(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.lt(60)
        if self.ycor() > 290:
            self.sety(290)
            self.lt(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.lt(60)

class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000, 1000)

    def fire(self):
        if self.status == "ready":
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "active"

    def move(self):

        if self.status == "ready":
            self.goto(-1000, 1000)

        if self.status == "active":
            self.fd(self.speed)

        #Border Check
        if self.xcor() < -290 or self.xcor() > 290 or self.ycor() < -290 or self.ycor() > 290:
            self.goto(-1000, 1000)
            self.status = "ready"



class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.pen2 = turtle.Turtle()
        self.lives = 3

    def draw_border(self):
        #Draw border
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.pendown()

    def show_status(self):
        self.pen.undo()
        msg = "Score: %s" %(self.score)
        self.pen.penup()
        self.pen.goto(-300, 310)
        self.pen.write(msg, move = False, align="center", font=("Arial", 16, "normal"))

    def show_status2(self):
        self.pen2.undo()
        self.pen2.color("white")
        msg = "Lives: %s" %(player.lives)
        self.pen2.penup()
        self.pen2.goto(-230, 310)
        self.pen2.write(msg, move = False, align="center", font=("Arial", 16, "normal"))

#Create the game border
game = Game()

#Draw the border
game.draw_border()

#Show the status
game.show_status()

#Create the sprites
player = Player("player", "white", 0, 0)
#enemy = Enemy("circle", "red", -100, 0)
missile = Missile("triangle", "yellow", 0, 0)
#ally = Ally("square", "blue", 0, 0)

enemies = []
for i in range(6):
    enemies.append(Enemy("circle", "red", -100, 0))

allies = []
for i in range(6):
    allies.append(Ally("square", "blue", 100, 0))

particles = []
for i in range(20):
    particles.append(Particles("circle", "orange", 0, 0))

#Keyboard bindings
wn.listen()
wn.onkeypress(player.turn_left, "Left")
wn.onkeypress(player.turn_right, "Right")
wn.onkeypress(player.accelerate, "Up")
wn.onkeypress(player.decelerate, "Down")
wn.onkeypress(missile.fire, "space")

#Main game loop
while True:

    wn.update()
    time.sleep(0.03)
    player.move()
    #enemy.move()
    missile.move()
    #ally.move()

    for enemy in enemies:
        enemy.move()

        #Check for collisions
        if player.is_collision(enemy):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            game.score -= 20
            game.show_status()

        #Check for a collision between the missile and the enemy
        if missile.is_collision(enemy):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            missile.status = "ready"
            #Increase the score
            game.score += 10
            game.show_status()

            #Do gthe explosion
            for particle in particles:
                particle.explode(missile.xcor(), missile.ycor())

    for particle in particles:
        particle.move()


    for ally in allies:
        ally.move()

        #Check for a collision between the missile and the ally
        if missile.is_collision(ally):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            missile.status = "ready"
            game.score -= 10
            game.show_status()


wn.mainloop()