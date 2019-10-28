## 
#  This application keeps track of the household chores completed in a shared
#  house over a number of weeks.
#
#  Author: Rae Harbird
#  Date: December 2019

from household_module import Household
from chores_list_module import ChoresList, Chore
from participants_list_module import Participants

## Constants used for validation

MENU_CHOICES = ['A', 'C', 'V', 'L', 'S', 'Q']

## Prints the menu for the application. 
#
def print_menu():
    menu_string = ("\n\nWelcome to Chore Chart:\n\n"
                 "\tAbout \t\t\t\t(A)\n"
                 "\tCreate Household \t(C)\n"
                 "\tView Household \t\t(V)\n"
                 "\tLog Chores Done \t(L)\n"
                 "\tShow Leaderboard \t(S) \n"
                 "\tQuit \t\t\t\t(Q)")
    print(menu_string)


## Prints a description of the application. 
#
#
def about() :
    about_string = ("\n\nWelcome to Chore Chart. "
                   "Chore Chart helps housemates (people sharing a house) "
                   "to keep a record of what needs doing every week and "
                   "who is doing it. The leaderboard shows who has earned "
                   "the most points for household tasks so far\n")
    print(about_string)


##  Creates a new household using the information entered by the user.
#   @param all_households a list of household objects
#
#
def create_household(all_households) :
    new_household_name = get_household_name()
    found = False
    household_obj = household_exists(new_household_name, all_households)
    
    if  household_obj == None:
        members_set = get_participants_names()
        chores_set = get_chores()
        household_obj = Household(new_household_name, members_set, chores_set)
        all_households.append(household_obj)
        print("\n\tHousehold entered:\n")
        print("\t\tHousehold Name: ", getattr(household_obj, "household_name"))
        print("\t\tParticipants: ", getattr(household_obj, "participants"))
        print("\t\tChores (Frequency): ", getattr(household_obj, "chores"))
    else:
       print("Household {} already exists, returning to the menu."
              .format(new_household_name))
        
    return 

##  Checks whether a household with a given name exists in the list
#   of households.
#
#   @param all_households a list of household objects
#   @param household_name the household name to check
#   @return the household object if the household exists and None if it
#   does not.
#
#
def household_exists(new_household_name, all_households) :
    h_obj = None

    for household in all_households :
        if household.household_name == new_household_name :
            h_obj = household

    return h_obj
        

##  Prompts the user for a household name and checks that the name is
#   reasonable.
#   @return a string containing the household name.
#
#   Invariants: a household name must be between the minimum and maximum length
#               and cannot be blank. The name must contain only alphanumeric
#               characters. 
#           
def get_household_name() :
    
    household_name = ""
    valid = False
    
    while not valid:
        household_name = input("\n\tEnter household name: ")
        try:
            Household.is_valid_name(household_name)
            valid = True
        except ValueError as err:
            print(err)

    return household_name


##  Prompts the user for the chore frequency and validates the number.
#   @return the chore frequency.
#
#   Invariants: the frequency must be between the minimum and maximum
#   frequency.
#
def get_chore_frequency() :

    valid = False
    chore_frequency = 0
    
    
    while not valid :
        chore_frequency = input("\n\t\tTimes per week: ")
        try :
            Chore.is_valid_frequency(chore_frequency)
            valid = True
        except (TypeError, ValueError) as err:
            print(err)

    return int(chore_frequency)


##  Gets the names for the people in the household and stores them in a set.
#
#   Invariants: duplicate names are not allowed
#
#   @return a set containing the names.
#
def get_participants_names():
    household_names = set()
    
    name = "AAA"    # dummy value so that we can start the while loop
    
    number_of_people = 1
    while name != "" :
        name = get_person_name(number_of_people)
 
        if name == "" :
            try :
                Participants.is_valid_length(household_names)
            except ValueError as err:
                print(err)
                name = "AAA"
        else:
            current_length = len(household_names)
            household_names.add(name)
            if current_length < len(household_names) :
                number_of_people = number_of_people + 1
            else:
                print(("\n\t\tSorry, you already have"
                       "a household member called {}, " + \
                      "try again.").format(name))       
        
    return household_names


