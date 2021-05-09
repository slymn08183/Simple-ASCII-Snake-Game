import ctypes
import os
import threading
import random
from time import sleep
import keyboard
from pip._vendor.colorama.win32 import COORD


class Snake:
    """
    Snake
    This class is written to keep coordinates of snake's every index
    And also its shape
    """

    def __init__(self, x: list, y: list, shape: str):  # Defining constructor for necessary values.
        # Checking if parameters are list else raising an exception
        if type(x) != list:
            raise Exception(f"Need list got {type(x)} instead.")
        if type(y) != list:
            raise Exception(f"Need list got {type(y)} instead.")
        # Store values in Snake class
        self.X = x
        self.Y = y
        self.SHAPE = shape


class MainSnakeWindow:
    """
     MainSnakeWindow
     This class is does everything about ASCII Snake game no need to call a function to
     run the game
     """
    def __init__(self):  # Setting constructor for constant values and necessary function to run

        # These constants are needed to set cursor position on console
        self.WIN32 = ctypes.WinDLL("kernel32")
        self.STDOUT = self.WIN32.GetStdHandle(-11)

        # Rate of key reading from console, used to run the function runs in every 0.01 second
        self.KEY_READ_RATE = 0.01

        # Rate of movement speed, used to run the function runs in every 0.4 second thus when needed
        # to make snake faster this value should be decreased for max value when reached 0, it stops
        # so max speed should be slightly high from 0
        # This value chances when snake eats a feed
        self.MOVEMENT_RATE = 0.4

        # This constant used to make snake faster
        self.MOVEMENT_RATE_INCREASE = 0.01

        # Vector of snake movement [up down left right]
        self.MOVEMENT_VECTOR = [False, False, False, True]

        # Ascii characters of snake's box
        self.BOX_TL = "\u250C"  # ->  ┌
        self.BOX_TR = "\u2510"  # ->  ┐
        self.BOX_BL = "\u2514"  # ->  └
        self.BOX_BR = "\u2518"  # ->  ┘
        self.VERTICAL_BORDER = "\u2500"   # ->  ─
        self.HORIZONTAL_BORDER = "\u2502"  # -> │

        # Dimensions of snake's box
        self.WIDTH = 75
        self.HEIGHT = 20

        # Creating snake object with pre defined coordinates
        # and pre defined length which is 5 characters
        # "#" represents snake's one character
        self.SNAKE = Snake([5, 4, 3, 2, 1], [1, 1, 1, 1, 1], "#")

        # Feed character
        self.FEED_SHAPE = "*"

        # Used to keep coordinates of feed will has 2 values represents x and y
        self.RANDOM_FEED = []

        # Call function to create random first feed's coordinates
        self.create_random_feed()
        # Call function to render snake's box
        self.render_frame()
        # Call function to render feed
        self.render_feed()
        # Call function to render score
        self.render_score()
        # Call function to check key inputs
        self.key_check()
        # Call function to create movement
        self.movement()

    def key_check(self):
        # The line below basically makes this function a loop the only differance
        # with self.KEY_READ_RATE constant tell this function run after self.KEY_READ_RATE seconds later
        # when it runs itself after given second it run itself again makes it stuck in a loop
        threading.Timer(self.KEY_READ_RATE, self.key_check).start()

        # With keyboard.is_pressed() function we get which key is pressed
        #   w UP
        #   s DOWN
        #   a LEFT
        #   d RIGHT
        # Then we set snake movement vector with one of [False, True, False, False] ---[up down left right]--- list
        # according to the pressed key these list has only one true value to make snake
        # move only one way at a time
        # Also we set movement vector after we check if it is a proper movement, what I mean by that is
        # snake can't go right when it moves to left or top to bottom, bottom to up also left to right
        if keyboard.is_pressed("w") and self.MOVEMENT_VECTOR != [False, True, False, False]:
            self.MOVEMENT_VECTOR = [True, False, False, False]
        if keyboard.is_pressed("s") and self.MOVEMENT_VECTOR != [True, False, False, False]:
            self.MOVEMENT_VECTOR = [False, True, False, False]
        if keyboard.is_pressed("a") and self.MOVEMENT_VECTOR != [False, False, False, True]:
            self.MOVEMENT_VECTOR = [False, False, True, False]
        if keyboard.is_pressed("d") and self.MOVEMENT_VECTOR != [False, False, True, False]:
            self.MOVEMENT_VECTOR = [False, False, False, True]

    def create_random_feed(self):
        # Creating random coordinates for feed inside of the box
        x = random.randint(1, self.WIDTH)
        y = random.randint(1, self.HEIGHT)

        # Checking if the seed top of the snake, if it is
        # returns to itself to try again
        for i in range(len(self.SNAKE.X)):
            if x == self.SNAKE.X[i] and y == self.SNAKE.Y[i]:
                return self.create_random_feed()

        # Returns with proper coordinates
        self.RANDOM_FEED = [x, y]

    def get_next_coordinates(self):
        # [up down left right]
        # [ 0   1    2    3  ]

        # Arranges next coordinates of snake

        # Holding old values of the head of the snake
        old_x = self.SNAKE.X[0]
        old_y = self.SNAKE.Y[0]

        # Summing with movement vector
        # Movement vector means [up down left right]
        # So if we sum and subtraction it like following
        # If the head of snake coordinate were X and Y
        #       [up down left right]
        # X +  (        -left +right)
        # Y +  (-up +down           )
        # New X and Y values will be next movement coordinates of snake's head
        # according to movement vector

        # Sum and subtraction
        new_x = old_x - self.MOVEMENT_VECTOR[2] + self.MOVEMENT_VECTOR[3]
        new_y = old_y - self.MOVEMENT_VECTOR[0] + self.MOVEMENT_VECTOR[1]

        # Check if the old values were on the limits of the box
        # if it is set opposite coordinates
        if old_x == 1 and self.MOVEMENT_VECTOR[2]:
            new_x = self.WIDTH

        if old_x == self.WIDTH and self.MOVEMENT_VECTOR[3]:
            new_x = 1

        if old_y == 1 and self.MOVEMENT_VECTOR[0]:
            new_y = self.HEIGHT

        if old_y == self.HEIGHT and self.MOVEMENT_VECTOR[1]:
            new_y = 1

        return new_x, new_y

    def render_frame(self):
        # Render the box with predefined border characters and limits
        # sep is given as to null to clear commas between constants
        print(self.BOX_TL, self.VERTICAL_BORDER * self.WIDTH, self.BOX_TR, sep='')

        for i in range(self.HEIGHT):
            # end is given as to null to clear \n -newline- after printed text
            print(self.HORIZONTAL_BORDER, end='')

            for pix in range(self.WIDTH):
                print(" ", end='')

            print(self.HORIZONTAL_BORDER)

        print(self.BOX_BL, self.VERTICAL_BORDER * self.WIDTH, self.BOX_BR, sep='')

    def render_snake(self):
        # Renders snakes every character coordinates
        for i in range(len(self.SNAKE.X)):
            # sets cursor position to snakes character coordinate
            self.go_cursor_position((self.SNAKE.X[i], self.SNAKE.Y[i]))
            # then print snake shape
            print(self.SNAKE.SHAPE)
            # finally sets cursor to end of box to not bother while playing
            self.go_cursor_position((0, self.HEIGHT + 1))

    def render_feed(self):
        # sets cursor position to feed coordinate
        self.go_cursor_position((self.RANDOM_FEED[0], self.RANDOM_FEED[1]))
        # print feed shape
        print(self.FEED_SHAPE)
        # finally sets cursor to end of box to not bother while playing
        self.go_cursor_position((0, self.HEIGHT + 1))

    def pop_tail(self):
        # When snake renderd we don't clear console so every spot that
        # snake passed will stay as its character so we follow its tail
        # and print there a blank " " character

        # sets cursor position to snake's last character coordinate
        self.go_cursor_position((self.SNAKE.X[-1], self.SNAKE.Y[-1]))
        # Print plank
        print(" ")
        # Pop the last pair X and Y coordinates
        # We do that because every new movement on snake adds a pair of x y
        # to top of snake coordinate list
        # so if we don't pop last one snake will grow forever
        # we won't use this when we want snake get bigger -When eats a feed-
        self.SNAKE.X.pop(-1)
        self.SNAKE.Y.pop(-1)

    def render_score(self):
        # Used to render score of player
        # Sets cursor to bottom of box
        self.go_cursor_position((0, self.HEIGHT + 2))
        # Prints score -Which is length of snake multiplied by 100-
        # We subtract 5 of snake length because initiated length is 5
        print(f"Score = {(len(self.SNAKE.X) - 5) * 100}")
        print(f"Speed multiplier = {self.MOVEMENT_RATE}")

        # finally sets cursor to end of box to not bother while playing
        self.go_cursor_position((0, self.HEIGHT + 1))

    def render_loose_screen(self):
        # Prints loose screen
        # Sets the cursor middle of the box
        self.go_cursor_position((int((self.WIDTH / 2) - (self.WIDTH / 4)),
                                 int((self.HEIGHT / 2) - (self.HEIGHT / 4))))
        # Print
        print("You lost! Don't try to eat yourself next time :)")
        # Sets the cursor middle of the box again
        self.go_cursor_position((int((self.WIDTH / 2) - (self.WIDTH / 4)),
                                 int((self.HEIGHT / 2) - (self.HEIGHT / 4)) + 1))
        # Print
        print(f"Your score was = {(len(self.SNAKE.X) - 5) * 100}")
        # Sets the cursor middle of the box again
        self.go_cursor_position((int((self.WIDTH / 2) - (self.WIDTH / 4)),
                                 int((self.HEIGHT / 2) - (self.HEIGHT / 4)) + 2))
        print("You will be main menu in 5 sec...")
        # Sleep
        sleep(5)
        # Clear screen
        clear()
        # Call the main menu
        main_menu()
        # Finally sets cursor to end of box to not bother while playing
        self.go_cursor_position((0, self.HEIGHT + 3))

    def movement(self):
        # The line below basically makes this function a loop the only differance
        # with self.MOVEMENT_RATE constant tell this function run after self.MOVEMENT_RATE seconds later
        # when it runs itself after given second it run itself again makes it stuck in a loop
        # we save this timer in thread variable to use it when we need to stop
        thread = threading.Timer(self.MOVEMENT_RATE, self.movement)
        # Start timer to next scheduled run
        thread.start()

        # run self.get_next_coordinates() to get next coordinates and get them
        x, y = self.get_next_coordinates()

        # Check if the next movement is crosses with snake itself if it is
        # cancel loop and print loose screen
        for i in range(len(self.SNAKE.X)):
            if x == self.SNAKE.X[i] and y == self.SNAKE.Y[i]:
                thread.cancel()
                self.render_loose_screen()

        # Insert nex coordinates inside of snake coordinate list
        self.SNAKE.X.insert(0, x)
        self.SNAKE.Y.insert(0, y)

        # Check if the head of snake is same coordinates with feed if it is then
        # increase speed, render new score, create new feed, render new feed
        # if it is not pop the tail -> we pop tail as explained above every new movement adds a head to snake so
        # if no need to get longer pop tail
        if self.RANDOM_FEED[0] == self.SNAKE.X[0] and self.RANDOM_FEED[1] == self.SNAKE.Y[0]:
            # Check if max speed is reached
            if self.MOVEMENT_RATE > 0.05:
                self.MOVEMENT_RATE = self.MOVEMENT_RATE - self.MOVEMENT_RATE_INCREASE
            self.render_score()
            self.create_random_feed()
            self.render_feed()
        else:
            self.pop_tail()

        # Render snake
        self.render_snake()

    def go_cursor_position(self, position=(0, 0)):
        # A function used to set cursor position in given X and Y parameter
        # If no parameter passed it will set it to 0,0 default coordinates
        self.WIN32.SetConsoleCursorPosition(self.STDOUT, COORD(*position))


def main_menu():
    # Print some informatins
    print("\t\tWelcome to ASCII snake game.\n\n")
    print("Inorder to start the game you have to initiate main snake class.")
    print("-W for Up- -S for DOWN- -A for LEFT- -D for RIGHT-")
    print("Which named as MainSnakeWindow so just type in as MainSnakeWindow()")
    # Get input
    input_value = input()

    if input_value == "MainSnakeWindow()":
        # In here I would call function with eval but when I do that I guess it runs another thread
        # therefore the loop of main function breaks snake game's render
        clear()
        MainSnakeWindow()
    else:
        # If typed input is not the main snake class then run the code with eval
        clear()
        try:
            # Try to run input if success print it and call itself
            # if now print error and call itself
            print("Wrong input to start snake game, but let me see what you just wrote down does.\n")
            print(input_value + ":", end="")
            print(eval(input_value), end="\n\n")
            main_menu()
        except Exception as e:
            print("Something went wrong while running your input! Please try again.\n\n")
            print(e)
            print("\n\n")
            main_menu()


def clear():
    # Clear console function
    os.system('cls')


if __name__ == '__main__':
    # Initiate main menu
    main_menu()
