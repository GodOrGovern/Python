''' Query music service APIs for information on genre and BPM '''

from urllib.parse import quote_plus, urlencode
from urllib.request import urlopen
import re
import requests

def main():
    ''' Generate list of genres and their respective average BPMs '''
    genres = set()
    pages = [
        'List of popular music genres',
        'List of styles of music: A\u2013F',
        'List of styles of music: G\u2013M',
        'List of styles of music: N\u2013R',
        'List of styles of music: S\u2013Z'
    ]
    averages = dict()
    for page in pages:
        genres.update(get_genres(page))
    for genre in sorted(genres):
        averages.update({genre : bpm_avg(get_songs(genre))})
        print(averages)

def get_songs(tag):
    ''' Query API for songs and artists given a genre '''
    root = 'http://ws.audioscrobbler.com/2.0/'
    api_key = '746b2089fd7870fa39d6e0d83e3b613c'
    result = requests.get('%s?method=tag.gettoptracks&tag=%s&limit=5&api_key=%s&format=json'
                          % (root, tag, api_key))
    return result.json()['tracks']['track']

def bpm_avg(songs):
    ''' Find average tempo given a JSON containing song information from
    Last.fm '''
    average = 0
    num_songs = len(songs)
    if not songs:
        return None
    for song in songs:
        bpm = get_bpm(quote_plus(song['name']), quote_plus(song['artist']['name']))
        try:
            average += int(bpm['search'][0]['tempo'])
        except (KeyError, TypeError):
            num_songs -= 1
    if num_songs == 0:
        return None
    average //= num_songs
    return average

def get_bpm(song, artist):
    ''' Query API for BPM given a song and artist '''
    root = 'https://api.getsongbpm.com'
    api_key = 'c984d06aafbecf6bc55569f964148ea3'
    result = requests.get('%s/search/?api_key=%s&type=both&lookup=song:%sartist:%s'
                          % (root, api_key, song, artist))
    return result.json()

def get_wiki(name):
    ''' Retrieve data from wikipedia '''
    root = 'http://en.wikipedia.org/w/index.php'
    name = name.replace(' ', '_').encode('utf8')
    params = {'title': name, 'action': 'raw'}
    return urlopen('%s?%s' % (root, urlencode(params))).read().decode('utf8')

def get_genres(page):
    ''' Get genres from wikipedia data '''
    start = re.compile(r'==.*==', re.M)
    end = '==References=='
    item = re.compile(r'\[\[(?:[^\]\|]*\|)?([^\]\|]*)\]\]')
    bad_name = re.compile(r'^[A-Z][a-z]?(-[A-Z][a-z]?)?$')
    link = re.compile(r'[a-z][a-z]:')
    drop = re.compile(r'\(.*\)$')
    text = get_wiki(page)
    if end in text:
        text, _ = text.split(end, 1)
    parts = start.split(text, 1)
    if len(parts) == 2:
        text = parts[1]
    for line in text.split('\n'):
        match = item.search(line)
        if match:
            name = match.group(1)
            if name.startswith('Section') or bad_name.match(name) or link.match(name):
                continue
            name = drop.sub('', name)
            name = name.strip().lower()
            if name:
                yield name

if __name__ == '__main__':
    main()
