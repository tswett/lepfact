from django.contrib.auth.models import User
import django.contrib.auth.views
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import django.db
from django.http import HttpResponse, HttpResponseRedirect
import django.shortcuts

from playerinfo.models import (
    Account, UserProfile, Currency, MoneyCurrency, Plot, Bid,
    Factory, FactoryType, BuildCostData, StartupCostData,
    IdleUpkeepData, ActiveUpkeepData, YieldData,
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
    bids = Bid.objects.all()

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
        'user': request.user,
        'profiles': profiles,
        'accounts': accounts,
        'plots': plots,
        'bids': bids,
        'factory_types': factory_types,
    }

    return django.shortcuts.render(request, 'playerinfo/index.html', context)

def login(request):
    return django.contrib.auth.views.login(request, template_name='playerinfo/login.html')

def dashboard(request):
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None

    context = {
        'accounts': Account.objects.filter(user=user),
        'bids': Bid.objects.filter(bidder=user),
        'currencies': Currency.objects.all(),
        'factory_types': FactoryType.objects.all(),
        'money': MoneyCurrency.objects.get().currency.name,
        'plots': Plot.objects.filter(lessee=user),
        'users': User.objects.all(),
    }
    return django.shortcuts.render(request, 'playerinfo/dashboard.html', context)

def transfer(request):
    """Transfer some currency to another player."""
    amount = int(request.POST['amount'])
    currency = Currency.objects.get(id=int(request.POST['currency']))
    recipient = User.objects.get(id=int(request.POST['player']))

    from_account, created = Account.objects.get_or_create(user=request.user, currency=currency)
    to_account, created = Account.objects.get_or_create(user=recipient, currency=currency)

    if amount < 0:
        raise ValidationError('Attempted to transfer a negative amount of currency')
    else:
        with django.db.transaction.atomic():
            from_account.credit_or_debit(-amount)
            to_account.credit_or_debit(amount)

    return HttpResponseRedirect('/playerinfo/dashboard/')

def cancelbid(request):
    bid = Bid.objects.get(id=int(request.POST['bid']))
    if bid.bidder != request.user:
        raise PermissionDenied("Tried to cancel someone else's bid")

    bid.delete()

    return HttpResponseRedirect('/playerinfo/dashboard/')

def bid(request):
    """Submit a bid for a plot of land."""
    rate = int(request.POST['rate'])
    days = int(request.POST['days'])

    if rate <= 0 or days <= 0:
        raise ValidationError('Daily rate and length of term for a bid must be positive')

    the_bid = Bid()

    the_bid.bidder = request.user
    the_bid.daily_rate = rate
    the_bid.currency = MoneyCurrency.objects.get().currency
    the_bid.days = days

    the_bid.save()

    return HttpResponseRedirect('/playerinfo/dashboard/')

def startup(request):
    """Try to start up a factory."""
    plot = Plot.objects.get(id=int(request.POST['plot']))
    if plot.lessee != request.user:
        raise PermissionDenied("Tried to start up someone else's factory")

    factory = plot.factory

    with django.db.transaction.atomic():
        startup_costs = StartupCostData.objects.filter(factory_type=factory.factory_type)
        for cost in startup_costs:
            account, created = Account.objects.get_or_create(user=request.user, currency=cost.currency)
            account.credit_or_debit(-cost.amount)

    factory.active = True
    factory.save()

    return HttpResponseRedirect('/playerinfo/dashboard/')

def shutdown(request):
    """Shut down a factory."""
    plot = Plot.objects.get(id=int(request.POST['plot']))
    if plot.lessee != request.user:
        raise PermissionDenied("Tried to shut down someone else's factory")

    factory = plot.factory

    factory.active = False
    factory.save()

    return HttpResponseRedirect('/playerinfo/dashboard/')

def demolish(request):
    """Demolish a factory."""
    plot = Plot.objects.get(id=int(request.POST['plot']))
    if plot.lessee != request.user:
        raise PermissionDenied("Tried to demolish someone else's factory")

    factory = plot.factory

    factory.delete()

    return HttpResponseRedirect('/playerinfo/dashboard/')

def build(request):
    """Try to build a factory on a plot."""
    plot = Plot.objects.get(id=int(request.POST['plot']))
    if plot.lessee != request.user:
        raise PermissionDenied("Tried to build on someone else's property")

    factory_type = FactoryType.objects.get(id=int(request.POST['type']))

    with django.db.transaction.atomic():
        build_costs = BuildCostData.objects.filter(factory_type=factory_type)
        for cost in build_costs:
            account, created = Account.objects.get_or_create(user=request.user, currency=cost.currency)
            account.credit_or_debit(-cost.amount)

        try:
            plot.factory.delete()
        except ObjectDoesNotExist:
            pass

        factory = Factory()
        factory.plot = plot
        factory.factory_type = factory_type
        factory.save()

    return HttpResponseRedirect('/playerinfo/dashboard/')
