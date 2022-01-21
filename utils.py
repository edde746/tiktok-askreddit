import logging,os
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def create_bot(headless=False):
    edge_options = EdgeOptions()
    edge_options.use_chromium = True
    edge_options.add_argument("--log-level=3")
    edge_options.add_argument('disable-infobars')
    if headless:
        edge_options.add_argument('headless')
        edge_options.add_argument('disable-gpu')

    driver = EdgeChromiumDriverManager(log_level=logging.NOTSET).install()
    bot = Edge(options=edge_options,executable_path=driver)

    bot.set_page_load_timeout(25)
    bot.set_window_size(1920, 1080)
    return bot