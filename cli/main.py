import retro_video_store

OPTIONS = {
    "1": "List all videos",
    "2": "List all customers",
    "3": "Add movie to database",
    "4": "Check out movie",
    "5": "Check in movie",
    "6": "List all options",
    "7": "Quit CLI",
}

def list_options():
    for number, command in OPTIONS.items():
        print(f"{number}. {command}")

def make_choice():
    valid_choices = OPTIONS.keys()
    choice = None

    while choice not in valid_choices:
        print("\nPlease make your selection.")
        choice = input("Enter the number your desired course of action.\nEnter 6 to view all options. Enter 7 to exit. \n")

        return choice

def print_single_row_of_stars():
    print("✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰")

def print_surround_stars(sentence):
    print_single_row_of_stars()
    print(sentence)
    print_single_row_of_stars()

def print_video(video):
    print_single_row_of_stars()
    print("Title: ", video["title"])
    print("Release Date: ", video["release_date"])
    print("Total Inventory: ", video["total_inventory"])
    print("ID: ", video["id"])
    print_single_row_of_stars()

def print_all_videos():
    videos = retro_video_store.list_videos()
    print( """

██    ██ ██ ██████  ███████  ██████  ███████ 
██    ██ ██ ██   ██ ██      ██    ██ ██      
██    ██ ██ ██   ██ █████   ██    ██ ███████ 
 ██  ██  ██ ██   ██ ██      ██    ██      ██ 
  ████   ██ ██████  ███████  ██████  ███████                                  

""")
    if not videos:
        print_surround_stars("No videos")
    else:
        for video in videos:
            print_video(video)
    print_single_row_of_stars()

def print_customer(customer):
    print_single_row_of_stars()
    print("Name: ", customer["name"])
    print("ID: ", customer["id"])
    print("Phone: ", customer["phone"])
    print("Postal Code: ", customer["postal_code"])
    print("Signup Date:", customer["register_at"])
    print_single_row_of_stars()

def print_all_customers():
    customers = retro_video_store.list_customers()
    print("""

 ██████ ██    ██ ███████ ████████  ██████  ███    ███ ███████ ██████  ███████ 
██      ██    ██ ██         ██    ██    ██ ████  ████ ██      ██   ██ ██      
██      ██    ██ ███████    ██    ██    ██ ██ ████ ██ █████   ██████  ███████ 
██      ██    ██      ██    ██    ██    ██ ██  ██  ██ ██      ██   ██      ██ 
 ██████  ██████  ███████    ██     ██████  ██      ██ ███████ ██   ██ ███████ 
                                                                              
                                                                              
""")
    if not customers:
        print_surround_stars("No customers")
    else:
        for customer in customers:
            print_customer(customer)
    print_single_row_of_stars()

def create_video():
    print("You would like to add a movie to the database.")
    title=input("Movie title: ")
    release_date=input("Release date of movie as datetime: ")
    total_inventory=input("Number of copies: ")
    response = retro_video_store.create_video(title, release_date, total_inventory)
    print_video(response)

def print_rental(rental):
    print_single_row_of_stars()
    print("Due date: ", rental["due_date"])
    print("Customer ID: ", rental['customer_id'])
    print("Video ID: ", rental['video_id'])
    print("Remaining copies of video: ", rental['available_inventory'])
    print(f"You have {rental['videos_checked_out_count']} videos currently checked out.")

def checkout_movie():
    print_single_row_of_stars()
    print("Video Check Out")
    customer_id = input("Please enter your customer id:\n")
    video_id = input("Please enter the video ID:\n")
    rental = retro_video_store.checkout_video(customer_id, video_id)
    print_rental(rental)

def checkin_movie():
    print_single_row_of_stars()
    print("Video Check In")
    customer_id = input("Please enter your customer id:\n")
    video_id = input("Please enter the video ID:\n")
    rental = retro_video_store.checkin_video(customer_id, video_id)
    print_rental(rental)

def run_cli():

    active = True
    while active:

        choice = make_choice()

        if choice=='1':
            print_all_videos()
        if choice=='2':
            print_all_customers()
        elif choice=='3':
            create_video()
        elif choice=='4':
            checkout_movie()
        elif choice=='5':
            checkin_movie()
        elif choice=='6':
            list_options()
        elif choice=='7':
            active = False


# On run:
print_single_row_of_stars()
print("""
 ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄            
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌           
▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌           
▐░▌       ▐░▌▐░▌               ▐░▌     ▐░▌       ▐░▌▐░▌       ▐░▌           
▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄      ▐░▌     ▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌           
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░▌     ▐░░░░░░░░░░░▌▐░▌       ▐░▌           
▐░█▀▀▀▀█░█▀▀ ▐░█▀▀▀▀▀▀▀▀▀      ▐░▌     ▐░█▀▀▀▀█░█▀▀ ▐░▌       ▐░▌           
▐░▌     ▐░▌  ▐░▌               ▐░▌     ▐░▌     ▐░▌  ▐░▌       ▐░▌           
▐░▌      ▐░▌ ▐░█▄▄▄▄▄▄▄▄▄      ▐░▌     ▐░▌      ▐░▌ ▐░█▄▄▄▄▄▄▄█░▌           
▐░▌       ▐░▌▐░░░░░░░░░░░▌     ▐░▌     ▐░▌       ▐░▌▐░░░░░░░░░░░▌           
 ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀       ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀            
                                                                            
 ▄               ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄      
▐░▌             ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░▌ ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     
 ▐░▌           ▐░▌  ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌     
  ▐░▌         ▐░▌       ▐░▌     ▐░▌       ▐░▌▐░▌          ▐░▌       ▐░▌     
   ▐░▌       ▐░▌        ▐░▌     ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌     
    ▐░▌     ▐░▌         ▐░▌     ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌     
     ▐░▌   ▐░▌          ▐░▌     ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░▌       ▐░▌     
      ▐░▌ ▐░▌           ▐░▌     ▐░▌       ▐░▌▐░▌          ▐░▌       ▐░▌     
       ▐░▐░▌        ▄▄▄▄█░█▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌     
        ▐░▌        ▐░░░░░░░░░░░▌▐░░░░░░░░░░▌ ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     
         ▀          ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀   ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀      
                                                                            
 ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄            
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌           
▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀            
▐░▌               ▐░▌     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌                     
▐░█▄▄▄▄▄▄▄▄▄      ▐░▌     ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄            
▐░░░░░░░░░░░▌     ▐░▌     ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌           
 ▀▀▀▀▀▀▀▀▀█░▌     ▐░▌     ▐░▌       ▐░▌▐░█▀▀▀▀█░█▀▀ ▐░█▀▀▀▀▀▀▀▀▀            
          ▐░▌     ▐░▌     ▐░▌       ▐░▌▐░▌     ▐░▌  ▐░▌                     
 ▄▄▄▄▄▄▄▄▄█░▌     ▐░▌     ▐░█▄▄▄▄▄▄▄█░▌▐░▌      ▐░▌ ▐░█▄▄▄▄▄▄▄▄▄            
▐░░░░░░░░░░░▌     ▐░▌     ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌           
 ▀▀▀▀▀▀▀▀▀▀▀       ▀       ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀            
                                                                            

""")
print("Select a course of action from the menu below:")
print_single_row_of_stars()
list_options()
run_cli()
