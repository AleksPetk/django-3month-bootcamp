


def user_access(request):
    if not request.user.is_authenticated:
        return {
            "can_access_anime": False,
            "can_access_movie": False
        }
    return {
        "can_access_anime": request.user.groups.filter(name="Anime").exists(),
        "can_access_movie": request.user.groups.filter(name="Movie").exists()
    }