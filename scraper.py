import time,re,utils,string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape(post_url):
    bot = utils.create_bot(headless=True)
    data = {}
    
    try:
        # Load cookies to prevent cookie overlay & other issues
        bot.get('https://www.reddit.com')
        for cookie in open('reddit.cookies','r').read().split('; '):
            cookie_data = cookie.split('=')
            bot.add_cookie({'name':cookie_data[0],'value':cookie_data[1],'domain':'reddit.com'})
        bot.get(post_url)

        # Fetching the post itself, text & screenshot
        post = WebDriverWait(bot, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.Post')))
        post_text = post.find_element_by_css_selector('h1').text
        data['post'] = post_text
        post.screenshot('output/post.png')

        # Let comments load
        bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # Fetching comments & top level comment determinator
        comments = bot.find_elements_by_css_selector('div[id^=t1_][tabindex]')
        allowed_style = comments[0].get_attribute("style")
        
        # Filter for top only comments
        NUMBER_OF_COMMENTS = 5
        comments = [comment for comment in comments if comment.get_attribute("style") == allowed_style][:NUMBER_OF_COMMENTS]

        print('💬 Scraping comments...',end="",flush=True)
        # Save time & resources by only fetching X content
        for i in range(len(comments)):
            try:
                print('.',end="",flush=True)
                # Filter out locked comments (AutoMod) 
                try:
                    comments[i].find_element_by_css_selector(".icon.icon-lock_fill")
                    continue
                except:
                    pass

                # Scrolling to the comment ensures that the profile picture loads
                # Credits: https://stackoverflow.com/a/57630350
                desired_y = (comments[i].size['height'] / 2) + comments[i].location['y']
                window_h = bot.execute_script('return window.innerHeight')
                window_y = bot.execute_script('return window.pageYOffset')
                current_y = (window_h / 2) + window_y
                scroll_y_by = desired_y - current_y

                bot.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
                time.sleep(0.2)

                # Getting comment into string
                text = "\n".join([element.text for element in comments[i].find_elements_by_css_selector('.RichTextJSON-root')])

                # Screenshot & save text
                comments[i].screenshot(f'output/{i}.png')
                data[str(i)] = ''.join(filter(lambda c: c in string.printable, text))
            except Exception as e:
                pass

        if bot.session_id:
            bot.quit()
        return data
    except Exception as e:
        if bot.session_id:
            bot.quit()
        return False