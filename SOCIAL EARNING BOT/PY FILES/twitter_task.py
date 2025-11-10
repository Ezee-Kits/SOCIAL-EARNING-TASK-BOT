import time
import asyncio
import pyperclip

from func import css_click_center,xpath_click_center,css_scroll_center


page_follow_amt = 0
async def X_Task_Bot(page,task,task_url):
    global page_follow_amt
    await page.bringToFront()

    if page_follow_amt >=8 and 'X/Page Follow'.lower() in task.lower():
        print('[ ERROR] TRYING TO RUN TWITTER FOLLOW OPTION ')
        return False
    
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
    # print('pages_before',pages_before)
    # print('pages_after',pages_after)

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
        print('TWITTER page_follow_amt ==',page_follow_amt)
        if 'X/Page Follow'.lower() in task.lower():
            try:
                print('Following the page...')
                await asyncio.sleep(3)
                await new_tab.waitForSelector('button[role="button"]', timeout=10000)
                follow_clicked = await new_tab.evaluate("""
                () => {
                    const followBtn = Array.from(document.querySelectorAll('button[role="button"]'))
                        .find(el => el.innerText.trim() === "Follow");
                    if (followBtn) { 
                        followBtn.click(); 
                        return true; 
                    }
                    return false;
                }
                """)

                if follow_clicked:
                    print("Follow button clicked ✅")
                    done_task = 1
                    page_follow_amt += 1
                else:
                    print("Follow button not found ⚠️")
            except Exception as err:
                print(f' THIS ERROR OCCURED {err}')


        elif 'X/Tweet Comment'.lower() in task.lower():
            await asyncio.sleep(1)
            try:
                await new_tab.waitForSelector('div[data-testid="tweetTextarea_0"]', timeout=10000)
                await css_scroll_center(new_tab,'div[data-testid="tweetTextarea_0"]')
                await asyncio.sleep(2)
                combox = await new_tab.waitForSelector('div[data-testid="tweetTextarea_0"]', timeout=10000)
                await combox.click()
                await asyncio.sleep(2)
                await combox.click()
                
                await combox.type('Nice content!',{'delay':100})
                await asyncio.sleep(2)
                await css_click_center(new_tab,'button[data-testid="tweetButtonInline"]')
                done_task = 1
            except Exception as err:
                print(f' THIS ERROR OCCURED {err}')


        elif 'X/Tweet Like'.lower() in task.lower():
            await asyncio.sleep(3)
            try:
                await new_tab.waitForSelector('button[aria-label*="Like"][data-testid="like"]', timeout=10000)
                await css_scroll_center(new_tab,'button[aria-label*="Like"][data-testid="like"]')
                clicked = await new_tab.evaluate("""
                () => {
                    const btn = document.querySelector('button[aria-label*="Like"][data-testid="like"]');
                    if (btn) { 
                        btn.click(); 
                        return true; 
                    } 
                    return false;
                }
                """)

                if not clicked:
                    await css_click_center(new_tab, 'button[aria-label*="Like"][data-testid="like"]')
                print("✅ Like button clicked (via JS or physical click)")
                done_task = 1
            except Exception as err:
                print(f' THIS ERROR OCCURED {err}')


        elif 'X/Tweet Repost'.lower() in task.lower():
            await asyncio.sleep(3)
            try:
                repost_selector = 'button[data-testid="retweet"][aria-label*="Repost"]'
                await new_tab.waitForSelector(repost_selector, {'timeout': 10000})
                repost_button = await new_tab.querySelector(repost_selector)

                if repost_button:
                    await repost_button.click()
                    print("✅ Repost button clicked.")

                    # Step 2: Wait for the confirm Repost button to appear
                    confirm_selector = 'div[data-testid="retweetConfirm"][role="menuitem"]'
                    await new_tab.waitForSelector(confirm_selector, {'timeout': 5000})
                    confirm_button = await new_tab.querySelector(confirm_selector)

                    if confirm_button:
                        await confirm_button.click()
                        print("✅ Repost confirmed.")
                        done_task = 1
                    else:
                        print("⚠️ Could not find the confirm Repost button.")
                else:
                    print("❌ Repost button not found.")
            except Exception as err:
                print(f' THIS ERROR OCCURED {err}')



        elif 'X/Tweet Views'.lower() in task.lower():
            
            print('Watching the tweet...')
            await asyncio.sleep(7)
            done_task = 1
        



        else:
            pass



        if done_task ==0:
            await asyncio.sleep(2)
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
            await asyncio.sleep(1)
            await xpath_click_center(page, "//button[contains(text(), 'Submit Task')]")
            await page.waitForNavigation({'waitUntil': 'networkidle2', 'timeout': 30000})
            await page.waitForSelector('#contactList', {'timeout': 30000})
            print("✅ Contact list loaded successfully after automatic reload!")
        else:
            pass