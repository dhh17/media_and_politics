# ylefetch.py
#
# A script that downloads articles from the Yle API with search keywords
# loaded from a given file (default: topics.txt, one keyword per line).
#
# The result is stored as CSV (default: articles-yle.csv).
#
# Requires the requests library and Python 2.7 or 3.5 or higher.
#
# Run with --help for more details.


from __future__ import print_function

import argparse
import csv
import json
import requests

yle_query_template = "https://articles.api.yle.fi/v2/articles.json?app_id={app_id}&app_key={app_key}&limit={l}&offset={o}&q={q}"
lemmatizer_url = "http://demo.seco.tkk.fi/las/baseform"
include_paragraphs_types = ['text', 'heading', 'quote']

default_topics_path = "topics.txt"
default_output_path = "articles-yle.csv"


def fetch_articles(app_id, app_key, topics, lemmatize=False, limit=1000):
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
            article = article_from_json(article, lemmatize)
            articles.append(article)

    return articles


def article_from_json(article_json, lemmatize=False):
    id = article_json['id']
    date = article_json['datePublished']
    publisher = article_json['publisher']['name']
    headline = article_json['headline']['full']
    authors = ",".join([author['name'] for author in article_json.get('authors', [])])
    language = article_json['language']
    url = article_json['url']['full']

    # fix the language code for Swedish (ISO-639-1 standard is 'sv', Yle API sometimes gives 'se')
    if language == 'se':
        language = 'sv'

    content = article_json.get('content', [])
    fulltext = "\n".join(
        [paragraph['text'].strip() for paragraph in content if paragraph.get('type') in include_paragraphs_types]
    )

    if lemmatize:
        lemmatized = lemmatize_remote(fulltext, language)
    else:
        lemmatized = ""

    article = {
        "article_id": id,
        "date_published": date,
        "publisher": publisher,
        "headline": headline,
        "authors": authors,
        "language": language,
        "url": url,
        "text": fulltext,
        "text_l": lemmatized
    }

    return article


def lemmatize_remote(text, locale):
    print("Lemmatizing through the LAS web service")
    params = {'text': text, 'locale': locale}
    baseform_resp = requests.post(lemmatizer_url, data=params)
    if baseform_resp.status_code == 200 and baseform_resp.text:
        lemmatized = json.loads(baseform_resp.text)
    else:
        lemmatized = text
    return lemmatized


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("app_id")
    parser.add_argument("app_key")
    parser.add_argument("-t", "--topics-file", dest="topics_path", default=default_topics_path,
                        help="path to the file containing a list of topics, one topic per line")
    parser.add_argument("-o", "--output-file", dest="output_path", default=default_output_path,
                        help="path of the output CSV file")
    parser.add_argument("-l", "--lemmatize", dest="lemmatize", action="store_true", default=False,
                        help="lemmatize the text using the SeCo LAS service (makes things a lot slower)")
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
    topics = map(lambda t: t.strip(), topics)
    topics = list(filter(lambda t: t, topics))

    articles = fetch_articles(app_id, app_key, topics, lemmatize=args.lemmatize)

    article_fieldnames = ['article_id', 'date_published', 'publisher', 'headline',
                          'authors', 'language', 'url', 'text', 'text_l']

    with open(output_path, "w") as f:
        writer = csv.DictWriter(f, article_fieldnames)
        writer.writeheader()
        writer.writerows(articles)


if __name__ == "__main__":
    main()
