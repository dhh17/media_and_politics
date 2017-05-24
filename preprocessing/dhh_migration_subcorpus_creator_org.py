"""
DHH17 Media Group

Yle migration subcorpus creator.

Creates a Yle migration subcorpus from the article IDs picked up based on the wanted lemmas by
dhh_migration_subcorpus_file_picker.py.

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

    # Files containing file names / article IDs matching with the lemma and picked up by the
    # dhh_migration_subcorpus_file_picker.py
    migration_files = ['yle2017_migration_käännyttää.txt', 'yle2017_migration_karkottaa.txt',
                       'yle2017_migration_karkottaminen.txt', 'yle2017_migration_kerjääminen.txt',
                       'yle2017_migration_kiintiöpakolainen.txt', 'yle2017_migration_kotouttaa.txt',
                       'yle2017_migration_kotouttaminen.txt', 'yle2017_migration_maahanmuuttaja.txt',
                       'yle2017_migration_maahanmuutto.txt', 'yle2017_migration_maahanpyrkijä.txt',
                       'yle2017_migration_maahantulija.txt', 'yle2017_migration_oleskelulupa.txt',
                       'yle2017_migration_pakolainen.txt', 'yle2017_migration_pakolaiskriisi.txt',
                       'yle2017_migration_rasismi.txt', 'yle2017_migration_turvapaikanhakija.txt',
                       'yle2017_migration_turvapaikka.txt', 'yle2017_migration_vastaanottokeskus.txt']

    destination = ""
    source = ""
    for migration_file in migration_files:
        json_file_names = read(migration_file)
        for json_file_name in json_file_names:
            destination = "/dhh17/yle_migration/" + json_file_name
            # two last digits of the id are folder names
            source = "/dhh17/yle2017/yle2017_analyzed/" + json_file_name[-6] + "/" + json_file_name[-7] + "/" + \
                     json_file_name
            print(source)
            print(destination)
            try:
                copyfile(source, destination)
            except IOError:
                print("Error in copying source file " + source + " to " + destination)


main()