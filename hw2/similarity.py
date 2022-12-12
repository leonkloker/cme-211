import math
import sys
import time

def get_data(data_file):
    """
    This function reads all the ratings from the data_file
    and puts them into a dictionary of dictionaries with 
    movie IDs as outer keys and user IDs as inner keys.

    Args:
        data_file: String, name of the data file.

    Returns:
        data: Dictionary containing all ratings.
    """

    file = open(data_file, "r")
    data = {}
    nlines = 0
    users = set()

    # parse through all lines
    for line in file:
        entry = [int(elem) for elem in line.split()]
        users.add(entry[0])

        # add rating to the movie's dictionary entry
        if entry[1] in data:
            data[entry[1]][entry[0]] = entry[2]
        
        # create new dictionary entry for the movie and add the rating
        else:
            data[entry[1]] = {}
            data[entry[1]][entry[0]] = entry[2]
        nlines += 1
    
    file.close()

    # print small statistics of data set
    print("Read {} lines with total of {} movies and {} users".format(nlines,
    len(data), len(users)))

    return data

def get_average_ratings(data):
    """
    This function calculates the average rating of every movie
    contained in the data set.

    Args:
        data: Dictionary of the ratings with movie ID as key.

    Returns:
        avg_ratings: Dictionary of the average rating with movie ID as key.
    """

    avg_ratings = {}

    # iterate over all movies
    for movie in data:
        avg_ratings[movie] = sum(data[movie].values()) / len(data[movie])

    return avg_ratings

def get_similarity(data, avg_ratings, movie1, movie2, user_thresh):
    """
    This function calculates the similarity of movie1 and movie2.

    Args:
        data: Dictionary of the ratings with movie ID as key.
        avg_ratings: Dictionary of the average rating with movie ID as key.
        movie1: Integer, ID of movie 1.
        movie2: Integer, ID of movie 2.
        user_thresh: Integer, amount of common raters required to output similarity.

    Returns:
        similarity: Float, adjusted cosine similarity of movie 1 and movie 2,
                    -2 if there are less common raters than user_thresh.
        amount of common raters used to calculate similarity.
    """

    raters = get_common_raters(data, movie1, movie2)

    # return -2 if not enough shared raters or movies are the same
    if len(raters) < user_thresh or movie1==movie2:
        return -2, len(raters)

    enumerator = 0
    sum1 = 0
    sum2 = 0

    # iterate over all raters and their ratings
    for rater in raters:
        r1_dif = data[movie1][rater] - avg_ratings[movie1]
        r2_dif = data[movie2][rater] - avg_ratings[movie2]
        enumerator += r1_dif * r2_dif
        sum1 += r1_dif**2
        sum2 += r2_dif**2

    # when all ratings are equal to their average for both movies return 1
    if sum1 == 0 and sum2 == 0:
        return 1, len(raters)
    
    # when all ratings are equal to their average for only one movie return 0
    if sum1 == 0 or sum2 == 0:
        return 0, len(raters)
    
    # calculate adjusted cosine similarity
    similarity = enumerator / math.sqrt(sum1*sum2)

    return similarity, len(raters)

def get_common_raters(data, movie1, movie2):
    """
    This function finds the common raters of movies
    movie1 and movie2.

    Args:
        data: Dictionary of the ratings with movie ID as key.
        movie1: Integer, ID of movie 1.
        movie2: Integer, ID of movie 2.

    Returns:
        common_raters: Set containing all shared raters of movie1 and movie2.
    """

    # find all raters of movie 1 and 2
    raters1 = set(data[movie1].keys())
    raters2 = set(data[movie2].keys())
    
    # get the intersection
    common_raters = raters1.intersection(raters2)
    return common_raters

def get_similarity_list(data, avg_ratings):
    """
    This function calculates the most similar movie based on the
    adjusted cosine similarity out of all the movies in the data.

    Args:
        data: Dictionary of the ratings with movie ID as key.
        avg_ratings: Dictionary of the average rating with movie ID as key.

    Returns:
        similar_movies: Dictionary with movies as key containing the most similar
        other movie, the similarity and the amount of shared raters.
    """

    similar_movies = {}

    # iterate over all movies
    for movie1 in data:
        max_similarity = -2
        similar_movies[movie1] = None

        # find the movie with highest similarity
        for movie2 in data:
            current_similarity, nraters = get_similarity(data, avg_ratings, movie1,
            movie2, user_thresh)

            # save the movie and other data in the dictionary
            if current_similarity > max_similarity:
                max_similarity = current_similarity
                similar_movies[movie1] = (movie2, current_similarity, nraters)

    return similar_movies

def write_output(similar_movies, output_file):
    """
    This function writes the output contained in similar_movies
    in output_file.

    Args:
        similar_movies: Dictionary of all movies and their most similar movie.
        output_file: String, name of the output file to write in

    Returns:

    """

    file = open(output_file, "w")

    # iterate over all movies
    for movie in similar_movies:
        file.write("{}".format(movie))

        # write most similar movie, similarity and amount of common users
        if similar_movies[movie] != None:
            file.write(" ({}, {:.2f}, {})\n".format(*similar_movies[movie]))

        # if no other movie has more than user_thresh common raters
        else:
            file.write("\n")

    file.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        # not enough arguments, print usage message
        print("Usage:")
        print("$ python3 similarity.py <data_file> ", end ="")
        print("<output_file> [user_thresh (default = 5)]")
        sys.exit(0)

    # read arguments
    data_file = sys.argv[1]
    output_file = sys.argv[2]
    user_thresh = 5

    # set user_thresh if given
    if len(sys.argv) == 4:
        user_thresh = int(sys.argv[3])

    print("Input MovieLens file: {}".format(data_file))
    print("Output file for similarity data: {}".format(output_file))
    print("Minimum number of common users: {}".format(user_thresh))
    
    start_time = time.time()

    # get data from file and calculate average ratings
    data = get_data(data_file)

    # calculate average ratings
    avg_ratings = get_average_ratings(data)

    # get the most similar movie for every movie in the data
    similar_movies = get_similarity_list(data, avg_ratings)

    end_time = time.time()
    print("Computed similarities in {:.3f} seconds".format(end_time-start_time))

    write_output(similar_movies, output_file)
