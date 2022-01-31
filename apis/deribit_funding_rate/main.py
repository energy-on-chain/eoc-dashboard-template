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
NUM_RECORDS = 744
RECORD_SPACING = 3600000
instrument_name = "BTC-PERPETUAL"


# FUNCTIONS
def output_data(existing_df, update_df, update_file_location, blob):
    df = pd.concat([existing_df, update_df])    # combine
    # df = df.drop_duplicates(subset=['unix'])    # remove overlap
    # df = df.sort_values(by='unix', ascending=True)    # sort
    df.to_csv(update_file_location, index=False)
    blob.upload_from_filename(update_file_location)


def parse_data(res):
    data = res['result']
    df = pd.DataFrame(data)
    df = df.rename(columns={'timestamp': 'unix'})    # rename cols
    df['utc'] = df['unix'].apply(lambda x: datetime.datetime.utcfromtimestamp(x/1000).strftime('%Y-%m-%d %H:%M:%S'))    # add utc
    df = df.drop_duplicates(subset='unix')    # remove overlap
    df = df.sort_values(by='unix', ascending=True)    # sort
    return df


def get_data(instrument_name, start_time, end_time):
    ws_flag = False
    try:
        ws = create_connection("wss://www.deribit.com/ws/api/v2")
        ws_flag = True
    except:
        print('There was an error establishing the Deribit websocket connection.')

    msg = \
        {
            "jsonrpc": "2.0",
            "id": 7617,
            "method": "public/get_funding_rate_history",
            "params": {
                "instrument_name": instrument_name,
                "start_timestamp": start_time,
                "end_timestamp": end_time
            }
        }

    ws.send(json.dumps(msg))
    res = json.loads(ws.recv())

    if ws_flag:
        ws.close()

    return res


def deribit_funding_rate():
# def deribit_funding_rate(event, context):
    print('Fetching deribit funding rate data...')

    # Get old data 
    print('Getting old data...')
    bucket_name = 'eoc-template-dashboard'
    bucket = storage_client.bucket(bucket_name)
    outfile = 'deribit_funding_rate_1h.csv'
    local_path = '/tmp/' + outfile
    cloud_path = 'api_data/' + outfile
    blob = bucket.blob(cloud_path)
    blob.download_to_filename(local_path)

    # Get new data
    print('Getting new data to append...')
    existing_df = pd.read_csv(local_path)
    end_time = int(existing_df.iloc[-1]['unix'])
    start_time = end_time - NUM_RECORDS * RECORD_SPACING
    now = int(time.time()) * 1000
    results = []

    while end_time < now + NUM_RECORDS * RECORD_SPACING:
        res = get_data(instrument_name, start_time, end_time)
        if len(res['result']) == 0:
            start_time = end_time
            end_time = end_time + NUM_RECORDS * RECORD_SPACING
            continue
        else:
            df = parse_data(res)    # parse
            results.append(df)
            start_time = end_time
            end_time = end_time + NUM_RECORDS * RECORD_SPACING

    update_df = pd.concat(results)

    # Output data
    print('Outputting data...')
    output_data(existing_df, update_df, local_path, blob)
    print('Done.')


if __name__ == '__main__':
    deribit_funding_rate()
