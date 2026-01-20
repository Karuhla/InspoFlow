from .models import Profile

def user_profile_context(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            return {'navbar_profile': profile}
        except Profile.DoesNotExist:
            return {'navbar_profile': None}
    return {}
