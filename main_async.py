from secrets import ACCESS_TOKEN
import timeit


from github import Github

import aiohttp
import asyncio

g = Github(ACCESS_TOKEN)


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def search_github(session, keyword):
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

    # queries only python files
    query = f'"{keyword}" in:file extension:py'
    results = g.search_code(query, order='desc')

    max_size = 40
    print(f'Found {results.totalCount} file(s)')
    print(f'printing first {max_size} files')
    if results.totalCount > max_size:
        results = results[:max_size]

    download_urls = []
    for result in results:
        download_urls.append(result.download_url)
    print(download_urls)
    print('downloading content')
    path = '/home/kevan/Desktop/github_dirs/github_search_code_snippet/tmp/github_search_results.txt'
    with open(path, 'w+') as f:
        for url in download_urls:
            content = await fetch(session, url)
            # content = requests.get(url).text
            f.write(content)
            f.write('---------------------------')
            f.write('\n')
            # content = requests.get(url).text.splitlines()
            # time.sleep(1)


async def main():
    async with aiohttp.ClientSession() as session:
        await search_github(session, keyword)
        # html = await fetch(session, 'http://python.org')


if __name__ == '__main__':
    keyword = input('Enter keyword[e.g french, german etc]: ')
    start_time = timeit.default_timer()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    elapsed = timeit.default_timer() - start_time
    print(elapsed)
