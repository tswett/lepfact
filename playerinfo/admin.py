from django.contrib import admin
from playerinfo.models import UserProfile, Currency, Account, Transaction

admin.site.register(UserProfile)
admin.site.register(Currency)
admin.site.register(Account)
admin.site.register(Transaction)
