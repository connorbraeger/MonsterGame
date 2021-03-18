#script for simplified Monster Capture
import random
class Room:
    """stores information about the locations that the player and monster
    will be moving through

    attributes:
    room_name(str)
    room_number(num)
    methods: .connect_to(), get_exit_set(), is_connected_to(), .description()"""
    def __init__(self, room_name, room_num):
        """initializes self with name of room, room number,and an empty set of
        rooms

        Room, str, num-> None"""
        self.room_name = room_name
        self.room_num = room_num
        self.__exit_set = set()
    def __repr__(self):
        """returns string of the form Room(room_name, room_num, room_set)

        Room->str"""
        return "Room(" + repr(self.room_name) + ", " + repr(self.room_num) +  ")"
    def connect_to(self,other):
        """takes another Room or an iterable of Rooms and adds connections
        between them

        Room, Room->None
        Room, iterable_of_Rooms -> None"""
        try:
            len(other)
            for room in other:
                self.__exit_set.add(room)
                room.__exit_set.add(self)
        except TypeError:
            self.__exit_set.add(other)
            other.__exit_set.add(self)
    def get_exit_set(self):
        """returns exit set of the Room

        Room-> set"""
        return self.__exit_set
    def is_connected_to(self,other):
        """returns True if self is connected to other, otherwise returns False

        Room, Room->bool"""
        if other in self.__exit_set:
            return True
        else:
            return False
    def description(self):
        """returns str of the form "You are in room_name. Possible Exits: exit_set"

        Room-> str"""
        roomstring = ""
        for room in sorted(self.__exit_set):
            roomstring =  roomstring + ", "  + str(room.room_num) 
        return "You are in " + self.room_name + ". Possible Exits: " + roomstring[2:] + "."
    def __gt__(self,other):
        """returns True if room number of self > than room number of other, returns False otherwise

        Room, Room-> bool"""
        if self.room_num> other.room_num:
            return True
        else:
            return False
room1= Room('the courtyard', 1)
room2 = Room('the basement corridor',2)
room3 = Room('the stairwell', 3)
room4 = Room('the torture chamber',4)
room5 = Room('the treasure room',5)
room6 = Room("the beast's lair",6)
room7 = Room("the old forgotten library",7)
room8 = Room('the kitchen', 8)
room9 = Room("the servants' lodging",9)

room1.connect_to((room2, room8, room9))
room2.connect_to((room1, room3, room4,room7))
room3.connect_to((room2, room5, room8))
room4.connect_to((room2, room5,room6))
room5.connect_to((room4, room3, room9))
room6.connect_to((room4, room8, room7))
room7.connect_to((room2, room6,room9))
room8.connect_to((room3, room6,room1))
room9.connect_to((room1, room5, room2))

                 
SET_OF_ROOMS ={room1, room2, room3, room4, room5, room6, room7, room8, room9}
class Command:
    """stores action type(either 'move' or 'shoot') and destination

    attributes: action_type(str)
    destination(Room)"""
    def __init__(self,action_command, action_destination):
        """initializes self with action command and destination

        Command, str, Room-> None"""
        self.action_command= action_command
        self.action_destination = action_destination
    def __repr__(self):
        """returns string of the form Command(self.action_command, self.action_destination)

        Command -> str"""
        return "Command(" + repr(self.action_command) + ", " + repr(self.action_destination) + ")"
        
class Movable:
    """represents objects and characters that have changeable locations

    methods: .move_to(), .get_location(), .update()"""
    def move_to(self,location):
        """sets location of selt to location.

        Movable,Room-> None"""
        self.__room_location = location
        
    def __init__(self,location):
        """initializes self with location

        Movable, Room->None"""
        self.__room_location = location
    def get_location(self):
        """getter for location of Movable

        Movable->Room"""
        return self.__room_location
        
    def __repr__(self):
        """returns string in the form Movable(location)

        Movable->str"""
        return "Movable(" + repr(self.get_location()) +")"
    
    def update(self):
        """called every turn. does nothing for Movable

        Movable->None"""
        pass
class Wanderer(Movable):
    """subclass of Movable for things that move randomly on their own

    additional attributes:
    is_awake(bool)(describes if awake or not)"""
    def __init__(self,location=None):
        """initializes Wanderer with location. If no location argument given, Wanderer
        placed in random Room from list. Wanderer always starts out awake

        Wanderer, Room->None
        Wander, None->None"""
        if location==None:
            random_int = random.randint(1,9)
            for room in SET_OF_ROOMS:
                if random_int == room.room_num:
                    location = room
                else:
                    pass
            super().__init__(location)
        else:
            super().__init__(location)
        self.is_awake = True
    def __repr__(self):
        """returns string in the form Wanderer(location, is_awake):

        Wanderer->str"""
        return "Wanderer(" + repr(self.get_location()) + ", " + repr(self.is_awake) + ")"
    def update(self):
        """moves Wanderer to a random room adjacent to current location,unless monster is not awake,
        meaning it won't move at all.

        Wanderer->none"""
        if self.is_awake:
            lst_of_roomnums=[]
            current_location = self.get_location()
            exits = current_location.get_exit_set()
            for rooms in exits:
                lst_of_roomnums.append(rooms)
            self.move_to(random.choice(lst_of_roomnums))
        else:
            pass
