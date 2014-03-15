from django.db import models

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    unix_uid = models.BigIntegerField(null=True, blank=True, unique=True)
    unix_username = models.CharField(max_length=32, null=True, blank=True, unique=True)
    sql_username = models.CharField(max_length=32, null=True, blank=True, unique=True)

    def __unicode__(self):
        return "UserProfile for user '" + self.user.username + "'"

class Currency(models.Model):
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        verbose_name_plural = 'currencies'

    def __unicode__(self):
        return "Currency '" + self.name + "'"

class Account(models.Model):
    user = models.ForeignKey(User)
    currency = models.ForeignKey(Currency)
    balance = models.BigIntegerField()

    class Meta:
        unique_together = ('user', 'currency')

    def __unicode__(self):
        return 'Account of user "' + self.user.username + '" in currency "' + str(self.currency) + '"'

class Transaction(models.Model):
    account = models.ForeignKey(Account)
    amount = models.BigIntegerField() # positive for a credit, negative for a debit
    date = models.DateTimeField(auto_now = True)
    description = models.CharField(max_length=128)

    def __unicode__(self):
        return 'Transaction to credit ' + self.amount + ' units of currency "' + str(self.account.currency) + '" to user "' + self.account.user.username + '" at ' + self.date + ' with description: ' + self.description

class Plot(models.Model):
    owner = models.ForeignKey(User)

class Factory(models.Model):
    plot = models.OneToOneField(Plot)

# build_cost is the price required to turn an empty plot of land into this
# factory, in an idle state.  startup_cost is the price required make an idle
# factory active.  idle_upkeep is the daily cost to maintain an idle factory; if
# this cost is not paid, the factory will be destroyed.  active_upkeep is the
# daily cost to maintain an active factory; if this cost is not paid, the
# factory will become idle.  Finally, yield_ is what an active factory produces
# each day.

class BasicWheatFarm(Factory):
    build_cost = {}
    startup_cost = {}
    idle_upkeep = {}
    active_upkeep = {}
    yield_ = {'bushel of wheat': 30}

class WheatFarm(Factory):
    build_cost = {}
    startup_cost = {}
    idle_upkeep = {}
    active_upkeep = {'barrel of oil': 15}
    yield_ = {'bushel of wheat': 300}

class BasicCornFarm(Factory):
    build_cost = {}
    startup_cost = {}
    idle_upkeep = {}
    active_upkeep = {}
    yield_ = {'bushel of corn': 50}

class CornFarm(Factory):
    build_cost = {'mcf of natural gas': 300}
    startup_cost = {'mcf of natural gas': 1000}
    idle_upkeep = {'mcf of natural gas': 30}
    active_upkeep = {'mcf of natural gas': 300}
    yield_ = {'bushel of corn': 500}

class BasicCattleFarm(Factory):
    build_cost = {'bushel of corn': 100}
    startup_cost = {'bushel of wheat': 50, 'bushel of corn': 100}
    idle_upkeep = {'bushel of corn': 10}
    active_upkeep = {'bushel of wheat': 20, 'bushel of corn': 30}
    yield_ = {'head of cattle': 5}

class CattleFarm(Factory):
    build_cost = {'barrel of oil': 30}
    startup_cost = {'bushel of wheat': 200, 'bushel of corn': 500, 'barrel of oil': 10}
    idle_upkeep = {'barrel of oil': 3}
    active_upkeep = {'bushel of wheat': 50, 'bushel of corn': 100, 'barrel of oil': 4}
    yield_ = {'head of cattle': 15}

class BasicGasWell(Factory):
    build_cost = {'bushel of corn': 20}
    startup_cost = {'bushel of corn': 100}
    idle_upkeep = {'bushel of corn': 2}
    active_upkeep = {'bushel of corn': 20}
    yield_ = {'mcf of natural gas': 100}

class GasWell(Factory):
    build_cost = {'bushel of corn': 500}
    startup_cost = {'bushel of corn': 400, 'tonne of steel': 2, 'kilogram of copper': 180}
    idle_upkeep = {'bushel of corn': 50}
    active_upkeep = {'bushel of corn': 120, 'tonne of steel': 1, 'kilogram of copper': 50}
    yield_ = {'mcf of natural gas': 600}

class BasicOilWell(Factory):
    build_cost = {'mcf of natural gas': 100}
    startup_cost = {'head of cattle': 4, 'mcf of natural gas': 50}
    idle_upkeep = {'mcf of natural gas': 10}
    active_upkeep = {'head of cattle': 1, 'mcf of natural gas': 20}
    yield_ = {'barrel of oil': 10}

class OilWell(Factory):
    build_cost = {'head of cattle': 10}
    startup_cost = {'head of cattle': 5, 'mcg of natural gas': 250, 'tonne of steel': 3}
    idle_upkeep = {'head of cattle': 1}
    active_upkeep = {'head of cattle': 2, 'mcf of natural gas': 100, 'tonne of steel': 1}
    yield_ = {'barrel of oil': 30}

class BasicIronOreMine(Factory):
    build_cost = {'bushel of wheat': 300}
    startup_cost = {'bushel of wheat': 400, 'barrel of oil': 20}
    idle_upkeep = {'bushel of wheat': 40}
    active_upkeep = {'bushel of wheat': 60, 'barrel of oil': 5}
    yield_ = {'tonne of iron ore': 6}

class IronOreMine(Factory):
    build_cost = {'barrel of oil': 18}
    startup_cost = {'bushel of wheat': 500, 'barrel of oil': 30, 'tonne of steel': 2}
    idle_upkeep = {'barrel of oil': 2}
    active_upkeep = {'bushel of wheat': 60, 'barrel of oil': 5, 'tonne of steel': 1}
    yield_ = {'tonne of iron ore': 14}

class SteelMill(Factory):
    build_cost = {'mcf of natural gas': 500}
    startup_cost = {'head of cattle': 10, 'barrel of oil': 15, 'mcf of natural gas': 500, 'tonne of iron ore': 8}
    idle_upkeep = {'mcf of natural gas': 70}
    active_upkeep = {'head of cattle': 3, 'barrel of oil': 4, 'mcf of natural gas': 110, 'tonne of iron ore': 3}
    yield_ = {'tonne of steel': 6}

class CopperMine(Factory):
    build_cost = {'mcf of natural gas': 1000}
    startup_cost = {'bushel of corn': 500, 'mcg of natural gas': 800}
    idle_upkeep = {'mcf of natural gas': 120}
    active_upkeep = {'bushel of corn': 140, 'mcf of natural gas': 170}
    yield_ = {'kilogram of copper': 50}

class SilverMine(Factory):
    build_cost = {'bushel of wheat': 400}
    startup_cost = {'bushel of wheat': 200, 'barrel of oil': 20, 'tonne of steel': 4}
    idle_upkeep = {'bushel of wheat': 40}
    active_upkeep = {'bushel of wheat': 70, 'barrel of oil': 5, 'tonne of steel': 1}
    yield_ = {'gram of silver': 750}

class GoldMine(Factory):
    build_cost = {'barrel of oil': 30}
    startup_cost = {'head of cattle': 20, 'barrel of oil': 30, 'tonne of steel': 3}
    idle_upkeep = {'barrel of oil': 4}
    active_upkeep = {'head of cattle': 4, 'barrel of oil': 6, 'tonne of steel': 1}
    yield_ = {'milligram of gold': 10000}
