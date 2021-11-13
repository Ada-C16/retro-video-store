import video_store, sys

#Menu lists
OPTIONS = {
        "1": "Actions for Videos",
        "2": "Actions for Customers",
        "3": "Actions for Rentals",
        "4": "Exit"
        }

VIDEO_OPTIONS = {
        "1": "Get all Videos",
        "2": "Create new Video",
        "3": "View Video",
        "4": "Update Video",
        "5": "Delete Video",
        "6": "Get all rentals for Video",
        "7": "Return to Main Menu",
        }

CUSTOMER_OPTIONS = {
        "1": "Get all Customers",
        "2": "Create new Customer",
        "3": "View Customer",
        "4": "Update Customer",
        "5": "Delete Customer",
        "6": "Get all rentals for Customer",
        "7": "Return to Main Menu",
        }

RENTAL_OPTIONS = {
        "1": "Checkout Rental",
        "2": "Checkin Rental",
        "3": "Return to Main Menu",
        }

#Action Functions
def print_all_instances(class_type):
    "Defines a function to print all objects in a specified database"

    filter_question = input ("Would you like to apply filters to your list y/n?: ")

    if filter_question == "y":
        query_params = query_filter_options(class_type)
    else:
        query_params = {}
    
    print("Your total list is below:")

    if class_type == "videos":
        objects = video_store.list_objects("videos", query_params)
    elif class_type == "customers":
        objects = video_store.list_objects("customers", query_params)

    if not objects:
        print_surround_breaks("No records to show!")

    else:
        for object in objects:
            print_object(object)

    ending_menu()

def create_object(class_type):
    """Defines a function to create an object in a specified database"""

    print(f"Great! Let's create a new {class_type}!")
    body_dictionary = {}

    if class_type == "Video":
        body_dictionary["title"] = input("Video title: ")
        body_dictionary["release_date"] = input("Video release date: ")
        body_dictionary["total_inventory"] = input("Total inventory: ")
        response = video_store.create_object(body_dictionary, "videos")
        title = check_for_object_dictionary(response, "title")

    elif class_type == "Customer":
        body_dictionary["name"] = input("Customer name: ")
        body_dictionary["postal_code"] = input("Postal: ")
        body_dictionary["phone"] = input("Phone Number: ")
        response = video_store.create_object(body_dictionary, "customers")
        title = check_for_object_dictionary(response, "name")
    
    print(f"\nDatabase response: {response}")
    print(f'\nCongratulations! {title} was added to the Megariah database!')
    ending_menu()

def view_object(class_type):
    """Defines a function to view an object in a specified database"""

    id = input(f"Please insert the id of the {class_type} would you like to view: ")
    print_single_break_line()

    object = check_id_if_object(class_type, id)
    
    if object: 
        for key, value in object.items():
            print(f"{key}: {value}")

    ending_menu()

def update_object(class_type):
    """Defines a function to update an object from a specified database"""

    id = input(f"Please insert the id of the {class_type} would you like to update: ")
    check_id_if_object(class_type, id)
    body_dictionary = {}

    if class_type == "Video":
        body_dictionary["title"] = input("Video title: ")
        body_dictionary["release_date"] = input("Video release date: ")
        body_dictionary["total_inventory"] = input("Total inventory: ")
        response = video_store.update_object(body_dictionary, id, "videos")
        title = check_for_object_dictionary(response, "title")

    elif class_type == "Customer":
        body_dictionary["name"] = input("Customer name: ")
        body_dictionary["postal_code"] = input("Postal: ")
        body_dictionary["phone"] = input("Phone Number: ")
        response = video_store.update_object(body_dictionary, id, "customers")
        title = check_for_object_dictionary(response, "name")
    
    print(f"\nDatabase response: {response}")
    print(f'\nCongratulations! {class_type} {title} was officially updated in the Megariah database!')
    ending_menu()

def delete_object(class_type):
    """Defines a function to delete an object from a specified database"""

    id = input(f"Please insert the id of the {class_type} would you like to delete: ")
    print_single_break_line()

    response = check_id_if_object(class_type, id)

    if class_type == "video":
        title = check_for_object_dictionary(response, "title")
        database = video_store.delete_object("videos", id)
    elif class_type == "customer":
        title = check_for_object_dictionary(response, "name")
        database = video_store.delete_object("customers", id)
    
    print(f"Database response: {database}")

    print(f"You have officially deleted {class_type} {title} from the Megariah database :(")
    ending_menu()

def retrieve_rentals(class_type):
    "Defines a function to retrieve all objects from a join table with specific foreign key"

    id = input(f"Please insert the id of the {class_type} would you like to rentals for: ")

    check_id_if_object(class_type, id)

    if class_type == "video":
        objects = video_store.retrieve_rentals("videos", id)

    elif class_type == "customer":
        objects = video_store.retrieve_rentals("customers", id)
    
    if not objects:
        print_surround_breaks("No rentals to show!")

    else:
        for object in objects:
            print_object(object)
    
    ending_menu()

def rental_status(status):
    """Defines a function for creating an object in the join table or changing the status to checked-in"""

    body_dictionary = {}
    body_dictionary["customer_id"] = input("Customer id: ")
    body_dictionary["video_id"] = input("Video id: ")

    response = video_store.rental_status(body_dictionary, status)
    
    print(f"\nDatabase response: {response}")
    customer_id = body_dictionary["customer_id"]
    video_id = body_dictionary["video_id"]

    customer = check_id_if_object("customer", customer_id)
    video = check_id_if_object("video", video_id)

    customer_name = customer["name"]
    video_title = video["title"]

    if status == "check-out":
        print(f'\nCongratulations! {customer_name} successfully checked out {video_title}!')
        
    elif status == "check-in":
        print(f'\nCongratulations! {customer_name} successfully checked in {video_title}!')
    
    ending_menu()

