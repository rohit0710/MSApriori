import re
from test.test_tools.test_pindent import PindentTests

## MS-Apriori
phase = 0
##READ THE INPUT FILE AND PROCESS THE INPUT.
# Read the inputfile.txt
input_data_file = open("E:\Python projects\Data Science\MS-Apriori\i2.txt", 'r')

# Read the input file and and split line by line.
transaction_data_list = input_data_file.read().strip().split("\n")

# Strip the unnecessary curly brackets and store it back in the list
transaction_data_list = [items.strip('{}') for items in transaction_data_list]

# INITIALISATIONS
support_difference_constraint = 1.
cannot_be_together = []
must_have = []

# READ THE PARAMETER FILE AND CREATE A DICTIONARY OF MIS OF EACH ITEM.
parameter_file = open('E:\Python projects\Data Science\MS-Apriori\p2.txt', 'r')

min_item_support_dict = {}
# Read the parameter-file and split line by line.
parameter_list = parameter_file.read().strip().split("\n")
for parameter in parameter_list:
    # Check if first 3 characters are MIS and extract the item name and minimium item support of the item.
    if parameter[:3] == "MIS":
        parameter = parameter.strip().replace(" ", "").split("=")
        try:
            # Using Regular Expression we extract everything between the two brackets
            item = re.search('\((.+?)\)', parameter[0]).group(1)
        except AttributeError:
            # Exception handling if there was no brackets or no string inbetween the brackets.
            item = ''
        # print("found =", item)
        min_item_support_dict[item] = float(parameter[1])

    elif parameter[:3] == "SDC":
        # check if parameter is mentioning about SDC and assign it to float.
        parameter = parameter.strip().replace(" ", "").split("=")
        support_difference_constraint = float(parameter[1])

    # Cannot be together list is made.
    elif "cannot_be_together" in parameter.lower():
        parameter = parameter.strip().replace(" ", "").split(":")
        # cannot_be_together = parameter[1].strip().replace(" ","").replace("},{",'};{').split(';')
        cannot_be_together = re.split(r'''(?:(?<=})|(?<=} )),(?= {|{)''', parameter[1])
        cannot_be_together = [i.strip() for i in cannot_be_together]

    # Must have list is made
    elif "must-have" in parameter.lower():
        parameter = parameter.strip().split(":")
        must_have = parameter[1].strip().split(" or ")


# used to splot the string on a separator string given a string and a separator.
def split_string(string, separator):
    string = re.split(separator, string)
    return [i.strip() for i in string]


# Get the support count of the items from the transactions
items_count_dict = dict()
for each_transaction in transaction_data_list:
    transaction_list_temp = split_string(each_transaction, ', |,')
    for each_item in transaction_list_temp:
        if (each_item) in items_count_dict:
            items_count_dict[each_item] += 1
        else:
            items_count_dict[each_item] = 1

# Contains the items which is sorted in ascending order of their MIS values from the minimum_item_support_dict.
sorted_mis_list = sorted(min_item_support_dict, key=min_item_support_dict.__getitem__)

# Initialisations
smallest_mis = 0

candidate_items_L_list = []
no_of_transactions = len(transaction_data_list)
final_frequent_itemset = dict()
tailcount_dict = dict()

for item in sorted_mis_list:
    if item in items_count_dict.keys() and (items_count_dict[item] / no_of_transactions) >= min_item_support_dict[item]:
        smallest_mis = min_item_support_dict[item]
        break
frequent_itemset_dict = dict()


def must_have_condition(final_frequent_itemset_def):
    frequent_itemset_def = dict()
    for itemset in list(final_frequent_itemset_def.keys()):
        flag = 1
        split_itemset = itemset.strip().replace(" ", "").split(",")
        for each_must_have in must_have:
            if each_must_have in split_itemset:
                flag = 1
                break
            else:
                flag = 0
        if flag == 1:
            frequent_itemset_def[itemset] = final_frequent_itemset_def[itemset]
    return frequent_itemset_def


