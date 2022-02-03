# AskReddit TikTok Bot
Automatic content bot using Selenium to scrape AskReddit and and post to TikTok with video rendering with MoviePY.
# Usage
Requires some manual setup, 
1. Install pip packages from `requirements.txt`
2. Get cookies for TikTok & Reddit
   1. Sign into TikTok in your browser by choice
   2. Open DevTools and go to the network tab
   3. Reload the page and find the sent cookie header
   4. Copy the header and save to `tiktok_cookies` in `config.yaml`
   5. Repeat for Reddit, however there is no need to sign in, only accept cookies to get rid of notice (`reddit_cookies` this time)
3. Add background video files to `backgrounds` folder, find some [here](https://www.pexels.com/videos/)
3. Enjoy!