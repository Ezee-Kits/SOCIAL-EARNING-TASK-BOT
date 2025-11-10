import asyncio
from func import css_click_center,xpath_click_center,css_scroll_center





page_follow_amt = 0

async def FB_Task_Bot(page,task,task_url):
    global page_follow_amt
    await page.bringToFront()

    if page_follow_amt >=8 and 'FACEBOOK/Page Follow'.lower() in task.lower():
        print('[ ERROR] TRYING TO RUN FACEBOOK FOLLOW OPTION ')
        return False
    
    await page.goto(url=task_url,timeout = 0,waitUntil='networkidle2')

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
        print('FACEBOOK page_follow_amt ==',page_follow_amt)


        if 'FACEBOOK/Page Follow'.lower() in task.lower():
            try:
                await asyncio.sleep(5)
                print('Following the page...')
                await css_scroll_center(new_tab,'div[aria-label="Follow"][role="button"]')
                await asyncio.sleep(2)
                await new_tab.waitForSelector('div[aria-label="Follow"][role="button"]', timeout=10000)
                await css_click_center(new_tab,'div[aria-label="Follow"][role="button"]')
                done_task = 1
                page_follow_amt +=1
            except Exception as err:
                print(f' THIS ERROR OCCURED {err}')


        elif 'FACEBOOK/Page Like'.lower() in task.lower():
            await asyncio.sleep(5)
            try:
                await new_tab.waitForSelector('div[aria-label="Share"][role="button"]', timeout=10000)
                print('Liking the post...')
                # Run your JS snippet inside the page context
                await new_tab.waitForSelector('body', timeout=10000)
                result = await new_tab.evaluate("""
                () => {
                    const likeButton = Array.from(document.querySelectorAll("div[role='button'], div"))
                        .find(el => el.innerText.trim() === "Like");

                    if (likeButton) {
                        likeButton.scrollIntoView({ behavior: "smooth", block: "center" });
                        likeButton.click();
                        console.log("✅ Like button clicked!");
                        return true;
                    } else {
                        console.log("❌ Like button not found.");
                        return false;
                    }
                }
                """)
                if ' Like button clicked' in result:
                    done_task = 1
            except Exception as err:
                print(f' THIS ERROR OCCURED {err}')


                
        elif 'FACEBOOK/Post Share'.lower() in task.lower():
            print('Sharing the post...')
            await asyncio.sleep(5)
            try:
                await new_tab.waitForSelector('div[aria-label="Share"][role="button"]', timeout=10000)
                # Step 1: Click the "Share" button
                result1 = await new_tab.evaluate("""
                () => {
                    const shareButton = document.querySelector('div[aria-label="Share"][role="button"]');
                    if (shareButton) {
                        shareButton.scrollIntoView({ behavior: "smooth", block: "center" });
                        shareButton.click();
                        return "✅ 'Share' button clicked successfully!";
                    }
                    return "❌ 'Share' button not found on this page.";
                }
                """)
                print(result1)
                await asyncio.sleep(3)

                try:
                    await new_tab.waitForSelector('div[aria-label="Share now"][role="button"]', timeout=5000)
                    result2 = await new_tab.evaluate("""
                    () => {
                        const shareNowButton = document.querySelector('div[aria-label="Share now"][role="button"]');
                        if (shareNowButton) {
                            shareNowButton.click();
                            return "✅ 'Share now' button clicked successfully!";
                        }
                        return "❌ 'Share now' button not found on this page.";
                    }
                    """)
                    done_task = 1
                except Exception as e:
                    result2 = f"⚠️ Exception while clicking 'Share now': {e}"
                print(result2)
            except Exception as err:
                print(f' THIS ERROR OCCURED {err}')


        elif 'FACEBOOK/Video View'.lower() in task.lower():
            await asyncio.sleep(7)
            try:
                print('\n CURRENTLY WATCHING VIDEO \n ')
                done_task = 1
            except Exception as err:
                print(f' THIS ERROR OCCURED {err}')


        elif 'FACEBOOK/Post Comment'.lower() in task.lower():
            await asyncio.sleep(5)
            try:
                print('Commenting on the post...')
                text_to_type = "nice content"
                await css_click_center(new_tab, 'div[aria-label="Comment"][role="button"]')
                await asyncio.sleep(2)
                commnt_selector = 'div[aria-label^="Comment as"][contenteditable="true"]'
                commntbtn = await new_tab.waitForSelector(commnt_selector, timeout=10000)
                await commntbtn.click()
                await commntbtn.type(text_to_type, {'delay': 50})
                print("✅ Text entered successfully!")
                await asyncio.sleep(2)
                await new_tab.waitForSelector('#focused-state-composer-submit', timeout=10000)
                await css_click_center(new_tab, '#focused-state-composer-submit')
                print("✅ Comment submitted.")
                done_task = 1
            except Exception as err:
                print(f' THIS ERROR OCCURED {err}')


        elif 'FACEBOOK/Page Review'.lower() in task.lower():
            print("Clicking 'Reviews' tab...")
            await asyncio.sleep(5)
            try:
                await css_click_center(new_tab,'a[role="tab"]')
                
                reviews_clicked = await new_tab.evaluate('''
                () => {
                    const reviewsTab = Array.from(document.querySelectorAll('a[role="tab"]'))
                        .find(el => el.innerText.trim() === "Reviews");
                    if (reviewsTab) {
                        reviewsTab.scrollIntoView({ behavior: "smooth", block: "center" });
                        reviewsTab.click();
                        return true;
                    }
                    return false;
                }
                ''')

                if reviews_clicked:
                    print("✅ 'Reviews' tab clicked successfully using JavaScript!")
                else:
                    print("❌ 'Reviews' tab not found.")

                # Step 2: Click the "Yes" button
                yes_clicked = await new_tab.evaluate("""
                () => {
                    const yesButton = document.querySelector('div[role="button"][aria-label="Yes"]');
                    if (yesButton) {
                        yesButton.scrollIntoView({ behavior: "smooth", block: "center" });
                        yesButton.click();
                        return true;
                    }
                    return false;
                }
                """)
                if yes_clicked:
                    print("✅ 'Yes' button clicked successfully!")
                else:
                    print("❌ 'Yes' button not found.")

                await asyncio.sleep(2)
                try:
                    review_box = await new_tab.waitForSelector('div[contenteditable="true"][role="textbox"][aria-placeholder^="What do you recommend"]', timeout=10000)
                    await review_box.click()
                    await asyncio.sleep(1)
                    await review_box.click()
                    await review_box.type('Best earning platform, I love this. They pay instantly', {'delay': 50})
                    print("✅ Review text entered successfully!")
                    await css_click_center(new_tab, 'div[aria-label="Post"][role="button"]')
                    done_task = 1
                except:
                    print(' \n CANNOT WRITE REVIEW \n')
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