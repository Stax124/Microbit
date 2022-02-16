# Snake game for microbit

import microbit as mb

playing = True
delay = 500


class Dir:
    "Class for storing directions of the snake"

    UP = [0, -1]
    RIGHT = [1, 0]
    DOWN = [0, 1]
    LEFT = [-1, 0]


class Food():
    """
    Food that snake eats to grow

    [args]:
        x -> x coordinate of the food
        y -> y coordinate of the food
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.brightness = 2

    def draw(self):
        "Draw self to the screen"
        mb.display.set_pixel(self.x, self.y, self.brightness)


# Instatiate food
food = Food(1, 1)


class Snake():
    """Snake as playable object

    [args]:
        None
    """

    def __init__(self, x: int = 2, y: int = 3, direction=Dir.UP):
        self.x = x
        self.y = y
        self.direction = direction
        self.body = [[self.x, self.y], [self.x, self.y+1]]
        self.brightnessHead = 7
        self.brightnessTail = 5
        self.dIndex = 1
        self.directions = [Dir.LEFT, Dir.UP, Dir.RIGHT, Dir.DOWN]
        self.append = False

    def move(self):
        "Move snake based on current direction and check for collisions"

        global playing

        xMove, yMove = self.direction

        # Check if snake is trying to move out of the field, then proceed to collision check
        if (self.body[0][0] + xMove < 0) or (self.body[0][0] + xMove > 4):
            print("Out of bounds X")
            playing = False
        elif (self.body[0][1] + yMove < 0) or (self.body[0][1] + yMove > 4):
            print("Out of bounds Y")
            playing = False
        else:
            index = 0
            placeholder = []
            for i in self.body:
                if index == 0:
                    placeholder = self.body[index]
                    self.body[index] = [i[0] + xMove, i[1] + yMove]
                else:
                    temp = self.body[index]
                    self.body[index] = placeholder
                    placeholder = temp

                index += 1

            if self.append:
                self.append = False
                self.body.append(placeholder)

            if self.body[0] in self.body[1:]:
                playing = False

            self.checkFood()

    def checkFood(self):
        if self.body[0] == [food.x, food.y]:
            self.append = True

            for x in range(0, 5):
                for y in range(0, 5):
                    if [x, y] not in self.body:
                        food.x = x
                        food.y = y
                        break

    def draw(self):
        index = 0
        for i in self.body:
            mb.display.set_pixel(
                i[0], i[1], self.brightnessTail if index != 0 else self.brightnessHead)
            index += 1

    def changeDir(self, turn: int):
        if turn == -1:
            self.dIndex = self.dIndex - 1 if self.dIndex > 0 else 3
            self.direction = self.directions[self.dIndex]
        elif turn == 1:
            self.dIndex = self.dIndex + 1 if self.dIndex < 3 else 0
            self.direction = self.directions[self.dIndex]


def pause():
    while True:
        mb.display.show("A")

        if mb.button_a.was_pressed():
            mb.display.clear()
            break


while True:
    pause()

    playing = True

    # Instantiate snake
    snake = Snake()
    food = Food(1, 1)

    # Draw first frame and start loop after one second
    food.draw()
    snake.draw()
    mb.sleep(1000)

    while playing:
        # Clear the screen
        mb.display.clear()

        # Change direction based on input
        if mb.accelerometer.get_y() < -200:
            pause()
        elif mb.button_a.was_pressed():
            snake.changeDir(-1)
        elif mb.button_b.was_pressed():
            snake.changeDir(1)

        # Display body
        snake.move()

        if playing == False:
            break

        food.draw()
        snake.draw()

        # Sleep for a bit if snake is alive
        if playing:
            mb.sleep(delay)
