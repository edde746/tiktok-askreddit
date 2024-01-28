from moviepy.editor import *
import random,os
import PIL

resolution = (1080,1920)

def render(name):
    # Create clip 'flow'
    flow = ['post']
    for i in range(10):
        if os.path.exists(f'output/{i}.mp3'):
            flow.append(str(i))

    # Load all the clips
    image_clips = []
    sound_clips = []
    duration = 0
    for part in flow:
        sound_clips.append(AudioFileClip(f"output/{part}.mp3"))
        image_clips.append(ImageClip(f"output/{part}.png").set_duration(sound_clips[-1].duration))
        duration += sound_clips[-1].duration
        # Ensure length of video
        if duration > 90:
            break

    # Combine all the clips into one
    image_clips = concatenate_videoclips(image_clips).set_position(("center","center"))
    sound_clips = concatenate_audioclips(sound_clips)

    # 3 minute limit
    if sound_clips.duration > 60*2.9:
        return False

    #Loading background
    background_clip = "backgrounds/" + random.choice(os.listdir("backgrounds"))
    background = VideoFileClip(background_clip).loop(n=None).set_duration(sound_clips.duration).resize((resolution[0],resolution[1]), PIL.Image.Resampling.LANCZOS) 

    # Overlaying background
    final = CompositeVideoClip([background, image_clips]).set_audio(sound_clips)

    # Save video
    final.write_videofile(f"render/{name}.mp4", fps=30, threads=8, preset='ultrafast', audio_codec='aac', remove_temp=True)
    return True
