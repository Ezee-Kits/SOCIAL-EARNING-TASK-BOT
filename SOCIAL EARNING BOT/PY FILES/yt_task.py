import time
import asyncio
import pyperclip

from func import css_click_center,xpath_click_center,css_scroll_center



async def YT_Task_Bot(page,task,task_url):
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
        # return False
    
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

        if 'YOUTUBE/Channel Subscribe---Video like---Video Comment'.lower() in task.lower():
            print(' \n CURRENTLY ON YOUTUBE/Channel Subscribe---Video like---Video Comment \n')
            try:
                #================ SUBSCRIBE =============
                subscribe_button_selector = '#subscribe-button yt-button-shape button'
                await new_tab.waitForSelector(subscribe_button_selector)
                clicked = await new_tab.evaluate(f'''
                    (function() {{
                        const subscribeBtn = document.querySelector("{subscribe_button_selector}");
                        if (subscribeBtn) {{
                            subscribeBtn.click();
                            return true;
                        }} else {{
                            return false;
                        }}
                    }})()
                ''')

                if clicked:
                    print("Subscribe button clicked ✅")
                else:
                    print("Subscribe button not found ⚠️")

                #================ VIDEO LIKE =====================
                await css_scroll_center(new_tab,'button-view-model button[aria-pressed]')
                result = await new_tab.evaluate("""
                () => {
                    const likeButton = document.querySelector('button-view-model button[aria-pressed]');
                    if (likeButton) {
                        likeButton.scrollIntoView({ behavior: "smooth", block: "center" });
                        likeButton.click();
                        return "✅ Like button clicked!";
                    } else {
                        return "❌ Like button not found!";
                    }
                }
                """)


                #=================== VIDEO COMMENT =======================
                await new_tab.waitForSelector('video')
                for i in range(12):  # scroll 10 times
                    await new_tab.evaluate('window.scrollBy(0, window.innerHeight)')
                    try:
                        checking_scroll = await page.waitForSelector('#placeholder-area', {'visible': True, 'timeout': 2500})
                        if checking_scroll:
                            break                        
                    except:
                        print('Nothing found after the scroll')


                await css_scroll_center(new_tab,'#placeholder-area')
                await new_tab.evaluate('''
                    const commentSection = document.querySelector('#placeholder-area');
                    if (commentSection) {
                        commentSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                ''')
                comment_box = await new_tab.evaluate('''
                    const commentBox = document.querySelector('#placeholder-area #simplebox-placeholder');
                    if (commentBox) {
                        commentBox.click();

                        const textArea = commentBox.closest('ytd-comment-simplebox-renderer')
                                            .querySelector('#contenteditable-root');
                        if (textArea) {
                            textArea.innerText = 'Great Content';

                            const postButton = commentBox.closest('ytd-comment-simplebox-renderer')
                                                        .querySelector('#submit-button');
                            if (postButton) {
                                postButton.click();
                                console.log("Comment posted ✅");
                            } else {
                                console.log("Post button not found ⚠️");
                            }
                        } else {
                            console.log("Textarea not found ⚠️");
                        }
                    } else {
                        console.log("Comment box not found ⚠️");
                    }
                ''')
                if comment_box:
                    done_task = 1
            except:
                print(' \n WAS NOT ABLE TO CARRYOUT THE YOUTUBE/Channel Subscribe---Video like---Video Comment {{{TASK}}} \n')


        elif 'YOUTUBE/Video Views'.lower() in task.lower():
            print(' \n CURRENTLY ON YOUTUBE/Video Views \n')
            await new_tab.waitForSelector('video')
            print('Playing video for views...')
            await new_tab.evaluate("""
                const vid = document.querySelector('video');
                if (vid) {
                    vid.muted = true;  // Avoid autoplay restrictions
                    vid.play();
                }
            """)
            print('done playing video for views')
            done_task = 1


        elif '5 minute(s) Watch hour'.lower() in task.lower():
            await new_tab.waitForSelector('video')
            await new_tab.evaluate("""
                const vid = document.querySelector('video');
                if (vid) {
                    vid.muted = true;  // Avoid autoplay restrictions
                    vid.play();
                }
            """)
            print('done playing video for views')
            done_task = 1
            await asyncio.sleep(10)  # Wait for 5 minutes (20 seconds)
        

        elif 'YOUTUBE/Video Comment'.lower() in task.lower():
            await new_tab.waitForSelector('video')
            for i in range(12):  # scroll 10 times
                await new_tab.evaluate('window.scrollBy(0, window.innerHeight)')
                try:
                    checking_scroll = await page.waitForSelector('#placeholder-area', {'visible': True, 'timeout': 2500})
                    if checking_scroll:
                        break                        
                except:
                    print('Nothing found after the scroll')

            await css_scroll_center(new_tab,'#placeholder-area')
            await new_tab.evaluate('''
                const commentSection = document.querySelector('#placeholder-area');
                if (commentSection) {
                    commentSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            ''')

            # Click the comment box, type comment, and click post
            comment_box = await new_tab.evaluate('''
                const commentBox = document.querySelector('#placeholder-area #simplebox-placeholder');
                if (commentBox) {
                    commentBox.click();

                    const textArea = commentBox.closest('ytd-comment-simplebox-renderer')
                                        .querySelector('#contenteditable-root');
                    if (textArea) {
                        textArea.innerText = 'Great Content';

                        const postButton = commentBox.closest('ytd-comment-simplebox-renderer')
                                                    .querySelector('#submit-button');
                        if (postButton) {
                            postButton.click();
                            console.log("Comment posted ✅");
                        } else {
                            console.log("Post button not found ⚠️");
                        }
                    } else {
                        console.log("Textarea not found ⚠️");
                    }
                } else {
                    console.log("Comment box not found ⚠️");
                }
            ''')
            if comment_box:
                done_task = 1



        elif 'YOUTUBE/Channel Subscribe'.lower() in task.lower():
            subscribe_button_selector = '#subscribe-button yt-button-shape button'
            await new_tab.waitForSelector(subscribe_button_selector)
            clicked = await new_tab.evaluate(f'''
                (function() {{
                    const subscribeBtn = document.querySelector("{subscribe_button_selector}");
                    if (subscribeBtn) {{
                        subscribeBtn.click();
                        return true;
                    }} else {{
                        return false;
                    }}
                }})()
            ''')

            if clicked:
                print("Subscribe button clicked ✅")
                done_task = 1
            else:
                print("Subscribe button not found ⚠️")
            await asyncio.sleep(2)
        

        elif 'YOUTUBE/like'.lower() in task.lower():
            print(' \n CURRENTLY ON YOUTUBE/Video Like \n')
            await css_scroll_center(new_tab,'button-view-model button[aria-pressed]')
            result = await new_tab.evaluate("""
            () => {
                const likeButton = document.querySelector('button-view-model button[aria-pressed]');
                if (likeButton) {
                    likeButton.scrollIntoView({ behavior: "smooth", block: "center" });
                    likeButton.click();
                    return "✅ Like button clicked!";
                } else {
                    return "❌ Like button not found!";
                }
            }
            """)
            if 'Like button clicked'.lower() in result.lower():
                done_task = 1


        else:
            print("No matching task found. Skipping...")    



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