def cannot_be_together_def(final_frequent_itemset_def):
    frequent_itemset_def = dict()
    global cannot_be_together

    # print ("PARAMETER LENGTH: ", len(final_frequent_itemset_def))
    for each_cannot_be_together in cannot_be_together:
        split_each_cannot_be_together = re.search('\{(.+?)\}', each_cannot_be_together).group(1)
        split_each_cannot_be_together = split_each_cannot_be_together.strip().replace(" ", "").split(",")
        # print("--------------------------------------------------------------------------------------------------------")
        # print("split_each_cannot_be_together", set(split_each_cannot_be_together))
        for itemset in list(final_frequent_itemset_def.keys()):
            if sorted(set(split_each_cannot_be_together)) == sorted(
                    set(itemset.strip().replace(" ", "").split(",")).intersection(set(split_each_cannot_be_together))):
                # print ("YES", itemset)
                # print("set of deleted to be",set(to_be_deleted))
                # print("cannot be together",split_each_cannot_be_together)
                del (final_frequent_itemset_def[itemset])

    # print(split_each_cannot_be_together)
    return final_frequent_itemset_def

filename = "E:\Python projects\Data Science\MS-Apriori\Output_Adarsh_RohitVC.txt"
file = open(filename, "w+")
e = 1


# Generation of candidate set. list L(as per the textbook)
for item in sorted_mis_list:
    if item in items_count_dict.keys() and (items_count_dict[item] / no_of_transactions) >= smallest_mis:
        candidate_items_L_list.append(item)
#print ("\ncandidate_items_L_list 1st Pass :",candidate_items_L_list)

# Generation of 1- itemset Frequent Itemset. (Initial Pass)
for item in candidate_items_L_list:
    if min_item_support_dict[item] <= (items_count_dict[item] / no_of_transactions):
        frequent_itemset_dict[item] = items_count_dict[item]

if len(frequent_itemset_dict) == 0:
    file.write('\nfrequent {1}-itemset(s) = 0\n\n')
    file.write('\tTotal number of frequent {1}-itemsets = 0')

# frequent_itemset_dict = must_have_condition(frequent_itemset_dict)
# print ("\nfrequent_itemset_dict 1st Pass: ",frequent_itemset_dict)
# print ("\nfrequent_itemset_dict 1st Pass: ",len(frequent_itemset_dict))
# show_output(frequent_itemset_dict)



def print_subsets2(input_name, tailcount):
    global e
    print('frequent {0}-itemset(s)\n'.format(e))
    file.write('\nfrequent {0}-itemset(s)\n'.format(e) + "\n")

    for i in range(0, len(input_name)):
        print('\t {0} : {{{1}}}'.format(list(input_name.values())[i], list(input_name.keys())[i]))
        if len(list(input_name.keys())[i]) > 1:
            print('Tailcount = {0}'.format(tailcount[list(input_name.keys())[i]]))
        file.write('\t {0} : {{{1}}}'.format(list(input_name.values())[i], list(input_name.keys())[i]) + '\n')
        file.write('Tailcount = {0}'.format(tailcount[list(input_name.keys())[i]]) + '\n')

    print("\n \t Total number of frequent {}-itemsets = {}".format(e, len(input_name)))
    file.write("\n \t Total number of frequent {}-itemsets = {}".format(e, len(input_name)) + '\n')
    # file.write('\n')
    print('\n')
    e += 1


def print_subsets(input_name):
    print("0")
    if not input_name:
        print('Total number of frequent {}-itemsets = 0')
    else:
        global e
        print('frequent {0}-itemset(s)\n'.format(e))
        file.write('frequent {0}-itemset(s)\n'.format(e) + "\n")

        for i in range(0, len(input_name)):
            print('\t {0} : {{{1}}}'.format(list(input_name.values())[i], list(input_name.keys())[i]))
            file.write('\t {0} : {{{1}}}'.format(list(input_name.values())[i], list(input_name.keys())[i]) + '\n')

        print("\n \t Total number of frequent {}-itemsets = {}".format(e, len(input_name)))
        file.write("\n \t Total number of frequent {}-itemsets = {}".format(e, len(input_name)) + '\n')
        print('\n')
        e += 1


