from django.shortcuts import render
from .random_video import get_random_video_id
from time import asctime

# Create your views here.
youtube_embed_url = "https://www.youtube.com/embed/"


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_download_ips():
    with open("download.txt", "r", encoding="utf-8") as f:
        data = f.read()
    ips = []
    for i in data.split("\n"):
        try:
            ips.append(i.split(" => ")[1])
        except IndexError:
            continue
    return ips


def index(request, word=None):
    # get designed types
    if word == "img":
        url = youtube_embed_url + get_random_video_id(word, img=True, ip=get_client_ip(request))
    elif word == "wiki":
        url = youtube_embed_url + get_random_video_id(word, wiki=True, ip=get_client_ip(request))
    elif word == "word_list":
        url = youtube_embed_url + get_random_video_id(word, word_list=True, ip=get_client_ip(request))
    elif word == "vid":
        url = youtube_embed_url + get_random_video_id(word, vid=True, ip=get_client_ip(request))
    elif word == "mvi":
        url = youtube_embed_url + get_random_video_id(word, mvi=True, ip=get_client_ip(request))
    elif word == "mov":
        url = youtube_embed_url + get_random_video_id(word, mov=True, ip=get_client_ip(request))
    elif word == "new":
        url = youtube_embed_url + get_random_video_id(word, new=True, ip=get_client_ip(request))
    # get designed word or not designed random word
    else:
        url = youtube_embed_url + get_random_video_id(word, ip=get_client_ip(request))
    context = {
        "url": url,
    }
    return render(request, "index.html", context)


def download(request):
    with open("download.txt", "a", encoding="UTF-8") as f:
        f.write("{} => {}\n".format(asctime(), get_client_ip(request)))
    context = {
    }
    return render(request, "download.html", context)
