import requests

url = "http://api.coinlayer.com/"
api_key = "9c34686dbd6c309b03fa6cc0c6399dc2"

def get_crypto_data():
    crypto_data = requests.get(url + "live?access_key=" + api_key).json()  # Get the data from the API
    return crypto_data

def organize_crypto_data(crypto_data):
    organized_data = {}  # Create an empty dictionary to store the organized data
    for crypto in crypto_data['rates']:  # Loop through the rates in the data
        organized_data[crypto] = crypto_data['rates'][crypto]  # Add the rate to the dictionary
    return organized_data