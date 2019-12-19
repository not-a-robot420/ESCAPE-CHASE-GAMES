#! python3
# Midnight Rider
# Survive through the night

import time, random, math
import escape, chase

def main():
    escape_the_game = escape.Escape()
    chase_the_game = chase.mains()



    if escape_the_game.win == False:
        print(escape_the_game.intro())

        while not escape_the_game.done:
            escape_the_game.update()
    else:
        print("""
        ----
        You will now continue on to the second half of the game.
        ----
        """)
        time.sleep(1)
        chase_the_game()



if __name__ == "__main__":
    main()

