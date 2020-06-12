import csv
from collections import Counter
import requests
import io
import zipfile

url = 'https://www.sec.gov/files/node/add/data_distribution/2020q1.zip'
#url = 'https://www.sec.gov/files/dera/data/financial-statement-data-sets/2019q4.zip'

FILE_ORDER = ['sub.txt', 'num.txt']


def download_extract_zip(url):
    """
    Download a ZIP file and extract its contents in memory
    yields (filename, file-like object) pairs
    """
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
        info_list = thezip.infolist()
        for filename in FILE_ORDER:
            file_index = next((index for (index, d) in enumerate(info_list) if d.filename == filename), None)
            with thezip.open(info_list[file_index], 'r') as f:
                yield info_list[file_index].filename, f


def process_sub(f):
    ten_ks = []
    c = Counter()
    text_file = io.TextIOWrapper(f)

    reader = csv.reader(text_file, dialect='excel', delimiter='\t')
    headers = next(reader, None)
    print(headers)
    for row in reader:
        c.update([row[headers.index('form')]])
        if row[headers.index('form')] == '10-K':
            ten_ks.append(row)

    print(f'10-K count: {len(ten_ks)}')
    print(f'Forms count: {c}')


def process_num(f):
    pass


for filename, f in download_extract_zip(url):
    if filename == 'sub.txt':
        process_sub(f)
    elif filename == 'num.txt':
        process_num(f)

