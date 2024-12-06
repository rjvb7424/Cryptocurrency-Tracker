import requests
import tkinter as tk
import time

url = "http://api.coinlayer.com/"
api_key = "9c34686dbd6c309b03fa6cc0c6399dc2"

previous_data = {}

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

def round_crypto_data(selected_data):
    for crypto in selected_data:
        selected_data[crypto] = round(selected_data[crypto], 2)
    return selected_data

def get_current_time():
    current_time = time.localtime()
    return current_time

def current_crypto_data():
    global previous_data

    crypto_data = get_crypto_data()
    organized_data = organize_crypto_data(crypto_data)
    selected_data = select_crypto_data(organized_data)
    selected_data = round_crypto_data(selected_data)

    comparison = {}
    for crypto in selected_data:
        if crypto in previous_data:
            if selected_data[crypto] > previous_data[crypto]:
                comparison[crypto] = "↑" 
            elif selected_data[crypto] < previous_data[crypto]:
                comparison[crypto] = "↓" 
            else:
                comparison[crypto] = "-" 
        else:
            comparison[crypto] = "-"
    previous_data = selected_data
    return selected_data, comparison

root = tk.Tk()
root.title("Crypto Prices")
root.geometry("400x300")

title_label = tk.Label(root, text="Crypto Prices", font=("Helvetica", 24))
title_label.pack()
last_updated_label = tk.Label(root, text="Last Updated: --:--")
last_updated_label.pack()

empty_label = tk.Label(root, text="--------------------------------")
empty_label.pack()

crypto_labels = {}

for crypto in ['BTC', 'ETH', 'XRP', 'LTC', 'BCH']:
    label = tk.Label(root, text=f"{crypto}: $--")
    label.pack()
    crypto_labels[crypto] = label

def update_prices():
    selected_data, comparison = current_crypto_data()

    for crypto in selected_data:
        crypto_labels[crypto].config(text=f"{crypto}: ${selected_data[crypto]} {comparison[crypto]}")
    current_time = get_current_time()
    last_updated_label.config(text="Last Updated: {:02d}:{:02d}".format(current_time.tm_hour, current_time.tm_min))

    root.after(100000, update_prices)  
update_prices()

root.mainloop()