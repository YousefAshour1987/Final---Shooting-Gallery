from turtle import *
import random
import time

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
    def __init__(self, x, y, color, screen, right_key, left_key, fire_key, score_display):
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
        self.score_display = score_display
        self.st()
        screen.onkeypress(self.turn_left, left_key)
        screen.onkeypress(self.turn_right, right_key)
        screen.onkey(self.fire, fire_key)
    def turn_left(self):
        self.left(10)
    def turn_right(self):
        self.right(10)
    def fire(self):
        if len(self.bullets) < 5 and self.alive:
            self.bullets.append(Bullet(self))
    def die(self):
        self.alive = False
        self.hideturtle()
class Bullet(Turtle):
    def __init__(self, player):
        super().__init__()
        self.ht()
        self.penup()
        self.goto(player.xcor(), player.ycor())
        self.seth(player.heading())
        self.color("white")
        self.st()
        self.player = player
        self.alive = True
    def move(self):
        self.forward(10)
        x = self.xcor()
        y = self.ycor()
        if x > 235:
            self.setx(235)
            self.setheading(180 - self.heading())
        elif x < -235:
            self.setx(-235)
            self.setheading(180 - self.heading())
        if y > 235:
            self.die()
        elif y < -235:
            self.die()
    def die(self):
        self.hideturtle()
        self.alive = False
class Block(Turtle):
    def __init__(self, x, y, color):
        super().__init__()
        self.ht()
        self.speed(0)
        self.shape("square")
        self.penup()
        self.goto(x, y)
        self.health = 3
        self.color(color)
        self.alive = True
        self.st()
    def strike(self):
        if self.alive == False:
            return False
        self.health -= 1
        if self.health == 2:
            self.color("orange")
        elif self.health == 1:
            self.color("red")
        elif self.health <= 0:
            self.die()
            return True
        return False
    def die(self):
        self.hideturtle()
        self.alive = False
    def move(self):
        self.sety(self.ycor() - 20)
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
screen = Screen()
screen.setup(520, 600)
screen.bgcolor("black")
screen.tracer(0)
screen.listen()

playing_area()
blocks = []
game_over = False

p1_score = Score(-120, 260, "Player 1")
p2_score = Score(120, 260, "Player 2")

p1 = Player(-100, -200, "red", screen, "d", "a", "w", p1_score)
p2 = Player(100, -200, "blue", screen, "Right", "Left", "Up", p2_score)

def new_row(y):
    new_rows = []
    num_blocks = 0
    for x in range(-100, 120, 20):
        if num_blocks % 2 == 0:
            color = "gray"
        else:
            color = "black"
        new_rows.append(Block(x, y, color))
        num_blocks += 1
    return new_rows

for y in range(220, 160, -20):
    for block in new_row(y):
        blocks.append(block)

start = time.time()

while True:
    screen.update()

    if time.time() - start > 2:
        start = time.time()
        for j in blocks:
            if j.alive:
                j.move()
                if j.ycor() <= -230:
                    game_over = True
                    break
                if p1.alive and p1.distance(j) < 25:
                    game_over = True
                    break
                if p2.alive and p2.distance(j) < 25:
                    game_over = True
                    break
        if game_over:
            break

        for block in new_row(220):
            blocks.append(block)

        new_blocks = []
        for block in blocks:
            if block.alive:
                new_blocks.append(block)
        blocks = new_blocks

    for player in (p1, p2):
        if player.alive:
            bullets = []
            for bullet in player.bullets:
                if bullet.alive:
                    bullets.append(bullet)
            player.bullets = bullets

            for k in player.bullets:
                k.move()
                for i in blocks:
                    if i.alive and bullet.distance(i) < 20:
                        block_hit = i.strike()
                        bullet.die()

                        if block_hit:
                            player.score_display.add_score(1)
                        break

screen.tracer(1)
if game_over:
    pen = Turtle()
    pen.ht()
    pen.penup()
    pen.goto(0, 50)
    pen.color("white")
    pen.write("GAME OVER")
    pen.goto(0, -20)
    pen.write(f"Player 1 Score: {p1_score.score}")
    pen.goto(0, -60)
    pen.write(f"Player 2 Score: {p2_score.score}")

screen.exitonclick()