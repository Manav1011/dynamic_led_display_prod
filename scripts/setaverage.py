import requests

def make_api_call(url):
    try:
        # Make a GET request
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the response content
            print("API Response:")
            print(response.json())  # Assuming the response is in JSON format
        else:
            # Print an error message
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example API URL
api_url = "http://10.81.7.25:8000/set_yesterday_average"

# Make the API call
make_api_call(api_url)