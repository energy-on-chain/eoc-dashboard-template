import os
import time
import json
import pandas as pd
import datetime
from websocket import create_connection
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
currency = 'BTC'


# FUNCTIONS
def output_data(existing_df, update_df, update_file_location, blob):
    df = pd.concat([existing_df, update_df])    # combine
    # df = df.drop_duplicates(subset=['unix'])    # remove overlap
    # df.to_csv('/Users/hartimat/Desktop/test.csv', index=False)
    df.to_csv(update_file_location, index=False)
    blob.upload_from_filename(update_file_location)


def parse_data(res):
    data = res['result']
    df = pd.DataFrame(data)
    df = df.rename(columns={0: 'unix', 1: 'historical_volatility'})    # rename cols
    df['utc'] = df['unix'].apply(lambda x: datetime.datetime.utcfromtimestamp(x/1000).strftime('%Y-%m-%d %H:%M:%S'))    # add utc
    return df


def get_data(currency):
    ws_flag = False
    try:
        ws = create_connection("wss://www.deribit.com/ws/api/v2")
        ws_flag = True
    except:
        print('There was an error establishing the Deribit websocket connection.')

    msg = \
        {
        "jsonrpc" : "2.0",
        "id" : 8387,
        "method" : "public/get_historical_volatility",
        "params" : {
            "currency" : "BTC",
        }
    }

    ws.send(json.dumps(msg))
    res = json.loads(ws.recv())

    if ws_flag:
        ws.close()

    return res


def deribit_historical_volatility():
# def deribit_historical_volatility(event, context):
# def deribit_historical_volatility():
    print('Fetching deribit historical volatility data...')

    # Get old data 
    print('Getting old data...')
    bucket_name = 'eoc-template-dashboard'
    bucket = storage_client.bucket(bucket_name)
    outfile = 'deribit_historical_volatility_1h.csv'
    local_path = '/tmp/' + outfile
    cloud_path = 'api_data/' + outfile
    blob = bucket.blob(cloud_path)
    blob.download_to_filename(local_path)

    # Get new data
    print('Getting new data...')
    existing_df = pd.read_csv(local_path)
    res = get_data(currency)
    update_df = parse_data(res)    # parse

    # Output data
    print('Outputting data...')
    output_data(existing_df, update_df, local_path, blob)
    print('Done.')


if __name__ == '__main__':
    deribit_historical_volatility()
