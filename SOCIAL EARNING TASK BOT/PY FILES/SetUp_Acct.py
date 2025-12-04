import os
import asyncio
from pyppeteer import launch
from func import css_scroll_center,css_click_center,save_daily_csv2

save_dir = save_daily_csv2(main_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)),'CSV FILES'),second_dir_path_name='BROSWER INFOS')



async def main(): 
    browser = await launch({
        'executablePath': r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        'headless': False,
        'userDataDir':save_dir,  # Enter cloned profile folder or Any path you want to save your informations here e.g C:\Users\HP\Desktop\ChromeProfileClone
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