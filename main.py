import requests
import tkinter as tk
import time

url = "https://api.coinlayer.com/"
api_key = "9c34686dbd6c309b03fa6cc0c6399dc2"

previous_data = {}

def get_crypto_data():
    try:
        response = requests.get(url + "live?access_key=" + api_key)
        response.raise_for_status()
        crypto_data = response.json()
        if 'error' in crypto_data:
            print("API Error:", crypto_data['error'])
            return None
        return crypto_data
    except requests.RequestException as e:
        print("Network Error:", e)
        return None

def organize_crypto_data(crypto_data):
    if crypto_data and 'rates' in crypto_data:
        return crypto_data['rates']
    return {}

def select_crypto_data(organized_data):
    selected_data = {}
    selected_cryptos = ['BTC', 'ETH', 'XRP', 'LTC', 'BCH']
    for crypto in selected_cryptos:
        # Safely get the price, defaulting to None if not found
        selected_data[crypto] = organized_data.get(crypto, None)
    return selected_data

def round_crypto_data(selected_data):
    for crypto in selected_data:
        if selected_data[crypto] is not None:
            selected_data[crypto] = round(selected_data[crypto], 2)
        else:
            # If no data is found for that crypto, set it to 0.0 for display purposes
            selected_data[crypto] = 0.0
    return selected_data

def get_current_time():
    current_time = time.localtime()
    return current_time

def current_crypto_data():
    global previous_data

    crypto_data = get_crypto_data()
    if crypto_data is None:
        selected_data = previous_data if previous_data else {c: 0.0 for c in ['BTC', 'ETH', 'XRP', 'LTC', 'BCH']}
        comparison = {c: "-" for c in selected_data}
        return selected_data, comparison

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
    previous_data = selected_data
    return selected_data, comparison

root = tk.Tk()
root.title("Cryptocurrency Tracker")

title_label = tk.Label(root, text="Crypto Prices", font=("Helvetica", 24))
title_label.pack()
last_updated_label = tk.Label(root, text="Last Updated: --:--:--")
last_updated_label.pack()

separator_label_top = tk.Label(root, text="--------------------------------")
separator_label_top.pack()

crypto_labels = {}
for crypto in ['BTC', 'ETH', 'XRP', 'LTC', 'BCH']:
    label = tk.Label(root, text=f"{crypto}: $--")
    label.pack()
    crypto_labels[crypto] = label

separator_label_bottom = tk.Label(root, text="--------------------------------")
separator_label_bottom.pack()

info_label = tk.Label(root, text="Prices are updated every 10 seconds.")
info_label.pack()

def update_prices():
    selected_data, comparison = current_crypto_data()

    for crypto in selected_data:
        symbol = comparison[crypto]
        price_text = f"{symbol} {crypto}: ${selected_data[crypto]}"
        if symbol == "↑":
            crypto_labels[crypto].config(text=price_text, fg="green")
        elif symbol == "↓":
            crypto_labels[crypto].config(text=price_text, fg="red")
        else:
            crypto_labels[crypto].config(text=price_text, fg="white")

    current_time = get_current_time()
    last_updated_label.config(
        text="Last Updated: {:02d}:{:02d}:{:02d}".format(current_time.tm_hour, current_time.tm_min, current_time.tm_sec)
    )
    root.after(10000, update_prices)

update_prices()

root.mainloop()