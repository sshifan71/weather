from django.shortcuts import render
import json
import requests
import os

def index(request):
    data = {}
    if request.method == 'POST':
        longitude = request.POST['lon']
        latitude = request.POST['lat']
        print(f"Received longitude: {longitude}, latitude: {latitude}")  # Debug: print coordinates

        try:
            # Validate latitude and longitude values
            lat = float(latitude)
            lon = float(longitude)
            if not (-90 <= lat <= 90):
                raise ValueError("Invalid latitude value. It should be between -90 and 90.")
            if not (-180 <= lon <= 180):
                raise ValueError("Invalid longitude value. It should be between -180 and 180.")

            api_key = os.getenv('WEATHER_API_KEY')
            if not api_key:
                raise ValueError("No API key found in environment variables.")
            url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
            print(f"API URL: {url}")  # Debug: print API URL

            response = requests.get(url)
            print(f"API response status code: {response.status_code}")  # Debug: print response status code

            # Check for a successful response
            if response.status_code == 200:
                list_of_data = response.json()
                print(f"API response data: {list_of_data}")  # Debug: print API response data

                if 'sys' in list_of_data and 'coord' in list_of_data and 'main' in list_of_data:
                    data = {
                        "coordinate": f"{list_of_data['coord']['lon']}, {list_of_data['coord']['lat']}",
                        "temp": f"{list_of_data['main']['temp']}K",
                        "pressure": str(list_of_data['main']['pressure']),
                        "humidity": str(list_of_data['main']['humidity']),
                    }
                    print(data)
                else:
                    data = {"error": "Incomplete data received from the API."}
                    print(data)
            else:
                error_message = response.json().get('message', 'Unknown error occurred.')
                print(f"Error message from API: {error_message}")  # Debug: print error message
                data = {"error": f"API Error: {response.status_code} - {error_message}"}

        except ValueError as e:
            print(f"ValueError: {e}")  # Debug: print value error
            data = {"error": str(e)}
        except requests.HTTPError as e:
            print(f"HTTPError: {e.response.status_code} - {e.response.reason}")  # Debug: print HTTP error
            data = {"error": f"HTTPError: {e.response.status_code} - {e.response.reason}"}
        except requests.RequestException as e:
            print(f"RequestException: {e}")  # Debug: print request exception
            data = {"error": f"RequestException: {e}"}
        except json.JSONDecodeError:
            print("Error decoding JSON from API response.")  # Debug: print JSON decode error
            data = {"error": "Error decoding JSON from API response."}
        except Exception as e:
            print(f"Exception: {str(e)}")  # Debug: print any other exception
            data = {"error": str(e)}

    return render(request, "index.html", {'data': data})
