# crawl-scholar
Some code to automatically search Google scholar for a list of pre-defined search terms. 

I used it for two structured literature reviews that I conducted for my dissertation. It contains some hard coded portions that I might eventually move to config files, but that is currently no priority. I commented it so that it would be accessible for people with minimal python background, because I assume that this is the group who will benefit most from it.

The code is based on https://python.plainenglish.io/scrape-google-scholar-with-python-fc6898419305 and I made some adjustments to make it fit my needs. Feel free to adjust or share as you like.

## Prerequisites

This code was written with python3. 

You need the following libraries to crawl and dump results in JSON format:
* BeautifulSoup
* requests
* json

To get from JSON to CSV format you need
* pandas
