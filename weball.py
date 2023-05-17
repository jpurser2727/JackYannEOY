import googlemaps
from googlemaps.exceptions import ApiError
import json
import time

# Set up the API client
api_key = 'AIzaSyAs23gW_71NGisb2N1CzsfeXDsoafe1h2Y'
gmaps = googlemaps.Client(api_key)

# Define the place ID for the location you want to get reviews for
place_id = 'ChIJ0Zk7Uz8sTIYR4xsLxj0X8Mk'

# Define a function to handle pagination of results
def get_all_reviews(results, next_page_token):
    while next_page_token:
        try:
            next_results = gmaps.place(place_id, fields=['reviews'], page_token=next_page_token)
            if 'reviews' in next_results['result']:
                results.extend(next_results['result']['reviews'])
            next_page_token = next_results.get('next_page_token')
        except ApiError as e:
            # Handle API request errors
            print(f"API Error: {e}")
            break
        # Wait for a few seconds before making the next request
        time.sleep(2)
    return results

# Call the Places API to retrieve the first page of results
first_results = gmaps.place(place_id, fields=['reviews'])
result = first_results['result']
all_reviews = result.get('reviews', [])

# Handle pagination of results if there are multiple pages
next_page_token = result.get('next_page_token')
all_reviews = get_all_reviews(all_reviews, next_page_token)

# Print out the reviews in a formatted JSON string
print(json.dumps(all_reviews, indent=2))
