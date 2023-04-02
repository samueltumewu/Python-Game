import turtle
import math
import random as rand

# Rectangle area boundaries
LENGTH =                500
HEIGHT =                460
MIDPOINT_SHOOTER_INIT = [HEIGHT/2, 0]
COR_LEFT_TOP  =         [-270, 240]
COR_RIGHT_TOP =         [230, 240]
COR_RIGHT_BOTTOM =      [230, -220]
COR_LEFT_BOTTOM =       [-270, -220]
EXTRA_BUFFER =          10
TARGET_SPEED =          8
BULLET_SPEED =          TARGET_SPEED*10
BULLET_MAX =            3
MISSED_SHOT =           0
SCORE =                 0
TARGET_BATCH =          5
TARGET_XCOR_RANGE =     [COR_LEFT_BOTTOM[0], (LENGTH/2)+COR_LEFT_BOTTOM[0]]
# TARGET_YCOR_RANGE =     [-1*COR_LEFT_BOTTOM[1], -1*(COR_LEFT_BOTTOM[1]+200)]

def shooter_go_up():
    if(Game.ycor() < COR_RIGHT_TOP[1] + -(EXTRA_BUFFER)):
        Game.setheading(90)
        Game.forward(10)
def shooter_go_down():
    if(Game.ycor() > COR_RIGHT_BOTTOM[1] + EXTRA_BUFFER):
        Game.setheading(270)
        Game.forward(10)
def draw_game_screen():
    Game_Screen = turtle.Turtle()
    Game_Screen.speed(0)
    Game_Screen.hideturtle()
    Game_Screen.penup()
    Game_Screen.setposition(COR_LEFT_TOP)
    Game_Screen.pendown()
    Game_Screen.forward(LENGTH)
    Game_Screen.right(90)
    Game_Screen.forward(HEIGHT)
    Game_Screen.right(90)
    Game_Screen.forward(LENGTH)
    Game_Screen.right(90)
    Game_Screen.forward(HEIGHT)
def set_shooter_init_point():
    Game.setposition(MIDPOINT_SHOOTER_INIT)
    Game.showturtle()
def show_targets(index = -1):
    if index == -1:
        for balloon in Target:
            balloon.showturtle()
    else:
        Target[index].showturtle()
def bullet_release():
    bullet_was_released = 0
    global bullet_on_fire
    for i in range(BULLET_MAX):
        if bullet_on_fire[i] == 0:
            Bullet[i].speed(0)
            Bullet[i].hideturtle()
            Bullet[i].setposition(Game.position())
            Bullet[i].showturtle()
            bullet_on_fire[i] = 1
            bullet_was_released = 1
            break
    if bullet_was_released == 0:
        print("reloading...")
def detect_collission():
    global SCORE
    for i in range(BULLET_MAX):
        for j in range(TARGET_BATCH):
            distance = math.sqrt(math.pow(Target[j].xcor()-Bullet[i].xcor(),2)+math.pow(Target[j].ycor()-Bullet[i].ycor(),2))
            if distance < BULLET_SPEED*0.6:
                Bullet[i].hideturtle()
                Target[j].hideturtle()

                #put those objects out
                Bullet[i].setposition(-800, -800)
                Target[j].setposition(-800, -800)

                Bullet[i].clear()
                Target[j].clear()

                balloons_on_air[j] = 0
                SCORE += 1
                print(f"score: {SCORE}")
                break
def refresh_stray_balloons_position(_Target, _ycor):
    Target = _Target
    ycor = _ycor
    if ycor > COR_LEFT_TOP[1]+5:
        Target.setposition(
                rand.randint(TARGET_XCOR_RANGE[0], TARGET_XCOR_RANGE[1]), 
                -1*rand.randint(HEIGHT/2, 100+(HEIGHT/2))
                )

# The shooter
Game = turtle.Turtle()
Game.speed(0)
Game.penup()
Game.hideturtle()

# Multiple balloons
Target = []
balloons_on_air = []
for i in range(TARGET_BATCH):
    Target.append(turtle.Turtle())
    Target[i].hideturtle()
    Target[i].color("red")
    Target[i].shape("circle")
    Target[i].penup()
    Target[i].speed(0)
    Target[i].setposition(
        rand.randint(TARGET_XCOR_RANGE[0], TARGET_XCOR_RANGE[1]), 
        -1*rand.randint(HEIGHT/2, 100+(HEIGHT/2))
        )
    balloons_on_air.append(1)

# Multiple bullets
Bullet = []
bullet_on_fire = []
for i in range(BULLET_MAX):
    Bullet.append(turtle.Turtle())
    Bullet[i].hideturtle()
    Bullet[i].penup()
    Bullet[i].setheading(180)
    bullet_on_fire.append(0)

draw_game_screen()
set_shooter_init_point()
show_targets()

turtle.listen()
turtle.onkeypress(shooter_go_up, "Up")
turtle.onkeypress(shooter_go_down, "Down")
turtle.onkeypress(bullet_release, "space")
# turtle.mainloop()

while True:
    # Enemy movement
    for i in range(TARGET_BATCH):
        refresh_stray_balloons_position(Target[i], y_cor)
        y_cor = Target[i].ycor()
        if balloons_on_air[i] == 1:
            y_cor += TARGET_SPEED
            Target[i].sety(y_cor)
        # UNREVEAL THIS TO ENABLE UNLIMITED BALLOONS!
        # elif balloons_on_air[i] == 0:
        #     Target[i].setposition(
        #         rand.randint(TARGET_XCOR_RANGE[0], TARGET_XCOR_RANGE[1]), 
        #         -1*rand.randint(HEIGHT/2, 100+(HEIGHT/2))
        #         )
        #     balloons_on_air[i] = 1
        #     show_targets(i) 

    for i in range(BULLET_MAX):
        if bullet_on_fire[i] == 1:
            x_cor = Bullet[i].xcor()
            x_cor -= BULLET_SPEED
            Bullet[i].setx(x_cor)

    for i in range(BULLET_MAX):
        if Bullet[i].xcor() < COR_LEFT_BOTTOM[0]:
            bullet_on_fire[i] = 0
            Bullet[i].clear()
            
    detect_collission()

