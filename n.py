from datetime import datetime, timedelta
import os

# فایل‌ها
USER_FILE = "users.txt"
ROOM_FILE = "rooms.txt"
BOOKING_FILE = "bookings.txt"

# --- کلاس کاربر (User) ---
class User:
    def init(self, username, password, credit, name_family):
        self.username = username
        self.password = password
        self.credit = int(credit)
        self.name_family = name_family

    def menu(self):
        while True:
            print("\nWelcome to Rozhin's hotel booking system!")
            print("1. Sign up")
            print("2. Log in")
            print("3. Exit")
            choice = input("what can we do for you? ")
            
            if choice == '1':
                self.signup()
            elif choice == '2':
                user_obj = self.login()
                if user_obj:
                    user_obj.user_panel()
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")

    def signup(self):
        name = input("Enter your name: ")
        family_name = input("Enter your family name: ")
        username = input("Enter your username: ")
        
        # چک کردن تکراری نبودن
        if self.check_user_exists(username):
            print("Username already exists.")
            return

        password = input("Enter your password: ")
        try:
            credit = int(input("Enter your credit: "))
        except:
            credit = 0
            
        full_name = f"{name} {family_name}"

        with open(USER_FILE, "a", encoding='utf-8') as f:
            # اگر فایل خالی نیست خط جدید بزن
            if os.path.exists(USER_FILE) and os.path.getsize(USER_FILE) > 0:
                f.write("\n")
            f.write(f"{username},{password},{credit},{full_name}")
            
        print('You have successfully added!!')

    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        
        try:
            with open(USER_FILE, "r", encoding='utf-8') as f: 
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
        if not os.path.exists(USER_FILE): return False
        with open(USER_FILE, "r", encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(",")
                if parts[0] == username:
                    return True
        return False

    def user_panel(self):
        # اینجا آبجکت منیجر را می‌سازیم و اطلاعات خودمان را به آن می‌دهیم
        manager = Booking_management_system(self.username, self.password, self.credit, self.name_family)
        
        # اول از همه وضعیت رزروهای قدیمی را آپدیت می‌کنیم
        manager.auto_finish_bookings()

        while True:
            print(f"\nUser Panel (Credit: {manager.credit})")
            print("1. Book room")
            print("2. Show my bookings")
            print("3. Cancel booking")
            print("4. Increase Credit")
            print("5. Exit")

            ch = input("Choose one option: ")

            if ch == "1":
                manager.book_room_process() # این تابع جدید را ساختم تا کدها مرتب شود
            elif ch == "2":
                manager.show_all_bookings(self.username)
            elif ch == "3":
                manager.cancel_booking(self.username)
            elif ch == "4":
                manager.credit_increase_process()
            elif ch == "5":
                break


# --- کلاس اتاق (Room) ---
class Room:
    def init(self, room_number, room_type, capacity, price, has_wifi, status):
        self.room_number = room_number
        self.room_type = room_type
        self.capacity = int(capacity)
        self.price = int(price)
        self.has_wifi = has_wifi
        self.status = status

    @classmethod   
    def load_rooms(cls):
        list_of_rooms = []
        if not os.path.exists(ROOM_FILE): return []
        with open(ROOM_FILE, "r", encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 6:
                    list_of_rooms.append(Room(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]))
        return list_of_rooms
    
    def str(self):
        return f"Room {self.room_number}: {self.room_type}, Cap: {self.capacity}, Price: ${self.price}, WiFi: {self.has_wifi}"

# --- کلاس رزرو (Booking) ---
class Booking:
    def init(self, room, username, check_in_date, check_out_date, status):
        self.room = room
        self.username = username
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.status = status

    @classmethod
    def load_bookings(cls):
        bookings = []
        if not os.path.exists(BOOKING_FILE): return []
        with open(BOOKING_FILE, "r", encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 5:
                    c_i = datetime.strptime(parts[2], "%Y-%m-%d")
                    c_o = datetime.strptime(parts[3], "%Y-%m-%d")
                    bookings.append(Booking(parts[0], parts[1], c_i, c_o, parts[4]))
        return bookings

# --- سیستم مدیریت رزرو (Booking Management System) ---
class Booking_management_system(User):
    def init(self, username, password, credit, name_family):
        super().init(username, password, credit, name_family)

    # این متد همه کارهای رزرو (نمایش، فیلتر، انتخاب) را انجام می‌دهد
    def book_room_process(self):
        # 1. گرفتن تاریخ
        try:
            print("\n--- Search Rooms ---")
            ci_str = input("Check-in (YYYY-MM-DD): ")
            co_str = input("Check-out (YYYY-MM-DD): ")
            check_in = datetime.strptime(ci_str, "%Y-%m-%d")
            check_out = datetime.strptime(co_str, "%Y-%m-%d")
            
            if check_out <= check_in:
                print("Error: Check-out must be after check-in.")
                return
        except ValueError:
            print("Invalid date format.")
            return

        # 2. پیدا کردن اتاق‌های خالی (منطق اصلاح شده)
        all_rooms = Room.load_rooms()
        all_bookings = Booking.load_bookings()
        
        # لیست اتاق‌های پر
        busy_rooms = []
        for b in all_bookings:
            if b.status == "active":
                # فرمول تداخل زمانی
                if not (check_out <= b.check_in_date or check_in >= b.check_out_date):
                    busy_rooms.append(b.room)
        
        # فیلتر کردن اتاق‌های خالی
        available_rooms = [r for r in all_rooms if r.room_number not in busy_rooms]

        # 3. فیلترهای کاربر (اختیاری)
        ask_filter = input("Do you want to filter results by type/price? (yes/no): ").lower()
        if ask_filter == 'yes':
            r_type = input("Room type (single/double/suite) or enter to skip: ").strip()
            max_p = input("Max price or enter to skip: ").strip()
            
            if r_type:
                available_rooms = [r for r in available_rooms if r.room_type == r_type]
            if max_p:
                available_rooms = [r for r in available_rooms if r.price <= int(max_p)]

        # نمایش نتایج
        if not available_rooms:
            print("No rooms available for these dates.")
            return

        print("\n--- Available Rooms ---")
        for r in available_rooms:
            print(r)
            # --- کلاس اتاق (Room) ---
class Room:
    def init(self, room_number, room_type, capacity, price, has_wifi, status):
        self.room_number = room_number
        self.room_type = room_type
        self.capacity = int(capacity)
        self.price = int(price)
        self.has_wifi = has_wifi
        self.status = status

    @classmethod   
    def load_rooms(cls):
        list_of_rooms = []
        if not os.path.exists(ROOM_FILE): return []
        with open(ROOM_FILE, "r", encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 6:
                    list_of_rooms.append(Room(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]))
        return list_of_rooms
    
    def str(self):
        return f"Room {self.room_number}: {self.room_type}, Cap: {self.capacity}, Price: ${self.price}, WiFi: {self.has_wifi}"

# --- کلاس رزرو (Booking) ---
class Booking:
    def init(self, room, username, check_in_date, check_out_date, status):
        self.room = room
        self.username = username
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.status = status

    @classmethod
    def load_bookings(cls):
        bookings = []
        if not os.path.exists(BOOKING_FILE): return []
        with open(BOOKING_FILE, "r", encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 5:
                    c_i = datetime.strptime(parts[2], "%Y-%m-%d")
                    c_o = datetime.strptime(parts[3], "%Y-%m-%d")
                    bookings.append(Booking(parts[0], parts[1], c_i, c_o, parts[4]))
        return bookings

# --- سیستم مدیریت رزرو (Booking Management System) ---
class Booking_management_system(User):
    def init(self, username, password, credit, name_family):
        super().init(username, password, credit, name_family)

    # این متد همه کارهای رزرو (نمایش، فیلتر، انتخاب) را انجام می‌دهد
    def book_room_process(self):
        # 1. گرفتن تاریخ
        try:
            print("\n--- Search Rooms ---")
            ci_str = input("Check-in (YYYY-MM-DD): ")
            co_str = input("Check-out (YYYY-MM-DD): ")
            check_in = datetime.strptime(ci_str, "%Y-%m-%d")
            check_out = datetime.strptime(co_str, "%Y-%m-%d")
            
            if check_out <= check_in:
                print("Error: Check-out must be after check-in.")
                return
        except ValueError:
            print("Invalid date format.")
            return

        # 2. پیدا کردن اتاق‌های خالی (منطق اصلاح شده)
        all_rooms = Room.load_rooms()
        all_bookings = Booking.load_bookings()
        
        # لیست اتاق‌های پر
        busy_rooms = []
        for b in all_bookings:
            if b.status == "active":
                # فرمول تداخل زمانی
                if not (check_out <= b.check_in_date or check_in >= b.check_out_date):
                    busy_rooms.append(b.room)
        
        # فیلتر کردن اتاق‌های خالی
        available_rooms = [r for r in all_rooms if r.room_number not in busy_rooms]

        # 3. فیلترهای کاربر (اختیاری)
        ask_filter = input("Do you want to filter results by type/price? (yes/no): ").lower()
        if ask_filter == 'yes':
            r_type = input("Room type (single/double/suite) or enter to skip: ").strip()
            max_p = input("Max price or enter to skip: ").strip()
            
            if r_type:
                available_rooms = [r for r in available_rooms if r.room_type == r_type]
            if max_p:
                available_rooms = [r for r in available_rooms if r.price <= int(max_p)]

        # نمایش نتایج
        if not available_rooms:
            print("No rooms available for these dates.")
            return

        print("\n--- Available Rooms ---")
        for r in available_rooms:
            print(r)
            # 4. انتخاب و پرداخت
        room_num = input("\nEnter room number to book (or 0 to cancel): ")
        if room_num == "0": return
        
        # پیدا کردن اتاق انتخاب شده
        selected_room = None
        for r in available_rooms:
            if r.room_number == room_num:
                selected_room = r
                break
        
        if selected_room:
            self.check_credit_and_pay(selected_room, check_in, check_out)
        else:
            print("Invalid room number.")

    def check_credit_and_pay(self, room, check_in, check_out):
        nights = (check_out - check_in).days
        total_cost = room.price * nights
        
        print(f"Total cost for {nights} nights: ${total_cost}")
        
        if self.credit >= total_cost:
            confirm = input("Confirm booking? (yes/no): ").lower()
            if confirm == "yes":
                # کسر اعتبار
                self.credit -= total_cost
                self.update_user_file_credit(self.credit)
                
                # ثبت رزرو
                self.finalize_booking(room.room_number, self.username, check_in, check_out, total_cost)
                print("Booking successful!")
        else:
            print("Insufficient credit!")
            ask = input("Do you want to add credit now? (yes/no): ")
            if ask == "yes":
                self.credit_increase_process()
                # ریکرسیو (دوباره تلاش کن)
                self.check_credit_and_pay(room, check_in, check_out)

    def finalize_booking(self, room_number, username, check_in_date, check_out_date, cost):
        with open(BOOKING_FILE, "a", encoding='utf-8') as f:
            if os.path.exists(BOOKING_FILE) and os.path.getsize(BOOKING_FILE) > 0:
                f.write("\n")
            f.write(f"{room_number},{username},{check_in_date.strftime('%Y-%m-%d')},{check_out_date.strftime('%Y-%m-%d')},active")

    def update_user_file_credit(self, new_credit):
        # خواندن همه، تغییر یکی، نوشتن همه
        lines = []
        with open(USER_FILE, "r", encoding='utf-8') as f:
            lines = f.readlines()
            
        with open(USER_FILE, "w", encoding='utf-8') as f:
            for line in lines:
                parts = line.strip().split(",")
                if parts[0] == self.username:
                    f.write(f"{parts[0]},{parts[1]},{new_credit},{parts[3]}\n")
                else:
                    f.write(line)

    def credit_increase_process(self):
        try:
            amount = int(input('Enter amount to add: '))
            self.credit += amount
            self.update_user_file_credit(self.credit)
            print(f"Credit updated. New balance: {self.credit}")
        except ValueError:
            print("Invalid amount.")

    def auto_finish_bookings(self):
        # تغییر وضعیت رزروهای گذشته به finished
        if not os.path.exists(BOOKING_FILE): return
        
        today = datetime.now()
        lines = []
        with open(BOOKING_FILE, "r", encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        updated = False
        
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) >= 5:
                # format: room,user,in,out,status
                try:
                    c_o = datetime.strptime(parts[3], "%Y-%m-%d")
                    status = parts[4]
                    if status == "active" and today > c_o:
                        parts[4] = "finished"
                        updated = True
                    new_lines.append(",".join(parts) + "\n")
                except:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        if updated:
            with open(BOOKING_FILE, "w", encoding='utf-8') as f:
                f.writelines(new_lines)
    def show_all_bookings(self, username):
            bookings = Booking.load_bookings()
            found = False
            print("\n--- Your Bookings ---")
            for b in bookings:
                if b.username == username:
                    print(f"Room {b.room}: {b.check_in_date.date()} -> {b.check_out_date.date()} | Status: {b.status}")
                    found = True
            if not found:
                print("No bookings found.")

    def cancel_booking(self, username):
        self.show_all_bookings(username)
        room_num = input("Enter room number to cancel: ")
        check_in_str = input("Enter check-in date of that booking (YYYY-MM-DD): ")
        
        bookings_lines = []
        with open(BOOKING_FILE, "r", encoding='utf-8') as f:
            bookings_lines = f.readlines()
            
        new_lines = []
        found = False
        
        for line in bookings_lines:
            parts = line.strip().split(",")
            # format: room, user, in, out, status
            if len(parts) >= 5:
                if (parts[0] == room_num and parts[1] == username and 
                    parts[2] == check_in_str and parts[4] == "active"):
                    
                    # پیدا کردیم! حالا محاسبه قانون ۴۸ ساعت
                    c_i = datetime.strptime(parts[2], "%Y-%m-%d")
                    c_o = datetime.strptime(parts[3], "%Y-%m-%d")
                    now = datetime.now()
                    
                    # محاسبه قیمت اتاق برای برگشت پول
                    # (در کد ساده شده فرض میکنیم قیمت را باید دوباره از فایل اتاق بخوانیم)
                    room_price = self.get_room_price(room_num)
                    nights = (c_o - c_i).days
                    total_cost = room_price * nights
                    
                    # محاسبه ساعت باقی مانده
                    hours_left = (c_i - now).total_seconds() / 3600
                    
                    refund = 0
                    if hours_left > 48:
                        refund = total_cost
                        print("Cancelled > 48h before. 100% refund.")
                    elif hours_left > 0:
                        refund = total_cost // 2
                        print("Cancelled < 48h before. 50% refund.")
                    else:
                        print("Cannot cancel (Check-in time passed).")
                        new_lines.append(line)
                        continue

                    # آپدیت پول کاربر
                    self.credit += refund
                    self.update_user_file_credit(self.credit)
                    
                    # تغییر وضعیت رزرو
                    parts[4] = "cancelled"
                    found = True
                    new_lines.append(",".join(parts) + "\n")
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
                
        if found:
            with open(BOOKING_FILE, "w", encoding='utf-8') as f:
                f.writelines(new_lines)
            print("Cancellation processed.")
        else:
            print("Active booking not found with these details.")

    def get_room_price(self, room_num):
        # تابع کمکی برای پیدا کردن قیمت اتاق جهت بازگشت وجه
        rooms = Room.load_rooms()
        for r in rooms:
            if r.room_number == room_num:
                return r.price
        return 0

# --- شروع برنامه ---
if __name__ == "main":
    # ایجاد فایل‌های اولیه اگر نباشند
    if not os.path.exists(USER_FILE): open(USER_FILE, 'w').close()
    if not os.path.exists(BOOKING_FILE): open(BOOKING_FILE, 'w').close()
    if not os.path.exists(ROOM_FILE):
        with open(ROOM_FILE, "w", encoding='utf-8') as f:
            f.write("101,single,1,500,yes,available\n")
            f.write("102,double,2,800,yes,available\n")
            f.write("103,suite,4,1500,yes,available\n")

    # اجرای منو
    app = User(None, None, 0, None)
    app.menu()