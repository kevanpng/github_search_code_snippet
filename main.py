import pprint
import time
from secrets import ACCESS_TOKEN

import requests
from github import Github

g = Github(ACCESS_TOKEN)

print(g.get_user().get_repos())

pp = pprint.PrettyPrinter(depth=6)


def search_github(keyword):
    rate_limit = g.get_rate_limit()
    rate = rate_limit.search
    if rate.remaining == 0:
        print(
            f'You have 0/{rate.limit} API calls remaining.'
            ' Reset time: {rate.reset}'
        )
        return
    else:
        print(f'You have {rate.remaining}/{rate.limit} API calls remaining')

    query = f'"{keyword}" in:file extension:py'
    result = g.search_code(query, order='desc')

    max_size = 10
    print(f'Found {result.totalCount} file(s)')
    print(f'printing first {max_size} files')
    if result.totalCount > max_size:
        result = result[:max_size]

    download_urls = []
    for file in result:
        download_urls.append(file.download_url)
    print(download_urls)
    print('downloading content')
    contents = []
    for url in download_urls:
        content = requests.get(url).text.splitlines()
        time.sleep(1)
        contents.append(content)
    pp.pprint(contents)


if __name__ == '__main__':
    keyword = input('Enter keyword[e.g french, german etc]: ')
    search_github(keyword)