monster = Wanderer()
class Player(Movable):
    """Subclass of Movable used for player character

    additional attributes:
    num_of_darts(int)
    additional methods:.shoot_into(), .get_command(),.execute_command()"""
    def __init__(self,num_of_darts,location=None):
        """initializes self with starting location of Player and starting
        number of darts player has

        Player, num, Room> None
        Player, num, None->None"""
        if location==None:
            while True:
                random_int = random.randint(1,9)
                if random_int !=monster.get_location().room_num:
                    break
            for room in SET_OF_ROOMS:
                if random_int == room.room_num:
                    location = room

            super().__init__(location)
        else:
            super().__init__(location)
        self.num_of_darts = num_of_darts
    def __repr__(self):
        """returns string in the form Player(num_of_darts, location)

        Player->str"""
        return "Player(" + repr(self.num_of_darts) + ", " + repr(self.get_location()) + ")"
    def shoot_into(self,destination):
        """decreases number of darts by 1. If monster is in destination room, monster's awake status
        changed to False and True is returned.If monster is not in destination room, False is returned

        Player, Room->bool"""
        self.num_of_darts = self.num_of_darts - 1
        if destination == monster.get_location():
            monster.is_awake=False
            return True
        else:
            return False
    def get_command(self):
        """communicates with user to figure out what user wants to do and will return
        appropriate Command object once valid command has been entered.

        Player->Command"""
        print("You have " + str(self.num_of_darts) + " darts left.")
        while True:
            print("What is your course of action?")
            print('Enter "shoot into NUMBER" or "go to NUMBER"')
            user_command = input()

            if user_command.lower().strip()[0:11] !='shoot into 'and user_command.lower().strip()[0:6]!= 'go to ':
                print("Not a valid command")
            elif user_command.lower()[0:11] =='shoot into ':
    
                try:
                    if int(user_command.lower().strip()[11:])<1 or int(user_command.lower().strip()[11:])>9:
                        print("Not a valid room number")                                                              
                    elif self.num_of_darts == 0:
                        print("You have no darts left")
                    else:
                        for room in self.get_location().get_exit_set():
                            if room.room_num ==int(user_command.lower().strip()[-1]):
                               return Command('shoot', room)
                        print("There is no exit to that room from here")
                except ValueError:
                        print("That is not a valid room number")
            else:
                try:
                    if int(user_command.lower().strip()[6:])<1 or int(user_command.lower().strip()[6:])>9:
                        print("Not a valid room number")
                    else:
                        for room in self.get_location().get_exit_set():
                            if room.room_num ==int(user_command.lower().strip()[-1]):
                               return Command('move', room)
                        print("There is no exit to that room from here")
                except ValueError:
                    print("Not a valid number")
    def execute_command(self, command):
        """takes Command object and carries out the corresponding action. First determines action type,
        then calls either .move_to() or .shoot_into() as needed.Afterwards, prints message indicating
        what action had been taken.

        Player, Command->None"""
        if command.action_command == 'move':
            self.move_to(command.action_destination)
            if command.action_destination == monster.get_location().room_num:
                print("You walk into room number " + str(command.action_destination.room_num) + ". The monster is here.")
            if command.action_destination in monster.get_location().get_exit_set():
                print("You walk into room room " + str(command.action_destination.room_num) + ". You can smell the monster; it must be near by!")
            else:
                print("You walk into room number " + str(command.action_destination.room_num) + ".")
        else:
            self.shoot_into(command.action_destination)
            if command.action_destination.room_num == monster.get_location().room_num:
                print("The gun goes *BOOM*, and a dart flies into room  " + str(command.action_destination.room_num) + "...")
                print("You hear a roar from the monster and a thump as it falls asleep.")
                print("Congratulations! You have captured the monster!")
            else:
                print("The gun goes *BOOM*, and a dart flies into room  " + str(command.action_destination.room_num) + "...")
                print("But it doesn't sound like you hit anything.")
    def update(self):
        """displays description of the Player's current Room, uses .get_command() to obtain a Command from
        the user, and then uses .execute_command() to carry out command.

        Player, ->None"""
        print(self.get_location().description())
        command = self.get_command()
        self.execute_command(command)

player1 = Player(70)
UPDATE_LIST = [monster, player1]
print("Welcome to Monster Capture!")
print("A wild monster is loose in the area and it's your job to capture it without getting devoured.")
print(" Travel around the map, and when you have figured out which room the monster is in, go to ")
print("an adjacent room and shoot a tranquilizer dart into that room. If you hit the monster, you win! ")
print("But you be careful, you only have three darts!")

if player1.get_location() in monster.get_location().get_exit_set():

    print('You can smell the monster')
else:
    print("You begin the game in room " + str(player1.get_location().room_num))
while True:


    player1.update()
    if player1.get_location()==monster.get_location() and monster.is_awake:
        print("The monster tears you limb from limb, savoring every last drop of your blood")
        break
    if not monster.is_awake:
        print("Rejoice, the monster is dead.")
        break
    for Movable in UPDATE_LIST:
        Movable.update()
   
        if player1.get_location()==monster.get_location() and monster.is_awake:
            print("The monster tears you limb from limb, savoring every last drop of your blood")
            break
    if player1.get_location()==monster.get_location() and monster.is_awake:
        break
    if not monster.is_awake:
        break

    
          

 
                
                            
            
        
                

    
