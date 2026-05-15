from turtle import *
import random
import time

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
    def __init__(self, x, y, color, screen, right_key, left_key, fire_key, show_score):
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
        self.score = 0
        self.show_score = show_score
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
class Score(Turtle):
    def __init__(self, x, y, player_name):
        super().__init__()
        self.ht()
        self.speed(0)
        self.penup()
        self.goto(x, y)
        self.color("white")
        self.score = 0
        self.player_name = player_name
        self.update_score()

    def update_score(self):
        self.clear()
        self.write(f"{self.player_name}: {self.score}")

    def add_score(self, points):
        self.score += points
        self.update_score()


### PROGRAM ###
screen = Screen()
screen.setup(520, 520)
screen.bgcolor("black")

screen.listen()

start = time.time()

playing_area()

blocks = []

p1 = Player(-100, 0, "red", screen, "d", "a", "w", 0)
p2 = Player(100, 0, "blue", screen, "Right", "Left", "Up", 0)
def update():
    if time.time() - start > 2:
        start = time.time()
        for block in blocks:
            block.sety(block.ycor()-20)
            blocks.append(Block(x, y))
            for y in range(210, 160, -20):
                for x in range(-220, 230, 20):
                    blocks.append(Block(x, y))
for y in range(210, 160, -20):
    for x in range(-220, 230, 20):
        blocks.append(Block(x, y))

while True:
    screen.update()
    if time.time() - start > 2:
        start = time.time()
        for block in blocks:
            block.sety(block.ycor()-20)
            blocks.append(Block(x, y))
        

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