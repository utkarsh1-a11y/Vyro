# This files look for new folder inside the user_uploads folder and converts them into reel if they are not aready converted.
import os
from text_to_audio import text_to_speech_file
import time
import subprocess

def text_to_audio(folder): # Convertes the text in the description.txt file to audio 
    with open(os.path.join("user_uploads", folder, "description.txt"), "r") as f:
        text = f.read()
        print(text,folder)
    text_to_speech_file(text, folder)

def create_reel(folder): # Generates the reel from the images and audio
    command = f'''ffmpeg -f concat -safe 0 -i user_uploads/{folder}/input.txt -i user_uploads/{folder}/audio.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/reels/{folder}.mp4'''
    subprocess.run(command, shell=True, check=True)



if(__name__ == "__main__"):  
    while True:
        print("Checking for new folders in user_uploads...")
        with open("done.txt", "r") as f:
            done_folders = f.read().splitlines() # Read the list of already processed folders from done.txt 
        
        for folder in os.listdir("user_uploads"):
            if folder not in done_folders:
                text_to_audio(folder) # Generate audio from the text in the description.txt file
                create_reel(folder)  # Create the reel from the images and audio 
                with open("done.txt", "a") as f:
                    f.write(folder + "\n")
        time.sleep(10) # Sleep for 10 seconds before checking for new folders again