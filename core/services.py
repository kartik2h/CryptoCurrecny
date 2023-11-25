from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from requests import Request, Session
import requests
import matplotlib.pyplot as plt
import os
from django.conf import settings
from .models import Cryptocurrency

from django.http import HttpResponse


def get_cryptocurrency_data(currency='USD'):
    # Fetch data from an API
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '100',
        'convert': currency
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '5bd81282-4bee-4ce6-8267-ce6b66e87cdc',
    }

    session = Session()
    session.headers.update(headers)

    try:

        json = requests.get(url, params=parameters, headers=headers).json()
        coins = json['data']
        # print(coins)
        # for d in coins:
        #     print(d['symbol'], end=' ')
        #     print(d['quote']['INR']['price'], end=' ')
        #     print(d['quote']['INR']['percent_change_1h'], end=' ')
        #     print(d['quote']['INR']['percent_change_24h'], end=' ')
        #     print(d['quote']['INR']['percent_change_7d'], end=' ')
        #     print(d['quote']['INR']['market_cap'], end=' ')
        #     print(d['quote']['INR']['volume_24h'], end=' ')
        #     print(d['circulating_supply'], end=' ')
        #     print(d['total_supply'])
        crypto_list = []
        for item in coins:
            quote_data = item['quote'][currency]

            crypto = Cryptocurrency(
                name=item['name'],
                symbol=item['symbol'],
                price=quote_data['price'],
                percent_change_1h=quote_data['percent_change_1h'],
                percent_change_24h=quote_data['percent_change_24h'],
                percent_change_7d=quote_data['percent_change_7d'],
                market_cap=quote_data['market_cap'],
                volume_24h=quote_data['volume_24h'],
                volume_change_24h=quote_data.get('volume_change_24h', 0),
                percent_change_30d=quote_data.get('percent_change_30d', 0),
                percent_change_60d=quote_data.get('percent_change_60d', 0),
                percent_change_90d=quote_data.get('percent_change_90d', 0),
                market_cap_dominance=quote_data.get('market_cap_dominance', 0),
                fully_diluted_market_cap=quote_data.get('fully_diluted_market_cap', 0),
                circulating_supply=item.get('circulating_supply', 0)
            )
            crypto_list.append(crypto)


        return crypto_list


    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return []


def get_crypto_chart(symbol,crypto_data,currency='USD'):
    # Fetch cryptocurrency data (reuse your existing logic or API call)


    # Extract price changes
    price_changes = {
        '1h': crypto_data.percent_change_1h,
        '24h': crypto_data.percent_change_24h,
        '7d': crypto_data.percent_change_7d,
        '30d': crypto_data.percent_change_30d,
        '60d': crypto_data.percent_change_60d,
        '90d': crypto_data.percent_change_90d
    }
    # Generate a bar chart
    labels = list(price_changes.keys())
    values = list(price_changes.values())

    plt.figure(figsize=(8, 4))
    plt.plot(labels, values, marker='o', linestyle='-', color='b')  # Line chart
    plt.xlabel('Time Period')
    plt.ylabel('Percentage Change')
    plt.title(f'{symbol} Price Changes')
    plt.grid(True)  # Adds a grid for easier reading
    plt.xticks(labels)  # Ensure all labels are shown
    plt.axhline(0, color='grey', linewidth=0.8)  # Horizontal line at y=0

    # Optionally, add data labels
    for i, txt in enumerate(values):
        plt.annotate(f'{txt}%', (labels[i], values[i]), textcoords="offset points", xytext=(0, 10), ha='center')

    # Save the plot as an image file
    image_path = os.path.join(settings.MEDIA_ROOT, f'{symbol}_price_changes.png')
    plt.savefig(image_path)
    plt.close()

    # Return the path of the saved image
    return os.path.join(settings.MEDIA_URL, f'{symbol}_price_changes.png')

def getsupply_chart(symbol,crypto_data,currency='USD'):
    # Fetch cryptocurrency data



    # Prepare data for scatter plot
    market_cap = crypto_data.market_cap
    circulating_supply = crypto_data.circulating_supply

    labels = ['Market Cap', 'Circulating Supply']
    sizes = [market_cap, circulating_supply]

    # Colors for each section
    colors = ['blue', 'green']

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)

    plt.title(f'Market Cap and Circulating Supply for {symbol}')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the plot as an image file
    filename = f'{symbol}_market_cap_vs_supply.png'
    image_path = os.path.join(settings.MEDIA_ROOT, filename)
    plt.savefig(image_path)
    plt.close()

    # Return the path of the saved image
    return os.path.join(settings.MEDIA_URL,filename)
