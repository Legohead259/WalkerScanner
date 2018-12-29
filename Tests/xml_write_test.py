import xml.etree.ElementTree as ET

_filename = "testwrite.xml"

try:
    tree = ET.parse(_filename)
    root = tree.getroot()
except ET.ParseError:
    root = ET.Element('database')
    tree = ET.ElementTree(root)

data_buffer = {'Title': "Star Wars",
                'Genre': "Musical, Comedy, Fantasy, Cartoon",
                'Rated': "PG",
                'Type': "BR&DVD&DC",
                'Format': "Widescreen",
                'Year': "2016",
                'Runtime': "137 mins",
                'Plot': "*Insert plot summary*",
                'Metascore': "73"}

movies = ET.SubElement(root, 'Movies')

for field in data_buffer:
    ET.SubElement(movies, field).text = data_buffer[field]

tree.write(_filename)
