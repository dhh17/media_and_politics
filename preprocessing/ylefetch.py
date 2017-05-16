# ylefetch.py
#
# A script that downloads articles from the Yle API with search keywords
# loaded from a given file (topics.txt, one keyword per line).
#
# The result is stored as CSV (articles-
#
# Requires the requests library and Python 2.7 or 3.5 or higher.


from __future__ import print_function

import argparse
import csv
import json
import requests

yle_query_template = "https://articles.api.yle.fi/v2/articles.json?app_id={app_id}&app_key={app_key}&limit={l}&offset={o}&q={q}"
include_paragraphs_types = ['text', 'heading', 'quote']

default_topics_path = "topics.txt"
default_output_path = "articles-yle.csv"


def fetch_articles(app_id, app_key, topics, limit=1000):
    # surround each topic with quotes so that multi-word search terms
    # get treated properly in the query string
    topics = ['"{t}"'.format(t=t) for t in topics]

    responses = []
    done = False
    offset = 0
    while not done:
        query = yle_query_template.format(app_id=app_id,
                                          app_key=app_key,
                                          l=limit,
                                          o=offset,
                                          q=" OR ".join(topics))
        print(query)
        resp = requests.get(query)
        response_content = resp.text
        responses.append(response_content)

        parsed = json.loads(response_content)
        count = parsed['meta']['count']
        if count < limit:
            done = True
        offset += count

    articles = []
    for r in responses:
        tree = json.loads(r)
        for article in tree['data']:
            article = article_from_json(article)
            articles.append(article)

    return articles


def article_from_json(article_json):
    id = article_json['id']
    date = article_json['datePublished']
    publisher = article_json['publisher']['name']
    headline = article_json['headline']['full']
    authors = ",".join([author['name'] for author in article_json.get('authors', [])])
    language = article_json['language']
    url = article_json['url']['full']

    content = article_json.get('content', [])
    fulltext = "\n".join(
        [paragraph['text'].strip() for paragraph in content if paragraph.get('type') in include_paragraphs_types]
    )

    article = {
        "article_id": id,
        "date_published": date,
        "publisher": publisher,
        "headline": headline,
        "authors": authors,
        "language": language,
        "url": url,
        "text": fulltext
    }

    return article


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("app_id")
    parser.add_argument("app_key")
    parser.add_argument("-t", "--topics-file", dest="topics_path", default=default_topics_path,
                        help="path to the file containing a list of topics, one topic per line")
    parser.add_argument("-o", "--output-file", dest="output_path", default=default_output_path,
                        help="path of the output CSV file")
    return parser


def main():
    argparser = get_arg_parser()
    args = argparser.parse_args()

    app_id = args.app_id
    app_key = args.app_key
    topics_path = args.topics_path
    output_path = args.output_path

    with open(topics_path, "r") as f:
        topics = f.read().split("\n")

    articles = fetch_articles(app_id, app_key, topics)

    article_fieldnames = ['article_id', 'date_published', 'publisher', 'headline',
                          'authors', 'language', 'url', 'text']

    with open(output_path, "w") as f:
        writer = csv.DictWriter(f, article_fieldnames)
        writer.writeheader()
        writer.writerows(articles)


if __name__ == "__main__":
    main()
