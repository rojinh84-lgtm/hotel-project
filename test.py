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
