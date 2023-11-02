import aiohttp
import ssl

async def fetch_data():
    url = 'https://v3bl.goszakup.gov.kz/ru/favorites'
    headers = {
        'Host': 'v3bl.goszakup.gov.kz',
        'Sec-Ch-Ua': '"Not=A?Brand";v="99", "Chromium";v="118"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Linux"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.90 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://v3bl.goszakup.gov.kz/ru/cabinet/profile',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'close'
    }

    cookies = {
        'ci_session': 'D2RfZVJlAW4EK1MiWjcGNwc0DTpSWwInXSYENldxVHUEb1doBTsNXglqWj5aBVYhAG8FdFU4W20DNAQzBQwKL1hkUDBdMVRjADAEZVQzDTQPZl8%2BUjUBYwRpU2daOgY1Bz0NM1JiAjZdMwQwVzZUNwQ3Vz4FZg0zCTFaYlptVjsAbQVmVTJbOQM1BG0FaApoWGVQYV0%2BVDQANAQxVGYNZw9mX2tSYwFiBGZTN1puBmUHNw1kUjQCZl1sBGVXZ1RlBFpXJQVuDXIJOVprWmlWOQAIBSVVa1srA18EaAU0CmlYIlBiXXtUdQBeBHZUPw1yDz9faFJrAQgEclNhWiMGNgcqDTBSKQI1XQkEcVc5VHUEPFc2BWUNOwlfWnhaLFZwADEFdVVdWzoDZwRsBT4KeVgMUCVdM1R1ADgEZVQ1DTQPP18DUnMBGQQ%2FUytaZAZqB2gNYVIoAjBdewRjVyJULgRRV24FOw1lCWxaLVoqViMAGgVTVSJbagMwBCcFYAo2WHBQUF1hVGgANARgVD8NIQ99X2lSZQF9BHBTEFp9BnYHaA1lUlACYF03BBhXa1RyBClXMgVmDTYJLVppWm9WIwB8BUxVSlsPA00ERQV8Ci1YPFBuXWNUYwAiBBNUYQ1iD25fMFJ4AXQEE1M5Wn8GaQdpDWVSKAI0XWQEa1csVDYEKFcyBWwNOAkwWnRaYFYzAHQFVFVjWz0DYQR7BTkKIlhlUDRdP1QoADEEYlRYDSMPPl8sUmsBZQRjU2taUQYkB2gNYVJ0AnFdCgQyV2FUcgRvV3EFPA11CXpaBlp7VjgAPQU9VTNbbQM5BDEFaAo7WGRQMV05VDYAOQQp'
    }

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        async with session.get(url, headers=headers, cookies=cookies) as response:
            response_text = await response.text()
            response_cookies = response.cookies
            print('response_cookies: ', response_cookies)
            with open("test.html", "w") as file:
                file.write(response_text)
                
import asyncio

loop = asyncio.get_event_loop()
loop.run_until_complete(fetch_data())
