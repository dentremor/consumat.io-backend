from consumatio.external.db.models import *
from consumatio.entities.movie import Movie
from consumatio.entities.tv import TV


def get_popular(external_id: str, tmdb: object, type: str, country: str,
                page: int) -> dict:
    """
    Get popular Movies/TV Shows for a provided country
    :param external_id: <str> External ID provided by OAuth 
    :param tmdb: <object> Tmdb object
    :param type: <str> Popular item type "movie" or "tv"
    :param country: <str> Country code (uppercase) currently only applicable for movies
    :param page: <int> Search page (minimum:1 maximum:1000)
    :return: <dict> popular media
    """
    dict = {}
    if type == "Movie":
        dict_movie_results = tmdb.get_popular_movies(country, page)
        results = dict_movie_results["results"]
        result_list = []

        for result in results:
            query = MediaData.query.join(User).filter(
                User.user_id_content == MediaData.user_id_content_media_data,
                MediaData.media_type_content == "Movie",
                User.external_id_content == external_id,
                MediaData.media_id_content == result["code"]).first()

            rating = None
            watch_status = None
            favorite = None

            if query != None:
                rating = query.rating_content
                watch_status = query.watch_status_content
                favorite = query.favorite_content

            result["rating"] = rating
            result["watch_status"] = watch_status
            result["favorite"] = favorite

            dict = {
                "code": result.get("code"),
                "title": result.get("title"),
                "genres": None,
                "overview": result.get("overview"),
                "popularity": result.get("popularity"),
                "rating_average": result.get("rating_average"),
                "rating_count": result.get("rating_count"),
                "release_date": result.get("release_date"),
                "runtime": None,
                "status": None,
                "backdrop_path": result.get("backdrop_path"),
                "poster_path": result.get("poster_path"),
                "providers": None,
                "cast": None,
                "directors": None,
                "tmdb_url":
                f'https://www.themoviedb.org/movie/{result.get("code")}',
                "watch_status": watch_status,
                "rating_user": rating,
                "favorite": favorite
            }

            movie = Movie.from_dict(dict)
            dict = movie.to_dict()

            dict["__typename"] = "Movie"

            result_list.append(dict)

        dict = {
            "total_pages": dict_movie_results.get("total_pages"),
            "results": result_list
        }

    elif type == "TV":
        dict_tv_results = tmdb.get_popular_tv(page)
        results = dict_tv_results["results"]
        result_list = []

        for result in results:
            query = MediaData.query.join(User).filter(
                User.user_id_content == MediaData.user_id_content_media_data,
                MediaData.media_type_content == "TV",
                User.external_id_content == external_id,
                MediaData.media_id_content == result["code"]).first()

            rating = None
            watch_status = None
            favorite = None

            if query != None:
                rating = query.rating_content
                watch_status = query.watch_status_content
                favorite = query.favorite_content

            result["rating"] = rating
            result["watch_status"] = watch_status
            result["favorite"] = favorite

            dict = {
                "code": result.get("code"),
                "title": result.get("title"),
                "genres": None,
                "overview": result.get("overview"),
                "popularity": result.get("popularity"),
                "rating_average": result.get("rating_average"),
                "rating_count": result.get("rating_count"),
                "first_air_date": result.get("first_air_date"),
                "last_air_date": None,
                "status": None,
                "backdrop_path": result.get("backdrop_path"),
                "poster_path": result.get("poster_path"),
                "providers": None,
                "creators": None,
                "cast": None,
                "number_of_episodes": None,
                "number_of_seasons": None,
                "tmdb_url":
                f'https://www.themoviedb.org/tv/{result.get("code")}',
                "watch_status": watch_status,
                "rating_user": rating,
                "favorite": favorite,
                "runtime": None
            }

            tv = TV.from_dict(dict)
            dict = tv.to_dict()

            dict["__typename"] = "TV"

            result_list.append(dict)

        dict = {
            "total_pages": dict_tv_results.get("total_pages"),
            "results": result_list
        }

    return dict
