import os
import json
from bs4 import BeautifulSoup

## Designate input XLM file
xml_filepath = "Datasets/IRGC_sanctions.xml"


## Convert XML soup to JSON format
def xml_to_json(element):
    """
    Recursively parses XML soup, returning as JSON format 
    """
    
    if isinstance(element, str):
        return element
    
    if not element.contents:
        return element.string
    
    result = {}
    
    for child in element.children:
        
        if isinstance(child, str):
            continue
        
        if child.name not in result:
            result[child.name] = xml_to_json(child)
            
        else:
            if not isinstance(result[child.name], list):
                result[child.name] = [result[child.name]]
            result[child.name].append(xml_to_json(child))
            
    ### Directly capture text nodes without 'text' key
    if element.string and element.string.strip():
        return element.string.strip()
    
    return result





### Execute with main 
def main(input_file):
    
    with open(xml_filepath, "r") as file:
        xml_data = file.read()

    soup = BeautifulSoup(xml_data, features='xml')
    
    entity_json = xml_to_json(soup)
    