##  Prompts the user for a person's name and validates it.
#   @param participant_number the number of participants entered so far.
#   @return a string containing the person's name.
#
#   Invariants: a person's name must be between the minimum and maximum length
#               and cannot be blank. The name must contain 
#               alphanumeric characters.
#
def get_person_name(participant_number) :
    
    # Finish when we have a valid answer which is either a blank or a
    # valid name
    finish = False
    
    while not finish :
        person_name = input("\n\tEnter the name of participant {}: " \
                                    .format(participant_number)).strip()
        if is_blank(person_name) :
            finish = True
        else :
            try :
                Participants.is_valid_name(person_name)
                finish = True
            except ValueError as err:
                print(err)
                
    return person_name


##  Gets the chores.
#
#   Invariants: duplicate chore names are not allowed,
#               names must consist of words which are alphanumeric characters,
#               names must >= the minimum valid length,
#               names must be <= the maximum valid length,
#               chore frequency must be >= the minimum frequency,
#               chore frequency must be <= the maximum frequency
#
#   @return a list containing chore objects.
#
def get_chores():

    chores_list = set()
    new_chore = "AAA"    # dummy value so that we can start the while loop
    number_of_chores = 0

    while new_chore != "" :
        new_chore = get_chore(number_of_chores + 1)
        if new_chore == "" :
            try :
                ChoresList.is_valid_length(chores_list)
            except ValueError as err:
                print(err)
                new_chore = "AAA"
        else:
            try :
                ChoresList.is_unique(new_chore, chores_list)
                chore_frequency = get_chore_frequency()
                chore_obj = Chore(new_chore, chore_frequency)
                chores_list.add(chore_obj)
                number_of_chores = number_of_chores + 1
                
            except ValueError as err :
                print(err)

    return chores_list 


##  Prompts the user for a chore name and validates it.
#   @param chore_number the number of chores entered so far.
#   @return a string containing the chore name.
#
#   Invariants: a chore name must be between the minimum and maximum length
#   and cannot be blank. The name must be composed of alphanumeric characters.
#
def get_chore(chore_number) :
    
    # A valid answer is either a blank or a valid name
    valid_answer = False
    
    while not valid_answer :

        chore_name = input("\n\tEnter"
                           " the name of chore {}: ".format(chore_number))

        if chore_name == "" :
            valid_answer = True
        else : 
            try :
                Chore.is_valid_chore_name(chore_name)
                valid_answer = True
            except ValueError as err :
                print(err)
                
    return chore_name


##  Validates the option choice.
#
#   @return True or False
#
#   Invariants: The option must be a valid choice from MENU_CHOICES
#
def is_valid_option(option):
    if is_blank(option):
        return False
    elif option[0].upper() in MENU_CHOICES:
        return True
    else:
        return False


##  Checks whether a string contains only whitespace
#
#   @param any_string a string
#   @return True or False
#
#
def is_blank(any_string):
    test_str = "".join(any_string.split())
    if len(test_str) == 0:
        return True
    else :
        return False


##  View household.
# @param all_households, a list of household objects
#
def view_household(all_households):

    view = input("\n\tEnter a household to view: ")
    house = household_exists(view, all_households)
    while house == None:
        print("\n\tThat household does not exist.")
        view = input("\n\tEnter a household to view: ")
        house = household_exists(view, all_households)
    print("\n", house)
    
    
    return    


##  Log chores.
# @param all_households, a list of household objects
#
def log_chores(all_households):
    
    # Gets an existing household name and object 
    house = None
    while house == None:
        house_log = get_household_name()
        house = household_exists(house_log, all_households)
        if house == None:
            print("That household does not exist.")
    # Converts the participants and chores sets to lists so they can be referenced using an index
    participants=list(house.participants.participants)
    chores=list(house.chores.chores)
    # Prints the household
    print("\n", house)
    # Gets the number assigned to the relevant participant and that participant's name
    name_number = get_number("participants'", participants)
    log_name = participants[int(name_number)-1]
    print("\n\tYou are logging {}’s chores. ".format(log_name))
    # Gets the number assigned to the relevant chore and that chore's name
    chore_number = get_number("chores'", chores)
    log_chore = str(chores[int(chore_number)-1])[:-4]
    # Gets the current chore log data for the relevant participant and chore
    current_completed = house.chore_log[log_name][log_chore]
    print("\n\t{} has done '{}' {} times."
          .format(log_name, log_chore, current_completed))
    number_completed = input("\n\tHow many more times has {} done '{}': "
                             .format(log_name, log_chore))
    # Asks for the number of chores completed and checks that it the input is a number, and that it is between 0 and the maximum number
    while number_completed.isdigit()==False or (int(number_completed) + int(current_completed)) > Household.MAXIMUM_CHORES_DONE or int(number_completed) <= 0 :
        print("\n\tThat is not a valid number completed. The total number completed must be between 0 and {}."
              .format(Household.MAXIMUM_CHORES_DONE))
        number_completed = input("\n\tHow many more times has {} done '{}': "
                                 .format(log_name, log_chore))
    # Updates the chore log
    house.update_log(log_name, log_chore, int(number_completed))
    # Gets the new chore log and prints it 
    current_completed = house.chore_log[log_name][log_chore]
    print("\n\t{} has done '{}' {} times."
          .format(log_name, log_chore, current_completed))
    return    


