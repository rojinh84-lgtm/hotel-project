#starting with sign in and sign up page for user
User_file = "users.txt"

def signup():
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



    with open("users.txt", "w") as f:
        f.write(f"{username},{password},{credit},{user}\n" )
    print(' you have succesfully added!!')

def login():
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
                        return
              
    print("Invalid username or password. Please try again. or sign up if you don't have an account.")
    
    
 # main menu using while loop
while True:
    print("Welcome to the hotel booking system!")
    print("1. Sign up")
    print("2. Log in")
    print("3. Exit")
    choice = input("what can we do for you?")
    
    
    if choice == '1':
         signup()
         break
    elif choice == '2':
         login()
         break
    elif choice == '3':
         print("Thank you for using the hotel booking system. Goodbye!")
         break
    else:
         print("Invalid choice. Please try again.")
            
    
    
    
    
    
    
    
    
    
    
    

    
