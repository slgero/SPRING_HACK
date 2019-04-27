
import xml.etree.ElementTree as ET
tree = ET.parse('main.xml')
root = tree.getroot()



for child in root.findall('company'):
    data ={
        "name": child.find('name').text
    }
    print(data["name"])
#py main.py
