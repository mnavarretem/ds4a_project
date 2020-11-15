# OFFCORSS Instagram Scraper

OFFCORSS Instagram Scraper is a development that we have made to deal with the problem of refreshing the database with the latest instagram publications for the company and their competitors.

## Requeriments
You need to install the dependences in the `requeriments.txt` file.

``` bash
$ pip install -r requeriments.txt
```

## Usage
Running the Instagram Scrapper

```bash
$ python main.py
```

## Notes
This scraper was programmed to get the las 12 post of each Instagram accounts that appears in the file **companies.txt**. If you want to add another instagram account, you could edit that file and add in separated lines all the instagram account names.

In the folder *utils* you can find a file named *db_credentials.py*. If you want to use this scraper to store the last comments in your own database, you could change those credentials.