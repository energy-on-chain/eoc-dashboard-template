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

secret_api_key = "EOC_GLASSNODE_API_KEY"    # api key
request = {"name": f"projects/{project_id}/secrets/{secret_api_key}/versions/latest"}
response = client.access_secret_version(request)
secret_string = response.payload.data.decode("UTF-8")


# DATA
market_prefix = 'market'
market_api_calls = {
    'btc_price_usd_ohlc': {'a': 'BTC', 's': '1230789600', 'u': int(time.time()), 'i': '24h', 'f': 'json', 'timestamp_format': 'unix'},
    'eth_price_usd_ohlc': {'a': 'ETH', 's': '1230789600', 'u': int(time.time()), 'i': '24h', 'f': 'json', 'timestamp_format': 'unix'},
    'ltc_price_usd_ohlc': {'a': 'LTC', 's': '1230789600', 'u': int(time.time()), 'i': '24h', 'f': 'json', 'timestamp_format': 'unix'},
    'aave_price_usd_ohlc': {'a': 'AAVE', 's': '1230789600', 'u': int(time.time()), 'i': '24h', 'f': 'json', 'timestamp_format': 'unix'},
    'matic_price_usd_ohlc': {'a': 'MATIC', 's': '1230789600', 'u': int(time.time()), 'i': '24h', 'f': 'json', 'timestamp_format': 'unix'},
    'sushi_price_usd_ohlc': {'a': 'SUSHI', 's': '1230789600', 'u': int(time.time()), 'i': '24h', 'f': 'json', 'timestamp_format': 'unix'},
}
api_dict = {
    market_prefix: market_api_calls,
}


# FUNCTION
def glassnode_api():
# def glassnode_api(event, context):
    for prefix, api_call_list in api_dict.items():
        print('Fetching glassnode data...')
        for endpoint, parameters in api_call_list.items():
            print('Fetching glassnode endpoint: ' + endpoint)

            # Get data
            print('Getting data...')
            try:
                url = 'https://api.glassnode.com/v1/metrics/' + prefix + '/price_usd_ohlc'
                parameters['api_key'] = secret_string
                res = requests.get(url, params=parameters)
                df = pd.DataFrame(res.json())
            except Exception as e:
                print('Error during glassnode api pull!')
                exit()
            
            # Parse data
            print('Parsing data...')
            df = df.join(pd.DataFrame(df.pop('o').values.tolist()))
            df['utc'] = df['t'].apply(lambda x: datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))    # utc time

            # Output data
            print('Outputting data...')
            bucket_name = 'eoc-template-dashboard'
            outfile = 'glassnode_' + endpoint + '_' + parameters['i'] + '.csv'
            # local_project_path = 'data/' + outfile
            # df.to_csv(local_project_path, index=False)
            local_path = '/tmp/' + outfile
            cloud_path = 'api_data/' + outfile
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(cloud_path)
            df.to_csv(local_path, index=False)
            blob.upload_from_filename(local_path)
            print('Done.')


if __name__ == '__main__':
    glassnode_api()
