import pytube


def download_video(url, resolution):
    itag = choose_resolution(resolution)
    video = pytube.YouTube(url)
    stream = video.streams.get_by_itag(itag)
    stream.download()
    return stream.default_filename


def download_videos(urls, resolution):
    for url in urls:
        download_video(url, resolution)


def download_playlist(url, resolution):
    playlist = pytube.Playlist(url)
    download_videos(playlist.video_urls, resolution)


def choose_resolution(resolution):
    if resolution in ["1", "low", "360", "360p"]:
        itag = 18
    elif resolution in ["2", "medium", "720", "720p", "hd"]:
        itag = 22
    elif resolution in ["3", "high", "1080", "1080p", "fullhd", "full_hd", "full hd"]:
        itag = 137
    elif resolution in ["4", "very high", "2160", "2160p", "4K", "4k"]:
        itag = 313
    else:
        itag = 18
    return itag


def input_links():
    print("Videolarning havolalarini kiriting (""STOP"" ni kiritish bilan yakunlang):")

    links = []
    link = ""

    while link != "STOP" and link != "stop":
        link = input()
        links.append(link)

    links.pop()

    return links