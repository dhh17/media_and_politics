"""
DHH17 Media Group

Yle gender subcorpus creator.

Creates a Yle gender subcorpus from the article IDs queried through the Octavo API matching to the wanted lemmas.

NB! No idea how the article IDs for this subcorpus were chosen and what was the idea for creating this subcorpus and
not using the whole corpus for the gender investigation.

Author: Kari Lajunen
"""
from shutil import copyfile


def read(filepath):
    lines = []
    try:
        file = open(filepath, "r", encoding='utf-8')  # encoding is needed for Windows

        line = file.readline()
        while line != "":
            lines.append(line)
            line = file.readline()
        file.close()
    except OSError:
        print("Error reading file.")

    # do not include the line feed "\n"
    return [line[:-1] for line in lines]


def get_file_ids(lines):

    id_list = []
    for line in lines:
        last_found = -1  # Begin at -1 so the next position to search from is 0
        end_index = -1
        while True:
            # Find next index of substring, by starting after its last known position
            last_found = line.find("{\"articleID\":\"", last_found + 1)
            end_index = line.find(",", last_found + 1)
            if last_found == -1:
                break  # All occurrences have been found
            id_list.append(line[last_found+14: end_index-1])

    return id_list


def main():

    # A file containing all wanted article IDs in separate lines.
    gender_file = "gender-yle-article-ids.txt"
    destination = ""
    source = ""

    file_ids = read(gender_file)
    for file_id in file_ids:
        destination = "/dhh17/yle_gender_subcorpus/" + file_id + ".json"
        source = "/dhh17/yle2017/yle2017_analyzed/" + file_id[-1] + "/" + file_id[-2] + "/" + file_id + ".json"
        print(source)
        print(destination)
        try:
            copyfile(source, destination)
        except IOError:
            print("Error in copying source file " + source + " to " + destination)


main()