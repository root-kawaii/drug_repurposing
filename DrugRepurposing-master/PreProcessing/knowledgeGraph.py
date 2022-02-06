import os.path
import random
import argparse

from support_function import save_dictionary, save_set


def knowledge_graph(dataset_folder, final_path, perc_train, perc_valid, delimiter='\t'):
    """
    Given a folder, it takes all the final that should be in a format <head,relation,tail> and create a unique KG.
    It creates relation2id file, entity2id file and the train, test and validation set.
    :param dataset_folder: the folder containing the Triple files
    :param final_path: the folder where save the KG
    :param delimiter: the delimiter for the KG
    :param perc_train: the % of triple for train
    :param perc_valid: the % of triple for validation
    """
    # Check existence of directories
    if os.path.isdir(dataset_folder):
        list_files = [dataset_folder + i for i in os.listdir(dataset_folder)]
    else:
        raise ValueError("DataSet Directory Not Exist")

    if not os.path.isdir(final_path):
        raise ValueError("Final Directory Not Exist")

    # Train File
    train_path = final_path + "train2id.txt"
    if os.path.isfile(train_path):
        os.remove(train_path)

    # Validation File
    valid_path = final_path + "valid2id.txt"
    if os.path.isfile(valid_path):
        os.remove(valid_path)

    # Test File
    test_path = final_path + "test2id.txt"
    if os.path.isfile(test_path):
        os.remove(test_path)

    # Check % division of DataSet
    if (perc_train + perc_valid) >= 1:
        raise ValueError("% Train or Validation or Test set Not valid")

    # Set Intervals
    range_random = 100
    perc_train = round(perc_train * range_random, 0)
    perc_valid = round(perc_valid * range_random, 0)
    # perc_test = 100 - perc_train - perc_valid

    # Init Variables
    entity_dictionary = {}
    relation_dictionary = {}

    # Info KG
    count_relation = 0
    count_entity = 0
    count_triple = 0
    count_train = 0
    count_test = 0
    count_valid = 0

    # Sets
    set_train = set([])
    set_valid = set([])
    set_test = set([])

    # Sets
    set_train_treat = set([])
    set_test_treat = set([])
    set_valid_treat = set([])


    # Start reading file in directory "dataset"
    for address in list_files:
        print("Reading: ", address, end='')
        with open(address) as file:
            for line in file:
                treat_flag = False

                if line.startswith('#'):
                    continue
                sp_line = line.strip('\n').split('\t')

                try:
                    head = sp_line[0]
                    relation = sp_line[1]
                    tail = sp_line[2]
                except IndexError:
                    continue

                # Check if an entity or a relation has already an ID, otherwise create it.
                if head not in entity_dictionary:
                    id_entity = count_entity
                    entity_dictionary[head] = id_entity
                    count_entity += 1
                if tail not in entity_dictionary:
                    id_entity = count_entity
                    entity_dictionary[tail] = id_entity
                    count_entity += 1
                if relation not in relation_dictionary:
                    id_entity = count_relation
                    relation_dictionary[relation] = id_entity
                    count_relation += 1

                if relation == "TREAT":
                    treat_flag = True

                # Create Train, Valid, Test set according to %
                random_number = random.randint(0, range_random - 1)

                line_to_write = str(entity_dictionary[head]) + delimiter + \
                                str(entity_dictionary[tail]) + delimiter + \
                                str(relation_dictionary[relation])

                count_triple += 1

                if random_number < perc_train:
                    set_train.add(line_to_write)
                    set_train_treat.add(line_to_write) if treat_flag else 0
                elif perc_train <= random_number < perc_train + perc_valid:
                    set_valid.add(line_to_write)
                    set_valid_treat.add(line_to_write) if treat_flag else 0
                elif random_number >= perc_train + perc_valid:
                    set_test.add(line_to_write)
                    set_test_treat.add(line_to_write) if treat_flag else 0


        file.close()
        print("\rReading: ", address, " ...ok")

    # Print Numerical result
    print("# Entity: ", f"{count_entity:,}")
    print("# Relation: ", f"{count_relation:,}")
    print("# Triple: ", f"{count_triple:,}")
    print("# Triple Unique: ", f"{len(set_train) + len(set_valid) + len(set_test):,}")
    print("# Train: ", f"{len(set_train):,}")
    print("# Valid: ", f"{len(set_valid):,}")
    print("# Test: ", f"{len(set_test):,}")
    print("# Drug-Disease: ", f"{len(set_test_treat) + len(set_test_treat) + len(set_valid_treat):,}")

    relation_path = final_path + "relation2id.txt"
    entity_path = final_path + "entity2id.txt"

    # Save Dictionaries
    save_dictionary(relation_path, relation_dictionary, "\t", count_relation)
    save_dictionary(entity_path, entity_dictionary, "\t", count_entity)

    # Save sets
    save_set(set_train, train_path)
    save_set(set_test, test_path)
    save_set(set_valid, valid_path)

    save_set(set_test_treat, final_path + "treat_test")
    save_set(set_valid_treat, final_path + "treat_valid")
    save_set(set_train_treat, final_path + "treat_train")


def main(args):
    dataset_folder = args["path"]
    final_path = args["final"]
    train = float(args["train"])
    valid = float(args["valid"])

    knowledge_graph(dataset_folder, final_path, train, valid)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="KnowledgeGraph Embedding Creator")
    parser.add_argument("-P", "--path", required=True, help="Folder with Triple")
    parser.add_argument("-F", "--final", required=True, help="Path folder of KG")
    parser.add_argument("-T", "--train", required=True, help="% Train")
    parser.add_argument("-V", "--valid", required=True, help="& Validation")

    main(vars(parser.parse_args()))
