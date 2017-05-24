"""
DHH17 Media Group

Yle migration subcorpus creator.

Creates a Yle migration subcorpus from article IDs queried through the Octavo API matching to the wanted lemmas.

Author: Kari Lajunen
"""

from shutil import copyfile


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


def get_file_ids(lines):
    """
    Returns an id list of the article IDs found from the given lines.
    :param lines: Lines returned by Octavo API query for the searched best lemmas.
    :return: An ID list of the article IDs found from the given lines.
    """

    # Here is an example snippet from a query result for the search "best lemma starting with "maahantulija*".
    # The article IDs are taken from the similar input line format.
    """"{"queryMetadata":{"parameters":{"method":"search","termVector":false,
    "query":"<ARTICLE§BL=maahantulija*§ARTICLE>","minScore":0,"maxDocs":50000,"pretty":false,"limit":-1,"sumScaling":
    "TTF","fields":["articleID"],"returnMatches":false,"returnNorms":false,"ctv_query":null,"ctv_minScore":0,
    "r_termTransformer":null,"r_termFilter":null,"r_localScaling":"ABSOLUTE","r_minTotalTermFreq":1,
    "r_maxTotalTermFreq":9223372036854775807,"r_minDocFreq":1,"r_maxDocFreq":2147483647,"r_minFreqInDoc":1,
    "r_maxFreqInDoc":9223372036854775807,"r_minTermLength":1,"r_maxTermLength":2147483647,"r_sumScaling":"TTF",
    "r_minSumFreq":1,"r_maxSumFreq":2147483647,"r_limit":20,"r_mdsDimensions":0,"r_distance":"COSINE"},
    "index":{"name":"YLE","version":"1.0"},"octavoVersion":"1.1.7","timeTakenMS":4},"results":{"total":359,
    "docs":[{"articleID":"20-155686","score":1},{"articleID":"20-171328","score":1},{"articleID":"20-173116","score":1},
    {"articleID":"20-177383","score":1},{"articleID":"20-185722","score":1},{"articleID":"20-30444","score":1},
    {"articleID":"20-31397","score":1},{"articleID":"20-74256","score":1},{"articleID":"3-5053741","score":1},
    {"articleID":"3-5062110","score":1},{"articleID":"3-5087557","score":1},{"articleID":"3-5089790","score":1},
    {"articleID":"3-5102418","score":1},{"articleID":"3-5103829","score":1},{"articleID":"3-5111999","score":1},
    {"articleID":"3-5112901", ..."""

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
            # ID starts right after {"articleID":" --> index = +14 and ends just before the comma (,) --> end_index - 1.
            id_list.append(line[last_found+14: end_index-1])

    return id_list


