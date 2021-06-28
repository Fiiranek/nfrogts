import requests
import ast
import csv
import sys
import os

project_id = '<YOU_PROJECT_ID>'

rows = []
arguments = len(sys.argv) - 1


def upload_file_to_blockfrost(filename: str):
    files = {'file': open(filename, 'rb')}
    headers = {'project_id': project_id}
    add_req = requests.post("https://ipfs.blockfrost.io/api/v0/ipfs/add", files=files, headers=headers)

    add_req_content = add_req.content.decode("utf-8")

    add_req_content = ast.literal_eval(add_req_content)
    cid = add_req_content['ipfs_hash']
    pin_req = requests.post(f"https://ipfs.blockfrost.io/api/v0/ipfs/pin/add/{cid}", headers=headers)
    pin_response = ast.literal_eval(pin_req.text)
    cid = pin_response['ipfs_hash']
    rows.append({
        'filename': filename, 'cid': cid
    })
    print(f"Uploaded: {filename} - {cid}")

def upload_files_from_dir_to_blockfrost(dirname: str):
    files = [f for f in os.listdir(dirname)]
    for file in files:
        upload_file_to_blockfrost(f'{dirname}/{file}')
    with open('ipfs_result.csv', mode="w", newline='', ) as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=' ', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            csv_writer.writerow([row['filename'], row['cid']])
        csv_file.close()


upload_files_from_dir_to_blockfrost(sys.argv[2])
