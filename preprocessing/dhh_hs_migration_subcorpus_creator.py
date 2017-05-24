"""
DHH17 Media Group

Helsingin Sanomat migration subcorpus creator.

Creates a Helsingin Sanomat migration subcorpus from the article IDs queried through the Octavo API matching to the
wanted lemmas.

NB! Contrary to the Yle files, HS files are located in the server in paths /dhh17/hs/hs_analyzed/x/y/ where x and y have
nothing to do with the article ID.
--> All locations need to be gone through to find a matching file.
However, x and y are digits between 0 and 9 just like in Yle article paths.

Author: Kari Lajunen
"""

from shutil import copyfile
from pathlib import Path


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

    migration_files = ['migration-hs-subcorpus-ids.txt']
    destination = ""
    source = ""

    for migration_file in migration_files:
        file_ids = read(migration_file)
        for file_id in file_ids:
            destination = "/dhh17/hs_migration_subcorpus/" + file_id + ".analysis.json"

            for i in range(0, 10):
                for j in range(0, 10):
                    source = "/dhh17/hs/hs_analyzed/" + str(i) + "/" + str(j) + "/" + file_id + ".analysis.json"
                    my_file = Path(source)
                    if my_file.is_file():
                        # the file exists
                        print(source)
                        print(destination)
                        try:
                            copyfile(source, destination)
                        except IOError:
                            print("Error in copying source file " + source + " to " + destination)


main()