Requirements
------------

You need Python 3.5 or later to run the facebook scraper.

In Ubuntu, Mint and Debian you can install Python 3 like this:

    $ sudo apt-get install python3 python3-pip

Pipenv can be installed using pip:

    $ pip install pipenv
 
Installing the remaining dependencies

    $ cd web_scrapping/facebook
    $ pip install pipenv
    $ pipenv install

Quick start
-----------

Running the FB Scraper

    $ pipenv shell
    $ robot data_extractor.robot

CSV and JSON data

The data is stored in the following path:

    $  web_scrapping/facebook/data
