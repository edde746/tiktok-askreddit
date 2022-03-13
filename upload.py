import time,os,utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from utils import config

# Huge credits to redianmarku
# https://github.com/redianmarku/tiktok-autouploader

def upload_to_tiktok(name,title):
    bot = utils.create_bot() # Might not work in headless mode
    bot.set_window_size(1920, 1080*2) # Ensure upload button is visible, does not matter if it goes off screen

    # Fetch main page to load cookies, sometimes infinte loads, except and pass to keep going
    try:
        bot.get('https://www.tiktok.com/')
    except:
        pass

    for cookie in config['tiktok_cookies'].split('; '):
        data = cookie.split('=')
        bot.add_cookie({'name':data[0],'value':data[1]})

    try:
        bot.get('https://www.tiktok.com/upload')
    except:
        pass

    bot.execute_script("document.querySelector('.cookie-banner').remove();")
    bot.switch_to.frame(bot.find_element_by_tag_name("iframe"))

    # Upload video
    file_uploader = WebDriverWait(bot, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[type="file"]')))
    file_uploader.send_keys(os.getcwd()+f'\\render\\{name}.mp4')

    # Focus caption element
    caption = WebDriverWait(bot, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.public-DraftStyleDefault-block.public-DraftStyleDefault-ltr')))
    ActionChains(bot).click(caption).perform()

    # Input title & tags
    print("✍ Writing description & adding tags...")
    try:
        ActionChains(bot).send_keys(title+" ").perform()
        tags = ["reddit","meme","askreddit","story","storytime","fyp"]
        for tag in tags:
            ActionChains(bot).send_keys("#"+tag).perform()
            WebDriverWait(bot, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.mentionSuggestions')))
            ActionChains(bot).send_keys(Keys.RETURN).perform()
            time.sleep(0.05)
    except:
        pass

    try:
        print("⏱ Waiting to post...")
        # Wait for 'Post' button to be active, then click
        post = WebDriverWait(bot, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.tiktok-btn-pc.tiktok-btn-pc-large.tiktok-btn-pc-primary:not(.tiktok-btn-pc-disabled)')))
        ActionChains(bot).move_to_element(post).perform()
        ActionChains(bot).click(post).perform()

        # Wait for confirmation, then exit
        WebDriverWait(bot,120).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#portal-container>div>div>div>.modal-btn.emphasis')))
        time.sleep(0.2)
        bot.close()
        return True
    except:
        bot.close()
        return False