import microbit as mb
import random

targeted_value = random.randint(0, 9)  # Pick a number for the user to guess
guess_limit = 3  # Set guess limit

print("Targeted: "+str(targeted_value))  # For debugging


def guess() -> int:
    "Let the user guess the number with A and B buttons"

    current_num = 0  # Currently selected number

    while True:
        mb.display.show(current_num)  # Show current number

        if mb.button_b.was_pressed():
            current_num = min(current_num + 1, 9)  # prevent overflow
        elif mb.button_a.was_pressed():
            current_num = max(current_num - 1, 0)  # prevent negative numbers
        elif mb.accelerometer.get_y() < -400:
            print("returning "+str(current_num))
            return current_num


def main():
    global guess_limit  # This variable is global, dont search for it locally

    while guess_limit > 0:
        num = guess()  # Get user input

        if targeted_value == num:
            mb.display.show(mb.Image.HAPPY)  # Happy ending
            break
        elif targeted_value > num:
            mb.display.show(mb.Image.ARROW_N)  # Number is higher
            mb.sleep(1000)
        elif targeted_value < num:
            mb.display.show(mb.Image.ARROW_S)  # Number is lower
            mb.sleep(1000)

        guess_limit -= 1  # Take one life if guess was unsuccessful

    if guess_limit < 1:
        mb.display.show(mb.Image.SAD)  # Game ended


main()
