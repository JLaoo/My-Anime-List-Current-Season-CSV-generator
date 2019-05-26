# My Anime List Current Season CSV generator

Generates a CSV file for the current season of airing anime from myanimelist.net

Current info:
- Name
- Type of anime
- Score
- Ranking
- Popularity
- Members
- MAL URL

Notes:
- I think it's possible to remove the time.sleeps in the scraping loop if you only run this script every once in a while. I have it set at at 0.5 second delay between each get request since MAL kept blocking me. The 0.5 second delay however does seem to consistently pull all data without throwing an error or getting blocked.
- Runtime will end up being between 5-10 minutes depending on the amount of anime this season.

To do:
- Pull more information.
- Make code more efficient by reducing amount of requests to server.
