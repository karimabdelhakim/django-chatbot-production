import requests
import json
import random

weatherKey = "0e24e886caae46e0bb8153748172504"
moviesKey = "a2b094bc91767343355b1f3a76678420"


def getResults(class_type, request_parameter):
    if class_type == "weather":
        key = weatherKey
    else:
        key = moviesKey
    tempClass = WeatherOrMovies(class_type, request_parameter, key)
    result = tempClass.executeApi()
    return result


class WeatherOrMovies:
    def __init__(self, _intentType, _requestParameter, _key):
        self.intentType = _intentType
        self.requestParameter = _requestParameter
        self.key = _key

        self.genres = {
            "action": 28,
            "adventure": 12,
            "animation": 16,
            "comedy": 35,
            "crime": 80,
            "drama": 18,
            "horror": 27,
            "mystery": 9648,
            "romance": 10749
        }

        self.genre_ids = {
            28: "action",
            12: "adventure",
            16: "animation",
            35: "comedy",
            80: "crime",
            18: "drama",
            27: "horror",
            9648: "mystrey",
            10749: "romance"
        }

    def executeApi(self):
        if (self.requestParameter is None):
            return_data = {}
            error = {}
            error["message"] = "The parameter passed is Null"
            return_data["status_code"] = 400
            return_data["error"] = error
            raise ValueError(json.dumps(return_data))
        self.requestParameter = self.requestParameter.replace(" ", "%20")

        if (self.intentType == "movie"):
            getTopRated = "top rated".replace(" ", "%20")
            getPopular = "popular"

            compareString = str(self.requestParameter)

            if (compareString == getTopRated or compareString == getPopular):
                self.requestParameter = self.requestParameter.replace("%20", "_")
                url = "https://api.themoviedb.org/3/movie/" + str(
                    self.requestParameter) + "?language=en-US&page=1&api_key=" + str(self.key)
                data = self._call(url)
                results = data['results']
                result = random.choice(results)
                return self._formatMovieResponse(result)

            elif (compareString.find("genre:") != -1):
                genre = compareString[compareString.index(":") + 1:]
                if genre in self.genres:
                    url = "https://api.themoviedb.org/3/genre/" + str(self.genres[
                                                                          genre]) + "/movies?api_key=" + self.key + "&language=en-US&include_adult=false&sort_by=created_at.asc"
                    data = self._call(url)
                    results = data['results']
                    result = random.choice(results)
                    return self._formatMovieResponse(result)
                else:
                    self.requestParameter = getPopular
                    return self.executeApi()

            else:
                url = "https://api.themoviedb.org/3/search/multi?api_key=" + str(
                    self.key) + "&language=en-US&query=" + str(self.requestParameter) + "&page=1&include_adult=false"
                data = self._call(url)
                results = data['results']
                if len(results) == 0:
                    return "No Movie Found"
                    # return_data = {}
                    # error = {}
                    # error["message"] = "No Movie Found"
                    # return_data["status_code"] = 400
                    # return_data["error"] = error
                    # raise ValueError(json.dumps(return_data))

                return self._formatMovieResponse(results[0])

        elif (self.intentType == "weather"):
            url = "http://api.apixu.com/v1/current.json?key=" + str(self.key) + "&q=" + str(self.requestParameter)
            data = self._call(url)

            return_data = {}
            try:
                return_data['Temperature In Celcius'] = data['current']['temp_c']
                return_data['Temperature In Fahrenheit'] = data['current']['temp_f']
                return_data['Weather Condition'] = data['current']['condition']['text']
                return_data['Feels Like In Celcius'] = data['current']['feelslike_c']
                return_data['Feels Like In Fahrenheit'] = data['current']['feelslike_f']
                return_data['Humidity'] = data['current']['humidity']
                return json.dumps(return_data)
            except ValueError:
                return "No Matching City Was Found"

        else:
            raise ValueError("This module does not deal with this intent type")

    def _formatMovieResponse(self, result):
        return_data = {}
        return_data['Original Title'] = result['original_title']
        return_data['Overview'] = result['overview']
        if (result['poster_path'] is not None):
            return_data['poster'] = " http://image.tmdb.org/t/p/w185/" + result['poster_path']
        if ('media_type' in result.keys()):
            return_data['Media Type'] = result['media_type']
        return_data['rating'] = result['vote_average']
        movieID = result['id']
        getVideoURL = "https://api.themoviedb.org/3/movie/" + str(movieID) + "/videos?language=en-US&api_key=" + str(
            self.key)
        videoData = self._call(getVideoURL)
        if (len(videoData['results']) > 0):
            videoResult = videoData['results'][0]
            if (videoResult['site'] == "YouTube"):
                return_data['Trailer Link'] = "https://www.youtube.com/watch?v=" + videoResult['key']

        return_data["genres"] = []
        for genre_id in result["genre_ids"]:
            if genre_id in self.genre_ids:
                return_data["genres"].append(self.genre_ids[genre_id])
        return json.dumps(return_data)


    def _call(self, url):
        response = requests.get(url)
        data = response.json()
        if (response.status_code != 200):
            print response.json()
            result = {}
            result['error'] = data['error']
            result['status_code'] = response.status_code
            raise ValueError(json.dumps(result))

        return data
