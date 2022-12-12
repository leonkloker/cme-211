CME 211 Homework 2

The test dataset should look somewhat realistic, meaning not every user has rated every movie, maybe there are even duplicate entries of the same rating, there can be multiple spaces between the different columns and the data is not ordered in any kind. I created a reference solution using some of the available methods in the pandas package in an additional short script.

$ python3 similarity.py ml-100k/u.data output.data
Input MovieLens file: ml-100k/u.data
Output file for similarity data: output.data
Minimum number of common users: 5
Read 100000 lines with total of 1682 movies and 943 users
Computed similarities in 56.322 seconds

The program is decomposed into:
get_data function, that reads from the data file into a dictionary
get_average_ratings function, that calculates the average rating of every movie once the data has been read
get_common_raters function, that returns the raters which have rated both movies
get_similarity function, that calculates the similarity of two movies with each other
get_similarity_list function, that finds the movie with the maximal similarity among all other movies
write_output function, that is used to write the data in the similarity_list in the output file

Time spent 6 hours.
