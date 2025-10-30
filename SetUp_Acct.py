import asyncio
from pyppeteer import launch





async def main(): 
    browser = await launch({
        'executablePath': r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        'headless': False,
        'userDataDir': r" ",  # Enter cloned profile folder or Any path you want to save your informations here e.g C:\Users\HP\Desktop\ChromeProfileClone
        'args': [
            '--no-sandbox',
            '--disable-infobars',
            '--disable-blink-features=AutomationControlled',
            '--disable-extensions-except',
            '--no-first-run',
            '--no-default-browser-check',
        ]
    })


    page = await browser.newPage()
    await page.goto('https://github.com/Ezee-Kits/SOCIAL-EARNING-TASK-BOT',timeout = 0,waitUntil='networkidle2')
    input('\n PRESS ENTER AFTER YOUR ARE DONE SETTING UP YOUR ACCOUNT ::::: \n')

    await browser.close()

asyncio.run(main())