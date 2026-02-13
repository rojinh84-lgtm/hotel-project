class Room:
      
      
      def __init__(self , room_number, room_type, capacity, price, has_wifi, status):
            self.room_number = room_number
            self.room_type = room_type
            self.capacity = capacity
            self.price = price
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
                        list_of_rooms.append(Room(r_n, r_t, c, p, h_w, s))
                return list_of_rooms
                # inja ye list of rooms dorost mikonim va har room ro be on ezafe mikonim va dar akhar return mikonim
            except FileNotFoundError:
                print("No rooms found. Please add rooms first.")

      def __str__(self):
           return f"Room number: {self.room_number}, Room type: {self.room_type}, Capacity: {self.capacity}, Price: {self.price}, Has WiFi: {self.has_wifi}, Status: {self.status}"

rooms = Room.load_rooms()

matches = [r for r in rooms if r.room_type == "single" and r.status == "available"]
'''
inja ma az list of rooms load shode estefade mikonim va har room ro check mikonim ke aya room type an single hast va aya status an available hast ya na
agar har do shart ro dasht be list matches ezafe mikonim va dar akhar akhar check mikonim ke aya list matches khali hast ya na va agar khali nabod har room ro print mikonim
noskhe sade shode khat bala
 matches = []

for r in rooms:
    if r.room_type.lower() == "single" and r.price < 700:
        matches.append(r)

'''

if matches:
    for r in matches:
        print(r)
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
     def __init__(self, room, username, check_in_date, check_out_date, booking=None):
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

    

bookings = Booking.load_bookings()

if check_in_date and check_out_date:
    conflicts = Booking.filter_bookings_by_date(
        bookings, check_in_date, check_out_date
    )
    new_list = [x for x in bookings if x not in conflicts]
else:
    new_list = bookings

for b in new_list:
    print(b)


print("----- Cancel Booking -----")
room_number_to_cancel = input("Enter room number to cancel booking: ").strip()
username = input("Enter your username: ").strip()                   




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