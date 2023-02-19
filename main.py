import os
import ffmpeg

from utils import generate_script, get_pexels_video_url, download_video, gen_audio


def main():
    topic = input("Enter a topic: ")
    filename = input("Enter a filename: ")
    topic_script = generate_script(topic)
    print("Script generated \n")
    sentences = topic_script.split(".")
    dir_name = topic.replace(" ", "_")
    os.mkdir(dir_name)
    vid_dict = {}
    for i, sentence in enumerate(sentences):
        url = get_pexels_video_url(sentence)
        try:
            download_video(url, f"{dir_name}/{i}.mp4")
            vid_dict[sentence] = f"{dir_name}/{i}.mp4"
        except:
            vid_dict[sentence] = f"text"
    print("Videos downloaded \n")
    gen_audio(topic_script, f"{dir_name}/{filename}.mp3")
    print("Audio generated \n")
    vids_to_concat = []
    for sentence, vid in vid_dict.items():
        if vid == "text":
            pass
        else:
            vids_to_concat.append(ffmpeg.input(vid))
    for i, vid in enumerate(vids_to_concat):
        vids_to_concat[i] = vid.filter("scale", 1080, 1920)
    concat = ffmpeg.concat(*vids_to_concat)
    audio_length = ffmpeg.probe(f"{dir_name}/{filename}.mp3")["format"]["duration"]
    concat = concat.filter("trim", duration=audio_length)
    audio_file_name = f"{dir_name}/{filename}.mp3"
    audio = ffmpeg.input(audio_file_name)
    out = ffmpeg.output(concat, audio, f"{dir_name}/{filename}.mp4")
    out.run()
    print("Videos concatenated \n")


if __name__ == "__main__":
    main()
