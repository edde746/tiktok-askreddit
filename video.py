from moviepy.editor import *
import random,os

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
        image_clips.append(ImageClip(f"output/{part}.png",duration=sound_clips[-1].duration).fx(vfx.resize,width=resolution[0]*0.9).set_position(("center","center")))
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
    background = VideoFileClip(background_clip).fx(vfx.resize, height=resolution[1]).fx(vfx.loop, duration=image_clips.duration).set_position(("center","center"))
    
    # Composite all the components
    composite = CompositeVideoClip([background,image_clips],resolution)
    composite.audio = sound_clips
    composite.duration = sound_clips.duration

    # Render
    composite.write_videofile(f'render/{name}.mp4',threads=4,fps=24)
    return True
