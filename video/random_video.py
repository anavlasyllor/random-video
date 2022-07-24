from bs4 import BeautifulSoup
from requests import get
from random import randrange, choice, randint
from time import asctime
from datetime import datetime
from googleapiclient.discovery import build

special_words = ["car", "food", "travel", "rocket", "space"]


def get_api_key():
    with open("apikey.txt", "r", encoding="utf-8") as f:
        return f.read()


def get_random_number():
    number = randrange(10000)
    if number >= 1000:
        return str(number)
    if number >= 100:
        return "0" + str(number)
    if number >= 10:
        return "00" + str(number)
    if number >= 0:
        return "000" + str(number)


def get_random_img_search():
    if choice([True, False]):
        return "IMG " + get_random_number()
    else:
        return "IMG_" + get_random_number()


def get_random_wiki_search():
    if choice([True, False]):
        r = get("https://en.m.wikipedia.org/wiki/Special:Random#/random")
        soup = BeautifulSoup(r.content, "html.parser")
        if choice([True, False]):
            words = []
            for i in soup.find_all("p"):
                for j in i.text.split():
                    if j in words:
                        continue
                    words.append(j)
            return choice(words)
        else:
            return soup.title.text.split("-")[0]
    else:
        r = get("https://en.wikipedia.org/wiki/Main_Page")
        soup = BeautifulSoup(r.content, "html.parser")
        return choice(soup.text.split())


def get_random_word_list_search():
    f = open("words.txt", "r", encoding="UTF-8")
    data = f.read()
    f.close()
    words = data.split("\n")
    return choice(words)


def get_random_vid_search():
    year = randint(2009, datetime.now().year)
    month = randint(1, 12)
    day = randint(1, 30)
    if year == datetime.now().year:
        month = randint(1, datetime.now().month)
    if month > datetime.now().month:
        day = randint(1, datetime.now().day)
    year = str(year)
    if month < 10:
        month = "0" + str(month)
    month = str(month)
    if day < 10:
        day = "0" + str(day)
    day = str(day)
    return "vid {}{}{}".format(year, month, day)


def get_random_mvi_search():
    if choice([True, False]):
        return "MVI " + get_random_number()
    else:
        return "MVI_" + get_random_number()


def get_random_mov_search():
    if choice([True, False]):
        return "MOV " + get_random_number()
    else:
        return "MOV_" + get_random_number()


def get_new_video():
    word = choice(["img", "vid", "mvi", "mov"])
    return youtube_search(word, new=True), word


def special_search(word):
    with open("special_search/{}.txt".format(word), "r", encoding="UTF-8") as f:
        data = f.read()
    return choice(data.splitlines())


def get_word(word=False, img=False, wiki=False, word_list=False, vid=False, mvi=False, mov=False):
    # random word types
    case = None
    if not word:
        case = randrange(6)
        if case == 0:
            word = get_random_img_search()
        if case == 1:
            word = get_random_wiki_search()
        if case == 2:
            word = get_random_word_list_search()
        if case == 3:
            word = get_random_vid_search()
        if case == 4:
            word = get_random_mvi_search()
        if case == 5:
            word = get_random_mov_search()

    # designed types
    if img:
        word, case = get_random_img_search(), 0
    if wiki:
        word, case = get_random_wiki_search(), 1
    if word_list:
        word, case = get_random_word_list_search(), 2
    if vid:
        word, case = get_random_vid_search(), 3
    if mvi:
        word, case = get_random_mvi_search(), 4
    if mov:
        word, case = get_random_mov_search(), 5

    return word, case


def youtube_search(word, new=False):
    if new:
        order = "date"
    else:
        order = choice(["date", "rating", "relevance", "title", "videoCount", "viewCount"])

    youtube = build("youtube", "v3", developerKey=get_api_key())
    search_response = youtube.search().list(
        q=word,
        part='snippet',
        maxResults=100,
        order=order
    ).execute()

    videos = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append('%s' % (search_result['id']['videoId']))
    return videos


def get_random_video_id(word=None, img=False, wiki=False, word_list=False, vid=False, mvi=False,
                        mov=False, new=False, ip=None):
    if (new or randrange(7) == 0) and (
            not img and not wiki and not word_list and not vid and not mvi and not mov) and (not word or word == "new"):
        id, word = get_new_video()
        save(word, -1, id, ip)
        return id  # get only new videos

    while True:
        special_word = False
        word, case = get_word(word=word, img=img, wiki=wiki, word_list=word_list, vid=vid, mvi=mvi, mov=mov)
        if word == "favicon.ico":
            word, case = get_random_wiki_search(), 1
        elif word == "car":
            special_word, word, case = "car", special_search("car"), -2
        elif word == "food":
            special_word, word, case = "food", special_search("food"), -2
        elif word == "travel":
            special_word, word, case = "travel", special_search("travel"), -2
        elif word == "rocket":
            special_word, word, case = "rocket", special_search("rocket"), -2
        elif word == "space":
            special_word, word, case = "space", special_search("space"), -2
        else:
            pass

        video_ids = youtube_search(word)

        id = None
        try:
            id = choice(video_ids)
            break
        except IndexError:
            continue

    save(word, case, id, ip, special_word)
    return id


def save(word, case, id, ip, special_word=False):
    with open("data.txt", "a", encoding="UTF-8") as f:
        if special_word:
            f.write("{} => {} => {} => {} => {} => {}\n".format(asctime(), ip, case, special_word, word, id))
        else:
            f.write("{} => {} => {} => {} => {}\n".format(asctime(), ip, case, word, id))
