import sys
import pafy
from pydub import AudioSegment

def download_videos(singer, n):
    videos = []
    for i in range(n):
        # Search for the next video of the singer on YouTube
        query = f"{singer} - video {i + 1}"
        video = pafy.new(query)
        # Download the video
        video.getbest().download()
        videos.append(video)
    return videos

def convert_to_audio(videos):
    audios = []
    for video in videos:
        # Convert the video to audio
        audio = AudioSegment.from_file(video.filename, video.extension[1:])
        audios.append(audio)
    return audios

def cut_audio(audios, duration):
    cut_audios = []
    for audio in audios:
        # Cut the first `duration` seconds of the audio
        cut_audio = audio[:duration * 1000]
        cut_audios.append(cut_audio)
    return cut_audios

def merge_audios(audios, output_filename):
    # Merge all of the audios into a single output file
    merged_audio = sum(audios)
    merged_audio.export(output_filename, format="mp3")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Incorrect number of parameters.")
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)
    
    singer = sys.argv[1]
    n = int(sys.argv[2])
    if n <= 10:
        print("Number of videos must be greater than 10.")
        sys.exit(1)
    
    duration = int(sys.argv[3])
    if duration <= 20:
        print("Audio duration must be greater than 20 seconds.")
        sys.exit(1)
    
    output_filename = sys.argv[4]
    
    try:
        videos = download_videos(singer, n)
        audios = convert_to_audio(videos)
        cut_audios = cut_audio(audios, duration)
        merge_audios(cut_audios, output_filename)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    
    print(f"Successfully created output file: {output_filename}")
