import asyncio
from func import css_click_center,xpath_click_center,css_scroll_center





page_follow_amt = 0

async def AudioMack_Task_Bot(page,task,task_url):
    global page_follow_amt
    await page.bringToFront()

    if page_follow_amt >=6 and 'FACEBOOK/Page Follow'.lower() in task.lower():
        print('[ ERROR] TRYING TO RUN FACEBOOK FOLLOW OPTION ')
        return False
    
    await page.goto(url=task_url,timeout=0,waitUntil='networkidle2')

    browser = page.browser
    pages_before = await browser.pages()

    try:
        element_exists = await page.waitForSelector('input[type="file"][name="proof_file"]', timeout=5000)
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

        # Wait for it to load fully
        try:
            await new_tab.waitForSelector('body', {'timeout': 15000})
        except Exception:
            print("[INFO] Page loaded with dynamic content (no full navigation).")

        await asyncio.sleep(1)
        print('\n \n CURRENT TASK TO PERFORM :: ',task,'\n \n')


        done_task = 0
        print('AUDIOMACK page_follow_amt ==',page_follow_amt)


        if 'AUDIOMACK/Page Follow'.lower() in task.lower():
            try:
                selector1 = 'button[data-amlabs-button="cta-clear "]'
                try:
                    await new_tab.waitForSelector(selector1, {'timeout': 10000})
                    await new_tab.click(selector1)
                    print("✅ 'Not Now' button clicked successfully.")
                except TimeoutError:
                    print("❌ 'Not Now' button not found (timeout).")
                except Exception as e:
                    print("❌ Error while clicking:", e)

                selector = 'button[data-testid="FollowArtist"]'
                await new_tab.waitForSelector(selector, {'timeout': 10000})
                clicked = await new_tab.evaluate('''(sel) => {
                    const btn = document.querySelector(sel);
                    if (btn) { btn.click(); return true; }
                    return false;
                }''', selector)
                if clicked:
                    print("✅ Follow button clicked successfully.")
                    done_task = 1
                    page_follow_amt += 1        
                    await asyncio.sleep(2)            
                else:
                    print("❌ Follow button not found inside evaluate.")
            except Exception as err:
                print(f' THIS ERROR OCCURED {err}')




        if done_task ==0:
            await asyncio.sleep(1)
            await new_tab.close()

        elif done_task==1:
            await asyncio.sleep(3)
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
            await xpath_click_center(page, "//button[contains(text(), 'Submit Task')]")


            await page.waitForNavigation({'waitUntil': 'networkidle2', 'timeout': 30000})
            await page.waitForSelector('#contactList', {'timeout': 30000})
            print("✅ Contact list loaded successfully after automatic reload!")

        else:
            pass