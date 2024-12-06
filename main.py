import requests
import tkinter as tk

url = "http://api.coinlayer.com/"
api_key = "9c34686dbd6c309b03fa6cc0c6399dc2"

def get_crypto_data():
    crypto_data = requests.get(url + "live?access_key=" + api_key).json()
    return crypto_data

def organize_crypto_data(crypto_data):
    organized_data = {} 
    for crypto in crypto_data['rates']:
        organized_data[crypto] = crypto_data['rates'][crypto]
    return organized_data

def select_crypto_data(organized_data):
    selected_data = {}
    selected_cryptos = ['BTC', 'ETH', 'XRP', 'LTC', 'BCH']
    for crypto in selected_cryptos:
        selected_data[crypto] = organized_data[crypto]
    return selected_data

root = tk.Tk()
root.title("Crypto Prices")
root.geometry("400x200")
title_label = tk.Label(root, text="Crypto Prices", font=("Helvetica", 24))
title_label.pack()
empty_lable = tk.Label(root, text="")
empty_lable.pack()

crypto_data = get_crypto_data()
organized_data = organize_crypto_data(crypto_data)
selected_data = select_crypto_data(organized_data)

bitcoin_label = tk.Label(root, text="Bitcoin: $" + str(selected_data['BTC']))
bitcoin_label.pack()
ethereum_label = tk.Label(root, text="Ethereum: $" + str(selected_data['ETH']))
ethereum_label.pack()
xrp_label = tk.Label(root, text="XRP: $" + str(selected_data['XRP']))
xrp_label.pack()
litecoin_label = tk.Label(root, text="Litecoin: $" + str(selected_data['LTC']))
litecoin_label.pack()
bitcoin_cash_label = tk.Label(root, text="Bitcoin Cash: $" + str(selected_data['BCH']))
bitcoin_cash_label.pack()

root.mainloop()