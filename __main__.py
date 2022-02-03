import asyncio,tts,os,video,requests
import imp
from scraper import scrape
from upload import upload_to_tiktok
from utils import config

async def main():
    # Fetching posts from r/AskReddit
    headers = { 'user-agent':'py-reddit-scraping:0:1.0 (by u/ur_name)' }
    posts = requests.get('https://www.reddit.com/r/AskReddit/top.json?t=day&limit=30', headers=headers).json()['data']['children']
    
    for post in posts:
        try:
            # Avoid getting banned, no NSFW posts
            if 'nsfw' in post['data']['whitelist_status']:
                continue

            url = post['data']['url']
            name = url.split('/')[-2]
            print(f"⏱ Processing post: {name}")

            # Make sure we have not already rendered/uploaded post
            if name in [entry.split('.')[0] for entry in os.listdir('render')]:
                print("❌ Post already processed!")
                continue

            # Clean 'temporary' files from last video
            for file in os.listdir('output'):
                os.remove(f'output/{file}')

            # Scraping the post, screenshotting, etc
            print("📸 Screenshotting post...")
            data = scrape(url)
            if not data:
                print("❌ Failed to screenshot post!")
                continue

            # Generate TTS clips for each comment
            print("\n📢 Generating voice clips...",end="",flush=True)
            voice = await tts.get_voice()
            for key in data.keys():
                print('.',end="",flush=True)
                await tts.generate(data[key], key, voice)

            # Render & Upload
            print("\n🎥 Rendering video...")
            if video.render(name):
                # Upload video if rendered
                print("🌟 Uploading to TikTok...")
                if upload_to_tiktok(name,data["post"]):
                    print("✅ Uploaded successfully!")
                else:
                    print("❌ Failed to upload!")
        except Exception as e:
            if config['debug']:
                raise e
            pass

if __name__ == '__main__':
    [os.mkdir(dir) for dir in ['output','render','backgrounds'] if not os.path.exists(dir)]
    asyncio.run(main())