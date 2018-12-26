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
    Wrapper function for printing the ENTIRE response of the url query.
    Used for DEBUG purposes only
    :param url: the query url provided by the API call function
    """
    r = get_response(url)

    print("-----" * 5)
    print(json.dumps(r.json(), indent=2))
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
    Automatically populates the data buffer with the queried information
    :param upc: the UPC code for the product
    """
    api_key = "p22mxd4119y2fd54lo3exitq62v0ce"
    url = "https://api.barcodelookup.com/v2/products?barcode=%s&formatted=n&key=%s" % (upc, api_key)
    # query_ombd(parse_upc_name(get_response(url).json()['products'][0]['title']))
    print_response(url)


def query_upcitemdp(upc):
    """
    Queries the UPC Item Database API (www.upcitemdp.com - 100 requests per day)
    Automatically populates the data buffer with the queried information
    :param upc: the UPC code for the product
    """
    url = "https://api.upcitemdb.com/prod/trial/lookup?upc=%s" % upc
    query_ombd(parse_upc_name(get_response(url).json()['items'][0]['title']))
    # print_response(url)  # Debug


def query_barcode_apis(data):
    """
    Wrapper function for querying and handling all the API services.
    To add a UPC API service, create its "query function" and add it to the try-catch chain
    :param data: the UPC code
    :return returns if the upc was successfully scanned
    """
    # TODO: Try and make the try-catch chain cleaner
    try:  # Try to query Barcode Lookup API with the UPC code
        query_barcodelookup(data)
        return True
    except ScanError:  # Any issue with scanning, try to query UPC Item Db API
        print("FAILED")
        # try:
        #     query_upcitemdp(data)
        #     return True
        # except ScanError:  # Any issue with scanning, report scanning failed
        #     return False


def query_ombd(title):
    """
    Queries the Open Movie Database API (www.omdb.com - 1000 calls per day)
    Automatically populates the data buffer with the queried information
    :param title: the title of the movie being queried
    :return if the title was successfully queried
    """
    api_key = "47fec2f"  # 1000 calls per day
    url = "http://www.omdbapi.com/?t=%s&apikey=%s" % (title, api_key)
    try:  # Try to query OMBd with the supplied title
        parse_omdb_data(get_response(url).json())
        return True
    except KeyError:  # Title supplied is incorrect
        print(vars.data_buffer["Title"])  # Debug
        print("-----INVALID TITLE!-----")
        return False


# =====END QUERY FUNCTIONS=====


# =====START PARSE FUNCTIONS=====


def parse_upc_name(name):
    """
    Parses information (if available) from the UPC API-supplied title and supplies a clean title for use by the OMDb API
    Automatically populates the "Format" field of the data buffer with any parsed information
    :param name: the title from the UPC API
    :return: the parsed title without any additional information for use by OMDb API
    """
    index_psis = name.find('(')  # First index of the parenthetical information. Should only be one such instance
    index_bracket = name.find('[')  # First index of the bracketed information. Should only be one such instance
    if index_psis != -1 or index_bracket != -1:  # If extra information is found

        # ===Start Parenthesis Parsing===

        if index_bracket == -1:  # If there is no bracketed information
            title = name[:index_psis-1]  # Gets the title up to the extra data (excluding space)
            vars.data_buffer.update(Format=name[index_psis+1:name.find(')')])  # Adds the extra information to "Format"
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
            vars.data_buffer.update(Format=name[index_bracket+1:name.find(']')])  # Adds the extra information to "Format"
            return title

        # ===End Bracket Parsing===

        vars.data_buffer.update(Format=info)
        return title
    else:  # There are no parenthesis or brackets for extra information
        return name


def parse_omdb_data(data):
    """
    Parses data from the OMDb API JSON file into the data buffer
    :param data: the JSON filed returned from the OMDb API service
    """
    print(vars.data_buffer["Title"])
    json_fields = ['Title', 'Genre', 'Rated', 'Year', 'Runtime', 'Plot', 'Metascore']
    for field in json_fields:
        vars.data_buffer[field] = data[field]


# =====END PARSE FUNCTIONS=====
