import googlemaps
from googlemaps.exceptions import InvalidRequest
import json

# Set up the API client
api_key = 'AIzaSyAs23gW_71NGisb2N1CzsfeXDsoafe1h2Y'
gmaps = googlemaps.Client(api_key)

# Define the place ID for the location you want to get reviews for
place_id = 'ChIJ0Zk7Uz8sTIYR4xsLxj0X8Mk'

# Define the fields you want to retrieve for each review
review_fields = ['rating', 'text', 'time']

# Define a function to handle pagination of results
def get_all_results(results, next_page_token):
    while next_page_token:
        try:
            next_results = gmaps.places(place_id, page_token=next_page_token, fields=['reviews'])
            results.extend(next_results['reviews'])
            next_page_token = next_results.get('next_page_token')
        except InvalidRequest:
            # Wait and retry if we hit the API rate limit
            time.sleep(2)
            continue
    return results

# Call the Places API to retrieve the first page of results
first_results = gmaps.places(place_id, fields=['reviews'])
all_results = first_results.get('reviews', [])

# Handle pagination of results if there are multiple pages
next_page_token = first_results.get('next_page_token')
all_results = get_all_results(all_results, next_page_token)

# Print out the reviews in a formatted JSON string
print(json.dumps(all_results, indent=2))