def main():

    # Files for the stored query results for the following queries:
    #
    # https://vm0824.kaj.pouta.csc.fi/octavo/yle/search?query=%3CARTICLE%C2%A7BL=ihminenkauppa*%C2%A7ARTICLE%3E&field=articleID&limit=-1
    # https://vm0824.kaj.pouta.csc.fi/octavo/yle/search?query=%3CARTICLE%C2%A7BL=karkottaa*%C2%A7ARTICLE%3E&field=articleID&limit=-1
    # https://vm0824.kaj.pouta.csc.fi/octavo/yle/search?query=%3CARTICLE%C2%A7BL=karkottaminen*%C2%A7ARTICLE%3E&field=articleID&limit=-1
    # https://vm0824.kaj.pouta.csc.fi/octavo/yle/search?query=%3CARTICLE%C2%A7BL=kerj%C3%A4%C3%A4minen*%C2%A7ARTICLE%3E&field=articleID&limit=-1
    # https://vm0824.kaj.pouta.csc.fi/octavo/yle/search?query=%3CARTICLE%C2%A7BL=kiinti%C3%B6pakolainen*%C2%A7ARTICLE%3E&field=articleID&limit=-1
    # https://vm0824.kaj.pouta.csc.fi/octavo/yle/search?query=%3CARTICLE%C2%A7BL=kotouttaa*%C2%A7ARTICLE%3E&field=articleID&limit=-1
    # https://vm0824.kaj.pouta.csc.fi/octavo/yle/search?query=%3CARTICLE%C2%A7BL=kotouttaminen*%C2%A7ARTICLE%3E&field=articleID&limit=-1
    # https://vm0824.kaj.pouta.csc.fi/octavo/yle/search?query=%3CARTICLE%C2%A7BL=k%C3%A4%C3%A4nnytt%C3%A4%C3%A4*%C2%A7ARTICLE%3E&field=articleID&limit=-1
    # https://vm0824.kaj.pouta.csc.fi/octavo/yle/search?query=%3CARTICLE%C2%A7BL=maahanmuuttaja*%C2%A7ARTICLE%3E&field=articleID&limit=-1
    # https://vm0824.kaj.pouta.csc.fi/octavo/yle/search?query=%3CARTICLE%C2%A7BL=maahanmuutto*%C2%A7ARTICLE%3E&field=articleID&limit=-1
    # https://vm0824.kaj.pouta.csc.fi/octavo/yle/search?query=%3CARTICLE%C2%A7BL=maahanpyrkij%C3%A4*%C2%A7ARTICLE%3E&field=articleID&limit=-1
    # https://vm0824.kaj.pouta.csc.fi/octavo/yle/search?query=%3CARTICLE%C2%A7BL=maahantulija*%C2%A7ARTICLE%3E&field=articleID&limit=-1
    # https://vm0824.kaj.pouta.csc.fi/octavo/yle/search?query=%3CARTICLE%C2%A7BL=oleskelulupa*%C2%A7ARTICLE%3E&field=articleID&limit=-1
    # https://vm0824.kaj.pouta.csc.fi/octavo/yle/search?query=%3CARTICLE%C2%A7BL=pakolainen*%C2%A7ARTICLE%3E&field=articleID&limit=-1
    # https://vm0824.kaj.pouta.csc.fi/octavo/yle/search?query=%3CARTICLE%C2%A7BL=pakolainenkriisi*%C2%A7ARTICLE%3E&field=articleID&limit=-1
    # https://vm0824.kaj.pouta.csc.fi/octavo/yle/search?query=%3CARTICLE%C2%A7BL=perheyhdist%C3%A4minen*%C2%A7ARTICLE%3E&field=articleID&limit=-1
    # https://vm0824.kaj.pouta.csc.fi/octavo/yle/search?query=%3CARTICLE%C2%A7BL=rasismi*%C2%A7ARTICLE%3E&field=articleID&limit=-1
    # https://vm0824.kaj.pouta.csc.fi/octavo/yle/search?query=%3CARTICLE%C2%A7BL=turvapaikanhakija*%C2%A7ARTICLE%3E&field=articleID&limit=-1
    # https://vm0824.kaj.pouta.csc.fi/octavo/yle/search?query=%3CARTICLE%C2%A7BL=turvapaikka*%C2%A7ARTICLE%3E&field=articleID&limit=-1
    # https://vm0824.kaj.pouta.csc.fi/octavo/yle/search?query=%3CARTICLE%C2%A7BL=vastaanottokeskus*%C2%A7ARTICLE%3E&field=articleID&limit=-1
    #
    # The following Omorfi/LAS rare lemma formats were fixed for the queries:
    # ihmiskauppa --> ihminenkauppa
    # käännyttäminen --> käännyttää
    # pakolaiskriisi --> pakolainenkriisi
    # perheenyhdistäminen --> perheyhdistäminen
    #
    migration_files = ['ihmiskauppa.txt', 'karkottaminen.txt',
                       'kerjääminen.txt', 'kiintiöpakolainen.txt',
                       'kiintiöpakolainen.txt', 'kotouttaa.txt',
                       'kotouttaminen.txt', 'käännyttää.txt',
                       'maahanmuuttaja.txt', 'maahanmuutto.txt',
                       'maahanpyrkijä.txt', 'maahantulija.txt',
                       'pakolainen.txt', 'perheenyhdistäminen.txt',
                       'rasismi.txt', 'turvapaikanhakija.txt',
                       'turvapaikka.txt', 'vastaanottokeskus.txt']

    destination = ""
    source = ""
    # Copy the chosen files (based on their file IDs) from 'source' to 'destination'.
    for migration_file in migration_files:
        print(migration_file, get_file_ids(read(migration_file)))
        file_ids = get_file_ids(read(migration_file))
        for file_id in file_ids:
            destination = "/dhh17/yle_migration_subcorpus/" + file_id + ".json"
            # Paths for the files in server are /dhh17/yle2017/yle2017_analyzed/i/j/ where i and j have values from 0
            # to 9 based on the two last digits of the id of the article / file name.
            # For example, a file with an ID / file name 20-123456.json would be located in
            # /dhh17/yle2017/yle2017_analyzed/6/5/.
            source = "/dhh17/yle2017/yle2017_analyzed/" + file_id[-1] + "/" + file_id[-2] + "/" + file_id + ".json"
            print(source)
            print(destination)
            try:
               copyfile(source, destination)
            except IOError:
                print("Error in copying source file " + source + " to " + destination)


main()