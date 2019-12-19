#! python3
# escape.py

import math, random, sys, textwrap, time
import constants

class Escape(object):
    def __init__(self):
        self.done = False
        self.distance_traveled = 0
        self.fatigue = 0
        self.food = 4
        self.hunger = 0
        self.enemy = 100
        self.turns = 0
        self.win = False
        self.difficulty = 0 # multiplier, multiply the values by difficulty
        
        self.level = input("""
        ----
        You are faced with three doors.
        Which one do you go through?

        Door: 1
        Door: 2
        Door: 3
        """)
        if self.level == "2":
            self.difficulty = 1

        if self.level == "3":
            self.difficulty = 2
        
        if self.level == "1":
            self.difficulty = 3
        
        file_contents = ""
        with open("score.txt", "r") as file:
            file_contents = file.readline()
        if file_contents == "01":
            self.win = True
            print(f"""
            ----
            You appear to have won the game before.
            Congrats, 
            it must have been very challenging.
            ----
            """)
        else:
            with open("score.txt", "w") as file:
                file.write("0")
                
            
    def intro(self):
        for char in textwrap.dedent(constants.INTRO):
            time.sleep(0.15)
            sys.stdout.write(char)
            sys.stdout.flush()

        time.sleep(1)


        
    def status(self):
        if self.hunger >= 25:
            print()
            print(f"You think to yourself, man, I'm real hungry")
            print()
        elif self.hunger >= 50:
            print()
            print(f"Okay, now you should probably eat something")
            print()

        if self.fatigue >= 25:
            print()
            print(f"You feel a little tired, but can keep going.")
            print()
        elif self.fatigue >= 50:
            print()
            print(f"You should probably take a nap.")
            print()

        if self.enemy <= 75:
            print()
            print(f"The enemy is making a good amount of progress towards you now.")
            print()
        elif self.enemy <= 50:
            print()
            print(f"You should keep moving faster.")
            print()

    def events(self, choice):
        if choice != "c" or "b":
            if random.random() < int(0.25* self.difficulty) and self.turns > 1:
                self.food += int(1* self.difficulty)
                
                
                print()
                print(f"You have found some old food that was left on a table.")
                print(f"Why would someone just leave unfinished food lying around?")
                print()
                time.sleep(0.5)
            
            elif random.random() > int(0.25* self.difficulty) and self.turns > 1:
                

                print()
                print(f"You found some food that was just left in the garbage or urinal.")
                print(f"You don't think urinal sandwiches are very appetizing...")
                print(f"You find no good food.")
                print()
                time.sleep(0.5)

    def enemymove(self, distance_covered):
        self.enemy += (random.randrange(5*self.difficulty, 15*self.difficulty) - distance_covered)

    def hungerbar(self):
        self.hunger += random.randrange(2*self.difficulty, 8*self.difficulty)
    
    def tired(self):
        self.fatigue += random.randrange(2*self.difficulty, 8*self.difficulty)
    
    def choice_made(self, choice):
        if choice.lower().strip(".,!") == "e":
            self.done = True
        elif choice.lower().strip(".,!") == "d":
            if random.random() > int(0.5*self.difficulty):
                self.food += 1
                print()
                print(f"A confused academic walks up to you. He is a nerd with glasses and he talks like one.")
                print(f"He gives you a loaf of bread.")
                print()
                time.sleep(0.5)

                self.enemymove(0)
                self.hungerbar()
                self.tired()
            elif random.random() < int(0.5*self.difficulty):
                self.food -= 1
                print()
                print(f"A violent juuler walks up to you and steals your bread.")
                print(f"You have lost a loaf of bread.")
                print()
                time.sleep(0.5)

                self.enemymove(0)
                self.hungerbar()
                self.tired()
    
        elif choice.lower().strip(".,!") == "c":
            self.fatigue -= 50

            self.enemymove(0)
            self.hungerbar()
            print()
            print(f"You take a pretty good nap.")
            print(f"You realize you have been sleeping in a men's washroom.")
            print(f"Why?")
            print()
            time.sleep(0.5)
        
        elif choice.lower().strip(".,!") == "b":
            if self.food >= 1:
                self.food -= 1

                self.hunger -= 25

                self.enemymove(1)
                self.tired()
                print()
                print(f"You eat a nice and tasty loaf of plain whole wheat bread.")
                print(f"You think to yourself,")
                print(f"\'was my mouth always this dry?\'")
                print(f"You feel more full than before.")
                print()
                time.sleep(0.5)
            elif self.food <= 0:
                print()
                print(f"You have no bread to consume.")
                print(f"Sorry, bud.")
                print()

        elif choice.lower().strip(".,!") == "a":
            self.distance_traveled += random.randrange((4*self.difficulty), (15*self.difficulty))
            
            self.enemymove(1)
            self.hungerbar()
            self.tired()


    def end(self):
        self.ending = None

        
        if self.distance_traveled > 100:
            time.sleep(1)
            ending = f"""\
                ----
                You run forward with determination,
                after a long and painful journey,
                you made it to one of the three exits. 

                You outran the 'enemy', 
                and avoided death in the tunnels.

                Congratulations!
                ----
                """
            self.done = True
            with open("score.txt", "a") as file:
                file.write("1")

        elif self.hunger >= 100:
            ending = f"""\
                ----
                Your stomach rumbles...
                You are too hungry to run away anymore.
                You go to the cafeteria and get caught.

                You should eat more next time, buddy.
                ----
                """
            self.done = True

        elif self.fatigue >= 100:
            ending = f"""\
                ----
                You are very tired.
                You should've taken more rests.

                You are too sleepy to continue.
                You get caught.
                ----
                """
            self.done = True
        
        elif self.enemy == 0:
            ending = f"""\
                ----
                Something is close behind.
                You turn around an the enemy has caught you.
                It was Mr Ubial the whole time. 

                It turns out you didn't finish your assignment.
                You should have been a more diligent student.
                ----
                """
            self.done = True

        if self.done == True:
            if ending != None:
                for credit in textwrap.dedent(ending):
                    time.sleep(0.15)
                    sys.stdout.write(credit)
                    sys.stdout.flush()

                print("Congrats on beating the game, play again any time.")
            else: 
                print("Thanks for playing, feel free to try again.")
    
    def update(self):
        print(constants.CHOICES)

        self.status()

        choice = input("Select one of your amazing options!")
        self.turns += 1

        self.events(choice)
        self.choice_made(choice)

        self.end()
        time.sleep(1)        

        

        
            

