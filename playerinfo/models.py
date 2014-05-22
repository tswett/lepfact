from django.db import models

from django.contrib.auth.models import User

class UserProfile(models.Model):
    """This is some game-specific data about users or players."""
    user = models.OneToOneField(User)
    unix_uid = models.BigIntegerField(null=True, blank=True, unique=True)
    unix_username = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        unique=False,
    )
    sql_username = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        unique=False
    )

    def __unicode__(self):
        return "UserProfile for user '" + self.user.username + "'"

class Currency(models.Model):
    """This is a currency in the game."""
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        verbose_name_plural = 'currencies'

    def __unicode__(self):
        return "Currency '" + self.name + "'"

class InsufficientFundsError(Exception):
    """This is an exception thrown to indicate that an operation has
    failed due to an insufficient account balance.
    """

    def __init__(self, account, balance, amount):
        self.account = account
        self.balance = balance
        self.amount = amount

class Account(models.Model):
    """This is an account of some user in some currency."""
    user = models.ForeignKey(User)
    currency = models.ForeignKey(Currency)
    # positive balance is an asset of user, negative is a liability.
    balance = models.BigIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'currency')

    def __unicode__(self):
        return ('Account of user "%s" in currency "%s"' %
            self.user.username, str(self.currency))

    def credit_debit(self, amount, allow_negative=False, description=''):
        # amount is positive for a credit, negative for a debit.

        # If allow_negative is false, we don't want to allow debits resulting
        # in a negative balance.  However, we do want to allow all credits.
        if (not allow_negative) and amount < 0 and self.balance + amount < 0:
            raise InsufficientFundsError(self, self.balance, amount)
        else:
            self.balance += amount
            self.save()
            
            Transaction(self, amount, description).save()

class Transaction(models.Model):
    """This is a record of a credit or debit to an account."""
    account = models.ForeignKey(Account)
    # 'amount' is positive for a credit, negative for a debit
    amount = models.BigIntegerField()
    date = models.DateTimeField(auto_now = True)
    description = models.CharField(max_length=128)

    def __init__(self, account, amount, description):
        self.account = account
        self.amount = amount
        self.description = description

    def __unicode__(self):
        return (
            'Transaction to credit %s units of currency "%s" to user "%s" at '
            '%s with description: %s' %
            self.amount, str(self.account.currency),
            self.account.user.username, self.date, self.description
        )

class Plot(models.Model):
    """This is an in-game plot of land on which something can be built."""
    lessee = models.ForeignKey(User, null=True)
    days_left = models.PositiveIntegerField(default=0)

class FactoryType(models.Model):
    name = models.CharField(max_length=32, unique=True)

    build_cost = models.ManyToManyField(
        Currency,
        through='BuildCostData',
        related_name='buildcost_factorytype_set',
    )
    startup_cost = models.ManyToManyField(
        Currency,
        through='StartupCostData',
        related_name='startupcost_factorytype_set',
    )
    idle_upkeep = models.ManyToManyField(
        Currency,
        through='IdleUpkeepData',
        related_name='idleupkeep_factorytype_set',
    )
    active_upkeep = models.ManyToManyField(
        Currency,
        through='ActiveUpkeepData',
        related_name='activeupkeep_factorytype_set',
    )
    yield_ = models.ManyToManyField(
        Currency,
        through='YieldData',
        related_name='yield_factorytype_set',
    )

    def __unicode__(self):
        return "Factory type '" + self.name + "'"

class Factory(models.Model):
    plot = models.OneToOneField(Plot)
    factory_type = models.ForeignKey(FactoryType)
    active = models.BooleanField(default=False)

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
    """This object represents the fact that the daily script has been
    run for a particular day.

    If a WorkDoneDay exists for a particular day, the script has already
    been run; otherwise, it hasn't.  When the script is run, it checks
    to make sure that a WorkDoneDay does not already exist for the
    relevant day.  If it runs successfully, it creates a WorkDoneDay
    for the relevant day.
    """

    day = models.DateField()
