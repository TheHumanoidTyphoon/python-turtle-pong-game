import turtle
import simpleaudio as sa
import random
import tkinter as tk
from tkinter import messagebox

# Constants
PADDLE_COLOR = "white"
PADDLE_SHAPE = "square"
PADDLE_SPEED = 0
PADDLE_SIZE = {"stretch_wid": 5, "stretch_len": 0.50}
BALL_COLOR = "white"
BALL_SHAPE = "square"
BALL_SPEED = 0
BALL_SIZE = {"stretch_wid": 0.65, "stretch_len": 0.65}
MIDDLE_LINE_COLOR = "white"
MIDDLE_LINE_SPEED = 0
MIDDLE_LINE_SIZE = 2.5
FONT = ("Courier", 80, "normal")
SOUND_FILE = "Sounds\8_bit_pong_sound.wav"
ICON_FILE = 'images/pong-1-32.png'


def start_game():
    screen = turtle.Screen()
    screen.clear()  # Clear the screen

    screen.title('Pong by @TheHumanoidTyphoon')
    screen.bgcolor('black')
    screen.setup(width=800, height=600)
    screen.tracer(0)
    score_a = 0
    score_b = 0


    def confirm_exit():
        """
        Asks the user if they want to exit the game.

        Returns:
            bool: True if the user confirms the exit, False otherwise.
        """
        return messagebox.askquestion('Exit Game', 'Are you sure you would like to leave the game?', icon='warning') == 'yes'



    def exit_game():
        """
        Exits the game if the user confirms the exit. If the user cancels the exit,
        adds event listeners back to the screen to continue playing the game.

        """
        if confirm_exit():
            # Unbind Escape key so user can't cancel the exit.
            screen.onkeypress(None, 'Escape')
            # Close the game window.
            screen.bye()
        else:
            # Re-add event listeners to continue playing the game.
            add_event_listeners()


    def add_event_listeners():
        """
        Binds event listeners to the screen to control the paddles and exit the game.

        """
        # Listen for events on the screen.
        screen.listen()
        # Bind key presses to move the paddles.
        screen.onkeypress(lambda: move_paddle(paddle_a, 20), 'w')
        screen.onkeypress(lambda: move_paddle(paddle_a, -20), 's')
        screen.onkeypress(lambda: move_paddle(paddle_b, 20), 'Up')
        screen.onkeypress(lambda: move_paddle(paddle_b, -20), 'Down')
        # Bind Escape key to exit the game.
        screen.onkeypress(exit_game, 'Escape')


    add_event_listeners()


    def move_paddle(paddle, y):
        """
        Moves the specified paddle up or down by the given distance. Handles collisions with the top and bottom of the screen.

        Args:
        - paddle: the turtle object representing the paddle to be moved
        - y: the distance to move the paddle, can be positive or negative

        """

        paddle.sety(paddle.ycor() + y)

        # Handle collisions with the screen borders
        if paddle_a.ycor() > 250:
            paddle_a.sety(250)
        elif paddle_a.ycor() < -250:
            paddle_a.sety(-250)
        if paddle_b.ycor() > 250:
            paddle_b.sety(250)
        elif paddle_b.ycor() < -250:
            paddle_b.sety(-250)


    def create_paddle(x, y):
        """
        Creates a new turtle object to represent a paddle at the specified coordinates.

        Args:
        - x: the x-coordinate of the center of the paddle
        - y: the y-coordinate of the center of the paddle

        Returns:
        - The turtle object representing the new paddle.

        """
        paddle = turtle.Turtle()
        paddle.speed(PADDLE_SPEED)
        paddle.shape(PADDLE_SHAPE)
        paddle.color(PADDLE_COLOR)
        paddle.shapesize(**PADDLE_SIZE)
        paddle.penup()
        paddle.goto(x, y)
        return paddle


    paddle_a = create_paddle(-350, 0)
    paddle_b = create_paddle(350, 0)


    # Middle line
    def create_middle_line():
        """
        Creates a turtle object to draw the middle line on the game screen.

        Returns:
        - The turtle object representing the middle line.

        """

        middle_line = turtle.Turtle()
        middle_line.speed(MIDDLE_LINE_SPEED)
        middle_line.color(MIDDLE_LINE_COLOR)
        middle_line.penup()
        middle_line.goto(0, 395)
        middle_line.pendown()
        middle_line.setheading(270)
        middle_line.pensize(MIDDLE_LINE_SIZE)

        for _ in range(20):
            middle_line.forward(20)
            middle_line.penup()
            middle_line.forward(20)
            middle_line.pendown()

        return middle_line


    middle_line = create_middle_line()


    def create_ball():
        """
        Creates a new turtle object to represent the game ball.

        Returns:
        - The turtle object representing the new ball.

        """

        ball = turtle.Turtle()
        ball.speed(BALL_SPEED)
        ball.shape(BALL_SHAPE)
        ball.color(BALL_COLOR)
        ball.shapesize(**BALL_SIZE)
        ball.penup()
        ball.goto(0, 0)
        ball.velocity_x, ball.velocity_y = 0.5, -0.5
        return ball

    ball = create_ball()


    def create_score():
        """
        Creates a turtle object to display the current score.

        Returns:
        - The turtle object representing the score display.

        """
        score = turtle.Turtle()
        score.speed(0)
        score.color(PADDLE_COLOR)
        score.penup()
        score.hideturtle()
        score.goto(0, 190)
        score.write(f"{score_a}     {score_b}", align="center", font=FONT)
        return score

    score = create_score()


    def play_sound(sound_file):
        """
        Plays the specified sound file.

        Args:
        - sound_file: the path to the sound file to be played

        """
        wave_obj = sa.WaveObject.from_wave_file(sound_file)
        play_obj = wave_obj.play()


    def update_score(score_a, score_b):
        """
        Updates the score display with the given scores for player A and player B.

        Args:
        - score_a: the current score for player A
        - score_b: the current score for player B

        """

        score.clear()
        score.write(f"{score_a}     {score_b}", align="center", font=FONT)


    # Main game loop
    while True:
        # Move the ball and update the window
        ball.setposition(ball.position() + (ball.velocity_x, ball.velocity_y))
        screen.update()

        # Update the scores and display them
        if ball.xcor() > 390:
            score_a += 1
            update_score(score_a, score_b)
            ball.goto(0, 0)
            ball.velocity_x *= -1
        elif ball.xcor() < -390:
            score_b += 1
            update_score(score_a, score_b)
            ball.goto(0, 0)
            ball.velocity_x *= -1

        # Check for collisions with paddles
        if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < paddle_b.ycor() + 40 and ball.ycor() > paddle_b.ycor() - 40):
            ball.setx(340)
            ball.velocity_x *= -1
            # add random variation to dy
            ball.velocity_y += random.uniform(-0.1, 0.1)
            play_sound(SOUND_FILE)

        if (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < paddle_a.ycor() + 40 and ball.ycor() > paddle_a.ycor() - 40):
            ball.setx(-340)
            ball.velocity_x *= -1
            # add random variation to dy
            ball.velocity_y += random.uniform(-0.1, 0.1)
            play_sound(SOUND_FILE)

        # Check for collisions with top and bottom borders
        if ball.ycor() > 290:
            ball.sety(290)
            ball.velocity_y *= -1
            play_sound(SOUND_FILE)

        if ball.ycor() < -290:
            ball.sety(-290)
            ball.velocity_y *= -1
            play_sound(SOUND_FILE)


