from django.http import HttpResponse
import django.shortcuts

from playerinfo.models import Account, UserProfile

def list_profiles(request):
    profiles = UserProfile.objects.all()
    accounts = Account.objects.all()

    context = {'profiles': profiles, 'accounts': accounts}
    return django.shortcuts.render(request, 'playerinfo/index.html', context)