def show_output(frequent_itemset_output):
    global cannot_be_together, must_have, tailcount_dict, phase
    if frequent_itemset_output:
        if not cannot_be_together:
            if phase == 0:
                print_subsets(must_have_condition(frequent_itemset_output))
            else:
                print_subsets2(must_have_condition(frequent_itemset_output), tailcount_dict)
        elif not must_have:
            if phase == 0:
                print_subsets((cannot_be_together_def(frequent_itemset_output)))
            else:
                print_subsets2((cannot_be_together_def(frequent_itemset_output)), tailcount_dict)
        else:
            # if phase == 0:
            #     print_subsets(((must_have_condition(cannot_be_together_def(frequent_itemset_output)))))
            # else:
            #     print_subsets2(((must_have_condition(cannot_be_together_def(frequent_itemset_output)))), tailcount_dict)
            print(must_have_condition(cannot_be_together_def(frequent_itemset_output)))

show_output(frequent_itemset_dict)


def generate_subsets(l):
    if l == []:
        return [[]]

    x = generate_subsets(l[1:])
    return x + [[l[0]] + y for y in x]


# Function to define the Generation of C2-Candidate keys.
def level2_candidate_gen(L, sdc):
    # Initialising variables and using some global variables.
    candidate_items = list()
    global no_of_transactions, items_count_dict, min_item_support_dict
    for each_item in L:
        if items_count_dict[each_item] / no_of_transactions >= min_item_support_dict[each_item]:
            for next_item in L[L.index(each_item) + 1:]:
                if items_count_dict[next_item] / no_of_transactions >= min_item_support_dict[each_item] and abs(
                                items_count_dict[next_item] - items_count_dict[each_item]) / no_of_transactions <= sdc:
                    candidate_items.append(each_item + ", " + next_item)
    print("Candidate Items 2nd Pass: ", len(candidate_items))
    return candidate_items


##Candidate Generation for k itemset other than 2
def MS_candidate_gen(candidate_gen_frequent_list, sdc):
    global sorted_mis_list, no_of_transactions, items_count_dict, min_item_support_dict
    print("MS_candidate_gen Parameter", len(candidate_gen_frequent_list))
    new_candidate_list = []
    for first_item in candidate_gen_frequent_list:
        for next_item in candidate_gen_frequent_list:
            if first_item != next_item:
                itemset_1_list = list(first_item.strip().replace(" ", "").split(","))
                itemset_2_list = list(next_item.strip().replace(" ", "").split(","))
                if itemset_1_list[:-1] == itemset_2_list[:-1]:
                    if sorted_mis_list.index(itemset_1_list[-1]) < sorted_mis_list.index(itemset_2_list[-1]) and (abs(
                                items_count_dict[itemset_1_list[-1]] - items_count_dict[
                                itemset_2_list[-1]]) / no_of_transactions) <= sdc:
                        single_candidate_temp = itemset_1_list[:-1]
                        single_candidate_temp.extend([itemset_1_list[-1], itemset_2_list[-1]])
                        # print(single_candidate_temp)
                        new_candidate_list.append(single_candidate_temp)
                        # print("new_candidate_list: ", new_candidate_list)
                        subset_list = generate_subsets(single_candidate_temp)
                        subset_list = [", ".join(i) for i in subset_list if len(i) == len(single_candidate_temp) - 1]
                        # print("Some: ",subset_list)
                        # print([i.strip().replace(" ","").split(",") for i in subset_list])
                        for s in [i.strip().replace(" ", "").split(",") for i in subset_list]:
                            if (single_candidate_temp[0] in s) or min_item_support_dict[single_candidate_temp[0]] == \
                                    min_item_support_dict[single_candidate_temp[1]]:
                                if set(subset_list) != set(candidate_gen_frequent_list).intersection(set(subset_list)):
                                    # print("Deleting :", single_candidate_temp)
                                    del new_candidate_list[-1]
                                    break
                            else:
                                break


                                # print("2. new_candidate_list: ", new_candidate_list)
                                # print("------------------------------------------------------------------------------------------------")

    print(new_candidate_list)
    return [", ".join(i) for i in new_candidate_list]


