import os
import time
import asyncio
import warnings
import pandas as pd
from pyppeteer import launch
from sign_url import sign_in
from yt_task import YT_Task_Bot
from fb_task import FB_Task_Bot
from twitter_task import X_Task_Bot
from insta_task import Insta_Task_Bot
from threads_task import Thread_Task_Bot
from datetime import datetime, timedelta
from yt_music_task import YT_Music_Task_Bot
from func import save_daily_csv,saving_files,save_daily_csv2,main_date


warnings.filterwarnings("ignore", category=RuntimeWarning, module="pyppeteer")



save_dir = save_daily_csv2(main_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)),'CSV FILES'),second_dir_path_name='LOGGIN TIMES')
save_path = f'{save_dir}/LOGIN_TIMES.csv'




async def main():
    browser = await launch({
        'executablePath': r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        'headless': False,
        'userDataDir': r"C:\Users\HP\Documents\SE_ChromeProfile",  # cloned profile folder
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
    await sign_in(page)

    csv_files_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'CSV FILES/{str(main_date())} Files')
    url_df = pd.read_csv(f'{csv_files_path}/tasks_urls.csv')

    pp_data = {'LOGIN_TIMES':[]}
    current_time = ':'.join([f"{x}" for x in time.localtime()[:6] ])
    now_time = datetime.strptime(current_time, "%Y:%m:%d:%H:%M:%S")
    pp_data['LOGIN_TIMES'].append(now_time)
    saving_files(data=pp_data,path=save_path)


    for index,  all_cont in enumerate(url_df['socialMedia']):
        task_SocialMedia = url_df['socialMedia'].to_list()[index]
        task_url = url_df['url'].to_list()[index]

        # if 'instagram/' in all_cont.lower():
        #     await Insta_Task_Bot(page,task_SocialMedia,task_url)

        # if 'youtube/' in all_cont.lower():
        #     await YT_Task_Bot(page,task_SocialMedia,task_url)

        if 'youtubemusic/' in all_cont.lower():
            await YT_Music_Task_Bot(page,task_SocialMedia,task_url)

        # if 'x/' in all_cont.lower():
        #     await X_Task_Bot(page,task_SocialMedia,task_url)

        # if 'facebook/' in all_cont.lower():
        #     await FB_Task_Bot(page,task_SocialMedia,task_url)

        # if 'threads/' in all_cont.lower():
        #     await Thread_Task_Bot(page,task_SocialMedia,task_url)



    await browser.close()
asyncio.run(main())



