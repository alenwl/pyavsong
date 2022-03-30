"""
This module provides the Python AvSong CLI.
"""
from typing import List, Optional

import typer

from pyavsong import __app_name__, __version__
from pyavsong.classes.pyav import PyAverageCalculator

app = typer.Typer(add_completion=False)

def _artist_callback(
    artists: List[str]
) -> None:
    """
    Callback triggered by artist() to parse
    parameters introduced by user
    
    """
    if artists:
        pyav_calc = PyAverageCalculator(artists)
        pyav_calc.process()
        raise typer.Exit()

@app.callback()
def artist(name: List[str] = typer.Option(
         None,
         "--artist",
         "-a",
         help="Name of band/artist",
         callback=_artist_callback,
         is_eager=True,
    )
) -> None:
    """
    Function to define parameters for 
    artist callback. 
    
    """
    return