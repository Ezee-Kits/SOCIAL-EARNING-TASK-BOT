

from tkinter import simpledialog
from datetime import date, timedelta
from bs4 import BeautifulSoup
from lxml import html
import tkinter as tk
import pandas as pd
import requests
import asyncio
import time
import os


match_day_date = 0

def main_date(day = match_day_date):
    last_date = date.today() + timedelta(day)
    return last_date


def save_daily_csv():
    outcome_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),'CSV FILES')
    todays_dir = str(main_date(match_day_date))+' Files'
    full_path = os.path.join(outcome_dir,todays_dir)
    try:
        os.makedirs(full_path)
    except:
        print('\n PATH ALREADY EXIST BUT WAS CREATED SUCCESFULLY \n')
    return full_path
    
    
def save_daily_csv2(main_dir,second_dir_path_name):
    outcome_dir = main_dir
    todays_dir = second_dir_path_name
    full_path = os.path.join(outcome_dir,todays_dir)
    try:
        os.makedirs(full_path)
    except:
        print('\n PATH ALREADY EXIST BUT WAS CREATED SUCCESFULLY \n')
    return full_path
    



def saving_files(data,path,encoding='utf-8'):
    df = pd.DataFrame(data)
    print(df.to_string())

    try:
        df2 = pd.read_csv(path)
        all_df = pd.concat([df2, df], ignore_index=True)
        all_df.to_csv(path, index=False,encoding=encoding)
        print(' ------------------------------------ ALL FILES SAVED  ------------------------------------- \n \n')

    except:
        df.to_csv(path, index=False)
        print('============================= SECOND FILE SAVED ==========================')



def drop_duplicate(path):
    all_df = pd.read_csv(path)
    all_df = all_df.drop_duplicates(keep='first')
    all_df = all_df.reset_index()
    all_df.drop(['index'], axis=1, inplace=True)
    all_df.to_csv(path, index=False)


def sorting_values(path,value,ascending_mode):
    df = pd.read_csv(path)
    df = df.sort_values(by=value,ascending=ascending_mode)
    df.to_csv(path, index=False)


def sorting_values_path_to_save(path,value,path_to_save,ascending_mode):
    df = pd.read_csv(path)
    df = df.sort_values(by=value,ascending=ascending_mode)
    df.to_csv(path_to_save, index=False)


def delet_dir_cont(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


def create_dir(dir_name):
    full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),dir_name)
    try:
        os.makedirs(full_path)
    except:
        print('\n PATH ALREADY EXIST BUT WAS CREATED SUCCESFULLY \n')
    return full_path


async def xpath_click_center(page, xpath: str, delay: float = 0.5):
    try:
        # 1️⃣ Wait for element to appear (XPath version)
        await page.waitForXPath(xpath, {'visible': True, 'timeout': 10000})

        # 2️⃣ Get the element handle
        elements = await page.xpath(xpath)
        if not elements:
            print(f"[WARNING] Element not found: {xpath}")
            return False
        
        element = elements[0]

        # 3️⃣ Scroll the element into the center of the viewport
        await page.evaluate('''
            (element) => {
                element.scrollIntoView({
                    behavior: "smooth",
                    block: "center",
                    inline: "center"
                });
            }
        ''', element)

        await asyncio.sleep(delay)  # wait for smooth scrolling

        # 4️⃣ Get the element's bounding box
        box = await element.boundingBox()
        if not box:
            print(f"[WARNING] Element '{xpath}' not visible or has no bounding box.")
            return False

        # 5️⃣ Calculate the center coordinates
        x = box['x'] + box['width'] / 2
        y = box['y'] + box['height'] / 2

        # 6️⃣ Perform the click at the center
        await asyncio.sleep(2)
        await page.mouse.click(x, y)
        print(f"[OK] Clicked center of '{xpath}' at ({x:.2f}, {y:.2f})")

        return True

    except Exception as e:
        print(f"[ERROR] Could not click on '{xpath}': {e}")
        return False



