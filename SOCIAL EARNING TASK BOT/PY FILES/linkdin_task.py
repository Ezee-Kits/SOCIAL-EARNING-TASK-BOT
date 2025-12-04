import asyncio
from func import css_click_center,xpath_click_center,css_scroll_center





page_follow_amt = 0

async def LinkedIn_Task_Bot(page,task,task_url):
    global page_follow_amt
    await page.bringToFront()

    if page_follow_amt >=8 and 'FACEBOOK/Page Follow'.lower() in task.lower():
        print('[ ERROR] TRYING TO RUN FACEBOOK FOLLOW OPTION ')
        return False
    
    await page.goto(url=task_url,waitUntil='networkidle2')

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
            await new_tab.waitForSelector('body', {'timeout': 30000})
        except Exception:
            print("[INFO] Page loaded with dynamic content (no full navigation).")

        if 'linkedin' in new_tab.url.lower():
            print("✅ New tab loaded with LinkedIn URL.")
        else:
            print("❌ New tab does not have a LinkedIn URL.")
            return False
        
        await asyncio.sleep(1)
        print('\n \n CURRENT TASK TO PERFORM :: ',task,'\n \n')


        done_task = 0
        print('LINKDIN page_follow_amt ==',page_follow_amt)


        if 'LINKEDIN/Page Follow'.lower() in task.lower():
            try:
                print('FOLLOWING LINKED-IN PAGE')
                await new_tab.waitForSelector('button[type="button"]', timeout=10000)
                done_task = 1
                await css_scroll_center(new_tab,'button[aria-label^="Follow"][type="button"]')

                result = await new_tab.evaluate("""
                    () => {
                        const followBtn = document.querySelector('button[aria-label="Follow"][type="button"]');
                        if (followBtn) {
                            followBtn.click();
                            return "✅ Follow button clicked successfully.";
                        } else {
                            return "❌ Follow button not found.";
                        }
                    }
                """)

                if 'Follow button clicked successfully' in result:
                    done_task = 1
                    page_follow_amt += 1
                else:
                    print("Follow button not found ⚠️")
            except Exception as err:
                print(f' THIS ERROR OCCURED {err}')




        elif 'LINKEDIN/Post Like'.lower() in task.lower():
            try:
                print('LINKING PAGE')
                await css_scroll_center(new_tab,'span')
                result = await new_tab.evaluate('''
                    () => {
                        const likeBtn = Array.from(document.querySelectorAll('div.flex-wrap.justify-center'))
                            .find(div => {
                                const span = div.querySelector('span.artdeco-button__text');
                                return span && span.innerText.trim() === 'Like';
                            });

                        if (likeBtn) {
                            likeBtn.scrollIntoView({ behavior: 'smooth', block: 'center' })
                            likeBtn.click()
                            return "✅ 'Like' button clicked successfully."
                        } else {
                            return "❌ 'Like' button not found."
                        }
                    }
                ''')
                if result:
                    done_task = 1
            except Exception as err:
                print(f' THIS ERROR OCCURED {err}')


   
        elif 'LINKEDIN/Post Comment'.lower() in task.lower():
            try:
                print('LINKEDIN PAGE COMMENTING')
                await css_scroll_center(new_tab,'div[contenteditable="true"][aria-placeholder="Add a comment…"]')
                comment_box = await new_tab.waitForSelector('div[contenteditable="true"][aria-placeholder="Add a comment…"]')
                await comment_box.click()
                await asyncio.sleep(1)
                await comment_box.click()
                await comment_box.type('Great Content as always',delay=50)
                await asyncio.sleep(1)
                result = await new_tab.evaluate('''
                () => {
                    const commentBtn = Array.from(document.querySelectorAll('button'))
                        .find(btn =>
                            btn.innerText &&
                            btn.innerText.trim() === 'Comment' &&
                            btn.className.includes('comments-comment-box__submit-button')
                        );

                    if (commentBtn) {
                        commentBtn.scrollIntoView({ behavior: 'smooth', block: 'center' })
                        commentBtn.click()
                        return "✅ Targeted 'Comment' button clicked successfully."
                    } else {
                        return "❌ Targeted 'Comment' button not found."
                    }
                }
                ''')
                if result:
                    done_task =1
            except Exception as err:
                print(f' THIS ERROR OCCURED {err}')



        elif 'LINKEDIN/Page Connect'.lower() in task.lower():
            try:
                print('LINKED-IN PAGE CONNECT')
                await new_tab.waitForSelector('button',timeout = 10000)
                connect_script = """
                () => {
                    const connectButton = Array.from(document.querySelectorAll('button'))
                        .find(btn => btn.innerText.trim() === "Connect");

                    if (connectButton) {
                        connectButton.scrollIntoView({ behavior: "smooth", block: "center" });
                        connectButton.click();
                        return "✅ 'Connect' button clicked successfully!";
                    } else {
                        return "❌ 'Connect' button not found on the page.";
                    }
                }
                """

                # Run inside your async function or event loop
                result = await new_tab.evaluate(connect_script)
                print(result)
                await asyncio.sleep(3)

                # Pyppeteer version of the "Send without a note" button click script
                send_script = """
                () => {
                    const sendButton = Array.from(document.querySelectorAll('button'))
                        .find(btn => btn.innerText.trim() === "Send without a note");

                    if (sendButton) {
                        sendButton.scrollIntoView({ behavior: "smooth", block: "center" });
                        sendButton.click();
                        return "✅ 'Send without a note' button clicked successfully!";
                    } else {
                        return "❌ 'Send without a note' button not found on the page.";
                    }
                }
                """

                # Run the script inside your async function or event loop
                result2 = await new_tab.evaluate(send_script)
                if 'button clicked successfully!' in result2:
                    done_task = 1
            except Exception as err:
                print(f' THIS ERROR OCCURED {err}')

        
        else:
            pass


        
        if done_task ==0:
            await asyncio.sleep(1)
            await new_tab.close()

        elif done_task==1:
            await asyncio.sleep(3)
            if element_exists:
                await new_tab.screenshot({'path': 'screenshot.jpg','type': 'jpeg','quality': 70,'fullPage': True})


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