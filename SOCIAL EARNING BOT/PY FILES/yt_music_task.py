import time
import asyncio
import pyperclip

from func import css_click_center,xpath_click_center,css_scroll_center


page_follow_amt = 0
async def YT_Music_Task_Bot(page,task,task_url):
    global page_follow_amt
    await page.bringToFront()
    
    await page.goto(url=task_url,timeout = 0,waitUntil='networkidle2')

    browser = page.browser
    pages_before = await browser.pages()
    
    try:
        element_exists = await page.waitForSelector('input[type="file"][name="proof_file"]', timeout=3000)
    except:
        element_exists = None

    await page.waitForXPath("//a[contains(text(), 'View Job')]", {'timeout': 5000})
    await page.evaluate('''
    () => {
        const el = Array.from(document.querySelectorAll('a'))
            .find(a => a.innerText && a.innerText.toLowerCase().includes("view job"));
        if (el) {
            el.scrollIntoView({ behavior: "smooth", block: "center" });
            el.click();
        }
    }
    ''')
    print("✅ 'View Job' clicked successfully")
    await asyncio.sleep(10)

    pages_after = await browser.pages()

    new_pages = [p for p in pages_after if p not in pages_before]

    if not new_pages:
        print("[WARNING] No new tab detected!")
        return False
    
    if new_pages:
        new_tab = new_pages[0]
        await new_tab.bringToFront()

        try:
            await new_tab.waitForSelector('body', {'timeout': 15000})
        except Exception:
            print("[INFO] Page loaded with dynamic content (no full navigation).")
        await asyncio.sleep(1)
        print('\n \n CURRENT TASK TO PERFORM :: ',task,'\n \n')

        done_task = 0
        print('page_follow_amt ==',page_follow_amt)

        if 'YOUTUBEMUSIC/Music Like'.lower() in task.lower():
            print(' \n CURRENTLY ON YOUTUBE/Music Like \n')
            await css_scroll_center(new_tab,'#button-shape-like button')
            like_button = await new_tab.waitForSelector('#button-shape-like button', visible=True)
            await asyncio.sleep(1)  # 1 second delay
            await like_button.click({'delay': 150})  # 150ms delay between mousedown and mouseup
            done_task = 1
        else:
            print("No matching task found. Skipping...")    



        if done_task ==0:
            await asyncio.sleep(2)
            await new_tab.close()

        elif done_task==1:
            if element_exists:
                await new_tab.screenshot({'path': 'screenshot.jpg','type': 'jpeg','quality': 75,'fullPage': True})

            await asyncio.sleep(2)
            await new_tab.close()

            await page.bringToFront()
            await asyncio.sleep(2)

            if element_exists:
                await element_exists.uploadFile('screenshot.jpg')
                print("✅ Image uploaded successfully!")
            else:
                print("⚠️ File input not found — skipping upload.")


            await page.waitForSelector('select[name="social_username"]')
            await page.evaluate('''
                const selectElement = document.querySelector('select[name="social_username"]');
                if (selectElement) {
                    selectElement.value = selectElement.options[1].value;
                    selectElement.dispatchEvent(new Event('change', { bubbles: true }));
                    console.log("✅ First dropdown option selected successfully!");
                } else {
                    console.log("❌ <select> element not found on the page.");
                }
            ''')
            await asyncio.sleep(2)
            # await xpath_click_center(page, "//button[contains(text(), 'Submit Task')]")

            await page.waitForNavigation({'waitUntil': 'networkidle2', 'timeout': 30000})
            await page.waitForSelector('#contactList', {'timeout': 30000})
            print("✅ Contact list loaded successfully after automatic reload!")
        else:
            pass