##  Gets a number of an entry in a list.
# @param number_type, a string representing what the number represents
# @param attr_list, a list of the attribute the number in referencing
#
def get_number(number_type, attr_list):
    # Asks for the number assigned to the relevant attribute
    # Checks that the input is a number, and that it is between 0 and the length if the attribute list
    number = input("\tEnter the {} number: ".format(number_type))
    while number.isdigit() == False or int(number) > len(attr_list) or int(number) <= 0:
        print("\n\tThat is not a valid {} number.".format(number_type))
        number = input("\n\tEnter the {} number: ".format(number_type))
    return number


##  Show the leaderboard for a house.
# @param all_households, a list of household objects
#
def show_leaderboard(all_households):
    
    # Asks for a household name and check if it exists
    leader_house = input("\n\tEnter the household name: ")
    house = household_exists(leader_house, all_households)
    while house == None:
        print("\n\tThat household does not exist.")
        leader_house = input("\n\tEnter the household name: ")
        house = household_exists(leader_house, all_households)
    # Gets the chore log for the selected household
    leaderboard_log = house.chore_log
    # Prints the leaderboard for the selected household
    print("\n\tChore Leaderboard for {}: \n".format(leader_house))
    for person in leaderboard_log:
        print("\t{}:".format(person))
        for chore in leaderboard_log[person]:
                print("\t\t{} ({})"
                      .format(chore, leaderboard_log[person][chore]))
    return


##  Prints the menu, prompts the user for an option and validates the option.
#
#   @return a character representing the option.
#
def get_option():  
    option = '*'
    
    while is_valid_option(option) == False:
        print_menu()
        option = input("\nEnter an option: ")
   
    return option.upper()

   
## The menu is displayed until the user quits
# 
def main() :
    
    all_households = []   
    option = '*'
    # Reads the household and chore log files and adds any valid data
    read_households(all_households)
    read_chore_log(all_households)
    while option != 'Q':
        option = get_option()        
        if option == 'A':
            about()
        elif option == 'C':
            create_household(all_households)
        elif option == 'V':
            # Only continues if household isn’t empty
            if check_empty_household(all_households) == False:
                view_household(all_households)
        elif option == 'L':
            # Only continues if household isn’t empty
            if check_empty_household(all_households) == False:
                log_chores(all_households)
        elif option == 'S':
            # Only continues if household isn’t empty
            if check_empty_household(all_households) == False:
                show_leaderboard(all_households)
    # Writes the household and chore log data to the respective files
    write_households(all_households)
    write_chore_log(all_households)
    print("\n\nBye, bye.")


## Checks if any household exists and returns a boolean
# @param all_households, a list of household objects
# @return boolean, True if no households, False if any households
#
def check_empty_household(all_households):
    
    # Checks if there are any households and if not prints an error message
    if len(all_households) == 0:
        print("\n\tNo households exist.")
        print("\tPlease enter a household to choose this option.")
        return True
    else:
        return False


## Reads a file line by line and returns it as a list
# @param file_name, the name of the file including file extension
# @return lines, a list containing the content of the file line by line, and split by comma
#
def read_file(file_name):
    
    try:
        # Creates an empty list to hold all the file from the file
        lines = []
        # Open the file and read it line by line
        with open(file_name) as file:
            line = file.readline()
            while line:
                # Removes the whitespace at the end of, and splits by comma, each line and adds it to the lines list
                line = line.rstrip()
                line = line.split(",")
                lines.append(line)
                line = file.readline()
        file.close()
    except IOError:
        # Print an error if the file can not be found
        print("Error: '{}' file can not be found.".format(file_name))
    return lines


