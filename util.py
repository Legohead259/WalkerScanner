import json
import requests
from errors import InvalidData, Forbidden, NotFound, ExceedLimit, ScanError, raise_error
import vars


# =====START RESPONSE FUNCTIONS=====


def get_response(url):
    """
    Gets the response from the queried API service URL
    :param url: the queried API service URL
    :return: the response from the queried API service URL
    """
    headers = {'cache-control': "no-cache"}
    response = requests.get(url, headers=headers)
    # print(response.status_code)  # Debug

    # ===Start Response Checking===

    if response.status_code != 200:  # 200 means that a valid response was sent back to the client
        def switch(arg):
            switcher = {
                400: InvalidData,
                403: Forbidden,
                404: NotFound,
                429: ExceedLimit
            }
            return switcher.get(arg, ScanError)

        raise_error(switch(response.status_code))

    # ===End Response Checking===

    return response


def print_response(url):
    """
    Wrapper function for printing the ENTIRE response of the url query
    :param url: the query url provided by the API call function
    """
    r = get_response(url)

    print("-----" * 5)
    print(json.dumps(r.json(), indent=2))
    # print(r.json()['products'][0]['product_name'])  # Barcode Lookup API
    # print(r.json()['items'][0]['title'])  # UPC Item DB API
    print("-----" * 5 + "\n")


# =====END RESPONSE FUNCTIONS=====


# =====START QUERY FUNCTIONS=====


@DeprecationWarning
def query_upcdb(upc):
    """
    Queries the UPC Database API (wwww.upcdatabase.org - 100 requests per day)
    :param upc: the UPC code for the product
    """
    api_key = "73CC4578E54A4B678F76627BE5B05BBE"
    url = "https://api.upcdatabase.org/product/%s/%s" % (upc, api_key)
    print_response(url)


def query_barcodelookup(upc):
    """
    Queries the Barcode Lookup API (www.barcodelookup.com - 50 requests per day)
    :param upc: the UPC code for the product
    """
    api_key = "p22mxd4119y2fd54lo3exitq62v0ce"
    url = "https://api.barcodelookup.com/v2/products?barcode=%s&formatted=n&key=%s" % (upc, api_key)
    # print_response(url)  # Debug
    r = get_response(url).json()
    query_ombd(parse_upc_name(r['products'][0]['title']))
    # print(vars.data_buffer)  # Debug


def query_upcitemdp(upc):
    """
    Queries the UPC Item Database API (www.upcitemdp.com - 100 requests per day)
    :param upc: the UPC code for the product
    """
    url = "https://api.upcitemdb.com/prod/trial/lookup?upc=%s" % upc
    # print_response(url)  # Debug
    query_ombd(parse_upc_name(get_response(url).json()['items'][0]['title']))
    # print(vars.data_buffer)  # Debug


def query_barcode_apis(data):
    """
    Wrapper function for querying and handling all the API services.
    To add a UPC API service, create its "query function" and add it to the try-catch chain
    :param data: the UPC code
    :return returns if the upc was successfully scanned
    """
    # TODO: Try and make the try-catch chain cleaner
    try:
        # query_upcdb(data)
        query_barcodelookup(data)
        # query_upcitemdp(data)
        return True
    except ScanError:
        try:
            # query_barcodelookup(data)
            query_upcitemdp(data)
            return True
        except ScanError:
            return False


def query_ombd(title):
    """
    Queries the Open Movie Database API (www.omdb.com - 1000 calls per day)
    :param title: the title of the movie being queried
    """
    api_key = "47fec2f"  # 1000 calls per day
    url = "http://www.omdbapi.com/?t=%s&apikey=%s" % (title, api_key)
    # print_response(url)  # Debug
    try:
        parse_omdb_data(get_response(url).json())
        # print(vars.data_buffer)  # Debug
        return True
    except KeyError:
        print("-----INVALID TITLE!-----")
        return False

# =====END QUERY FUNCTIONS=====


# =====START PARSE FUNCTIONS=====


def parse_upc_name(name):
    """
    Parses information (if available) from the UPC API-supplied title and supplies a clean title for use by the OMDb API
    :param name: the title from the UPC API
    :return: the parsed title without any additional information
    """
    print(vars.data_buffer)
    index_psis = name.find('(')
    # print(index_psis)  # Debug
    index_bracket = name.find('[')
    # print(index_bracket)  # Debug
    if index_psis != -1 or index_bracket != -1:  # If extra information is found

        # ===Start Parenthesis Parsing===

        if index_bracket == -1:  # If there is no bracketed information
            title = name[:index_psis-1]  # Gets the title up to the extra data (excluding space)
            # print(title)  # Debug
            vars.data_buffer.update(Format=name[index_psis+1:name.find(')')])  # Adds the extra information to "type"
            # print(vars.data_buffer)  # Debug
            return title
        elif index_bracket > index_psis:  # If the brackets come after the parenthesis
            title = name[:index_psis - 1]  # Gets the title up to the parenthetical information (excluding space)
            info = name[index_psis + 1:name.find(')')] + " " + name[index_bracket + 1:name.find(']')]  # Stores the parenthetical and bracketed information
        else:  # The brackets come before the parenthesis
            title = name[:index_bracket - 1]  # Gets the title up to the extra data (excluding space)
            info = name[index_psis + 1:name.find(')')] + " " + name[index_bracket + 1:name.find(']')]  # Stores the parenthetical and bracketed information

        # ===End Parenthesis Parsing===

        # ===Start Bracket Parsing===

        if index_psis == -1:  # If there is no parenthetical information
            title = name[:index_bracket - 1]  # Gets the title up to the extra data (excluding space)
            # print(title)  # Debug
            vars.data_buffer.update(Format=name[index_bracket+1:name.find(']')])  # Adds the extra information to "type"
            # print(vars.data_buffer)  # Debug
            return title

        # ===End Bracket Parsing===

        # print(title)  # Debug
        # print(info)  # Debug
        vars.data_buffer.update(Format=info)
        # print(vars.data_buffer)  # Debug
        return title
    else:
        # print(name)  # Debug
        return name


def parse_omdb_data(data):
    """
    Parses data from the OMDb API JSON file into the data buffer stored in "vars"
    :param data: the JSON filed returned from the OMDb API service
    """
    json_fields = ['Title', 'Genre', 'Rated', 'Year', 'Runtime', 'Plot', 'Metascore']
    for field in json_fields:
        vars.data_buffer[field] = data[field]
    # vars.data_buffer.update({'title': data['Title'],
    #                          'genre': data['Genre'],
    #                          'rating': data['Rated'],
    #                          'year': data['Year'],
    #                          'runtime': data['Runtime'][:data['Runtime'].find(' ')],
    #                          'plot': data['Plot'],
    #                          'reviews': data['Metascore']})
    # print(vars.data_buffer)  # Debug


# =====END PARSE FUNCTIONS=====
