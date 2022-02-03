import yaml
import undetected_chromedriver as uc

# Load and validate config
config = yaml.safe_load(open('config.yaml').read())

if not config['tiktok_cookies']:
    raise Exception('Missing TikTok Cookies')

if not config['reddit_cookies']:
    raise Exception('Missing Reddit Cookies')

def create_bot(headless=False):
    options = uc.ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_argument('disable-infobars')
    if headless:
        options.headless = True

    bot = uc.Chrome(options=options)

    bot.set_page_load_timeout(25)
    bot.set_window_size(1920, 1080)
    return bot