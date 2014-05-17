from django.http import HttpResponse
import django.shortcuts

from playerinfo.models import (
    Account, UserProfile, Plot, FactoryType, BuildCostData, StartupCostData,
    IdleUpkeepData, ActiveUpkeepData, YieldData
)

COST_CLASS = {
    'Build cost': BuildCostData,
    'Startup cost': StartupCostData,
    'Idle upkeep': IdleUpkeepData,
    'Active upkeep': ActiveUpkeepData,
    'Yield': YieldData,
}

def list_profiles(request):
    profiles = UserProfile.objects.all()

    accounts = Account.objects.all()

    plots = Plot.objects.all()

    factory_types = []

    for factory_type in FactoryType.objects.all():
        costtypes = []

        for costtype_name in COST_CLASS:
            cost_class = COST_CLASS[costtype_name]

            costs = cost_class.objects.filter(factory_type=factory_type)

            if not costs:
                continue

            costtype_info = {'name': costtype_name, 'costs': []}

            for cost in costs:
                cost_info = {'name': cost.currency.name, 'amount': cost.amount}
                costtype_info['costs'].append(cost_info)

            costtypes.append(costtype_info)

        factory_types.append({
            'name': factory_type.name,
            'costtypes': costtypes,
        })

    context = {
        'profiles': profiles,
        'accounts': accounts,
        'plots': plots,
        'factory_types': factory_types,
    }

    return django.shortcuts.render(request, 'playerinfo/index.html', context)
