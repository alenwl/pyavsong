"""
This module contains a class that defines the required
functions to get all artists ids and associated recordings.
This modules uses ``musicbrainzngs`` module to perform 
request to their API.
"""
import re, typer
from typing import List

import musicbrainzngs

musicbrainzngs.set_useragent(
        "pyavsong",
        "0.1",
)


class PyAvMusicbrainzngs():
    """
    Class definition for ``PyAvMusicbrainzgs``
    """

    def __init__(
        self, 
        artists: List[str],
    ):
        self.artists = artists
        self.artists_ids = {}
        self.tracklist = {}

    def get_artist_metadata(self) -> None:
        """
        This function will request artist ids
        and call ``get_tracklist()`` to get their
        record names.

        """
        self.get_artist_ids()
        if self.artists_ids:
            self.get_tracklist()

    def get_artist_ids(self) -> bool:
        """
        This function calls ``musicbrainzngs`` API
        to fetch artist ids.

        :return: boolean flag for artist ids found/not found

        """
        for name in self.artists:
            try:
                response = musicbrainzngs.search_artists(name)
                name = response.get('artist-list')[0].get('name')
                id = response.get('artist-list')[0].get('id')
                self.artists_ids[name] = id
            except:
                typer.echo(f'Error getting artist ids')
                return False
        return True

    def get_tracklist(self) -> None:
        """
        This function calls ``musicbrainzngs`` API
        to fetch artists recordings based on the artist ids

        """
        for (name, id) in self.artists_ids.items():
            try:
                response = musicbrainzngs.browse_releases(artist=id, 
                                                          includes=["recordings"])
                tracks = self.extract_tracks_from_response(response)
                self.tracklist[name] = tracks
            except:
                typer.echo(f'Error getting tracks for {name}')

    def extract_tracks_from_response(
        self, 
        response,
        ) -> List[str]:
        """
        This function iterates through response json
        to extract the tracks associated to a given artist.

        :param response:
        :return: list with artists track names

        """
        track_list = []
        for entry in response["release-list"]:
            for entry2 in entry["medium-list"]:
                for entry3 in entry2["track-list"]:
                    song = (
                        str(entry3["recording"]).split('\'title\': ')[1]
                                                .split(', \'length\':')[0]
                                                .replace('\'','')
                    )
                    song = re.sub(r'\(.*?\)', '', song)
                    song = (re.sub('[^a-zA-Z0-9 \n\.]', '', song).lstrip().rstrip())
                    if song not in track_list:
                        track_list.append(song)
        return track_list