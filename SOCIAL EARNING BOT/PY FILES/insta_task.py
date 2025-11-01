import time
import asyncio
import pyperclip

from func import css_click_center,xpath_click_center,css_scroll_center

page_follow_amt = 0
async def Insta_Task_Bot(page,task,task_url):
    global page_follow_amt
    await page.bringToFront()
    await page.goto(url=task_url,timeout = 0,waitUntil='networkidle2')

    browser = page.browser
    pages_before = await browser.pages()

    try:
        element_exists = await page.waitForSelector('input[type="file"][name="proof_file"]', timeout=3000)
    except:
        element_exists = None

    if page_follow_amt <=5:
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
        # return False
    
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
        print('page_follow_amt ==',page_follow_amt)

        if 'INSTAGRAM/Page Follow'.lower() in task.lower():
            if page_follow_amt <=5:
                print('Following the page...')
                follow_button_script = """
                Array.from(document.querySelectorAll('button'))
                    .find(btn => btn.innerText.trim() === 'Follow');
                """
                await new_tab.waitForSelector('button')
                follow_btn_exists = await new_tab.evaluate("""
                () => {
                    const btn = Array.from(document.querySelectorAll('button'))
                        .find(b => b.innerText.trim() === 'Follow');
                    if (btn) {
                        btn.click();
                        return true;
                    }
                    return false;
                }
                """)
                if follow_btn_exists:
                    print("Follow button clicked ✅")
                    done_task = 1
                    page_follow_amt += 1
                else:
                    print("Follow button not found ⚠️")
                

            

        elif 'INSTAGRAM/Post Like'.lower() in task.lower():
            print('Liking the post...')
            await new_tab.waitForSelector('[role="button"]')
            liked = await new_tab.evaluate("""() => {
                const likeBtn = Array.from(document.querySelectorAll('[role="button"]'))
                    .find(el => el.querySelector('svg[aria-label="Like"]'));
                if (likeBtn) {
                    likeBtn.click();
                    return true;
                }
                return false;
            }""")

            if liked:
                print("Like button clicked ✅")
                done_task = 1
            else:
                print("Like button not found ⚠️")


        elif 'INSTAGRAM/Post Comment'.lower() in task.lower():
            print('Commenting on the post...')
            await css_scroll_center(new_tab,'div[role="button"]')
            text_to_type = "Great content"

            # Step 1: Click the Comment button
            await new_tab.evaluate("""
            const commentBtn = Array.from(document.querySelectorAll('div[role="button"]'))
                .find(el => el.querySelector('svg[aria-label="Comment"]'));

            if (commentBtn) {
                commentBtn.click();
                console.log("Comment button clicked ✅");
            } else {
                console.log("Comment button not found ⚠️");
            }
            """)

            # Step 2: Wait for the comment input box to appear (manual comment opening assumed)
            input_selector = 'input[placeholder="Add a comment…"]'
            await new_tab.waitForSelector(input_selector)

            # Step 3: Click to focus the input
            await new_tab.click(input_selector)

            # Step 4: Type the text character by character
            await new_tab.type(text_to_type, {"delay": 100})  # 100ms delay between keystrokes
            print("Text typed into the comment box ✅")

            # Step 5: Click the Post button
            await new_tab.evaluate("""
            const postBtn = Array.from(document.querySelectorAll('div[role="button"]'))
                .find(el => el.innerText.trim() === "Post");

            if (postBtn) {
                postBtn.click();
                console.log("Comment posted ✅");
            } else {
                console.log("Post button not found ⚠️");
            }
            """)
            done_task = 1
        

        elif 'INSTAGRAM/Post View'.lower() in task.lower():
            print('\n CURRENTLY ON VIEWING OF POST \n')
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
