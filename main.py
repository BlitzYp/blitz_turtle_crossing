import turtle
from typing import List
from random import randint, choice
from math import sqrt

player = turtle.Turtle("turtle")
level = 1
car_density = 5
speed = 3
ONE_UNIT = 20
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
cars: List[turtle.Turtle] = []
info_about_cars = {}
scoreboard = turtle.Turtle()
scoreboard.hideturtle()
scoreboard.penup()

def setup_screen(screen: turtle.Screen) -> None:
    screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen.colormode(255)
    screen.title("Blitz crossing")
    screen.onkeypress(lambda: player.sety(player.ycor() + 10), "Up")
    screen.onkeypress(lambda: player.sety(player.ycor() - 10), "Down")
    screen.onkeypress(lambda: player.setx(player.xcor() + 10), "Right")
    screen.onkeypress(lambda: player.setx(player.xcor() - 10), "Left")
    screen.tracer(0)
    screen.listen()

def setup_player() -> None:
    player.penup()
    player.setpos(0, -(SCREEN_HEIGHT/2 - 30))
    player.left(90)

def handle_car(car: turtle.Turtle(), index: int) -> None:
    if car.xcor() <= -SCREEN_WIDTH/2 or car.xcor() >= SCREEN_WIDTH/2:
        car.setpos(-car.xcor(), car.ycor())
    car.setpos(car.xcor() + speed * info_about_cars[index], car.ycor())
    turtle.update()

def setup_cars() -> None:
    info_about_cars.clear()
    cars.clear()
    for i in range(int(car_density)):
        new_obj = turtle.Turtle("square")
        info_about_cars[i] = choice((1, -1))
        new_obj.shapesize(2, 4)
        new_obj.color((randint(0, 255), randint(0, 255), randint(0, 255)))
        new_obj.penup()
        new_obj.setpos(randint(-SCREEN_WIDTH/2 + 30, SCREEN_WIDTH/2 + 30), randint(-SCREEN_HEIGHT/2 + 100, SCREEN_HEIGHT/2))
        cars.append(new_obj)

def next_level(screen: turtle.Screen) -> None:
    global level, car_density, speed
    screen.resetscreen()
    level += 1
    car_density += 2
    speed *= 1.5 
    scoreboard.penup()
    scoreboard.setpos(-10, SCREEN_HEIGHT/2 - 30)
    scoreboard.write(f"Level {level}", move=False, align="center", font=("Arial", 20, "normal"))
    scoreboard.hideturtle()
    setup_player()
    setup_cars()

def check_collision(car: turtle.Turtle) -> bool:
    return int(sqrt(pow(player.xcor() - car.xcor(), 2) + pow(player.ycor() - car.ycor(), 2))) < ONE_UNIT * 2

if __name__ == "__main__":
    screen = turtle.Screen()
    setup_screen(screen)
    setup_player()
    setup_cars()
    scoreboard.setpos(-10, SCREEN_HEIGHT/2 - 30)
    scoreboard.write(f"Level {level}", move=False, align="center", font=("Arial", 20, "normal"))
    game_on = True
    while True:
        if not game_on:
            scoreboard.clear()
            scoreboard.write("GAME OVER", move=False, align="center", font=("Arial", 20, "normal"))
            continue
        screen.update()
        for i in range(len(cars)):
            handle_car(cars[i], i)
            if check_collision(cars[i]):
                game_on = False
                break
        if player.ycor() >= SCREEN_HEIGHT / 2:
            next_level(screen)

