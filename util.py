import csv
import json
import requests
from errors import InvalidData, Forbidden, NotFound, ExceedLimit, ScanError, raise_error
import vars
import xml.etree.ElementTree as ET


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


def query_upcdb(upc):
    """
    Queries the UPC Database API (wwww.upcdatabase.org - 100 requests per day)
    :param upc: the UPC code for the product
    :return if the UPC was successfully queried and the movie dta populated
    """
    api_key = "04B5A7D78FD480752FAB0382964D7AF7"
    url = "https://api.upcdatabase.org/product/%s/%s" % (upc, api_key)
    # print_response(url)  # Debug
    return query_ombd(parse_upc_name(get_response(url).json()['title']))


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
        data = get_response(url).json()
        json_fields = ['Title', 'Genre', 'Rated', 'Year', 'Runtime', 'Plot', 'Metascore']
        for field in json_fields:
            vars.data_buffer[field] = data[field]
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

    # ===START TYPE PARSING===

    temp = name.lower()
    temp_format = ""
    if temp.find("blu-ray") != -1:
        temp_format += "BR"
    if temp.find("4k") != -1:
        if temp_format != "":
            temp_format += "&"
        temp_format += "4K"
    if temp.find("dvd") != -1:
        if temp_format != "":
            temp_format += "&"
        temp_format += "DVD"
    if temp.find("digital copy"):
        if temp_format != "":
            temp_format += "&"
        temp_format += "DC"
    vars.data_buffer.update(Format=temp_format)

    # ===END TYPE PARSING===

    # ===START PARSING TITLE===

    temp_name = ""
    parsis_index = name.find("(")
    bracket_index = name.find("[")

    if parsis_index != -1:
        # print(parsis_index)  # Debug
        temp_name = name.replace(name[parsis_index-1:name.find(')')+1], "")
    if bracket_index != -1:
        temp_name = name.replace(temp_name[bracket_index-1:temp_name.find(']')+1], "")

    # print(temp_name)  # Debug
    return temp_name

    # ===END PARSING TILE===


# =====END PARSE FUNCTIONS=====


# =====START PUBLISH FUNCTIONS=====


@DeprecationWarning
def publish_to_csv():
    with open('data.csv', 'a', newline="") as csv_file:
        writer = csv.writer(csv_file, dialect='excel')
        writer.writerow(vars.data_buffer.values())


def publish_to_xml(filename):
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
    except ET.ParseError:
        root = ET.Element('database')
        tree = ET.ElementTree(root)

    movies = ET.SubElement(root, 'Movies')

    for field in vars.data_buffer:
        ET.SubElement(movies, field).text = vars.data_buffer[field]

    tree.write(filename)


def publish_to_txt(filename, data):
    with open(filename, 'a') as fail_text:
        fail_text.write(data)


# =====END PUBLISH FUNCTIONS=====
