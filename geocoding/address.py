import json
import urllib
import requests

def parse(response):
    response = json.loads(response)
    results = response['results']
    if not results:
        return None

    components = response['results'][0]['address_components']
    addr_tokens = {}
    for component in components:
        types = component['types']
        if 'street_number' in types:
            addr_tokens['street_number'] = component['long_name']
        elif 'route' in types:
            addr_tokens['street_name'] = component['long_name']
        elif 'locality' in types:
            addr_tokens['city'] = component['long_name']
        elif 'administrative_area_level_1' in types:
            addr_tokens['state'] = component['long_name']
        elif 'country' in types:
            addr_tokens['country'] = component['short_name']
        elif 'postal_code' in types:
            addr_tokens['postal_code'] = component['long_name']
    return map_address_to_tuple(addr_tokens)

def map_address_to_tuple(addr_tokens):
    street = None
    street_num = addr_tokens.get('street_number')
    if street_num:
        street = street_num

    street_name = addr_tokens.get('street_name')
    if street_name:
        if street:
            street += ' '
        else:
            street = ''
        street += street_name

    city = addr_tokens.get('city')
    state = addr_tokens.get('state')
    postal = addr_tokens.get('postal_code')
    country = addr_tokens.get('country')
    return street, city, state, postal, country

def geocode(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?' + urllib.urlencode({'address': address,
                                                                                   'key': 'AIzaSyC_BWr_m3f1OnclRlRBrQDaHoMvI0n9Loo'})
    response = requests.get(url)
    return response

def clean(address):
    response = geocode(address)
    return parse(response.text)


