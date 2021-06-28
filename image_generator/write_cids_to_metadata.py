import csv
from json import load
import json

if __name__ == '__main__':

    metadata_json = open("metadata_correct.json", "r")
    metadata_data = load(metadata_json)
    metadata_json.close()
    counter = 0
    with open('ipfs_result.csv', ) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=' ', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in csv_reader:
            cid = row[1]
            frog_num = row[0].split("/")[2].split(" ")[1].replace("#", "").replace(".png", "")
            metadata_data[frog_num]['image'] = cid
        csv_file.close()

    with open("metadata_completed.json", "w") as metadata_completed_json:
        json.dump(metadata_data, metadata_completed_json, indent=4)
        metadata_completed_json.close()
