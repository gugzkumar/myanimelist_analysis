# My Anime List Analysis
This is project that web scrapes https://myanimelist.net/ for Anime TV show data, formats them into easy to use CSV files, analyzes it and builds a Nearest Neighbors Model that recommends shows based on a given title.
<br>
<br>
There are 3 main components to this project.
1. `topanimespider.py` is Spider file that scrapes the top Anime of the TV category using the Scrapy framework and produces `anime.json`.
2. `AnimeListCleanup.ipynb` is Jupyter Notebook that cleans and formats `anime.json` easy to use csv files:
>  - `animelist.csv` contains the link to the show page, a title's rank, a title's score, and the size of title's member base
>  - `animepage.csv` contains the a titles genre, studio, producer, and air dates
>  - `animerecommendation.csv` contains a user recommendend shows of a given title
>  - `animestats.csv` contains a title's voting data from score 1 to 10, a titles average score and its standard deviation
3. `AnimeListAnalysis.ipynb` produces charts and tables by investigating Studio, Genre and Producer data; finds the top 20 anime by using different kinds of metrics; makes a Nearest Neighbor Model (uses Studio, Score and Genre) that produces recommended shows based on a given title.

## View The Notebooks here with The [nbviewer](https://nbviewer.jupyter.org/)
[AnimeListCleanup.ipynb](https://nbviewer.jupyter.org/github/gugzkumar/myanimelist_analysis/blob/master/AnimeListCleanup.ipynb)<br>
[AnimeListAnalysis.ipynb](https://nbviewer.jupyter.org/github/gugzkumar/myanimelist_analysis/blob/master/AnimeListAnalysis.ipynb)<br>
