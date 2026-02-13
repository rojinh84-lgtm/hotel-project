#starting with sign in and sign up page for user
from datetime import datetime, timedelta
import os


User_file = "users.txt"
class User:
    
    def __init__(self, username, password, credit, name_family):
        self.username = username
        self.password = password
        self.credit = int(credit) 
        self.name_family = name_family


    def menu (self):
 # main menu using while loop
        while True:
            print("Welcome to the Rozhin's hotel booking system!")
            print("1. Sign up")
            print("2. Log in")
            print("3. Exit")
            choice = input("what can we do for you?")
            
            
            if choice == '1':
                user = self.signup()
                
                break
            elif choice == '2':
                user=self.login()
                
                break
            elif choice == '3':
                print("Thank you for using the hotel booking system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


    def signup(self):
        
        name = input("Enter your name: ")
        family_name = input("Enter your family name: ")
        username = input("Enter your username: ")
        if self.check_user_exists(username):
            print("Username already exists.")
            return

        password = input("Enter your password: ")
        
        try:
            credit = int(input("Enter your credit: "))
        except:
            credit = 0
        user = f"{name}{family_name}"

        
        # Check if the username already exists in the file
        with open("users.txt", "a") as f:
           
            if os.path.exists("users.txt") and os.path.getsize("users.txt") > 0:
                f.write("\n")
            f.write(f"{username},{password},{credit},{user}\n" )
        print('You have successfully added!!')
        return User(username, password, credit, user)
    

    def check_user_exists(self, username):
        if not os.path.exists("users.txt"): return False
        with open("users.txt", "r", ) as f:
            for line in f:
                parts = line.strip().split(",")
                if parts[0] == username:
                    return True
        return False

    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        
        try:
            with open("users.txt", "r") as f: 
                data = f.readlines()
        except FileNotFoundError:
            print("No users found.")
            return None
        
        for line in data:
            parts = line.strip().split(",")
            if len(parts) < 4: continue
            u, p, c, nf = parts
            if u == username and p == password:
                print(f"Welcome back {nf}\n")
                return User(u, p, c, nf)
                
        print("Invalid username or password.")
        return None

    def check_user_exists(self, username):
        if not os.path.exists("users.txt"):
            print("No users yet. Please sign up first.")
            return None
        with open("users.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if parts[0] == username:
                    return True
        return False
    #useless function but we can use it to load users from the file and return a list of users that we can use to check if the username already exists or not in the signup function and also to check if the username and password are correct in the login function        
    
        
    
        

   



    
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
    # we can filter rooms based on criteria such as room type, capacity, price, wifi and status and return a list of rooms that match the criteria 



    def filter_rooms(self, room_type=None, max_price=None, wifi=None, status=None):

        filtered_rooms = self.rooms
        if room_type:
            filtered_rooms = [room for room in filtered_rooms if room.room_type.lower() == room_type.lower()]

        if max_price is not None:
            filtered_rooms = [room for room in filtered_rooms if int(room.price) <= int(max_price)]

        if wifi is not None:
            filtered_rooms = [room for room in filtered_rooms if room.has_wifi.lower() == wifi.lower()]

        return filtered_rooms
    

# now we want to show room list to the user and ask them to choose a room to book and then we can change the status of the room to booked and also we can add the booking to the user's bookings list and also we can add the booking to the bookings.
# txt file for whenever bookings are loaded again(depending on time that user books a room)

'''
show_room_list = Room.load_rooms()
i = input("do you want to see available rooms?")
if i =='yes':
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
        manager = Room_management_system(show_room_list)

        print("ROOM COUNT:", len(manager.rooms))


        filtered_rooms = manager.filter_rooms(
        room_type or None,
        max_price,
        wifi or None,
        
    )


        if filtered_rooms:
            print("Here are the rooms that match your criteria:")
            for room in filtered_rooms:
                print(room)
        else:
            print("No rooms found matching the criteria.")
else:
    print("we can pass")




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

    '''




from datetime import datetime
class Booking :
     def __init__(self, room, username, check_in_date, check_out_date,status):
          self.room = room
          self.username = username
          self.check_in_date = check_in_date
          self.check_out_date = check_out_date
          self.status = status
          

          

     
     
     @classmethod
     def load_bookings(cls):
        bookings = []
        if not os.path.exists("booking.txt"):
            return bookings

        with open("booking.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) < 5:
                    continue
                try:
                    c_i = datetime.strptime(parts[2], "%Y-%m-%d")
                    c_o = datetime.strptime(parts[3], "%Y-%m-%d")
                    bookings.append(cls(parts[0], parts[1], c_i, c_o, parts[4]))
                except:
                    continue
        return bookings

     @staticmethod
     def overlap(ci1, co1, ci2, co2):

        return not (co1 <= ci2 or ci1 >= co2)
  
     def __str__(self):
        return f"Room {self.room} | {self.check_in_date.date()} → {self.check_out_date.date()} | {self.status}"
    

# Right after you have parsed check_in_date and check_out_date
# (and after you possibly showed/filtered rooms)
'''
all_rooms = Room.load_rooms()
all_bookings = Booking.load_bookings()

available_rooms = []

for room in all_rooms:

    if room.status.lower() != "available":
        continue

    booked = False

    for booking in all_bookings:

        if booking.status != "active":
            continue

        if booking.room == room.room_number:

            if Booking.overlap(
                check_in_date,
                check_out_date,
                booking.check_in_date,
                booking.check_out_date
            ):
                booked = True
                break

    if not booked:
        available_rooms.append(room)


print("\nAvailable rooms:")
for r in available_rooms:
    print(r)'''


#here we have fcntion to increase credit we usre it when user doesn't have enough credit to book a room
def credit_increase(username):
    credit=int(input('enter more credit to your account: '))
    with open("users.txt", "r") as f:
        lines = f.readlines()
    with open("users.txt", "w") as f:
        for line in lines:
            u, p, c, nf = line.strip().split(",")
            if u == username:
                new_credit = int(c) + int(credit)
                f.write(f"{u},{p},{new_credit},{nf}\n")
            else:
                f.write(line)




class Booking_management_system(User):
    
    def __init__(self, username, password, credit, name_family):
        super().__init__(username, password, credit, name_family)



    def load_room(self, room_number, username, check_in_date, check_out_date):  
        # Here you would add logic to create a booking, update the room status, and save the booking to file.
        print(f"You have chosen to book room {room_number}. (Booking logic not implemented in this snippet.)")
        with open("rooms.txt","r") as f:
            data=f.readlines()
            for line in data:
                r_n, r_t, c, p, h_w, s  = line.strip().split(",")
                if r_n == room_number:
                    print(f" here is the room you have chosen: \n"
                          f"Room {r_n}: {r_t}, Capacity: {c}, Price: ${p}, WiFi: {h_w}, Status: {s}")
                    return int(p)
        print("Room not found")
        return None
    

    def get_room_price(self, room_num):
        rooms = Room.load_rooms()
        for r in rooms:
            if r.room_number == room_num:
                return r.price
        return 0

            
    def check_credit_and_pay(self, username, room_number, check_in_date, check_out_date):

        nights = (check_out_date - check_in_date).days
        if nights <= 0:
            print("Invalid date range")
            return False

        price = self.get_room_price(room_number)
        if price == 0:
            print("Room not found")
            return False

        total_price = price * nights
        print(f"Total price: {total_price}")

        # read users
        with open("users.txt", "r") as f:
            users = f.readlines()

        new_lines = []
        paid = False

        for line in users:
            u,p,c,nf = line.strip().split(",")

            if u == username:
                if int(c) >= total_price:
                    new_credit = int(c) - total_price
                    new_lines.append(f"{u},{p},{new_credit},{nf}\n")
                    paid = True
                else:
                    print("Not enough credit — add credit")
                    credit_increase(username)
                    return False
            else:
                new_lines.append(line)

        if paid:
            with open("users.txt","w") as f:
                f.writelines(new_lines)
            return True

        return False

    def finalize_booking(self, room_number, username, check_in_date, check_out_date):

        need_newline = os.path.exists("booking.txt") and os.path.getsize("booking.txt") > 0

        with open("booking.txt", "a") as f:
            if need_newline:
                f.write("\n")

            f.write(f"{room_number},{username},{check_in_date.strftime('%Y-%m-%d')},{check_out_date.strftime('%Y-%m-%d')},active")

        print("Booking saved.")


    from datetime import datetime
    # This function will automatically change the status of bookings to "finished" .
    def auto_finish_bookings(self):

        if not os.path.exists("booking.txt"):
            return

        today = datetime.today()

        with open("booking.txt", "r") as f:
            lines = f.readlines()




    def show_all_bookings(self, username):

        self.auto_finish_bookings()

        with open("booking.txt", "r") as f:
            bookings = f.readlines()
            found = False
            for reservation in bookings:
                r_n, u, c_i, c_o,s  = reservation.strip().split(",")
                if u == username:
                    print(f" here is  your  all time bookings: \n"
                          f"Room {r_n}: {c_i} → {c_o} | Status: {s}")
                    found = True
        if not found:
            print("No bookings found for this user.")

    #filter file for active bookings only and show them to the user
    def show_active_bookings(self, username):

        with open("booking.txt", "r") as f:
            bookings = f.readlines()
            found = False
            for reservation in bookings:
                r_n, u, c_i, c_o,s  = reservation.strip().split(",")
                if u == username and s == "active":
                    print(f" here is  your active bookings: \n"
                          f"Room {r_n}: {c_i} → {c_o} | Status: {s}")
                    found = True
        if not found:
            print("No active bookings found for this user.")
                
    def book_room_process(self):
        try:
            
            ci_str = input("Check-in (YYYY-MM-DD): ")
            co_str = input("Check-out (YYYY-MM-DD): ")
            ci = datetime.strptime(ci_str, "%Y-%m-%d")
            co = datetime.strptime(co_str, "%Y-%m-%d")

            if co <= ci:
                print("Check-out must be after check-in")
                return

        except ValueError:
            print("Invalid date format")
            return

        
        all_rooms = Room.load_rooms()
        all_bookings = Booking.load_bookings()
        available_rooms = []

        for room in all_rooms:
            if room.status.lower() != "available":
                continue
            is_booked = False
            for b in all_bookings:
                if b.room == room.room_number and b.status == "active":
                    if Booking.overlap(ci, co, b.check_in_date, b.check_out_date):
                        is_booked = True
                        break
            if not is_booked:
                available_rooms.append(room)

        
        if not available_rooms:
            print("No rooms available")
            return

        print("\nAvailable rooms:")
        for r in available_rooms:
            print(r)

        
        room_number = input("Enter room number to book: ").strip()

        
        ok = self.check_credit_and_pay(self.username, room_number, ci, co)

        
        if ok:
            self.finalize_booking(room_number, self.username, ci, co)

        

       
    def cancel_booking(self, username):

        print("if you want to cancel a booking, please enter the room number and the check-in date of the booking you want to cancel.")
        print("remember you can only cancel for 48 hours after reserving the room")
        

        print("Your bookings:")
        self.show_all_bookings(username)

        room_number_to_cancel = input("Room number: ").strip()
        check_in_str = input("Check-in date (YYYY-MM-DD): ").strip()

        now = datetime.now()

        with open("booking.txt", "r") as f:
            bookings = f.readlines()

        new_lines = []
        found = False
        refund = 0

        for line in bookings:
            r_n, u, c_i, c_o, status = line.strip().split(",")

            if r_n == room_number_to_cancel and u == username and c_i == check_in_str and status == "active":

                check_in_date = datetime.strptime(c_i, "%Y-%m-%d")
                check_out_date = datetime.strptime(c_o, "%Y-%m-%d")

                hours_left = (check_in_date - now).total_seconds() / 3600

                nights = (check_out_date - check_in_date).days

                # get room price
                total_price = 0
                with open("rooms.txt", "r") as rf:
                    for rline in rf:
                        rn, rt, cap, price, wifi, s = rline.strip().split(",")
                        if rn == r_n:
                            total_price = int(price) * nights
                            break

                if total_price == 0:
                    new_lines.append(line)
                    continue


                if hours_left > 48:
                    refund = total_price
                    print("Full refund (more than 48h before check-in)")
                elif hours_left > 0:
                    refund = total_price // 2
                    print("50% refund (less than 48h)")
                else:
                    print("Cannot cancel — check-in time passed")
                    new_lines.append(line)
                    continue

                new_lines.append(f"{r_n},{u},{c_i},{c_o},cancelled\n")
                found = True

            else:
                new_lines.append(line)

        if not found:
            print("Active booking not found")
            return

        # update booking file
        with open("booking.txt", "w") as f:
            f.writelines(new_lines)

        # refund credit
        with open("users.txt", "r") as f:
            users = f.readlines()

        with open("users.txt", "w") as f:
            for line in users:
                u, p, c, nf = line.strip().split(",")
                if u == username:
                    f.write(f"{u},{p},{int(c)+refund},{nf}\n")
                else:
                    f.write(line)

        print("Cancellation done + credit refunded")

   
def main_menu():
    while True:
        print("\n--- Welcome to Rozhin Hotel Booking ---")
        print("1. Sign up")
        print("2. Log in")
        print("3. Exit")
        
        choice = input("Choose (1-3): ").strip()
        
        if choice == '1':
            user = User("", "", 0, "").signup()
            if user:
                return user
        elif choice == '2':
            user = User("", "", 0, "").login()
            if user:
                return user
        elif choice == '3':
            print("Thank you. Goodbye!")
            exit()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    print("Starting hotel system...\n")
    
    logged_in_user = main_menu()
    bms = Booking_management_system(
            logged_in_user.username,
            logged_in_user.password,
            logged_in_user.credit,
            logged_in_user.name_family
        )

        # منوی اصلی کاربر
    while True:
            print("\n--- Main Menu ---")
            print("1. Book a room")
            print("2. Show my bookings")
            print("3. Cancel booking")
            print("4. show available room")
            print("5. show active rooms")
            print("6. Exit")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                bms.book_room_process()
            elif choice == "2":
                bms.show_all_bookings(bms.username)
            elif choice == "3":
                bms.cancel_booking(bms.username)
            elif choice == "4":
                
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
                        manager = Room_management_system(show_room_list)

                        print("ROOM COUNT:", len(manager.rooms))


                        filtered_rooms = manager.filter_rooms(
                        room_type or None,
                        max_price,
                        wifi or None,
                        
                    )


                        if filtered_rooms:
                            print("Here are the rooms that match your criteria:")
                            for room in filtered_rooms:
                                print(room)
                        else:
                            print("No rooms found matching the criteria.")
                            ask_to_filter_booking = input('Do you want to filter rooms based on check in and check out dates? (yes/no) ').strip().lower()

                            if ask_to_filter_booking == 'yes':

                                check_in_date = input("Enter check-in date (YYYY-MM-DD): ").strip()
                                check_out_date = input("Enter check-out date (YYYY-MM-DD): ").strip()

                                check_in_date = datetime.strptime(check_in_date, "%Y-%m-%d")
                                check_out_date = datetime.strptime(check_out_date, "%Y-%m-%d")

                            else:
                                check_in_date = None
                                check_out_date = None
            elif choice =='5':
                
                try:
                    ci_str = input("Check-in date (YYYY-MM-DD) or press Enter for today: ").strip()
                    if ci_str:
                        check_in_date = datetime.strptime(ci_str, "%Y-%m-%d")
                    else:
                        check_in_date = datetime.today()

                    co_str = input("Check-out date (YYYY-MM-DD): ").strip()
                    check_out_date = datetime.strptime(co_str, "%Y-%m-%d")

                    if check_out_date <= check_in_date:
                        print("Check-out must be after check-in.")
                        continue

                except ValueError:
                    print("Invalid date format.")
                    continue

                # then the same loop you already have
                all_rooms = Room.load_rooms()
                all_bookings = Booking.load_bookings()
                available_rooms = []

                for room in all_rooms:
                    if room.status.lower() != "available":   # you may want to remove this line
                        continue
                    booked = False
                    for booking in all_bookings:
                        if booking.status != "active":
                            continue
                        if booking.room == room.room_number:
                            if Booking.overlap(
                                check_in_date,
                                check_out_date,
                                booking.check_in_date,
                                booking.check_out_date
                            ):
                                booked = True
                                break
                    if not booked:
                        available_rooms.append(room)

                print("\nAvailable rooms for the selected period:")
                if not available_rooms:
                    print("No rooms available in this date range.")
                else:
                    for r in available_rooms:
                        print(r)
            elif choice =='6':
                break            
            else:
                print("Invalid choice")

