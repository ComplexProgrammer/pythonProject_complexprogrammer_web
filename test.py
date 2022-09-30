import os
import instaloader

from instaloader import Instaloader, Profile
print("start...")
L = Instaloader()
PROFILE = "benbucihanatv"
profile = Profile.from_username(L.context, PROFILE)

posts_sorted_by_likes = sorted(profile.get_posts(), key=lambda post: post.likes,reverse=True)

try:
    for post in posts_sorted_by_likes:
        print(post)
        print(post.url)
        L.download_post(post, PROFILE)
except IndexError:
    print("You have no saved posts yet.")
print("end...")


def save_insta_collection():
    username = "complexprogrammer"
    loader = instaloader.Instaloader()
    # loader.load_session_from_file(username)
    profile = instaloader.Profile.from_username(loader.context, username)

    post_list = []
    try:
        for saved_posts in profile.get_saved_posts():
            post_list.append(saved_posts)
        loader.download_post(post_list[0], 'mysavedcollection')

    except IndexError:
        print("You have no saved posts yet.")

    save_insta_collection()  # recursion


