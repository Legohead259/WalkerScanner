import xml.etree.ElementTree as ET
from util import query_ombd, publish_to_xml, publish_to_txt
import vars

_source_file = "Datafiles/Movies_old.xml"
_dest_file = "Datafiles/Movies.xml"
fail_list = []
limit = 200
c = 0

tree = ET.parse(_source_file)
root = tree.getroot()

vars.reset_buffer()

for movie in root.findall("Movies"):
    if c >= limit:
        break
    title = movie[1].text
    index = title.find(", The")
    if index != -1:
        temp_str = title[:index]
        title = "The " + temp_str
    index = title.find(", A")
    if index != -1:
        temp_str = title[:index]
        title = "A " + temp_str
    # print(title)  # Debug

    if query_ombd(title):
        c += 1
        print(c)  # Debug
        type = movie[2].text
        vars.data_buffer.update(Type=type)
        format = movie[3].text
        vars.data_buffer.update(Format=format)
        root.remove(movie)
        tree.write(_source_file)
        publish_to_xml(_dest_file)
    else:
        publish_to_txt("Datafiles/failed titles.txt", title+"\n")
    vars.reset_buffer()
    # print(movie)  # Debug

# print(fail_list)  # Debug
# print(vars.data_buffer)  # Debug