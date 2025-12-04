import os
import time
import asyncio
import warnings
import pandas as pd
from datetime import datetime, timedelta
from func import save_daily_csv,saving_files,save_daily_csv2,main_date,xpath_click_center,create_dir,delet_dir_cont,drop_duplicate #input_dialog
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pyppeteer")





save_dir = save_daily_csv2(main_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)),'CSV FILES'),second_dir_path_name='LOGGIN TIMES')
save_path = f'{save_dir}/LOGIN_TIMES.csv'

Err_Timeout = 30000





async def Getting_url(page):

    full_path = save_daily_csv()
    path = f'{full_path}/tasks_urls.csv'    
    try:
        delet_dir_cont(folder_path=create_dir(dir_name=save_dir))
        delet_dir_cont(folder_path=full_path)
    except:
        print('CONTENTS IS BEEN DELETED OR DOESNT EXIST \n')


    for pages in range(1,15): #HOW MANY PAGES LINK ARE YOU INTRESTED IN GETTING ( YOU EXTEND FROM (1 - 20) MAX)
        url = f'https://socialearning.org/earner/available/tasks?page={pages}&filter_social_media='
        await page.goto(url=url,timeout = 0,waitUntil='networkidle2')
        await asyncio.sleep(3)
        tasks = await page.evaluate('''() => {
            const rows = Array.from(document.querySelectorAll("table.table tbody tr"));
            return rows.map(row => {
                const socialMedia = row.querySelector("td:nth-child(2)")?.innerText.trim() || "";
                const url = row.querySelector("td:nth-child(3) a")?.href || "";
                const rate = row.querySelector("td:nth-child(4)")?.innerText.trim() || "";
                const status = row.querySelector("td:nth-child(6) span")?.innerText.trim() || "";
                return { socialMedia, url, rate, status };
            });
        }''')

        # Convert to Pandas DataFrame
        saving_files(data=tasks,path=path,encoding="utf-8-sig")



async def sign_in(page):
    pp_data = {'LOGIN_TIMES':[]}

    try:
        pp_data_df = pd.read_csv(save_path)
    except:
        pp_data_df = pd.DataFrame({'LOGIN_TIMES':['2024:10:27:3:51:9']})

    # ✅ Extra check: if file is empty or column is missing
    if pp_data_df.empty or 'LOGIN_TIMES' not in pp_data_df.columns or pp_data_df['LOGIN_TIMES'].isna().all():
        pp_data_df = pd.DataFrame({'LOGIN_TIMES': ['2024:10:27:3:51:9']})


    current_time = ':'.join([f"{x}" for x in time.localtime()[:6] ])
    now_time = datetime.strptime(current_time, "%Y:%m:%d:%H:%M:%S")
    bf_time = datetime.strptime(pp_data_df['LOGIN_TIMES'].to_list()[-1].replace('-', ':').replace(' ', ':'), "%Y:%m:%d:%H:%M:%S")
    pp_data['LOGIN_TIMES'].append(now_time)

    time_diff = abs((now_time - bf_time).total_seconds())/3600

    if time_diff >=5:
        email_info = input(' ENTER YOUR EMAIL FOR SIGN-IN : ')
        pass_info = input(' ENTER YOUR EMAIL PASSWORD FOR SIGN-IN : ')

        url = 'https://socialearning.org/sign-in'
        await page.goto(url=url,timeout = 0,waitUntil='networkidle2')
        email = await page.waitForXPath("//input[@id='email']",timeout = Err_Timeout)
        await email.click()
        await asyncio.sleep(1)
        await email.click()
        await page.keyboard.down('Control')
        await page.keyboard.press('A')
        await page.keyboard.up('Control')
        await page.keyboard.press('Backspace')
        await email.click()
        await email.type(email_info)

        password = await page.waitForXPath("//input[@id='password-input']",timeout = Err_Timeout)
        await password.click()
        await asyncio.sleep(1)
        await password.click()
        await page.keyboard.down('Control')
        await page.keyboard.press('A')
        await page.keyboard.up('Control')
        await page.keyboard.press('Backspace')
        await asyncio.sleep(1)
        await password.click()
        await password.type(pass_info)

        await xpath_click_center(page,"//button[text()='Sign In']")
        await asyncio.sleep(6)
        await Getting_url(page)
        saving_files(data=pp_data,path=save_path)
    else:
        print('\n YOU HAVE LOGGED-IN BEFORE AND THE 5HRS TIME PERIOD HAVENT REACHED ')