## Writes a list to a file line by line
# @param file_name, the name of the file including file extension
# @param lines, a list containing the content to be written to the file, line by line
#
def write_to_file(file_name, lines):
    
    # Creates a list to write to the file
    output = []
    # For each line in the lines list, join the elements into a string separated by a comma
    # Then add the string the output list
    for line in lines:
        line = ",".join(line)
        output.append(line)
    # Joins all the elements in the output list separated by a new line
    # This writes all the elements on different lines of the file
    output = "\n".join(output)
    # Opens the file, write the list to it, and then closes it
    # Creates the file if it does not exist
    file = open(file_name, "w+")
    file.write(output)
    file.close()


## Reads the households file and sorts the data from it
# @param all_households, a list of household objects
#
def read_households(all_households):
    
    # Gets the data from the households file
    lines = read_file("households.txt")
    # Creates empty lists of the households' properties
    all_household_names = []
    all_participants = []
    all_chores = []
    # For each line of the file data, it validates the elements based on the given format
    for line in lines:
        # Creates an error message referencing the line to be displayed when there is an error
        error_msg = "\nError on line {} of the 'households' file (This line will be omitted):\n\t".format(lines.index(line)+1)
        # Tries to get the household name and if it can not be found, gives an error and skips the whole line
        try:
            household_name = line[0]
        except (IndexError, ValueError):
            print(error_msg)
            print("\tThe first element should be the households name."
                  .format(lines.index(line)+1))
            continue
        # Tries to get the participants and if it can not be found, gives an error and skips the whole line
        try:
            number_of_participants = int(line[1])
            particpants_offset = number_of_participants + 2
            particpants = line[2:particpants_offset]
        except (IndexError, ValueError):
            print(error_msg)
            print("\tThe second element should be the number of participants followed by that number of participants.")
            continue
        # Tries to get the chores and if it can not be found, gives an error and skips the whole line
        try:
            number_of_chores = int(line[particpants_offset])
            chores_offest = particpants_offset + 1
            chores = line[chores_offest:chores_offest+(2*number_of_chores)]
        except (IndexError, ValueError):
            print(error_msg)
            print("\tThe element after the defined number of participants should be the number of chores followed by that number of chores and frequencies.")
            continue
        # Checks if the households’ name is valid and adds them to the respective list
        # If not valid, gives an error and skips the whole line
        try:
            Household.is_valid_name(household_name)
            if household_name in all_household_names:
                raise ValueError("The household name '{}' had already been used and can not be used again."
                                 .format(household_name))
        except (TypeError, ValueError) as err:
            print(error_msg, err)
            continue
        # Checks if the participants names' and number of participants are valid and adds them to the respective list
        # If not valid, gives an error and skips the whole line
        try:
            Participants.is_valid_length(particpants)
            for name in particpants:
                Participants.is_valid_name(name)
            particpants_set = set(particpants)
            if len(particpants) != len(particpants_set):
                raise ValueError("There are multiple participants with the same.")
        except (TypeError, ValueError) as err:
            print(error_msg, err)
            continue
        # Checks if the number of chores, chore name, and chore frequency are is valid and adds them to the respective list
        # If not valid, gives an error and skips the whole line
        try:
            chore_names = []
            for chore in chores:
                if chore.isdigit():
                    Chore.is_valid_frequency(chore)                
                else:
                    Chore.is_valid_chore_name(chore)
                    chore_names.append(chore)
            ChoresList.is_valid_length(chore_names)
            chore_names_set = set(chore_names)
            if len(chore_names) != len(chore_names_set):
                raise ValueError("There are multiple chores with the same.")
        except (TypeError, ValueError) as err:
            print(error_msg, err)
            continue
        all_household_names.append(household_name)
        all_participants.append(particpants)
        all_chores.append(chores)
    # Creates objects for all the valid households
    add_households(all_households, all_household_names, all_participants, all_chores)
    return


## Creates ojbects for all he valid households from teh file
# @param all_households, a list of household objects
# @param household_names, a list of all valid household names from file
# @param particpants, a list of all valid participants from file
# @param chores, a list of all valid chores and frequcnise from file
#
def add_households(all_households, household_names, particpants, chores):
    
    # For each household from the file, create the relevant objects for the household
    for household in range(len(household_names)):
        new_household_name = household_names[household]
        members_set = set(particpants[household])
        chores_set = set()
        for i in range(len(chores[household])):
            if i%2 == 0:
                chore_obj = Chore(chores[household][i], chores[household][i+1])
                chores_set.add(chore_obj)
        household_obj = Household(new_household_name, members_set, chores_set)
        all_households.append(household_obj)
    return


