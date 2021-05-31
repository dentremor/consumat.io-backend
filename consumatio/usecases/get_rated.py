def get_rated(external_id: str, tmdb: object, type: str, vote_avg: float,
              vote_count: int, released_from: str, country: str,
              page: int) -> dict:
    """
    Make all relevant API request for this usecase (items by rating) and assemble them into a dictionary
    :param tmdb: <object> Tmdb object
    :param type: <str> Popular item type "movie" or "tv"
    :param vote_avg: <float> filter media with average rating greater than set value
    :param vote_count: <int> minimum number of votes
    :param released_from: <str> search for media released after specified date (YYYY-MM-DD)
    :param country: <str> Country code (uppercase) currently only applicable for movies
    :param page: <int> Search page (minimum:1 maximum:1000)
    :return: <dict> popular media
    """
    dict = {}
    if type == "Movie":
        dict_movie_results = tmdb.get_movies_by_rating(country, external_id,
                                                       vote_avg, vote_count,
                                                       released_from, page)
        dict = {
            "total_pages": dict_movie_results.get("total_pages"),
            "results": dict_movie_results.get("results")
        }

    elif type == "TV":
        dict_tv_results = tmdb.get_tv_by_rating(country, external_id, vote_avg,
                                                vote_count, released_from,
                                                page)
        dict = {
            "total_pages": dict_tv_results.get("total_pages"),
            "results": dict_tv_results.get("results")
        }

    return dict