async def xpath_scroll_center(page, xpath: str, delay: float = 0.5):
    try:
        # 1️⃣ Wait for element to appear (XPath version)
        await page.waitForXPath(xpath, {'visible': True, 'timeout': 10000})

        # 2️⃣ Get the element handle
        elements = await page.xpath(xpath)
        if not elements:
            print(f"[WARNING] Element not found: {xpath}")
            return False
        
        element = elements[0]

        # 3️⃣ Scroll the element into the center of the viewport
        await page.evaluate('''
            (element) => {
                element.scrollIntoView({
                    behavior: "smooth",
                    block: "center",
                    inline: "center"
                });
            }
        ''', element)

        print(f"[OK] Scrolled To center of '{xpath}'")

        return True

    except Exception as e:
        print(f"[ERROR] Could not scroll on '{xpath}': {e}")
        return False



def input_dialog():
    class LoginDialog(simpledialog.Dialog):
        def body(self, master):
            self.title("Login")
            tk.Label(master, text="Email:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
            self.email_entry = tk.Entry(master, width=36); self.email_entry.grid(row=0, column=1, padx=6, pady=6)
            tk.Label(master, text="Password:").grid(row=1, column=0, sticky="e", padx=6, pady=6)
            self.pass_entry = tk.Entry(master, show='*', width=36); self.pass_entry.grid(row=1, column=1, padx=6, pady=6)
            return self.email_entry

        def apply(self):
            self.result = (self.email_entry.get(), self.pass_entry.get())

    root = tk.Tk()
    root.withdraw()
    dlg = LoginDialog(root)   # modal dialog handled by simpledialog
    root.destroy()
    return dlg.result


async def css_click_center(page, selector: str, delay: float = 0.5):
    try:
        # 1️⃣ Wait for the element to appear (Selector version)
        await page.waitForSelector(selector, {'visible': True, 'timeout': 10000})

        # 2️⃣ Get the element handle
        element = await page.querySelector(selector)
        if not element:
            print(f"[WARNING] Element not found: {selector}")
            return False

        # 3️⃣ Scroll the element into the center of the viewport
        await page.evaluate('''
            (element) => {
                element.scrollIntoView({
                    behavior: "smooth",
                    block: "center",
                    inline: "center"
                });
            }
        ''', element)

        await asyncio.sleep(delay)  # wait for smooth scrolling

        # 4️⃣ Get the element's bounding box
        box = await element.boundingBox()
        if not box:
            print(f"[WARNING] Element '{selector}' not visible or has no bounding box.")
            return False

        # 5️⃣ Calculate the center coordinates
        x = box['x'] + box['width'] / 2
        y = box['y'] + box['height'] / 2

        # 6️⃣ Perform the click at the center
        await asyncio.sleep(2)
        await page.mouse.click(x, y)
        print(f"[OK] Clicked center of '{selector}' at ({x:.2f}, {y:.2f})")

        return True

    except Exception as e:
        print(f"[ERROR] Could not click on '{selector}': {e}")
        return False




async def css_scroll_center(page, selector: str, delay: float = 0.5):
    try:
        # 1️⃣ Wait for the element to appear (Selector version)
        await page.waitForSelector(selector, {'visible': True, 'timeout': 10000})

        # 2️⃣ Get the element handle
        element = await page.querySelector(selector)
        if not element:
            print(f"[WARNING] Element not found: {selector}")
            return False

        # 3️⃣ Scroll the element into the center of the viewport
        await page.evaluate('''
            (element) => {
                element.scrollIntoView({
                    behavior: "smooth",
                    block: "center",
                    inline: "center"
                });
            }
        ''', element)

        print(f"[OK] Scrolled To center of '{selector}'")
        return True

    except Exception as e:
        print(f"[ERROR] Could not scroll on '{selector}': {e}")
        return False

