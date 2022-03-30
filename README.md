# pyavsong

`pyavsong` is a Python CLI application that given the name of an artist, will display the number of average words in their songs. 

## Installation

Make sure Pip package manager is installed on your local machine. [You can check the installation process here.](https://pypi.org/project/pip/).

Once `pip` has been successfully installed on your local machine, please follow the steps below to clone the repo into your local hard drive: 
1. `$ git clone https://github.com/alenwl/pyavsong.git`
2. `$ cd pyavsong/`

The following commands will create a virtual environment in your local machine and install all the dependencies:

1. `$ python -m venv ./venv`
2. `$ source venv/bin/activate`
3. `(venv) $ pip install -r requirements.txt`

## Usage:
-------------

    $ python -m pyavsong -a <nameofartist>
    $ python -m pyavsong --artist <nameofartist>

Options:
-------------

    -a,--artist The name of the artits to use
    --help Prints out help menu

Running tests:
--------------

    $ python -m pytest tests/

Command line usage examples:
-------------

    $ python -m pyavsong --artist "The Rolling Stones"
    $ python -m pyavsong --artist "The Rolling Stones" --artist "Queen"
    $ python -m pyavsong -a "The Rolling Stones"
    $ python -m pyavsong -a "The Rolling Stones" -a "Queen"
