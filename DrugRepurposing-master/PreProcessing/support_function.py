import os.path


def save_list_triple(file_name, lista, first_line=""):
    with open(file_name, mode='w+') as file:
        if first_line is not "":
            file.write(first_line + "\n")
        for element in lista:
            line = str(element)
            file.write(line)
            file.write('\n')


def save_dictionary(file_name, dictionary, delimiter='\t', first_line=''):
    with open(file_name, mode='w+') as file:
        file.write(str(first_line) + "\n")
        for key in dictionary:
            text = str(key) + delimiter + str(dictionary[key])
            file.write(text)
            file.write('\n')


def check_dir(file_name):
    path = file_name[:file_name.rfind("/")]
    return os.path.isdir(path)


def true_xor(*args):
    return sum(bool(x) for x in args) == 1


def save_set(my_set, path):
    import csv

    with open(path, "w") as file:
        file.write(str(len(my_set)) + "\n")
        wr = csv.writer(file, delimiter="\n")
        wr.writerow(list(my_set))

