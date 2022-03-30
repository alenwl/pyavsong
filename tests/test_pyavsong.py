from typer.testing import CliRunner
from pyavsong import __app_name__, __version__, cli
from pyavsong.classes.pyav_music_brainzngs import PyAvMusicbrainzngs
from pyavsong.classes.pyav_lyrics import PyAvLyrics

import musicbrainzngs

runner = CliRunner()

musicbrainzngs.set_useragent(
    "pyavsong",
    "0.1",
)

def test_get_artist_ids():
    """
    Test get artists ids from musicbrainzngs API
    """
    name = 'The Rolling Stones'
    try:
        response = musicbrainzngs.search_artists(name)
        id = response.get('artist-list')[0].get('id')
    except:
        pass
    assert id == 'b071f9fa-14b0-4217-8e97-eb41da73f598'

def test_get_tracklist():
    """
    Test get artist metadata from musicbrainzngs API
    """
    artists=['The Rolling Stones']
    test = PyAvMusicbrainzngs(artists)
    test.artists_ids[artists[0]] = 'b071f9fa-14b0-4217-8e97-eb41da73f598'
    test.get_tracklist()
    assert 'Fortune Teller' in test.tracklist[artists[0]]
    assert 'La macarena' not in test.tracklist[artists[0]]

def test_get_urls():
    """
    Test bulk generation of urls for HTTP request
    """
    test_track_list = {}
    artist = 'The Rolling Stones'
    songs = ('Fortune Teller', 'Come On', 'Poison Ivy')
    test_track_list[artist] = songs
    test = PyAvLyrics(test_track_list)
    test.get_urls()
    assert 'https://api.lyrics.ovh/v1/The%20Rolling%20Stones/Poison%20Ivy' in test.urls[2].replace(' ','%20')
    assert 'https://api.lyrics.ovh/v1/The%20Rolling%20Stones/Fortune%20Teller'in test.urls[0].replace(' ','%20')
    assert 'https://api.lyrics.ovh/v1/The%20Rolling%20Stones/Come%20On' in test.urls[1].replace(' ','%20')

def test_get_stats():
    """"
    Function to test word average calculation
    """
    test_track_list = {}
    artist = ['Artist 1','Artist 2']
    test = PyAvLyrics(test_track_list)
    test.word_counts = [('Artist 1', 0), 
                        ('Artist 1', 10),
                        ('Artist 2', 0),
                        ('Artist 2', 30)]
    test.get_stats(artist)
    assert 5 is test.word_averages['Artist 1']
    assert 15 is test.word_averages['Artist 2']

def test_url_requests():
    """
    Function to test asyncronous
    HTTP get requests
    """
    test_track_list = {}
    artist = 'The Rolling Stones'
    songs = ('Fortune Teller','Come On')
    test_track_list[artist] = songs
    test = PyAvLyrics(test_track_list)
    test.get_urls()
    test.get_url_requests()
    assert 249 in [item[1] for item in test.word_counts if artist in item[0]]
    assert 201 in [item[1] for item in test.word_counts if artist in item[0]]
