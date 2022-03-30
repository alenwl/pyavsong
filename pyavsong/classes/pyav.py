"""
This function contains a class with the definition
of a single process to fetch music artist metadata and
stats
"""
import typer

from pyavsong.classes.pyav_music_brainzngs import PyAvMusicbrainzngs
from pyavsong.classes.pyav_lyrics import PyAvLyrics

from typing import List

class PyAverageCalculator():

    def __init__(
        self, 
        artists: List[str],
    ):
        self.artists = artists

    def process(self):
        """
        This function defines the process for
        artist metadata processing. Relies on 
        ``PyAvMusicbrainzgs`` to fetch metadata
        using ``musicbrainzngs`` API and also on
        ``PyAvLyrics`` to download and process
        lyrics. It will also print the relevant artist
        metada returned by music APIs

        """
        pyav_mbrainz = PyAvMusicbrainzngs(artists = self.artists)
        typer.echo(f'Fetching artist metada...')
        pyav_mbrainz.get_artist_metadata()
        if pyav_mbrainz.tracklist:
            pyav_lyric = PyAvLyrics(pyav_mbrainz.tracklist)
            typer.echo(f'Preparing urls for HTTP requests to lyrics API...')
            pyav_lyric.get_urls()
            typer.echo(f'Downloading lyrics...')
            pyav_lyric.get_url_requests()
            typer.echo(f'Computing word averages...')
            pyav_lyric.get_stats(pyav_mbrainz.artists)
            for artist in self.artists:
                typer.echo(f'Average words per song for {artist} is: {pyav_lyric.word_averages[artist]}')
