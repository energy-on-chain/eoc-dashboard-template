import os
import sys
import json
import time
import datetime
import requests
import pandas as pd 
from google.oauth2 import service_account
from google.cloud import storage
from google.cloud import secretmanager


# CREDENTIALS
project_id = "eoc-template"
client = secretmanager.SecretManagerServiceClient()

secret_service_acct_key = "EOC_TEMPLATE_SERVICE_ACCOUNT_KEY"    # service account access
secret_service_acct_key_request = {"name": f"projects/{project_id}/secrets/{secret_service_acct_key}/versions/latest"}
secret_service_acct_key_response = client.access_secret_version(secret_service_acct_key_request)
secret_service_acct_key_json = secret_service_acct_key_response.payload.data.decode("UTF-8")
secret_service_acct_key_creds = service_account.Credentials.from_service_account_info(json.loads(secret_service_acct_key_json))
storage_client = storage.Client(credentials=secret_service_acct_key_creds)    # google cloud storage


# DATA
# coin_list = ['bitcoin']
coin_list = ['bitcoin', 'ethereum', 'litecoin', 'aave', 'matic-network', 'sushi', 'usd-coin'] 
currency = 'usd'
days = 0
interval = 'daily'


# FUNCTION
def coingecko_api():
    # header=['Coin', 'Unix', 'Price', 'Market Cap ($)', 'Volume', 'UTC']
    df_list = []

    for coin in coin_list:
        print('Fetching coingecko data for ' + coin + '...')

        # Get data
        print('Getting data...')
        try:
            url = 'https://api.coingecko.com/api/v3/coins/' + coin + '/market_chart?vs_currency=' + currency + '&days=' + str(days) + '&interval=' + interval
            res = requests.get(url).json()
            # df = pd.DataFrame(res.json())
        except Exception as e:
            print('Error during coingecko api pull!')
            exit()
        
        # Parse data
        print('Parsing data...')
        parsed_dict = {}
        # parsed_dict['Unix'] = res['prices'][0][0] / 1000
        parsed_dict['Coin'] = coin
        parsed_dict['Price ($)'] = res['prices'][0][1]
        # parsed_dict['Market Cap ($)'] = res['market_caps'][0][1]
        # parsed_dict['Volume'] = res['total_volumes'][0][1]
        parsed_dict['Last Updated (UTC)'] = datetime.datetime.utcfromtimestamp(res['prices'][0][0] / 1000).strftime('%Y-%m-%d %H:%M:%S')    # utc time

        # Convert to data frame
        df = pd.DataFrame(parsed_dict, index=[0])
        df_list.append(df)

        print('Done.')
    result_df = pd.concat(df_list, ignore_index=True)
    result_df.reset_index()
    result_df['Coin'] = result_df['Coin'].apply(lambda x: x.capitalize())

    return result_df


if __name__ == '__main__':
    coingecko_api()
