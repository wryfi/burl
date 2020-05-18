import re
import time

import requests
import urllib.parse

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from burl.redirects.models import Redirect


class Command(BaseCommand):
    help = 'imports URLs from the PLOS solr API'

    def add_arguments(self, parser):
        parser.add_argument('user', type=str)
        parser.add_argument('start_date', type=str)
        parser.add_argument('end_date',  type=str)
        parser.add_argument('--rows', '-r', type=str, default=500)

    def handle(self, *args, **options):
        user = get_user_model().objects.get(username=options['user'])
        start_date, end_date, rows = options['start_date'], options['end_date'], options['rows']
        response = requests.get(_make_url(start_date, end_date, 0, rows))
        total = response.json().get('response', {}).get('numFound', 0)
        docs = response.json().get('response', {}).get('docs', [])
        _save_results(docs, user)
        saved = len(docs)
        while saved < total:
            response = requests.get(_make_url(start_date, end_date, saved, rows))
            docs = response.json().get('response', {}).get('docs', [])
            _save_results(docs, user)
            saved += len(docs)
            time.sleep(0.5)
        print(saved)


def _make_url(start_date, end_date, row_start, rows):
    qstring = f'publication_date:[{start_date} TO {end_date}] AND abstract:[* TO *]'
    qstring = '&'.join([qstring, 'fl=id,title'])
    qstring = '&'.join([qstring, f'&rows={rows}&start={row_start}'])
    qstring = re.sub(r'\s+', '%20', qstring)
    return f'https://api.plos.org/search?q={qstring}'


def _save_results(results, user):
    for result in results:
        redirect = Redirect.objects.create(url=_get_url(result['id']), description=result['title'], user=user)
        print(f'/{redirect.burl} -> {redirect.url} ({redirect.description})')
        time.sleep(0.5)


def _get_url(doi):
    response = requests.head(f'https://dx.plos.org/{doi}')
    if response.status_code != 301:
        return f'https://dx.plos.org/{doi}'
    return response.headers['Location']
