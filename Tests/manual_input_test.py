from util import get_response
import vars


def query_ombd(title):
    api_key = "47fec2f"  # 1000 calls per day
    url = "http://www.omdbapi.com/?t=%s&apikey=%s" % (title, api_key)
    # print_response(url)
    parse_omdb_data(get_response(url).json())


def parse_omdb_data(data):
    """
    Parses data from the OMDb API JSON file into the data buffer stored in "vars"
    :param data: the JSON filed returned from the OMDb API service
    """
    vars.data_buffer.update({'title': data['Title'],
                             'genres': data['Genre'],
                             'rating': data['Rated'],
                             'year': data['Year'],
                             'length': data['Runtime'][:data['Runtime'].find(' ')],
                             'plot': data['Plot'],
                             'reviews': data['Metascore']})
    print(vars.data_buffer)  # Debug


if __name__ == "__main__":
    query_ombd("Tropic Thunder")