# print(frequent_itemset_dict)
# frequent_itemset_dict=must_have_condition(frequent_itemset_dict)
# print_subsets(frequent_itemset_dict)

while frequent_itemset_dict:
    phase = len(list(frequent_itemset_dict.keys())[0].replace(" ", "").split(","))
    # print("Phase: ", phase)
    if phase + 1 == 2:
        candidate_items_L_list = level2_candidate_gen(candidate_items_L_list, support_difference_constraint)
    else:
        # print(" K > 2 -------TRUE")
        candidate_items_L_list = MS_candidate_gen(list(frequent_itemset_dict.keys()), support_difference_constraint)
    print("candidate_items_L_list",len(candidate_items_L_list))
    frequent_itemset_dict.clear()
    for t in transaction_data_list:
        for c in candidate_items_L_list:
            split_candidates = c.strip().replace(", ", ",").split(",")
            split_transactions = t.strip().replace(", ", ",").split(",")
            split_candidates_1 = split_candidates[1:]
            # print("split_candidates: ",split_candidates)
            # print("split_transactions: ", split_transactions)
            if set(split_candidates) == set(split_transactions).intersection(set(split_candidates)):
                if c in frequent_itemset_dict:
                    frequent_itemset_dict[c] += 1
                else:
                    frequent_itemset_dict[c] = 1

            if set(split_candidates_1) == set(split_transactions).intersection(set(split_candidates_1)):
                if c in tailcount_dict:
                    tailcount_dict[c] += 1
                else:
                    tailcount_dict[c] = 1

    # print('Length frequent_itemset_dict = ', len(frequent_itemset_dict))
    for item_c in list(frequent_itemset_dict.keys()):
        if frequent_itemset_dict[item_c] / no_of_transactions < (
        min_item_support_dict[item_c.strip().replace(" ", "").split(",")[0]]):
            frequent_itemset_dict.pop(item_c, None)
            tailcount_dict.pop(item_c, None)
            # print('happening - %s %s'%((item_c.strip().replace(" ","").split(",")[0]),(min_item_support_dict[item_c.strip().replace(" ","").split(",")[0]])))
            # print("-------------------------------------------------------------------------------------------------------------------------------------")

    # frequent_itemset_dict = must_have_condition(frequent_itemset_dict)
    # frequent_itemset_dict = cannot_be_together_def(frequent_itemset_dict)


    if len(frequent_itemset_dict.keys()) > 0:
        final_frequent_itemset = dict(frequent_itemset_dict)

    # print("frequent_itemset_dict",frequent_itemset_dict)
    # print("final_frequent_itemset: ",final_frequent_itemset)

    # print(frequent_itemset_dict)
    show_output(frequent_itemset_dict)
    # print("-------------------------------------------------------------------------------------------------------------------------------------")
# print("\n-------------------------------------------------------------------------------------------------------------------------------------")
# print("Transaction_data_List ", transaction_data_list)
# #print("parameter_list ",parameter_list)
# print("min_item_support_dict = ",min_item_support_dict)
# print("SDC = ", support_difference_constraint)
# print("cannot_be_together = ", cannot_be_together)
# print("must-have ", must_have)
# print("items_count_dict = ", items_count_dict )
# print("sorted_mis_list = ",sorted_mis_list)
# print("smallest_mis= ",smallest_mis)
# print('no_of_transactions = ', no_of_transactions)
# print('candidate_items_L_list = ',candidate_items_L_list)
# print('frequent_itemset_dict = ', final_frequent_itemset)
# print('Length frequent_itemset_dict = ', len(final_frequent_itemset))
file.close()