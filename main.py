import praw
import praw.models
import gtts 
import playwright
from playwright.sync_api import sync_playwright, Playwright
from moviepy.editor import *
import os
from random import randint
reddit = praw.Reddit(
    client_id = "gEuZsqs-ZYcV3ueKSrsV_Q",
    client_secret = "wKLAqtnx91UWtHJIZ7EFRRw_QREsSA",
    user_agent = "python:tiktokbot:v0.1 (by u/neveredditstories)"
)
def fetch_selected():
    global url
    global title
    global comment_dic
    global comment
    comment_counter  = 0
    comment_dic = {}
    selected = input("Enter submission id: ")
    submission = reddit.submission(selected)
    print("Fetching data from reddit")
    url = submission.url
    title = submission.title
    submission.comment_sort = "top"
    submission.comments.replace_more(limit = 0)
    for comment in submission.comments:
        if comment_counter == 10:
            break
        else:
            if isinstance(comment, praw.models.MoreComments) or comment.stickied or len(comment.body) > 150 or comment.body == "[removed]":
                continue
            comment_counter += 1
            comment_dic[comment_counter] = comment.body, comment.id
def fetch_submission():
    global title
    global comment_dic
    global url
    global comment
    selected = input("Select subreddit: r/")
    print("Fetching data from reddit")
    comment_counter  = 0
    comment_dic = {}
    for submission in reddit.subreddit(selected).hot(limit = 10):
        id = submission.id
        url = submission.url
        if not submission.stickied:
            if "AITA" in submission.title:
                title = submission.title.replace("AITA", "Am i the asshole for")
            else:
                title = submission.title
            break
    submission.comment_sort = "top"
    submission.comments.replace_more(limit = 0)
    for comment in submission.comments:
        if len(comment_dic) == 10:
            break
        else:
            if isinstance(comment, praw.models.MoreComments) or comment.stickied or len(comment.body) > 150 or comment.body == "[removed]":
                continue
            else:
                comment_counter += 1
                comment_dic[comment_counter] = comment.body, comment.id

def text_to_speech():
    print("Creating the audios")
    text = title
    title_tts = gtts.gTTS(text = text, lang="en", slow=False)
    title_tts.save("title.mp3")
    for num in range(len(comment_dic)):
        text = comment_dic[num + 1][0]
        comment_text = gtts.gTTS(text = text, lang="en", slow=False)
        comment_text.save(f"audio/comment{num + 1}.mp3")
        print(f"Audios Created {num + 1}/10")

def screen_shot():
    print("Getting the screenshots")
    id = 0
    with sync_playwright() as p:
        chrome = p.chromium.launch(headless=False)
        page = chrome.new_page()
        page.goto(url)
        page.locator("div.flex.justify-between.text-12.px-md.relative.xs\\:px-0.pb-2xs.pt-md").screenshot(path="main_post/auhtor.png")
        page.locator("h1.font-semibold.text-neutral-content-strong.m-0.text-18.xs\\:text-24.mb-xs.px-md.xs\\:px-0.xs\\:mb-md.overflow-hidden").screenshot(path="main_post/title.png")
        for id in range(len(comment_dic)):
            id += 1
            trimed_url = url.split("/")
            new_url = "/".join(trimed_url[0:7]) 
            finished_url = new_url + "/comment/" + f"{comment_dic[id][1]}"
            page.goto(finished_url)
            page.locator("summary.grid.grid-cols-\\[24px_minmax\\(0\\,1fr\\)\\].xs\\:grid-cols-\\[32px_minmax\\(0\\,1fr\\)\\]").nth(0).screenshot(path=f"users/comment_user{id}.png")
            page.locator("div.md.text-14.rounded-\\[8px\\].pb-2xs.overflow-hidden").nth(0).screenshot(path=f"comments/comment{id}.png")
            
def calculate():
    print("Editing the video")
    title_audio = AudioFileClip("title.mp3")
    amk = 0
    audio_stamps = title_audio.duration
    audios = [title_audio]
    images = [ImageClip("main_post/title.png").set_duration(title_audio.duration).set_position((50,550)),ImageClip("main_post/auhtor.png").set_duration(title_audio.duration).set_position((50,500))]
    index = 0
    for i in range(len(comment_dic)):
        index += 1
        audio = AudioFileClip(f"audio/comment{index}.mp3").set_start(audio_stamps)
        audios.append(audio)
        img = ImageClip(f"comments/comment{index}.png").set_start(audio_stamps).set_duration(audio.duration).set_position((50,540)).resize(width=620)
        header = ImageClip(f"users/comment_user{index}.png").set_start(audio_stamps).set_duration(audio.duration).set_position((50,500))
        images.append(img)
        images.append(header)
        audio_stamps += audio.duration
        amk += audio.duration
    length = amk + title_audio.duration
    audios.append(AudioFileClip("music.mp3").set_duration(length + 1).fx(afx.volumex, 0.1))
    bmk = CompositeAudioClip(audios)
    random = randint(1,3)
    vid = VideoFileClip(f"video/{random}.mp4").subclip(10,length + 11)
    images.insert(0,vid)
    final_wo = CompositeVideoClip(images).fx(vfx.fadein, 1)
    final = final_wo.set_audio(bmk)
    final.write_videofile("/Users/umuttengiz/Desktop/done.mp4", codec="libx264", audio_codec="aac")
dir = os.getcwd()
file = os.path.join(dir, "audio")
file1 = os.path.join(dir, "comments")
file2 = os.path.join(dir, "users")
file3 = os.path.join(dir, "main_post")
file4 = os.path.join(dir, "title.mp3")
def clean_up():
    print("Cleaning up the folder")
    for i in os.listdir(file):
        file_path = os.path.join(file, i)
        if os.path.isfile(file_path) and i.endswith(('.mp3')):
            os.remove(file_path)
    for i in os.listdir(file1):
        file_path = os.path.join(file1, i)
        if os.path.isfile(file_path) and i.endswith(('.png')):
            os.remove(file_path)
    for i in os.listdir(file2):
        file_path = os.path.join(file2, i)
        if os.path.isfile(file_path) and i.endswith(('.png')):
            os.remove(file_path)
    for i in os.listdir(file3):
        file_path = os.path.join(file3, i)
        os.remove(file_path)
    os.remove(file4)
while True:
    answer = input("Do you want to enter a submission or subreddit(1/2): ")
    if answer == "1":
        fetch_selected()
        break
    elif answer == "2":
        fetch_submission()
        break

text_to_speech()
screen_shot()
calculate()
clean_up()


