import asyncio
import os
import re
import aiohttp
import my_utils

headers = {
    "User-Agent": my_utils.get_random_ua()
}

url_get_header = 'https://telegra.ph'
proxy = "http://localhost:10809"


async def fetch_urls(session, url):
    async with session.get(url, proxy=proxy) as response:
        if response.status == 200:
            html = await response.text()

            # 获取标题
            title = re.findall("<title>(.*?)</title>", html)[0]
            # 去除操作系统下不允许的文件名字符
            title = my_utils.sanitize_filename(title)

            os.mkdir(title)
            os.chdir(title)

            # 获取所有图片的url
            url_list = re.findall("img src=\"(.*?)\"", html)

            for i in range(len(url_list)):
                url_list[i] = url_get_header + url_list[i]

            return url_list
        else:
            print(f"Failed to fetch URLs from {url}")
            return []


async def download_image(session, url):
    async with session.get(url, proxy=proxy) as response:
        if response.status == 200:
            data = await response.read()
            filename = url.split("/")[-1]
            with open(filename, "wb") as f:
                f.write(data)
                print(f"Downloaded {filename}")
        else:
            print(f"Failed to download {url}")


async def download_images(url):
    async with aiohttp.ClientSession(headers=headers) as session:
        urls = await fetch_urls(session, url)
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(download_image(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks)


def get_main(url):
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_images(url))
    os.chdir("..")


if __name__ == '__main__':
    get_main('https://telegra.ph/轩萧学姐-公路JK3月15打赏群资源-03-16')