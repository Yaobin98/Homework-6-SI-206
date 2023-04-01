import requests
import json
import unittest
import os

###########################################
# Your name:                              #
# Who you worked with:                    #
###########################################

def load_json(filename):
    '''
    Loads a JSON cache from filename if it exists

    Parameters
    ----------
    filename: string
        the name of the cache file to read in

    Returns
    -------
    dict
        if the cache exists, a dict with loaded data
        if the cache does not exist, an empty dict
    '''
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    else:
        return {}   
    

def write_json(filename, dict):
    '''
    Encodes dict into JSON format and writes
    the JSON to filename to save the search results

    Parameters
    ----------
    filename: string
        the name of the file to write a cache to
    
    dict: cache dictionary

    Returns
    -------
    None
        does not return anything
    '''  
    with open(filename, "w") as file:
        json.dump(dict, file)


def get_swapi_info(url, params=None):
    '''
    Check whether the 'params' dictionary has been specified. Makes a request to access data with 
    the 'url' and 'params' given, if any. If the request is successful, return a dictionary representation 
    of the decoded JSON. If the search is unsuccessful, print out "Exception!" and return None.

    Parameters
    ----------
    url (str): a url that provides information about entities in the Star Wars universe.
    params (dict): optional dictionary of querystring arguments (default value is 'None').
        

    Returns
    -------
    dict: dictionary representation of the decoded JSON.
    '''
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except:
        print("Exception!")
        return None

def cache_all_pages(people_url, filename):
    '''
    1. Checks if the page number is found in the dict return by `load_json`
    2. If the page number does not exist in the dictionary, it makes a request (using get_swapi_info)
    3. Add the data to the dictionary (the key is the page number (Ex: page 1) and the value is the results).
    4. Write out the dictionary to a file using write_json.
    
    Parameters
    ----------
    people_url (str): a url that provides information about the 
    characters in the Star Wars universe (https://swapi.dev/api/people).
    filename(str): the name of the file to write a cache to
        
    '''
    file = load_json(filename)
    page_number = 1
    while people_url != None:
        if page_number not in file:
            data = get_swapi_info(people_url)
            if data != None:
                results = data.get("results", [])
                file[f"page {page_number}"] = results
                write_json(filename, file)    
        page_number += 1
        people_url = data.get("next")

  

def get_starships(filename):
    '''
    Access the starships url for each character (if any) and pass it to the get_swapi_info function 
    to get data about a person's starship.
    
    Parameter
    ----------
    filename(str): the name of the cache file to read in 
    
    Returns
    -------
    dict: dictionary with the character's name as a key and a list of the name their 
    starships as the value
    '''
    
    starships_dict = {}
    file = load_json(filename)
    for page_number, result in file.items():
        for person in result:
            person_name = person["name"]
            starships_urls = person.get('starships', [])
            starship_name = []
            for starships_url in starships_urls:
                starships_result = get_swapi_info(starships_url)
                if starships_result != None:
                    starship_name.append(starships_result["name"])
            if len(starship_name) != 0:
                starships_dict[person_name] = starship_name
    return starships_dict
                     
#################### EXTRA CREDIT ######################

def calculate_bmi(filename):
    '''
    Calculate each character's Body Mass Index (BMI) if their height and mass is known. With the metric 
    system, the formula for BMI is weight in kilograms divided by height in meters squared. 
    Since height is commonly measured in centimeters, an alternate calculation formula, 
    dividing the weight in kilograms by the height in centimeters squared, and then multiplying 
    the result by 10,000, can be used.

    Parameter
    ----------
    filename(str): the name of the cache file to read in 
    
    Returns
    -------
    dict: dictionary with the name as a key and the BMI as the value
    '''

    file = load_json(filename)
    bmi_dict = {}
    for page, result in file.items():
        for character in result:
            name = character["name"]
            height = character["height"].replace(',', '')
            mass = character["mass"].replace(',', '')
            if height == "unknown" or mass == "unknown":
                continue
            height = float(height)
            mass = float(mass)
            bmi = (mass /height**2 )*10000
            bmi_dict[name] = round(bmi,2)

    return bmi_dict





class TestHomework6(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.filename = dir_path + '/' + "swapi_people.json"
        self.cache = load_json(self.filename)
        self.url = "https://swapi.dev/api/people"

    def test_write_json(self):
        write_json(self.filename, self.cache)
        dict1 = load_json(self.filename)
        self.assertEqual(dict1, self.cache)

    def test_get_swapi_info(self):
        people = get_swapi_info(self.url)
        tie_ln = get_swapi_info("https://swapi.dev/api/vehicles", {"search": "tie/ln"})
        self.assertEqual(type(people), dict)
        self.assertEqual(tie_ln['results'][0]["name"], "TIE/LN starfighter")
        self.assertEqual(get_swapi_info("https://swapi.dev/api/pele"), None)
    
    def test_cache_all_pages(self):
        cache_all_pages(self.url, self.filename)
        swapi_people = load_json(self.filename)
        self.assertEqual(type(swapi_people['page 1']), list)

    def test_get_starships(self):
        starships = get_starships(self.filename)
        self.assertEqual(len(starships), 19)
        self.assertEqual(type(starships["Luke Skywalker"]), list)
        self.assertEqual(starships['Biggs Darklighter'][0], 'X-wing')

    def test_calculate_bmi(self):
        bmi = calculate_bmi(self.filename)
        self.assertEqual(len(bmi), 59)
        self.assertAlmostEqual(bmi['Greedo'], 24.73)
    
if __name__ == "__main__":
    unittest.main(verbosity=2)

    


