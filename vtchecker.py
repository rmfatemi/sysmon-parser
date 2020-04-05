import requests
import csv
import time

with open('final.csv') as csvin:
    data = csv.reader(csvin)
    next(data)
    hashes = set()

    for row in data:
        hash = ''.join(row[3])
        hashes.add(hash)
    hashes = list(hashes)

    for md5 in hashes:
        params = {'apikey': '128a4fbb3e281a9f023bc851d054a8d1c98f65cca977cf314d45d07a609e15e4', 'resource': md5}
        try:
            response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params).json()
            positives = response.get('positives', None)
            total = response.get('total', None)
            print(md5, positives, total, 'malicious' if positives else 'clean')
        except:
            time.sleep(59)
