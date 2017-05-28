__author__ = 'Sudo Pnet'
from housing import LivingSpace, Staff, Office, Fellow
import random
import re


class Dojo(object):

    def __init__(self):
        """ The Dojo class contains the required utilities that will
        automate the process of calling instances of the other classes
        think of it as the main logic area that links a classes operations and
        the arguments parsed through the docopt.
        """
        self.unallocated_list = []
        self.unallocated_living_list = []
        self.staff_list = []
        self.fellow_list = []
        self.office_dict = {}
        self.living_space_dict = {}


    @staticmethod
    def get_number(list_arg):
        # will return the length of any list or dictionary passed to it.
        return len(list_arg)

    def create_room(self, room_type, parsed_name_list):
        """ uses room_type to decide what type of rooms to create, then loops through
        room_name_list creating a room for each element in the list"""
        for i in parsed_name_list:
            if not str.isalnum(str(i)):
                return "Invalid room name"

        # check that a room is non_existent before is is added to list of current rooms:
        # implementation is two fold: for offices and living_spaces
        if room_type == "living_space":
            for i in parsed_name_list:
                try:
                    if i not in self.living_space_dict.keys():
                        self.living_space_dict[LivingSpace(str(i)).name] = []
                        print("An office called %s has been successfully created!" %
                              LivingSpace(str(i)).name)
                    else:
                        raise ValueError("Room named: %s is already created" % LivingSpace(str(i)).name)
                except ValueError as error:
                    print(error)
                    return "Error raised"

            return self.living_space_dict

        if room_type == "office":
            for i in parsed_name_list:
                try:
                    if i not in self.office_dict.keys():
                        self.office_dict[Office(str(i)).name] = []
                        print("An office called %s has been successfully created!" % Office(str(i)).name)
                    else:
                        raise ValueError("Room named: %s is already created" % Office(str(i)).name)
                except ValueError as error:
                    print(error)
                    # return "Error raised"

            return self.office_dict

    def add_person(self, person_name, occupation, accommodate="n"):
        """ uses occupation and decides what constructor of either the subclasses
        fellow or staff that it should call. depending on the accommodate parameter
         a fellow occupant can be assigned an office and a living_space"""
        person_name = person_name.lower()
        occupation = occupation.lower()
        accommodate = accommodate.lower()
        if occupation == "fellow":
            if accommodate == "yes" or accommodate == "y":
                fellow_obj = Fellow(str(person_name))
                if fellow_obj.person_id:
                    if self.id_is_present(fellow_obj.person_id):
                        self.fellow_list.append(fellow_obj)
                        # randomise adding this fellow to the living_space_list
                        office_assign_check = self.assign_office(fellow_obj)
                        print(fellow_obj.person_name, "has been successfully added")
                        living_assign_check = self.assign_living_space(fellow_obj)
                        if not office_assign_check:
                            # the fellow was not assigned to an office
                            print(fellow_obj.person_name, "has been added but not assigned to any office")
                            self.unallocated_list.append(fellow_obj)
                        if not living_assign_check:
                            self.unallocated_living_list.append(fellow_obj)
                            print(fellow_obj.person_name, "has been added but not assigned to any living_space")
                    else:
                        print(fellow_obj.person_name, "has not been added; the id is already in the system")

            elif accommodate == "no" or accommodate == "n":
                fellow_obj = Fellow(str(person_name))
                if fellow_obj.person_id:
                    if self.id_is_present(fellow_obj.person_id):
                        self.fellow_list.append(fellow_obj)
                        office_assign_check = self.assign_office(fellow_obj)
                        print(fellow_obj.person_name, "has been successfully added")
                        if not office_assign_check:
                            print(fellow_obj.person_name, "has been added but not assigned to any office")
                            self.unallocated_list.append(fellow_obj)
                else:
                    print(fellow_obj.person_name, "has not been added; the id is already in the system")

        elif occupation == "staff":
            staff_obj = Staff(str(person_name))
            if staff_obj.person_id:
                if self.id_is_present(staff_obj.person_id):
                    self.staff_list.append(staff_obj)
                    # add the staff to the office dict ?
                    office_assign_check = self.assign_office(staff_obj)
                    if not office_assign_check:
                        print(staff_obj.person_name, "has been added but not allocated to any office")
                        self.unallocated_list.append(staff_obj)
                else:
                    print("detected an id collision for", staff_obj.person_name)
        else:
            print("Person has not been added")

    def assign_office(self, person_object):
        empty_office_dict = self.get_empty_rooms(self.office_dict, 6)
        try:
            random_office_key = random.choice(list(empty_office_dict.keys()))
            self.office_dict[random_office_key].append(person_object.person_name)
            print(person_object.person_name, "has been allocated the office",
                  random_office_key)
            return True
        except IndexError:
            return False

    def assign_living_space(self, person_object):
        try:
            empty_living_space_dict = self.get_empty_rooms(self.living_space_dict, 4)
            random_living_key = random.choice(list(empty_living_space_dict.keys()))
            self.living_space_dict[random_living_key].append(person_object.person_name)
            print(person_object.person_name, "has been allocated to the living space: ",
                  random_living_key)
            return True
        except IndexError:
            return False

    def print_room(self, room_name):
        """ Task1: input: room_name
        takes that room_name and prints all the people allocated to that room """
        if self.search_name(room_name):
            print('x'*12, '==> ', room_name.upper(), ' <==', 'x'*12, '\n')
            if room_name in self.living_space_dict.keys():
                if len(self.living_space_dict[room_name]) > 0:
                    for list_index in self.living_space_dict[room_name]:
                        print(list_index)
                else:
                    print("Not a single soul stored in this room")
                    return False
            elif room_name in self.office_dict.keys():
                if len(self.office_dict[room_name]) > 0:
                    for list_index in self.office_dict[room_name]:
                        print(list_index)
                else:
                    print("Not a single soul is in this room")
                    return False
            print("End of file reached")
        else:
            print("Room_", room_name, "was not found")
            return False

    def print_allocations(self, file_name=''):
        """Task1: Input: nothing; output:  print allocations to the screen.
         if -o argument is given => dump the allocations in a text file """
        """ Retrieve the office_dict and living_space_dict;
            Loops through them and prints the room name and
            comma separated names of the occupants"""
        print_string = ""
        for space_obj in self.living_space_dict.keys():
            if len(self.living_space_dict[space_obj]) == 0:
                pass  # i do not know yet what to do for the rooms that do not have occupants
            elif len(self.living_space_dict[space_obj]) == 1:
                print_string += "\n" + '(living_space)' + space_obj.upper() + "\n"
                print_string += self.living_space_dict[space_obj][len(self.living_space_dict[space_obj]) - 1] + "\n"
            elif len(self.living_space_dict[space_obj]) > 1:
                print_string += "\n" + '(living_space)' + space_obj + "\n"
                print_string += "\n" + space_obj.upper() + "\n"
                for person_index in range(0, len(self.living_space_dict[space_obj]) - 1):
                    print_string += self.living_space_dict[space_obj][person_index] + ", "
                print_string += self.living_space_dict[space_obj][len(self.living_space_dict[space_obj]) - 1] + "\n"
        for office_object in self.office_dict.keys():
            if len(self.office_dict[office_object]) == 0:
                pass
            if len(self.office_dict[office_object]) == 1:
                print_string += "\n" + '(office)' + office_object.upper() + "\n"
                print_string += self.office_dict[office_object][len(self.office_dict[office_object]) - 1] + "\n"
            if len(self.office_dict[office_object]) > 1:
                print_string += "\n" + '(office)' + office_object.upper() + "\n"
                for person_index in range(0, len(self.office_dict[office_object]) - 1):
                    print_string += self.office_dict[office_object][person_index] + ", "
                print_string += self.office_dict[office_object][len(self.office_dict[office_object]) - 1] + "\n"
        print(print_string)
        # Now for the file handling
        self.file_handler_func(print_string, file_name)

    def file_handler_func(self, print_string, file_name):
        if file_name:
            """ Check if file's content is more than 0, if true; query on an append or overwrite"""
            try:
                file_handler = open(file_name, 'r')
                file_handler.close()
            except FileNotFoundError as error:
                print("\nTrying to create a file called: ", file_name, "\n")
                file_handler = open(file_name, 'w+')
                file_handler.close()

            file_handler = open(file_name, 'r')
            if len(file_handler.read()) > 0:
                print("**file is not Empty,key in y to append, n to overwrite: ")
                choice = input()
                file_handler.close()
                if choice == 'Y' or choice == 'y':
                    file_handler = open(file_name, 'a')
                    file_handler.write(print_string)
                    print("Allocations succesfully appended to: ", file_name)
                    file_handler.close()
                elif choice == 'N' or choice == 'n':
                    file_handler = open(file_name, 'w')
                    file_handler.write(print_string)
                    print("succesfully overwrote: ", file_name)
                    file_handler.close()
            elif len(file_handler.read()) == 0:
                file_handler = open(file_name, 'w')
                file_handler.write(print_string)
                print("succesfully wrote to: ", file_name)
                file_handler.close()


    def print_unallocated(self, file_name=""):
        """Task1: Input: nothing; output:  print names of unallocated people on the screen.
         if -o argument is given => dump the names to a text file """
        # first write the print strings then call the file handler function
        print_string = " names of both the staff and the fellows who did not office allocations"
        second_print_string = " names of fellows who requested accommodation and are not yet accommodated"
        # unallocated_living-list contains the names of fellows who requested accommodation and are not yet accommodated
        # unallocated_list contains the name of both the staff and the fellows who did not office allocations
        for person in self.unallocated_list:
            print_string += "\n" + person.person_name + "\n"
        for person in self.unallocated_living_list:
            second_print_string += "\n" + person.person_name + "\n"
        total_string = print_string + second_print_string
        self.file_handler_func(total_string, file_name)

    # def reallocate_person(self, person_id, new_room):
    #     """ takes in two inputs the personal id and new room name.
    #     assign the person identified by the id to a new room name"""
    #     # logic: check if id exists; if it does check that room exists and is not full;
    #     # if it to exists remove the person with the specified id from all unallocated_lists
    #     # can also be used to assign an unallocated person to a room -> so far not
    #
    #     if self.id_is_present(person_id):
    #         #  first retrieve the room that the person_id is in and then restrict movement
    #         #  within that line(living_space or office)
    #         double_list = self.retrieve_person_by_id(person_id)
    #         if new_room in self.office_dict.keys():
    #             # the whole logic : remember to consider that staff should not rellocate to living space
    #             # unimplemented consideration : reallocating a fellow who does not want accommodation to
    #             # a living_space
    #             if len(self.office_dict[new_room]) < 6:
    #                 if new_room != double_list[0]:
    #                     if double_list[1] == "office":
    #                         # pop the person name from its current office and append it to the new office
    #                         self.office_dict[double_list[0]].pop(double_list[2])
    #                         self.office_dict[new_room].append(double_list[2])
    #                     else:
    #                         print("cannot rellocate from office to living_space")
    #                 else:
    #                     print("Person already in", new_room)
    #             else:
    #                 print(new_room, "seems to be full.")
    #         elif new_room in self.living_space_dict.keys():
    #             if len(self.living_space_dict[new_room]) < 4:
    #                 if new_room != double_list[0]:
    #                     if double_list[1] == "living_space":
    #                         # pop the person name from its current living_space and append it to the new living space
    #                         self.living_space_dict[double_list[0]].pop(double_list[2])
    #                         self.living_space_dict[new_room].append(double_list[2])
    #                     else:
    #                         print("cannot rellocate from living_space to office")
    #                 else:
    #                     print("Person already in", new_room)
    #             else:
    #                 print(new_room, "seems to be full")
    #         else:
    #             print("The room " + new_room + "has not yet been created")
    #     else:
    #         print("no one by the id" + person_id + "was found\n")

    def load_people(self, file_name):
        """ will take in one compulsory argument, which is the name of the file from which to read data
        from. for each record in this file we can then add_people"""
        # check if if file exists

        if self.if_file_exists(file_name):
            multi_list = self.read_file_names(file_name)
            for person in multi_list:
                self.add_person(person[0], person[1], person[2])
        else:
            print("Dojo could not find any file by the name: " + file_name)
            return False

    def if_file_exists(self, file_name):
        # Task2: this function checks if a file exists; if not it will return False
        try:
                file_handler = open(file_name, 'r')
                file_handler.close()
                return True
        except FileNotFoundError as error:
            return False

    def read_file_names(self, file_name):
        file_handler = open(file_name, 'r')
        return_list = []
        for line in file_handler:
            # maybe like create like a multi dimensional list; the main index will contain the line number
            # while the secondary index will like contain the list contents for each line.
            temp = line.strip("\n").split(" ")
            return_list.append(self.refractor_line_feed(temp))
        file_handler.close()
        return return_list

    def refractor_line_feed(self, temp_list):
        full_name = temp_list[0] + " " + temp_list[1]
        occupation = temp_list[2]
        temp = []
        temp.append(full_name)
        temp.append(occupation)
        if len(temp_list) == 3:
            temp.append("n")
            return temp
        elif len(temp_list) == 4:
            temp.append(temp_list[3])
            return temp

    def save_state(self):
        pass

    def load_state(self):
        pass

    def get_empty_rooms(self, current_diction, max_num_of_rooms):
        """ gets a diction with rooms that are full and others that are not full
        it then returns the offices that are not full"""
        non_full_diction = {}
        for i in current_diction.keys():
            if len(current_diction[i]) < max_num_of_rooms:
                non_full_diction[i] = current_diction[i]
        return non_full_diction

    def get_number_in_room_dictionary(self, dictionary):
        count = 0
        for i in dictionary.keys():
            for list_value in dictionary[i]:
                if list_value:
                    count += 1
        return count

    def display(self):
        """ using this only for debugging purposes"""
        print("\nliving_space ", self.living_space_dict)
        print("office_dict", self.office_dict)
        print("staff_list", self.staff_list)
        print("fellow_list", self.fellow_list)
        print("unallocate_list", self.unallocated_list)
        print("unallocated_living_list", self.unallocated_living_list, "\n")

    def search_name(self, search_parameter):
        """" Task1: Takes in a str name of any object and finds the object associated with that string"""

        if len(re.findall('\S+', search_parameter)) < 2:
            if search_parameter in self.living_space_dict:
                return "LivingSpace"
            elif search_parameter in self.office_dict:
                return "Office"
        elif len(re.findall('\S+', search_parameter)) >= 2:
            for i in self.unallocated_list:
                if i.person_name == search_parameter:
                    return i.get_type
            for i in self.fellow_list:
                if i.person_name == search_parameter:
                    return i.get_type
            for i in self.staff_list:
                if i.person_name == search_parameter:
                    return i.get_type
        return False

    def get_all_ids(self):
        """ retrieve all dictionaries that store people with ids an returns a list containing the ids"""
        person_ids_list = []
        for obj_index in self.fellow_list:
            person_ids_list.append(obj_index.person_id)
        for obj_index in self.staff_list:
            person_ids_list.append(obj_index.person_id)

        return person_ids_list

    def id_is_present(self, person_id):
        """ retrieve the all ids list"""
        # then checks if the parsed in id is present and then returns True or False
        all_ids = self.get_all_ids()
        if person_id in all_ids:
            return False
        else:
            return True

    def retrieve_person_by_id(self, person_id):
        """ Task2: Thought: have a function that can retrieve a person object when only given either the person's id
         or the person's name"""
        for person in self.fellow_list:
            if person.person_id == person_id:
                return person
        for person in self.staff_list:
            if person.person_id == person_id:
                return person
        return "no one was found with the id: " + person_id

    def retrieve_room(self, person_id):
        """Thought: to return a rooms information from a person_id """
        # so first retrieve the person name through its person object
        # then use the person name to identify the name of the office in which the name is listed in the occupants
        person_obj = self.retrieve_person_by_id(person_id)
        person_name = person_obj.person_name
        #now we use the name to get the room
        for office in self.office_dict.keys():
            if person_name in self.office_dict[office]:
                return [office, "office", person_name]
        for space in self.living_space_dict.keys():
            if person_name in self.living_space_dict[space]:
                return [space, "living_space", person_name]
        #returns a list of the room name and its type; its an index in the respective dictionary

    def view_person_id(self):
        """Seeing that ids are assigned by the system i thought it wise to include a function that lists
        a person and his/her id"""
        # for person in fellow and staff list, format string output, first column as name and second as id
        for person in self.fellow_list:
            print(person.person_name, ": ", person.person_id)
        for person in self.staff_list:
            print(person.person_name, ": ", person.person_id)



        """                                     NOTES
            CONSIDERATIONS:
                1 the reallocate person should have also been used to allocate unallocated persons to a room.
                2 i also think that the os.path module can help simplify on the functionality of testing to see
                if a certain file is existent.
                3 using mock module to simulate a user's input for successful testing --> still very allusive
                4 the add_person maybe can have a fourth parameter that takes in a person's id => the problem
                    is that if we say that a person can be assigned an id after their objects are initialised then
                    that would mean that we are not fully initialising our objects.
                    """