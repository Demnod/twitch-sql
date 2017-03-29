import requests
import json
import datetime
import time


def get_creds():
    with open('../.credbox/.twitch-creds') as cred_file:
        cred_string = cred_file.read().rstrip()
        return cred_string


def set_time():
    now = datetime.datetime.now()
    future = now + datetime.timedelta(hours=1)
    return future


def get_all_assets():
    test = set_time()
    print(test)
    exit()

    while datetime.datetime.now() < datetime.datetime(2017, 3, 23, 21, 33, 0):
        print('Test')
        time.sleep(10)

    url_headers = {'client_id': '4zc20ucqrn70b7gctrpd5l7ey7vsfk',
                   'Accept': 'application/vnd.twitchtv.v5+json'}
    t = requests.get('https://api.twitch.tv/kraken/streams/tsm_dyrus', params=url_headers).json()
    # print(json.dumps(t, indent=2, sort_keys=False))


def main():
    get_all_assets()


if __name__ == '__main__':
    main()
