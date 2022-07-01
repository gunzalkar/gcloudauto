import requests
import json
import pandas as pd

df = pd.read_csv('test2_result.csv')
back_half = df['1'] + '-' + df['2']
long_links = df['13']
shorten_urls = []
custom_urls = []

for i, each_link in enumerate(long_links):
    url = "https://api-ssl.bitly.com/v4/bitlinks"

    payload = json.dumps({
    "long_url": each_link,
    "domain": "encore-boston.com",
    "title": "Search Rentals",
    "tags": [
    "Auto YGL Link"
    ]
    })

    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ede49380bd61cafb0ca80e9c0b0eae27d08f3f76'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json().get('id'))
    use_id = response.json().get('id')
    shorten_urls.append(response.json().get('link'))

    custom_id = "encore-boston.com/" + back_half[i]

    json_data = { "custom_bitlink": custom_id, "bitlink_id": use_id }


    response = requests.post('https://api-ssl.bitly.com/v4/custom_bitlinks', headers=headers, json=json_data)
    # final_custom_bitlink = response.json().get('custom_bitlink')
    final_custom_bitlink = response.json().get('bitlink').get('custom_bitlinks')[0]
    print(final_custom_bitlink)
    custom_urls.append(final_custom_bitlink)

links_df = pd.DataFrame (shorten_urls, columns = ['Shorten_URL'])
custom_links_df = pd.DataFrame (custom_urls, columns = ['Custom_URL'])
links_result = pd.concat([df, links_df, custom_links_df], axis=1)
print(links_result)
links_result.to_csv('custom_links_result.csv')