## Formats the household objects for writing to a file
# @param all_households, a list of household objects
#
def write_households(all_households):
    
    # Creates an empty list for all the lines to write to the file
    all_lines = []
    # For all the household objects, format the data to write to the file
    for household in all_households:
        line = []
        # Gets all the attributes for the household
        household_name = getattr(household, "household_name")
        participants = str(getattr(household, "participants"))
        chores = str(getattr(household, "chores"))
        # Get the number of participants and chores
        number_of_people = str(len(participants.split(",")))
        number_of_chores = str(len(chores.split(",")))
        # Adds the household name and number of people to the formatted line
        line.append(household_name)
        line.append(number_of_people)
        # Removes whitespaces
        participants = participants.replace(" ","")
        # Adds the participants and number of chores to the formatted line
        line.append(participants)
        line.append(number_of_chores)
        # Removes the brackets and whitespaces
        chores = chores.replace(" (", ",").replace(")", "").replace(" ", "")
        # Adds the chores to the formatted line
        line.append(chores)
        # Ads the lines to the all_lines list
        all_lines.append(line)
    # Write the all_lines list to the households file
    write_to_file("households.txt", all_lines)
    return


## Reads the chore_log from a file and updates the chore log from it
# @param all_households, a list of household objects
# 
def read_chore_log(all_households):
    
    # Read all the lines from the chore_log file
    lines = read_file("chore_log.txt")
    # Creates a list of all the names of current households
    valid_households = []
    for household in all_households:
         valid_households.append(getattr(household, "household_name"))
    # For all the lines from the file, validate the data and update the chore log
    for line in lines:
        # Creates an error message referencing the line to be displayed when there is an error
        error_msg = "\nError on line {} of the 'chore_log' file (This line will be omitted):\n\t".format(lines.index(line)+1)
        try:
            # If the first element in the line is a valid household, continue
            # If not print an error message
            if line[0] in valid_households:
                # Gets the attribute for the respective household
                household_obj_index = valid_households.index(line[0])
                household_obj = all_households[household_obj_index]
                participants = str(getattr(household_obj, "participants"))
                chores = str(getattr(household_obj, "chores"))
                # If the second element is not a current participant, print an error and skip the line
                if line[1] not in participants:
                    raise ValueError("The second element should be the name of a current participant.")
                # For every pair of elements after the second element, check that the two elements are valid 
                for i in range(2, len(line), 2):
                    # If the first of the pair is not a current chore, print an error and skip the line
                    if line[i] not in chores:
                        raise ValueError("The chores should be current chores.")
                    # If the second of the pair is not a digit, print an error and skip the line
                    elif line[i+1].isdigit() == False:
                        raise ValueError("The number completed should be a digit")
                    # If the second of the pair larger than the maximum number allowed, an error and skip the line
                    elif int(line[i+1]) > Household.MAXIMUM_CHORES_DONE:
                        raise ValueError("The number completed must be under {}".format(MAX_NUMBER_COMPLETED))
                    # If all checks are passed, update the household
                    else:
                        household_obj.update_log(line[1], line[i], line[i+1])
            else:
                raise ValueError("The first element should be the name of a current household.")
        except ValueError as err:
            print(error_msg, err)
        except IndexError:
            print(error_msg, "The 'chore_log' file is incomplete")
    return


## Formats the chore_log attribute for writing to a file
# @param all_households, a list of household objects
# 
def write_chore_log(all_households):
    
    # Creates an empty list of the lines to be written to a file
    lines = []
    # For every household, format the data to be written to the file
    for household in all_households:
        # Gets the chore_log for the respective household 
        household_name = getattr(household, "household_name")
        log = getattr(household, "chore_log")
        # Creates a sting from the chore_log in the format household name, participant, chore_name, number completed
        for name in log:
            file_line=[]
            file_line.append(household_name)
            file_line.append(name)
            for chore in log[name]:
                file_line.append(chore)
                file_line.append(str(log[name][chore]))
            lines.append(file_line)
    # Write all the chore log data to the file
    write_to_file("chore_log.txt", lines)
    return


# Start the program
if __name__ == "__main__":
    main()



