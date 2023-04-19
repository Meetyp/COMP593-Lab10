'''
Library for interacting with the PokeAPI.
https://pokeapi.co/
'''
import requests
import image_lib
import os

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def main():
    # Test out the get_pokemon_into() function
    # Use breakpoints to view returned dictionary
    # poke_info = get_pokemon_info("Rockruff")
    # get_pokemon_names()
    dowload_pokemon_artwork(123, r'c:/temp')
    return

def get_pokemon_info(pokemon_name):
    """Gets information about a specified Pokemon from the PokeAPI.

    Args:
        pokemon_name (str): Pokemon name (or Pokedex number)

    Returns:
        dict: Dictionary of Pokemon information if successful Otherwise None
    """
    # Clean the Pokemon name parameter by:
    # - Converting to a string object,
    # - Removing leading and trailing whitespace, and
    # Converting to all lowercase letters
    pokemon_name = str(pokemon_name).strip().lower()

    # Build the clean URL for the GET request
    url= POKE_API_URL + pokemon_name

    # Send GET request for Pokemon info
    print (f'Getting information for {pokemon_name}...', end='')
    resp_msg = requests.get(url)

    # Check if request was successful
    if resp_msg.status_code == requests.codes.ok:
        print('success')
        # Return dictionary of Pokemon info
        return resp_msg.json()
    else:
        print('failure')
        print (f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
        return
    
def get_pokemon_names(offset=0, limit=100000):

    query_params = {
        "limit" : limit,
        "offset" : offset
    }

    # Send GET requests for pokemon names
    print(f'Getting list of Pokemon names...', end='')
    resp_msg = requests.get(POKE_API_URL, query_params)

    # Check if request was successful
    if resp_msg.status_code == requests.codes.ok:
        print('success')
        # Return dictionary of Pokemon info
        resp_dict =  resp_msg.json()
        pokemon_names = [p['name'] for p in resp_dict['results']]
        return pokemon_names
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
        return
    
def dowload_pokemon_artwork(pokemon_name, folder_path):
    
    poke_info = get_pokemon_info(pokemon_name)
    if poke_info is None:
        return False

    poke_image_url = poke_info['sprites']['other']['official-artwork']['front_default']

    image_data = image_lib.download_image(poke_image_url)
    if image_data is None:
        return False

    # Determine the path at which to save the Image file
    image_ext = poke_image_url.split('.')[-1]
    file_name = f'{poke_info["name"]}.{image_ext}'
    file_path = os.path.join(folder_path, file_name)

    if image_lib.save_image_file(image_data, file_path):
        return file_path
    
    return False

if __name__ == '__main__':
    main()