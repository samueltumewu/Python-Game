import turtle
import math
import random as rand

# Rectangle area boundaries
LENGTH =                500
HEIGHT =                460
COR_LEFT_TOP  =         [-270, 240]
COR_RIGHT_TOP =         [230, 240]
COR_RIGHT_BOTTOM =      [230, -220]
COR_LEFT_BOTTOM =       [-270, -220]

# shooter's variables
MIDPOINT_SHOOTER_INIT = [HEIGHT/2, 0]
EXTRA_BUFFER_SHOOTER =  10                                                  # extra buffer for shooter limited area of movement

# bullets and targets variables
TARGET_SPEED =          8
BULLET_SPEED =          TARGET_SPEED*10                                     # bullet speed is 10 times the target's
BULLET_MAX =            3                                                   # the amount of bullet before reloading
TARGET_BATCH =          5                                                   # the amount of targets
TARGET_XCOR_RANGE =     [COR_LEFT_BOTTOM[0], (LENGTH/2)+COR_LEFT_BOTTOM[0]] # define position of targets on X-axis

# scoring variables
MISSED_SHOT =           0
SCORE =                 0

# Functions declaration
def shooter_go_up():
    if(Shooter.ycor() < COR_RIGHT_TOP[1] + -(EXTRA_BUFFER_SHOOTER)):
        Shooter.setheading(90)
        Shooter.forward(10)
def shooter_go_down():
    if(Shooter.ycor() > COR_RIGHT_BOTTOM[1] + EXTRA_BUFFER_SHOOTER):
        Shooter.setheading(270)
        Shooter.forward(10)
def draw_game_screen():
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
def create_shooter():
    Shooter.shape("turtle")
    Shooter.speed(0)
    Shooter.penup()
    Shooter.hideturtle()
    Shooter.setposition(MIDPOINT_SHOOTER_INIT)
    Shooter.showturtle()
def create_bullets():
    for i in range(BULLET_MAX):
        Bullet.append(turtle.Turtle())
        Bullet[i].hideturtle()
        Bullet[i].penup()
        Bullet[i].setheading(180)
        bullet_on_fire.append(0)
def create_targets():
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
def show_targets():
    for balloon in Target:
        balloon.showturtle()
def bullet_release():
    global bullet_on_fire
    for i in range(BULLET_MAX):
        if bullet_on_fire[i] == 0:
            Bullet[i].speed(0)
            Bullet[i].hideturtle()
            Bullet[i].setposition(Shooter.position())
            Bullet[i].showturtle()
            bullet_on_fire[i] = 1
            break
    if sum(bullet_on_fire) >= BULLET_MAX:
        print("reloading...")
def detect_collission():
    global SCORE
    for i in range(BULLET_MAX):
        for j in range(TARGET_BATCH):
            distance = math.sqrt(math.pow(Target[j].xcor()-Bullet[i].xcor(),2)+math.pow(Target[j].ycor()-Bullet[i].ycor(),2))
            if bullet_on_fire[i] and distance < BULLET_SPEED*0.6:
                Bullet[i].hideturtle()
                Target[j].hideturtle()

                #put those objects out
                Bullet[i].setposition(-800, -800)
                Target[j].setposition(-800, -800)

                Bullet[i].clear()
                Target[j].clear()

                balloons_on_air[j] = 0
                bullet_on_fire[i] = 0
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
def draw_missed_shot():
    Missed_Shot_Turtle.speed(0)
    Missed_Shot_Turtle.color("black")
    Missed_Shot_Turtle.penup()
    Missed_Shot_Turtle.setposition(0-(LENGTH/2),COR_LEFT_TOP[1])
    Missed_Shot_Turtle.write("Missed Shot: %s" %MISSED_SHOT, False, align="left", font=("Arial",12,"normal" ))
    Missed_Shot_Turtle.hideturtle()
def update_missed_shot():
    Missed_Shot_Turtle.clear()
    Missed_Shot_Turtle.write("Missed Shot: %s" %MISSED_SHOT, False, align = "left", font = ("Arial",12, "normal"))

# Object turtles creation
Game_Screen = turtle.Turtle()
Game_Screen.hideturtle()
Missed_Shot_Turtle = turtle.Turtle()
Missed_Shot_Turtle.hideturtle()
Shooter = turtle.Turtle()
Shooter.hideturtle()
Bullet = []
bullet_on_fire = []
Target = []
balloons_on_air = []

# Init function at the startup
draw_game_screen()
create_shooter()
create_bullets()
create_targets()
draw_missed_shot()
show_targets() 

# Keybindings
turtle.listen()
turtle.onkey(shooter_go_up, "Up")
turtle.onkey(shooter_go_down, "Down")
turtle.onkey(bullet_release, "space")

# Game loop
while True:
    # Stopping condition
    if SCORE == TARGET_BATCH:
        break
    # Enemy movement
    for i in range(TARGET_BATCH):
        y_cor = Target[i].ycor()
        if balloons_on_air[i] == 1:
            y_cor += TARGET_SPEED
            Target[i].sety(y_cor)
        refresh_stray_balloons_position(Target[i], y_cor)
    # Bullet movement
    for i in range(BULLET_MAX):
        if bullet_on_fire[i] == 1:
            x_cor = Bullet[i].xcor()
            x_cor -= BULLET_SPEED
            Bullet[i].setx(x_cor)
    # Bullet missed
    for i in range(BULLET_MAX):
        if bullet_on_fire[i] == 1 and Bullet[i].xcor() < COR_LEFT_BOTTOM[0]:
            bullet_on_fire[i] = 0
            MISSED_SHOT += 1
            print(f"Missed {MISSED_SHOT}")
            update_missed_shot()
            Bullet[i].setposition(Shooter.position())
            Bullet[i].hideturtle()
            Bullet[i].clear()
    # Collission management
    detect_collission()


# When all targets are down
Endgame = turtle.Turtle()
Endgame.hideturtle()
Endgame.speed(0)
Endgame.penup()
# Do the stopping condition loop
while True:
    Endgame.color("black")
    Endgame.setposition(-50,0)
    Endgame.write("Game Over", False, align="left", font=("Arial",12,"normal" ))