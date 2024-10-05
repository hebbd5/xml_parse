import sys
from loguru import logger
import regex as re
import json

## Functions
def parse_entity(entity):
    
    """
    Given an XML line of sanction data for an individual,
    populates a dictionary with useful information.
    
    Returns the dictionary.
    """
    
    def format_name(entity_name):
    
        """
        Standardize the format for entity names retrieved from "formattedFullName"  
        """
        
        # Arrange name based on comma location, if present
        if ", " in entity_name:
            name_parts = entity_name.split(", ")
            entity_name = f"{name_parts[1]} {name_parts[0]}"
        
        # Apply title-case formatting
        entity_name = entity_name.title()
        
        # Capitalize any parenthetical text
        def capitalize(match):
            return match.group(1) + match.group(2).upper() + match.group(3)
        
        pattern = r'(\()([^\)]+)(\))'
        entity_name = re.sub(pattern, capitalize, entity_name)
        
        return entity_name



    entity_dict = {
        "name": "",
        "entity_type": "",
        "sanctions_lists": [],
        "sanctions_programs": [],
        "sanctions_types": "",
        "legal_authorities": [],
        "aliases": [],
        # "relationships": [],
        # "identity_documents": [],
        # "addresses": [],             # Not currently implemented
        # "features": [],
        # "remarks": "",
        # "title":, ""
    }
    
    
    ## Entity Type
    entity_dict["entity_type"] = entity["generalInfo"]["entityType"]


    ## Name and aliases
    name_element = entity["names"]["name"]
    
    if type(name_element) == dict:
        
        translation_element = name_element["translations"]["translation"]
        
        if type(translation_element) == dict:
            entity_dict["name"] = format_name(translation_element["formattedFullName"])
            
        elif type(translation_element) == list:
            for trans in translation_element:
                if trans["script"] == "Latin":
                    entity_dict["name"] = format_name(trans["formattedFullName"])
                         
    ### If element is a list, aliases are present 
    elif type(name_element) == list:
        
        for name in name_element:
            if name["isPrimary"] == "true":
                translation_element = name["translations"]["translation"]

                if type(translation_element) == dict:
                    entity_dict["name"] = format_name(translation_element["formattedFullName"])
                    
                elif type(translation_element) == list:
                    for trans in translation_element:
                        if trans["script"] == "Latin":
                            entity_dict["name"] = format_name(trans["formattedFullName"])
            
    ## Add non-primary names as aliases  
            elif name["isPrimary"] == "false":
                
                ##### Create an alias dict value if none exist 
                if "aliases" not in entity_dict.keys():
                    entity_dict["aliases"] = []
                
                translation_element = name["translations"]["translation"]
 
                if type(translation_element) == dict:
                    alias = format_name(translation_element["formattedFullName"])

                elif type(translation_element) == list:
                    for trans in translation_element:
                        if trans["script"] == "Latin":
                            alias = format_name(trans["formattedFullName"])
                                
                entity_dict["aliases"].append(alias)
        
        
    logger.debug(f"Parsing entity: {entity_dict["name"]}")
    
    
    ## Sanctions list, program, type, legal authority
    entity_dict["sanctions_lists"] = entity["sanctionsLists"]["sanctionsList"]
    entity_dict["sanctions_types"] = entity["sanctionsTypes"]["sanctionsType"]
    entity_dict["sanctions_programs"] = entity["sanctionsPrograms"]["sanctionsProgram"]

    legal_authorities = entity["legalAuthorities"]["legalAuthority"]
    if legal_authorities != None:
        entity_dict["legal_authorities"] = legal_authorities
    else: entity_dict["legal_authorities"] = ""
 
 
    ## Remarks
    if "remarks" in entity["generalInfo"].keys():
        entity_dict["remarks"] = entity["generalInfo"]["remarks"]
        
    
    ## Title
    if "title" in entity["generalInfo"].keys():
        entity_dict["title"] = entity["generalInfo"]["title"]
 

    ## Relationships
    if "relationships" in entity.keys():
        
        if entity["relationships"] != None:
            
            relationships = entity["relationships"]["relationship"]
            
            if type(relationships) == dict:
                
                rel_type = relationships["type"]
                rel_entity = relationships["relatedEntity"]
                
                if rel_entity != None:
                    
                    rel_entity = format_name(rel_entity)
                    
                    if entity_dict["relationships"]:
                        entity_dict["relationships"].append([rel_type, rel_entity])
                    else:
                        entity_dict["relationships"] = [[rel_type, rel_entity]]
                
            elif type(relationships) == list: 
                
                for rel in relationships:
                    rel_type = rel["type"]
                    rel_entity = rel["relatedEntity"]
                    
                    if rel_entity != None:
                        
                        rel_entity = format_name(rel_entity)
                        
                        if entity_dict["relationships"]:
                            entity_dict["relationships"].append([rel_type, rel_entity])
                        else:
                            entity_dict["relationships"] = [[rel_type, rel_entity]]
                    


    ## Identity Documents
    if "identityDocuments" in entity.keys():
        
        if entity["identityDocuments"] != None:

            entity_dict["identity_documents"] = []
            id_docs = entity["identityDocuments"]["identityDocument"]
            
            if type(id_docs) == dict:
                
                id_type = id_docs["type"]
                id_name = id_docs["name"]
                id_docno = id_docs["documentNumber"]
                id_valid = id_docs["isValid"]
                
                if "issuingCountry" in id_docs.keys(): 
                    id_issuer = id_docs["issuingCountry"]
                else: id_issuer = ""
                
                entity_dict["identity_documents"].append([id_type, id_name, id_docno, id_valid, id_issuer])
                
            elif type(id_docs) == list: 
                
                for id in id_docs:
                    
                    id_type = id["type"]
                    id_name = id["name"]
                    id_docno = id["documentNumber"]
                    id_valid = id["isValid"]
                    
                    if "issuingCountry" in id.keys(): 
                        id_issuer = id["issuingCountry"]
                    else: id_issuer = ""
                
                    entity_dict["identity_documents"].append([id_type, id_name, id_docno, id_valid, id_issuer])

            
    ## Features
    if "features" in entity.keys():
        
        entity_dict["features"] = []
        features = entity["features"]["feature"]
        
        if type(features) == dict:
            feature_type = features["type"]
            feature_value = features["value"]
            
            # if "valueDate" in features.keys():
            #     feature_date_from = features["documentNumber"]
            # else: feature_date_from = ""
            
            entity_dict["features"].append([feature_type, feature_value])
            
        elif type(features) == list: 
            
            for feature in features:
                feature_type = feature["type"]
                feature_value = feature["value"]
                entity_dict["features"].append([feature_type, feature_value])


    return entity_dict

def json_gen(entity_data):
    
    """
    Accepts an XML of US OFAC sanctions information, returning a csv of relationship nodes and edges 
    """
     
    ## Extract entity data as dicts
    entity_dicts = [parse_entity(entity) for entity in entity_data]
    
    return entity_dicts