This code will fetch data using a title code and convert the data to JSON format.

Example of usage:

./convert_imdb_to_json.py tt0117731

The movie_data.ndjson.zst file contains movie / episode data for over 1 million shows. The data is in ndjson format and is sorted by the number of votes. This data also contains basic metadata for each show including genres, start/end year, title, adult classification and run time. You can use the "titleCode" in each movie object to download data from IMDB in json format using the code provided.

Movie title codes and other metadata can be downloaded from here: https://datasets.imdbws.com/

This should get you started.

2020-08-19: Added ratings metadata

2020-08-19: Added reviews metadata

To do:

Add additional logging

Add better error handling (for requests)

