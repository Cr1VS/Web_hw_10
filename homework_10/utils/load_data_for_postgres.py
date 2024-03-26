import os
import django


# Установка переменной окружения DJANGO_SETTINGS_MODULE, если она еще не установлена
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homework_10.settings')

# Инициализация Django
django.setup()

import json
from django.contrib.auth.models import User
from quotes.models import Author, Quote, Tag

def load_authors_from_json(file_path):
    with open(file_path, 'r', encoding="utf-8") as fh:
        authors_data = json.load(fh)
        for author_data in authors_data:
            author = Author.objects.create(
                fullname=author_data['fullname'],
                born_date=author_data['born_date'],
                born_location=author_data['born_location'],
                description=author_data['description']
            )

def load_quotes_from_json(file_path):
    with open(file_path, 'r', encoding="utf-8") as fh:
        quotes_data = json.load(fh)
        for quote_data in quotes_data:
            author_fullname = quote_data['author']
            author = Author.objects.get(fullname=author_fullname)
            quote = Quote.objects.create(
                name=quote_data['quote'],
                author=author
            )
            tags = quote_data['tags']
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                quote.tags.add(tag)

def main():
    load_authors_from_json('authors.json')
    load_quotes_from_json('quotes.json')

if __name__ == "__main__":
    main()
