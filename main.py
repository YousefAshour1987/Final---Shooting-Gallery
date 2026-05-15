from turtle import *
import random

### CLASS and FUNCTION DEFINITIONS ###

def generate_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"

def playing_area():
    pen = Turtle()
    pen.ht()
    pen.speed(0)
    pen.color('teal')
    pen.begin_fill()
    pen.goto(-240,240)
    pen.goto(240,240)
    pen.goto(240,-240)
    pen.goto(-240,-240)
    pen.goto(-240,240)
    pen.end_fill()

class Player(Turtle):
    def __init__(self, x, y, color, screen, right_key, left_key, fire_key, health):
        super().__init__()
        self.ht()
        self.speed(0)
        self.hue = color
        self.color(color)
        self.penup()
        self.goto(x,y)
        self.setheading(90)
        self.shape("turtle")
        self.bullets = []
        self.alive = True
        self.st()
        screen.onkeypress(self.turn_left, left_key)
        screen.onkeypress(self.turn_right, right_key)
        screen.onkey(self.fire, fire_key)
    def turn_left(self):
        self.left(10)

    def turn_right(self):
        self.right(10)
        
    def fire(self):
        self.bullets.append(Bullet(self))

    def die(self):
        self.alive = False
        self.hideturtle()

class Bullet(Turtle):
    def __init__(self, player):
        super().__init__()
        self.ht()
        self.speed(0)
        self.penup()
        self.goto(player.xcor(), player.ycor())
        self.seth(player.heading())
        self.color("white")
        self.st()
        self.player = player

    def move(self):
        self.forward(10)
        if not (-250 < self.xcor() < 250 and -250 < self.ycor() < 250):
            self.die()

    def die(self):
        self.hideturtle()
        self.player.bullets.remove(self)

class Block(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.ht()
        self.speed(255)
        self.color("gray")
        self.shape("square")
        self.health = 3
        self.penup()
        self.goto(x, y)
        self.alive = True
        self.st()

### PROGRAM ###
screen = Screen()
screen.setup(520, 520)
screen.bgcolor("black")

screen.listen()

playing_area()

blocks = []

p1 = Player(-100, 0, "red", screen, "d", "a", "w", 3)
p2 = Player(100, 0, "blue", screen, "Right", "Left", "Up", 3)

for y in range(190, 140, -20):
    for x in range(-100, 120, 20):
        blocks.append(Block(x, y))

while True:
    for bullet in p1.bullets:
        bullet.move()
        if p2.distance(bullet) < 20:
            bullet.die()
            p2.health -=1
            if p2.health == 2: 
                p2.color("yellow")
            elif p2.health == 1: 
                p2.color("red")
            else:
                p2.hideturtle()
    for bullet in p2.bullets:
        bullet.move()

        if p1.distance(bullet) < 20:
            bullet.die()
            p1.health -=1
            if p1.health == 2: 
                p1.color("yellow")
            elif p1.health == 1: 
                p1.color("red")
            else:
                p1.hideturtle()
screen.exitonclick()