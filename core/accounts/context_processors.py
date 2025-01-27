from accounts.models import Profile

def user_profile_context_processor(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            return {'profile': profile}
        except Profile.DoesNotExist:
            return {}
    return {}
