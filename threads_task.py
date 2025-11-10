import time
import asyncio
import pyperclip

from func import css_click_center,xpath_click_center,css_scroll_center

page_follow_amt = 0
async def Thread_Task_Bot(page,task,task_url):
    global page_follow_amt
    await page.bringToFront()

    if page_follow_amt >=8 and 'THREADS/Page Follow'.lower() in task.lower():
        print('[ ERROR] TRYING TO RUN THREADS FOLLOW OPTION ')
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
        print('THREADS page_follow_amt ==',page_follow_amt)

        
        if 'THREADS/Page Follow'.lower() in task.lower():
            try:
                print('Following the page...')
                await css_scroll_center(new_tab,'div[role="button"]')
                result = await new_tab.evaluate("""
                () => {
                    const followButton = Array.from(document.querySelectorAll('div[role="button"]'))
                        .find(el => el.innerText && el.innerText.trim().toLowerCase() === "follow");

                    if (followButton) {
                        followButton.scrollIntoView({ behavior: "smooth", block: "center" });
                        followButton.click();

                        let tries = 0;
                        const maxTries = 30;

                        return new Promise(resolve => {
                            const interval = setInterval(() => {
                                tries++;
                                if (followButton.innerText.trim().toLowerCase() === "following") {
                                    clearInterval(interval);
                                    resolve("🎉 Successfully followed!");
                                } else if (tries >= maxTries) {
                                    clearInterval(interval);
                                    resolve("⚠️ Clicked, but text did not change to 'Following'.");
                                }
                            }, 100);
                        });
                    } else {
                        return "❌ 'Follow' button not found!";
                    }
                }
                """)

                if 'Successfully followed'.lower() in result.lower():
                    done_task = 1
                    page_follow_amt+=1                    
            except Exception as err:
                print(f' THIS ERROR OCCURED {err}')


        elif 'THREADS/Post Like'.lower() in task.lower():
            try:
                print('Liking the post...')
                await css_scroll_center(new_tab,'svg[aria-label="Like"]')
                result = await new_tab.evaluate('''
                () => {
                    // Find the SVG icon with aria-label="Like"
                    const svg = document.querySelector('svg[aria-label="Like"]');

                    if (svg) {
                        // Get the closest clickable parent (usually a button or div)
                        const clickableParent = svg.closest('button, div[role="button"], span');

                        if (clickableParent) {
                            clickableParent.scrollIntoView({ behavior: "smooth", block: "center" });
                            clickableParent.click();
                            console.log("✅ 'Like' button clicked successfully!");
                        } else {
                            console.log("⚠️ Found SVG but no clickable parent detected!");
                        }
                    } else {
                        console.log("❌ 'Like' button not found!");
                    }
                }
                ''')
                if 'button clicked successfully!'.lower() in result.lower():
                    done_task = 1
            except Exception as err:
                print(f' THIS ERROR OCCURED {err}')

                
        elif 'THREADS/Post Comment'.lower() in task.lower():
            try:
                print('Commenting on the post...')
                await css_scroll_center(new_tab,'svg[aria-label="Reply"]')
                await new_tab.evaluate('''
                    () => {
                        const svg = document.querySelector('svg[aria-label="Reply"]');
                        if (svg) {
                            const clickableParent = svg.closest('button, div[role="button"], span');
                            if (clickableParent) {
                                clickableParent.scrollIntoView({ behavior: "smooth", block: "center" });
                                clickableParent.click();
                                console.log("✅ 'Reply' button clicked successfully!");
                            } else {
                                console.log("⚠️ Found SVG but no clickable parent detected!");
                            }
                        } else {
                            console.log("❌ 'Reply' button not found!");
                        }
                    }
                ''')

                text_area = await new_tab.waitForSelector('div[aria-label="Empty text field. Type to compose a new post."]', timeout=10000)
                await text_area.click()
                await asyncio.sleep(1)
                await text_area.click()
                await text_area.type('GREAT CONTENT')
                await asyncio.sleep(1)
                result = await new_tab.evaluate('''
                () => {
                    // Find the button containing the word 'Post'
                    const postButton = Array.from(document.querySelectorAll('div[role="button"]'))
                        .find(el => el.innerText && el.innerText.trim().toLowerCase() === "post");

                    if (postButton) {
                        // Scroll to make sure it's visible, then click it
                        postButton.scrollIntoView({ behavior: "smooth", block: "center" });
                        postButton.click();
                        console.log("✅ 'Post' button clicked successfully!");
                        return "✅ 'Post' button clicked successfully!";
                    } else {
                        console.log("❌ 'Post' button not found on this page!");
                        return "❌ 'Post' button not found on this page!";
                    }
                }
                ''')

                if 'button clicked successfully!'.lower() in result.lower():
                    done_task = 1
            except Exception as err:
                print(f' THIS ERROR OCCURED {err}')
        

        elif 'THREADS/Post View'.lower() in task.lower():
            try:
                print('\n CURRENTLY ON VIEWING OF POST \n')
                await asyncio.sleep(3)
                done_task = 1
            except Exception as err:
                print(f' THIS ERROR OCCURED {err}')


        elif 'THREADS/Threads Repost'.lower() in task.lower():
            try:
                await css_scroll_center(new_tab,'svg[aria-label="Repost"]')
                await new_tab.evaluate('''
                    () => {
                        const svg = document.querySelector('svg[aria-label="Repost"]');
                        if (svg) {
                            const clickableParent = svg.closest('button, div[role="button"], span');
                            if (clickableParent) {
                                clickableParent.scrollIntoView({ behavior: "smooth", block: "center" });
                                clickableParent.click();
                                console.log("✅ 'Repost' button clicked successfully!");
                            } else {
                                console.log("⚠️ Found SVG but no clickable parent detected!");
                            }
                        } else {
                            console.log("❌ 'Repost' button not found!");
                        }
                    }
                ''')
                await asyncio.sleep(1)
                result = await new_tab.evaluate('''
                () => {
                    // Find any <div role="button"> that contains text 'Repost'
                    const repostBtn = Array.from(document.querySelectorAll('div[role="button"]'))
                        .find(el => el.innerText && el.innerText.trim().toLowerCase() === "repost");

                    if (repostBtn) {
                        repostBtn.scrollIntoView({ behavior: "smooth", block: "center" });
                        repostBtn.click();
                        console.log("✅ 'Repost' button clicked successfully!");
                        return "✅ 'Repost' button clicked successfully!";
                    } else {
                        console.log("❌ 'Repost' button not found!");
                        return "❌ 'Repost' button not found!";
                    }
                }
                ''')
                if 'button clicked successfully!'.lower() in result.lower():
                    done_task = 1
            except Exception as err:
                print(f' THIS ERROR OCCURED {err}')

                

        else:
            pass


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
            await asyncio.sleep(1)
            await xpath_click_center(page, "//button[contains(text(), 'Submit Task')]")
            await page.waitForNavigation({'waitUntil': 'networkidle2', 'timeout': 30000})
            await page.waitForSelector('#contactList', {'timeout': 30000})
            print("✅ Contact list loaded successfully after automatic reload!")
        else:
            pass