def main_menu():
    """
    Displays the main menu of the Pong game, including the game title, 
    "Press Any Key To Play" text, two NPC paddles, a ball, and the 
    middle line. When a key is pressed, the game starts by calling the 
    start_game() function.
    """
    root = tk.Tk()
    icon = tk.PhotoImage(file=ICON_FILE)
    root.iconphoto(True, icon)
    root.destroy()

    screen = turtle.Screen()
    screen.title('Pong by @TheHumanoidTyphoon')
    screen.bgcolor('black')
    screen.setup(width=800, height=600)
    screen.tracer(0)
    
    # Add the "Pong" text
    pong_text = turtle.Turtle()
    pong_text.hideturtle()
    pong_text.penup()
    pong_text.color("gray")
    pong_text.write("Pong", align="center", font=("Courier", 80, "normal"))
    pong_text.color("white")
    pong_text.goto(0, -2)
    pong_text.write("Pong", align="center", font=("Courier", 80, "normal"))

    # Add the "Press Any Key To Play" text
    play_text = turtle.Turtle()
    play_text.hideturtle()
    play_text.penup()
    play_text.color("gray")
    play_text.goto(0, -100)
    play_text.write("Press Any Key To Play", align="center", font=("Courier", 30))
    play_text.color("white")
    play_text.goto(1.4, -101)
    play_text.write("Press Any Key To Play", align="center", font=("Courier", 30))

    # Add two NPC paddles and a ball
    
    def create_paddle(x, y):
        """
        Creates a paddle turtle object at the specified coordinates with the specified size and color.

        Parameters:
            x (int): The x-coordinate of the paddle.
            y (int): The y-coordinate of the paddle.

        Returns:
            turtle.Turtle: The created paddle turtle object.
        """
        paddle = turtle.Turtle()
        paddle.speed(PADDLE_SPEED)
        paddle.shape(PADDLE_SHAPE)
        paddle.color(PADDLE_COLOR)
        paddle.shapesize(**PADDLE_SIZE)
        paddle.penup()
        paddle.goto(x, y)
        return paddle

    paddle_npc1 = create_paddle(-350, 0)
    paddle_npc2 = create_paddle(350, 0)


    def create_middle_line():
        """
        Creates a turtle object that draws the middle line of the game court.

        Returns:
            turtle.Turtle: The created middle line turtle object.
        """
        middle_line = turtle.Turtle()
        middle_line.speed(MIDDLE_LINE_SPEED)
        middle_line.color(MIDDLE_LINE_COLOR)
        middle_line.penup()
        middle_line.goto(0, 395)
        middle_line.pendown()
        middle_line.setheading(270)
        middle_line.pensize(MIDDLE_LINE_SIZE)

        for _ in range(20):
            middle_line.forward(20)
            middle_line.penup()
            middle_line.forward(20)
            middle_line.pendown()

        return middle_line


    middle_line = create_middle_line()

   
    def create_ball():
        """
        Creates a turtle object for the game ball at the center of the game court with the specified shape, size, and color.

        Returns:
            turtle.Turtle: The created ball turtle object.
        """
        ball = turtle.Turtle()
        ball.speed(BALL_SPEED)
        ball.shape(BALL_SHAPE)
        ball.color(BALL_COLOR)
        ball.shapesize(**BALL_SIZE)
        ball.penup()
        ball.goto(0, 0)
        ball.velocity_x = random.choice([-0.5, 0.5])
        ball.velocity_y = random.choice([-0.5, 0.5])
        return ball

    ball = create_ball()
    

    def move_paddles():
        """
        Moves the non-player paddles based on the ball's position and handles collisions with the screen borders.
        """
        # Calculate the distance between the ball and each paddle
        distance1 = ball.distance(paddle_npc1)
        distance2 = ball.distance(paddle_npc2)

        # Move the paddles towards the ball
        if distance1 < 247.5:
            if paddle_npc1.ycor() < ball.ycor():
                paddle_npc1.sety(paddle_npc1.ycor() + 1)
            elif paddle_npc1.ycor() > ball.ycor():
                paddle_npc1.sety(paddle_npc1.ycor() - 1)
        if distance2 < 247.5:
            if paddle_npc2.ycor() < ball.ycor():
                paddle_npc2.sety(paddle_npc2.ycor() + 1)
            elif paddle_npc2.ycor() > ball.ycor():
                paddle_npc2.sety(paddle_npc2.ycor() - 1)

        # Handle collisions with the screen borders
        if paddle_npc1.ycor() > 250:
            paddle_npc1.sety(250)
        elif paddle_npc1.ycor() < -250:
            paddle_npc1.sety(-250)
        if paddle_npc2.ycor() > 250:
            paddle_npc2.sety(250)
        elif paddle_npc2.ycor() < -250:
            paddle_npc2.sety(-250)

    score_a = 0
    score_b = 0

    
    def create_score():
        """
        Creates a turtle object for the game score at the top center of the game court.

        Returns:
            turtle.Turtle: The created score turtle object.
        """
        score = turtle.Turtle()
        score.speed(0)
        score.color(PADDLE_COLOR)
        score.penup()
        score.hideturtle()
        score.goto(0, 190)
        score.write(f"{score_a}     {score_b}", align="center", font=FONT)
        return score

    score = create_score()

    # Bind start_game() function to any key press
    screen.listen()
    screen.onkeypress(start_game)
    
    def update_score(score_a, score_b):
        """
        Updates the score displayed on the screen with the current score values.

        Parameters:
            score_a (int): The score of player A.
            score_b (int): The score of player B.
        """
        score.clear()
        score.write(f"{score_a}     {score_b}", align="center", font=FONT)

    while True:
        # Move the ball and update the window
        ball.setposition(ball.position() + (ball.velocity_x, ball.velocity_y))
        screen.update()  # Update the screen
        move_paddles()  # Move the paddles randomly
        

        # Update the scores and display them
        if ball.xcor() > 390:
            score_a += 1
            update_score(score_a, score_b)
            ball.goto(0, 0)
            ball.velocity_x *= -1
        elif ball.xcor() < -390:
            score_b += 1
            update_score(score_a, score_b)
            ball.goto(0, 0)
            ball.velocity_x *= -1

        # Check for collisions with paddles
        if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < paddle_npc2.ycor() + 40 and ball.ycor() > paddle_npc2.ycor() - 40):
            ball.setx(340)
            ball.velocity_x *= -1
            # add random variation to dy
            ball.velocity_y += random.uniform(-0.1, 0.1)

        if (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < paddle_npc1.ycor() + 40 and ball.ycor() > paddle_npc1.ycor() - 40):
            ball.setx(-340)
            ball.velocity_x *= -1
            # add random variation to dy
            ball.velocity_y += random.uniform(-0.1, 0.1)

        # Check for collisions with top and bottom borders
        if ball.ycor() > 290:
            ball.sety(290)
            ball.velocity_y *= -1

        if ball.ycor() < -290:
            ball.sety(-290)
            ball.velocity_y *= -1
    

main_menu()