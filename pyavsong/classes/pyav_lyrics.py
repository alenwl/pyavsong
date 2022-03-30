"""
This module contains a class that defines the required
functions to generate the URLs, send asynchronous 
requests to 'https://api.lyrics.ovh/v1/' and fetch
lyrics of a defined set of artists and songs
"""
import asyncio, aiohttp
from typing import Dict, List

API_URL = 'https://api.lyrics.ovh/v1/'


class PyAvLyrics():
    """
    Class definition for ``PyAvLyrics``
    """

    def __init__(
        self, 
        tracklist: Dict
    ):
        self.tracklist = tracklist
        self.urls = []
        self.word_counts = []
        self.word_averages = {}

    def get_urls(self) -> None:
        """
        Generate the URLs required to make the asynchronous
        HTTP requests to API_URL

        """
        for (artist_name, track_name) in self.tracklist.items():
            for track in track_name:
                self.urls.append(('{:}{:}/{:}'.format(API_URL, 
                                                      artist_name, 
                                                      track)))

    def get_stats(
        self, 
        artists: List[str],
    ) -> None:
        """
        This function will iterate through ``artists`` and 
        collect the number of words found for each song.
        Finally, the average is computed and stored in 
        a dictionary called ``word_averages``

        :param artists: list with artists typed in by the user

        """
        for name in artists:
            count = [item[1] for item in self.word_counts 
                     if name.upper() in item[0].upper()]
            if count:
                self.word_averages[name] = round((sum(count) / 
                                                  len(count)))
            else:
                self.word_averages[name] = 0

    async def get_word_count(
        self, 
        session: aiohttp, 
        url: str, 
    ) -> None:
        """
        This function performs asyncronous http get 
        request to ``API_URL``

        :param session: ``aiohttp`` HTTP Client session
        :param url: url to make the HTTP get request to

        """
        async with session.get(url) as res:
            try: 
                response = await res.json()
                if 'error' not in response:
                    self.word_counts.append(
                                            (url.split(API_URL)[1].split('/')[0],
                                            len(response["lyrics"].split()))
                    )
            except:
                pass

    async def get_url_requests_async(self) -> None:
        """
        This function starts the HTTP client session
        and wraps all coroutines into a task

        """
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in self.urls:
                tasks.append(asyncio.ensure_future(self.get_word_count(session, url)))
            await asyncio.gather(*tasks)

    def get_url_requests(self) -> None:
        """
        Function to execute the main coroutine 
        ``self.get_url_requests_async()``

        """
        asyncio.run(self.get_url_requests_async())