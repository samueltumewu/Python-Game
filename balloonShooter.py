import turtle

# Rectangle area boundaries
LENGTH =                500
HEIGHT =                460
MIDPOINT_SHOOTER_INIT = [HEIGHT/2, 0]
COR_LEFT_TOP  =         [-270, 240]
COR_RIGHT_TOP =         [230, 240]
COR_RIGHT_BOTTOM =      [230, -220]
COR_LEFT_BOTTOM =       [-270, -220]
EXTRA_BUFFER =          10
TARGET_SPEED =          2
BULLET_SPEED =          5
BULLET_MAX =            3

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
    Game.setposition(MIDPOINT_SHOOTER_INIT[0], MIDPOINT_SHOOTER_INIT[1])
    Bullet.setposition(MIDPOINT_SHOOTER_INIT[0], MIDPOINT_SHOOTER_INIT[1])
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

# The shooter
Game = turtle.Turtle()
Game.speed(0)
Game.penup()

# The balloon
Target = turtle.Turtle()
Target.color("red")
Target.shape("circle")
Target.penup()
Target.speed(0)
Target.setposition(-250, 240-460)

# Multiple bullets
Bullet = []
bullet_on_fire = []
for i in range(BULLET_MAX):
    Bullet.append(turtle.Turtle)
    print(Bullet[i])
    # Bullet[i].penup()
    # Bullet[i].hideturtle()
    # Bullet[i].setheading(180)
    # bullet_on_fire[i] = 0 

draw_game_screen()
set_shooter_init_point()

turtle.listen()
turtle.onkeypress(shooter_go_up, "Up")
turtle.onkeypress(shooter_go_down, "Down")
turtle.onkeypress(bullet_release, "space")
# turtle.mainloop()

while True:
    # Enemy movement
    y_cor = Target.ycor()
    y_cor += TARGET_SPEED
    Target.sety(y_cor)

    for i in range(BULLET_MAX):
        if bullet_on_fire[i] == 1:
            x_cor = Bullet.xcor()
            x_cor -= BULLET_SPEED
            Bullet[i].setx(x_cor)
    # if is_fire == 1:
    #     x_cor = Bullet.xcor()
    #     x_cor -= BULLET_SPEED
    #     Bullet.setx(x_cor)

    if Bullet.xcor() < -270:
        is_fire = 0

