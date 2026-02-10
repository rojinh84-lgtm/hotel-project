#starting with sign in and sign up page for user
from datetime import datetime


User_file = "users.txt"
class User:
    def __init__(self, username, password, credit, name_family):
        self.username = username
        self.password = password
        self.credit = credit
        self.name_family = name_family


    def signup(self):
        
        name = input("Enter your name: ")
        family_name = input("Enter your family name: ")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        credit = int(input("Enter your credit: "))
        user = f"{name} {family_name} "
        
        # Check if the username already exists in the file
        try:
            with open("users.txt", "r") as f:
                data = f.readlines()
                for line in data:
                        u, p, c, nf = line.strip().split(",")
                        
                        if u == username:

                            print("Username already exists ❌")
                            return 
                
        except  FileNotFoundError:
                pass 
    


        with open("users.txt", "a") as f:
            f.write(f"{username},{password},{credit},{user}\n" )
        print(' you have succesfully added!!')

    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        try:
            with open("users.txt", "r") as f: 
                data = f.readlines()
                
        except FileNotFoundError:
            print(" user not found. Please sign up first.")
            return
        
        
        for line in data:
                        u, p, c, nf = line.strip().split(",")
                        if u == username and p ==password:
                            print(f"welcome back {nf}\n"
                                "1. Book a room\n"
                                "2. View your bookings\n"
                                "3. Cancel a booking\n")
                            return u, p, c, nf 
              
        print("Invalid username or password. Please try again. or sign up if you don't have an account.")
    
    def menu (self):
 # main menu using while loop
        while True:
            print("Welcome to the hotel booking system!")
            print("1. Sign up")
            print("2. Log in")
            print("3. Exit")
            choice = input("what can we do for you?")
            
            
            if choice == '1':
                self.signup()
                break
            elif choice == '2':
                self.login()
                break
            elif choice == '3':
                print("Thank you for using the hotel booking system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    #useless function but we can use it to load users from the file and return a list of users that we can use to check if the username already exists or not in the signup function and also to check if the username and password are correct in the login function        
    def list_of_users(self):
        users = []
        try:
            with open("users.txt", "r") as f:
                data = f.readlines()
                for line in data:
                        u, p, c, nf = line.strip().split(",")
                        users.append(User(u, p, c, nf))
            return users
        except FileNotFoundError:
            print("No users found. Please sign up first.")
            return []   
    
    
# room management system
class Room:
      
      
      def __init__(self, room_number, room_type, capacity, price, has_wifi, status):
        self.room_number = room_number
        self.room_type = room_type
        self.capacity = int(capacity)
        self.price = int(price)
        self.has_wifi = has_wifi
        self.status = status

            
                    
      @classmethod   
      def load_rooms(cls):
            try:
                list_of_rooms = []
                with open("rooms.txt", "r") as f:
                    data = f.readlines()
                    for line in data:
                        r_n, r_t, c, p, h_w, s  = line.strip().split(",")
                        list_of_rooms.append(Room(r_n, r_t,int(c), int(p), h_w, s))
                return list_of_rooms
            except FileNotFoundError:
                print("No rooms found. Please add rooms first.")
                return []
            
      def __str__(self):
          return f"Room {self.room_number}: {self.room_type}, Capacity: {self.capacity}, Price: ${self.price}, WiFi: {self.has_wifi}, Status: {self.status}"


# a list of rooms that we can use to add rooms to it and also to filter rooms based on criteria            


        
    
class Room_management_system:
    def __init__(self, rooms=None):
         self.rooms = rooms if rooms is not None else Room.load_rooms()
        
    # we can add a room to the list of rooms and also to the rooms.txt file for whenever rooms are loaded again(depending on time that user adds room)
    def add_room(self, room_number, room_type, capacity, price, has_wifi, status):
        room = Room(room_number, room_type, capacity, price, has_wifi, status)
        self.rooms.append(room)
        with open("rooms.txt", "a") as f:
            f.write(f"{room_number},{room_type},{capacity},{price},{has_wifi},{status}\n")
        print("Room added successfully!") 
        return room
    # we can filter rooms based on criteria such as room type, capacity, price, wifi and status and return a list of rooms that match the criteria 



    def filter_rooms(self, room_type=None, max_price=None, wifi=None, status=None):

        filtered_rooms = self.rooms
        if room_type:
            filtered_rooms = [room for room in filtered_rooms if room.room_type.lower() == room_type.lower()]

        if max_price is not None:
            filtered_rooms = [room for room in filtered_rooms if int(room.price) <= int(max_price)]

        if wifi is not None:
            filtered_rooms = [room for room in filtered_rooms if room.has_wifi.lower() == wifi.lower()]

        if status:
            filtered_rooms = [room for room in filtered_rooms if room.status.lower() == status.lower()]

        return filtered_rooms
    

# now we want to show room list to the user and ask them to choose a room to book and then we can change the status of the room to booked and also we can add the booking to the user's bookings list and also we can add the booking to the bookings.
# txt file for whenever bookings are loaded again(depending on time that user books a room)

show_room_list = Room.load_rooms()
print(f" here is the list of rooms available in our hotel: \n")
for room in show_room_list:
    print(room)
print(f" to book easier  you can filter rooms based on criteria such as room type, capacity, price, wifi and status and return a list of rooms that match the criteria \n")
ask_to_filter =input('do you want to filter rooms based on criteria? (yes/no) ')

if ask_to_filter.lower() == 'yes':
    room_type = input("Enter room type (single/double/suite) or leave blank to skip: ").strip()
    max_price_input = input("Enter maximum price or leave blank to skip: ").strip()
    max_price = int(max_price_input) if max_price_input else None
    wifi = input("Do you want a room with WiFi? (yes/no) or leave blank to skip: ").strip()
    status = input("Enter room status (available/booked) or leave blank to skip: ").strip()
    manager = Room_management_system(show_room_list)

    print("ROOM COUNT:", len(manager.rooms))


    filtered_rooms = manager.filter_rooms(
    room_type or None,
    max_price,
    wifi or None,
    status or None
)


    if filtered_rooms:
        print("Here are the rooms that match your criteria:")
        for room in filtered_rooms:
            print(room)
    else:
        print("No rooms found matching the criteria.")


from datetime import datetime

ask_to_filter_booking = input(
    'Do you want to filter rooms based on check in and check out dates? (yes/no) ').strip().lower()

if ask_to_filter_booking == 'yes':

    check_in_date = input("Enter check-in date (YYYY-MM-DD): ").strip()
    check_out_date = input("Enter check-out date (YYYY-MM-DD): ").strip()

    check_in_date = datetime.strptime(check_in_date, "%Y-%m-%d")
    check_out_date = datetime.strptime(check_out_date, "%Y-%m-%d")

else:
    check_in_date = None
    check_out_date = None

    




from datetime import datetime
class Booking :
     def __init__(self, room, username, check_in_date, check_out_date):
          self.room = room
          self.username = username
          self.check_in_date = check_in_date
          self.check_out_date = check_out_date
          

          

     
     @classmethod
     def load_bookings(cls):
          try:
                list_of_bookings = []
                with open("bookings.txt", "r") as f:
                    data = f.readlines()
                    for line in data:
                        r, u, c_i, c_o  = line.strip().split(",")
                        c_i = datetime.strptime(c_i, "%Y-%m-%d")
                        c_o = datetime.strptime(c_o, "%Y-%m-%d")
                        list_of_bookings.append(Booking(r, u, c_i, c_o))
                # a list of all reservations
                return list_of_bookings
          except FileNotFoundError:
                print("No bookings found. Please book a room first.")
                return []
          


     
         
     
     @staticmethod
     def filter_bookings_by_date(bookings, check_in_date, check_out_date):

        filtered_bookings = []

        for booking in bookings:
            c_i = booking.check_in_date
            c_o = booking.check_out_date

            if check_in_date <= c_o and check_out_date >= c_i:
                filtered_bookings.append(booking)

        return filtered_bookings
     
          
     def __str__(self):
      return f"Room {self.room} | {self.check_in_date.strftime('%Y-%m-%d')} → {self.check_out_date.strftime('%Y-%m-%d')}"

    

# Right after you have parsed check_in_date and check_out_date
# (and after you possibly showed/filtered rooms)

all_rooms = Room.load_rooms()           # or use your Room_management_system().rooms
all_bookings = Booking.load_bookings()

if check_in_date and check_out_date:
    available_rooms = []
    
    for room in all_rooms:
        # Skip rooms that are not even marked available in general
        if room.status.lower() != "available":
            continue
            
        # Check if this room has ANY overlapping booking
        is_booked_in_period = False
        for booking in all_bookings:
            if booking.room == room.room_number:
                if check_in_date <= booking.check_out_date and check_out_date >= booking.check_in_date:
                    is_booked_in_period = True
                    break
        
        if not is_booked_in_period:
            available_rooms.append(room)
else:
    # No date filter → show all generally available rooms
    available_rooms = [r for r in all_rooms if r.status.lower() == "available"]

print("\nAvailable rooms for your requested dates:")
if available_rooms:
    for room in available_rooms:
        print(room)
    print(f"\nTotal available: {len(available_rooms)}")
else:
    print("Sorry, no rooms available for the selected dates.")




