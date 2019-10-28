def log_chores(all_households):
    
    
    # Asks for a household name and check if it exists
    # house_log = input("\n\tEnter the household name: ")
    # house = household_exists(house_log, all_households)
    # while house == None:
    #     print("\n\tThat household does not exist.")
    #     house_log = input("\n\tEnter the household name: ")
    #     house = household_exists(house_log, all_households)
    house = None
    while house == None:
        house_log = get_household_name()
        house = household_exists(house_log, all_households)
        if house == None:
            print("That household does not exist.")
    
        
    # Converts the participants and chores sets to lists so they can be referenced using an index
    participants=list(house.participants.participants)
    chores=list(house.chores.chores)
    # Creates name and chore counters
    name_count = 1
    chore_count = 1
    # Prints a numbered list of participants and chores of the chosen household
    house_string = "\tParticipants:\n"
    for name in participants:
        house_string += "\t\t{}\n".format(str(name_count) + ". " + name)
        name_count = name_count + 1
    house_string += "\n\tChores:\n"
    for chore in chores:
        house_string += "\t\t{}\n".format(str(chore_count) + ". " + str(chore)[:-4])
        chore_count = chore_count + 1
    print("\n", house_string)
    # Asks for the number assigned to the relevant participant and checks that the input is a number, and that it is between 0 and the number of participants in the household
    name_number = input("\tEnter the participant number: ")
    while name_number.isdigit()==False or int(name_number)>len(participants) or int(name_number)<=0 :
        print("\n\tThat is not a valid participant number.")
        name_number = input("\n\tEnter the participant number: ")
    log_name = participants[int(name_number)-1]
    print("\n\tYou are logging {}’s chores. ".format(log_name))
    # Asks for the number assigned to the relevant chore and checks that it the input is a number, and that it is between 0 and the number of chores in the household
    chore_number = input("\n\tEnter the chore number: ")
    while chore_number.isdigit()==False or int(chore_number)>len(chores) or int(chore_number)<=0 :
        print("\n\tThat is not a valid chore number.")
        chore_number = input("\n\tEnter the participant number: ")
    log_chore = str(chores[int(chore_number)-1])[:-4]
    # Gets the current chore log data for the relevant participant and chore
    current_completed = house.chore_log[log_name][log_chore]
    print("\n\t{} has done '{}' {} times.".format(log_name, log_chore, current_completed))
    number_completed = input("\n\tHow many more times has {} done '{}': ".format(log_name, log_chore))
    # Asks for the number of chores completed and checks that it the input is a number, and that it is between 0 and the maximum number
    while number_completed.isdigit()==False or int(number_completed)>Household.MAXIMUM_CHORES_DONE or int(number_completed)<=0 :
        print("\n\tThat is not a valid number completed. It must be between 0 and {}.".format(Household.MAXIMUM_CHORES_DONE))
        number_completed = input("\n\tHow many more times has {} done '{}': ".format(log_name, log_chore))
    # Updates the chore log
    house.update_log(log_name, log_chore, number_completed)
    # Gets the new chore log and prints it 
    current_completed = house.chore_log[log_name][log_chore]
    print("\n\t{} has done '{}' {} times.".format(log_name, log_chore, current_completed))
    return




chores = "cook (4) skdhfks (45)"

chores = chores.replace(")", "").replace(" (", ",").replace(" ", "")
print(chores)