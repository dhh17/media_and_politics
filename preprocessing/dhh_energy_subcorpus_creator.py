"""
DHH17 Media Group

Yle energy subcorpus creator.

Creates a Yle energy subcorpus from the article IDs queried through the Octavo API matching to the wanted lemmas.

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


def main():

    # A file containing all wanted article IDs in separate lines.
    energy_file = 'energy-yle-article-ids.txt'
    destination = ""
    source = ""
    file_ids = read(energy_file)

    for file_id in file_ids:
        destination = "/dhh17/yle_energy_subcorpus/" + file_id + ".json"
        source = "/dhh17/yle2017/yle2017_analyzed/" + file_id[-1] + "/" + file_id[-2] + "/" + file_id + ".json"
        print(source)
        print(destination)
        try:
            copyfile(source, destination)
        except IOError:
            print("Error in copying source file " + source + " to " + destination)


main()