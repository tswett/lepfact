from django.db import models

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    unix_uid = models.BigIntegerField(null=True, blank=True, unique=True)
    unix_username = models.CharField(max_length=32, null=True, blank=True, unique=False)
    sql_username = models.CharField(max_length=32, null=True, blank=True, unique=False)

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

class FactoryType(models.Model):
    name = models.CharField(max_length=32, unique=True)
    build_cost = models.ManyToManyField(Currency, through='BuildCostData', related_name='buildcost_factorytype_set')
    startup_cost = models.ManyToManyField(Currency, through='StartupCostData', related_name='startupcost_factorytype_set')
    idle_upkeep = models.ManyToManyField(Currency, through='IdleUpkeepData', related_name='idleupkeep_factorytype_set')
    active_upkeep = models.ManyToManyField(Currency, through='ActiveUpkeepData', related_name='activeupkeep_factorytype_set')
    yield_ = models.ManyToManyField(Currency, through='YieldData', related_name='yield_factorytype_set')

    def __unicode__(self):
        return "Factory type '" + self.name + "'"

class Factory(models.Model):
    plot = models.OneToOneField(Plot)
    factory_type = models.ForeignKey(FactoryType)

class FactoryCostData(models.Model):
    amount = models.PositiveIntegerField()
    factory_type = models.ForeignKey(FactoryType)
    currency = models.ForeignKey(Currency)

    class Meta:
        abstract = True

class BuildCostData(FactoryCostData):
    pass

class StartupCostData(FactoryCostData):
    pass

class IdleUpkeepData(FactoryCostData):
    pass

class ActiveUpkeepData(FactoryCostData):
    pass

class YieldData(FactoryCostData):
    pass

class WorkDoneDay(models.Model):
    # If a WorkDoneDay exists for a particular day, that means that the daily
    # script has run for that day.

    day = models.DateField()
