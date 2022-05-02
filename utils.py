import concurrent.futures
import requests
import click
from concurrent.futures import wait


def check_url_validity(url_to_check):
    pass

def check_range_header(url):
    # 
    rv = requests.head(url)
    click.secho(f"Metadata about the file ")
    print(f"File Type {rv.headers['Content-Type']}")
    if 'Accept-Ranges' not in rv.headers:
        print(f"File does not support concurrent downloading")
    print(f'File Size {int(rv.headers["Content-Length"])//(1024*1024)} MB')

    return int(rv.headers["Content-Length"])
 
def ranged_download(z):
    url, temp_name, start_range, end_range = z
    print(z)
    # return
    headers = {"Range": f"bytes={start_range}-{end_range}"}
    print(headers)
    rv = requests.get(url)
    
    with open(temp_name, "wb") as f:
        f.write(rv.content)

def q(*args):
    print(*args)

def aggregator(files):
    complete= "completewe.flv"
    
    with open(complete, "wb") as file:
        for d in files:
            with open(d, "rb") as temp_file:
                file.write(temp_file.read())




def download_concurrently(url, content_length, concurrency=1):
    output_file="tempjj"
    split = content_length // concurrency
    file_ranges = []
    file_count=0
    for i in range(0,content_length, split+1):
        ct = i+split
        if i+split > content_length:
            ct = content_length
        file_ranges.append((url, output_file+str(file_count), i,ct))
        file_count+=1

    with concurrent.futures.ProcessPoolExecutor() as executor:
        print("exec")
        executor.map(ranged_download, file_ranges)
        # executor.map(q, file_ranges)
    aggregator(map(lambda x: x[1], file_ranges))




if __name__=="__main__":
    url ="https://www.ibrahimabah.com/ibfilms/Harry.Potter-The.Ultimate.Collection.%20I%20-%20VIII%20.%202001-2011.1080p.Bluray.x264.anoXmous/Harry%20Potter%201/Harry.Potter.And.The.Sorcerers.Stone.2001.UEE.1080p.Bluray.x264.anoXmous_.mp4"
    
    # url = "https://www.ibrahimabah.com/ibfilms/Harry.Potter-The.Ultimate.Collection.%20I%20-%20VIII%20.%202001-2011.1080p.Bluray.x264.anoXmous/Harry%20Potter%201/Harry.Potter.And.The.Sorcerers.Stone.2001.UEE.1080p.Bluray.x264.anoXmous_eng.srt"
    # ranged_download(url, "t1")
    # check_range_header(url)
    url="https://www.sample-videos.com/video123/flv/480/big_buck_bunny_480p_30mb.flv"
    ct=check_range_header(url)
    download_concurrently(url, ct)
    # z= ('https://www.sample-videos.com/video123/flv/480/big_buck_bunny_480p_30mb.flv', "A0", 0, 7878188)
    # ranged_download(z)