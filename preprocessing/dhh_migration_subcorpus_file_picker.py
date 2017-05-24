"""
DHH17 Media Group

Yle migration subcorpus file picker.

Creates a subcorpus file list from the original preprocessed Yle json files stored in the server in
/dhh17/yle2017/yle2017_analyzed/i/j/ where i and j have values from 0 to 9 based on the two last digits of the id of
the article / file name. For example, a file with an id / file name 20-123456.json would be located in
/dhh17/yle2017/yle2017_analyzed/6/5/.

Goes through all the files in /dhh17/yle2017/yle2017_analyzed/* and picks all the unique lemmas which exist in those
files. Then compares if any of our wanted_list lemmas occur in the lemma list of that certain file. If exists, then
the file is picked.

NB! This script checks all the lemmas, not just "best match lemmas". The result is almost the same as if all the
"best match lemmas starting with <wanted_lemma>" would be chosen through the Octavo API.

Please change the hard coded wanted_list and output file name to be read from a file if you want to change
this code to be more generic.

WARNING: The execution of this program for the Yle article files from 1997 to 2017 stored in the server takes several
         hours.

Author: Kari Lajunen
"""
from collections import defaultdict
from os import listdir, write
from os.path import isfile, join


def read(filepath):
    """
    Reads the file in a given path and returns a list of lines.
    :param filepath: Path and file name to be read.
    :return: A list of lines in the given file.
    """
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

    return lines


def get_lemmas(file_lines):
    """
    Returns a list of unique lemmas found in the given lines of a file.
    :param file_lines: A list of the lines in a file.
    :return: A list of unique lemmas found in the given lines of a file.
    """
    lemmas = set()
    for line in file_lines:
        # Let's pick the actual lemmas from the lemma lines.
        # An example of a lemma line: "lemma":"puolue",
        # --> start index is +2 after the :
        # --> end index is -3
        if "\"lemma\":" in line:
            lemmas.add(line[line.index(":")+2:-3].lower())

    return list(lemmas)


def write(output_file_name, selected_files):
    """
    write(output_file, output_file_name) writes the output given as a parameter to the given output file.
    :param selected_files: The selected files which contain a wanted lemma.
    :param output_file_name: The name of the output file.
    :return:
    """
    try:
        output_file = open(output_file_name, "w")
        for filename in selected_files:
            output_file.write(filename + "\n")
        output_file.close()
    except OSError:
        print(output_file_name + ": Error in writing output: " + filename)
    except UnicodeEncodeError:
        print(output_file_name + ": UnicodeEncodeError in writing output:\n" + filename)


def main():

    wanted_list = ['maahanmuutto', 'turvapaikanhakija', 'käännyttäminen', 'käännyttää', 'karkottaa',
                   'karkottaminen', 'kiintiöpakolainen', 'kotouttaa', 'kotouttaminen', 'maahanmuuttaja',
                   'maahanpyrkijä', 'maahantulija', 'pakolainen', 'rasismi',
                   'turvapaikka', 'vastaanottokeskus', 'pakolaiskriisi', 'ihmiskauppa', 'perheenyhdistäminen',
                   'kerjääminen', 'oleskelulupa']

    selected_files = []
    selected_files_paths = []
    file_count = 0

    # Let's store all the paths which exist in the server.
    paths = []
    for i in range(0, 10):
        for j in range(0, 10):
            paths.append("/dhh17/yle2017/yle2017_analyzed/" + str(i) + "/" + str(j) + "/")

    print(paths)

    # Let's store all the file names with its path to a list of tuples: (<path>, <list of files>).
    # Let's count the files at the same time.
    all_files = []
    for path in paths:
        files = [file for file in listdir(path) if isfile(join(path, file))]
        all_files.append((path, files))
        file_count += len(files)

    #print(all_files)

    # Let's pick all the files which contain any of the lemmas in wanted_list and store them with a matching lemma.
    for path, files in all_files:
        for file in files:
            print(path + file)
            lemmas = get_lemmas(read(path + file))
            for lemma in lemmas:
                if lemma in wanted_list:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!      " + lemma +
                          "      " +
                          "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    selected_files.append((file, lemma))
                    selected_files_paths.append(path + file)

    print("file count:", file_count)

    # Let's put a list of the picked files for matching key lemma file name to a default dictionary.
    wanted_dic = defaultdict(list)
    for wanted in wanted_list:
        for filename, lemma in selected_files:
            if wanted == lemma:
                wanted_dic["yle2017_migration_" + wanted + ".txt"].append(filename)

    # Finally, let's write the selected file names to the output files.
    for output_file_name, selected_filenames in wanted_dic.items():
        write(output_file_name, selected_filenames)


main()
