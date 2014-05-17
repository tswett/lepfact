from django.contrib import admin
from playerinfo.models import *

admin.site.register(UserProfile)
admin.site.register(Currency)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Plot)
admin.site.register(Factory)
admin.site.register(FactoryType)
admin.site.register(BuildCostData)
admin.site.register(StartupCostData)
admin.site.register(IdleUpkeepData)
admin.site.register(ActiveUpkeepData)
admin.site.register(YieldData)
