from instaloader import Instaloader, Profile


def save_insta_collection(user_name):
    print("start...")
    L = Instaloader()
    PROFILE = user_name
    profile = Profile.from_username(L.context, PROFILE)
    posts_sorted_by_likes = sorted(profile.get_posts(), key=lambda post: post.likes, reverse=True)

    try:
        for post in posts_sorted_by_likes:
            print(post)
            print(post.profile)
            print(post.url)
            L.download_post(post, PROFILE)
    except IndexError:
        print("You have no saved posts yet.")
        return 'IndexError'
    print("end...")
    return PROFILE

    # save_insta_collection()  # recursion