#Helper Functions
def list_options(initial_choice):
    """Defines a helper function to tist all options in specified menu"""

    if initial_choice == '0':
        for number, feature in OPTIONS.items():
            print(f"{number}. {feature}")
    
    elif initial_choice == '1':
        for number, feature in VIDEO_OPTIONS.items():
            print(f"{number}. {feature}")
    
    elif initial_choice == '2':
        for number, feature in CUSTOMER_OPTIONS.items():
            print(f"{number}. {feature}")

    elif initial_choice == '3':
        for number, feature in RENTAL_OPTIONS.items():
            print(f"{number}. {feature}")

def make_choice(valid_choices):
    """Defines a helper function to choose an action from a menu"""

    choice = None

    while choice not in valid_choices:
        print("\nWhat would you like to do?")
        choice = input("Please choose from the list above: ")
        print_single_break_line()

    return choice

def check_for_object_dictionary(response, dict_key):
    """Defines a helper function to make sure a k:v exists in dictionary"""

    try:
        response[dict_key]

    except KeyError:
        ending_menu()

    return response[dict_key]

def check_id_if_object(class_type, id):
    """Defines a helper function to verify that id is a valid object"""

    if class_type == "video":
        object = video_store.view_object("videos", id)
    elif class_type == "customer":
        object = video_store.view_object("customers", id)
    
    return object

def print_object(object):
    """Defines a helper function to print a single object from dictionary"""

    print_single_break_line()

    for key, value in object.items():
        print(f"{key}: {value}")

def query_filter_options(class_type):
    """Defines a helper function to request clients filter section and put in dictionary"""

    print_single_break_line()

    query_params = {}
    query_params["sort"] = input("Sort by name asc or desc?: ")
    query_params["n"] = check_if_numeric(input("If you would like to limit the number of responses per page please input number or None: "), class_type)
    query_params["p"] = check_if_numeric(input("Please input the page number you would like to see if limiting responses, in no input None: "), class_type)

    return query_params

def check_if_numeric(thing_to_check, class_type):
    """Defined helper function if value is numeric"""

    if not thing_to_check.isnumeric():
        print("\nmessage: Please use a number")
        print_all_instances(class_type)

    else:
        return thing_to_check

#Running the program
def run_cli():
    """Defines a function to start up and run Megariah Retro Video Store program"""

    play = True
    while play:

        list_options('0')
        print_single_break_line()
        choice = make_choice(OPTIONS.keys())

        #Video Menu
        if choice == '1':
            list_options('1')
            secondary_choice = make_choice(VIDEO_OPTIONS.keys())
            video_cli(secondary_choice)
        
        #Customer Menu
        if choice == '2':
            list_options('2')
            secondary_choice = make_choice(CUSTOMER_OPTIONS.keys())
            customer_cli(secondary_choice)
        
        #Rental Menu
        if choice == '3':
            list_options('3')
            secondary_choice = make_choice(RENTAL_OPTIONS.keys())
            rental_cli(secondary_choice)

        #Exit
        if choice == '4':
            print_surround_breaks("Goodbye!")
            quit()

def video_cli(secondary_choice):
    """Defines a helper function to display and action the video menu"""

    play = True
    while play:

        if secondary_choice == '1':
            print_all_instances("videos")
        
        elif secondary_choice == '2':
            create_object("Video")
        
        elif secondary_choice == '3':
            view_object("video")
        
        elif secondary_choice == '4':
            update_object("Video")
        
        elif secondary_choice == '5':
            delete_object("video")
        
        elif secondary_choice == "6":
            retrieve_rentals("video")
        
        elif secondary_choice == '7':
            play = False

def customer_cli(secondary_choice):
    """Defines a helper function to display and action the customer menu"""

    play = True
    while play:

        if secondary_choice == '1':
            print_all_instances("customers")
        
        elif secondary_choice == '2':
            create_object("Customer")
        
        elif secondary_choice == '3':
            view_object("customer")

        elif secondary_choice == '4':
            update_object("Customer")

        elif secondary_choice == '5':
            delete_object("customer")

        elif secondary_choice == "6":
            retrieve_rentals("customer")
        
        elif secondary_choice == '7':
            play = False

def rental_cli(secondary_choice):
    """Defines a helper function to display and action the rental menu"""

    play = True
    while play:
        if secondary_choice == '1':
            rental_status("check-out")
        
        elif secondary_choice == '2':
            rental_status("check-in")

        elif secondary_choice == '3':
            play = False

def ending_menu():
    """Defines a helper function to display and action the ending menu"""

    print_single_break_line()
    list_options('4')
    tertiary_choice = input("Return to main menu? y/n? If no you will exit the program.\nTo do action again, type redo: \n")
    print_single_break_line()

    if tertiary_choice == 'y':
        run_cli()
    
    elif tertiary_choice == 'n':
        quit()
    
    elif tertiary_choice =="redo":
        return None
    
    else:
        return None

def print_break_line():
    print("\n===================================================")
    print("                    *********                      ")
    print("===================================================\n")

def print_surround_breaks(sentence):
    print("\n===================================================")
    print(sentence)
    print("===================================================\n")

def print_single_break_line():
    print("\n===================================================\n")

print("\nWelcome to the Megariah Video Store!")
print("Where all your MEGA sized video needs are met!")
print("Please choose from the options below:")
print_break_line()
run_cli()
