from django.core.exceptions import ValidationError
from django.db.models import (
    CharField, ForeignKey, OneToOneField,
    TextChoices,
    CASCADE, PROTECT, SET_NULL,
    Manager,
    Sum,
)

from django_base.models.models import BaseAuditable
from django_base.utils import default_related_names, pascal_case_to_snake_case

from . import managers
from . import _querysets


class Account(BaseAuditable):
    """Double-entry style account.

    If money goes into it or comes out of it, literally or figuratively, it may
    be tracked as an account.
    Assets, Expenses, Dividends, Losses:
        increased by debit; decreased by credit
    Liabilities, Income, Capital, Revenue, Gains, Equity:
        decreased by debit; increased by credit
    """

    txn_line_item_set: Manager

    class Subtype(TextChoices):
        ASSET = 'ASSET'  # Checking, Savings, Real, Discrete, Inventory
        LIABILITY = 'LIABILITY'  # Loan, Mortgage, Credit Card
        EQUITY = 'EQUITY'  # Not sure yet
        INCOME = 'INCOME'  # Salary
        EXPENSE = 'EXPENSE'  # Rent, Utilities, Internet, Fees
        OTHER = 'OTHER'  # Not likely to use

    name = CharField(max_length=255, unique=True)
    parent_account = ForeignKey(
        'self',
        on_delete=SET_NULL,
        related_name='child_accounts',
        null=True,
        blank=True
    )
    subtype = CharField(
        max_length=9, choices=Subtype.choices, default=Subtype.OTHER
    )

    objects = managers.account.AccountManager.from_queryset(
        _querysets.AccountQuerySet)()
    assets = managers.account.AccountManagerAsset()
    liabilities = managers.account.AccountManagerLiability()
    equities = managers.account.AccountManagerEquity()
    incomes = managers.account.AccountManagerIncome()
    expenses = managers.account.AccountManagerExpense()

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return f'{self.name}'

    def clean(self) -> None:
        if self.parent_account == self:
            raise ValidationError("An account may not be its own parent.")

    def get_balance(self) -> int:
        agg = self.txn_line_item_set.aggregate(
            total=Sum('amount')
        )
        return agg['total']

    def debit_polarity(self, debit: bool) -> int:
        if self.debit_increases is debit:
            return 1
        else:
            return -1

    @property
    def debit_increases(self) -> bool:
        if self.subtype in (self.Subtype.ASSET, self.Subtype.EXPENSE):
            return True
        elif self.subtype in (
            self.Subtype.EQUITY,
            self.Subtype.INCOME,
            self.Subtype.LIABILITY
        ):
            return False


class AccountAsset(BaseAuditable):
    """An asset account.

    Examples: a bank checking account, or a physical item with value.
    """

    class Subtype(TextChoices):
        FINANCIAL = 'FINANCIAL', 'FINANCIAL'
        REAL = 'REAL', 'REAL'
        OTHER = 'OTHER', 'OTHER'

    account_id: int

    account = OneToOneField(
        Account, on_delete=CASCADE, primary_key=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )
    subtype = CharField(
        max_length=31, choices=Subtype.choices, default=Subtype.OTHER
    )

    objects = Manager()
    financials = managers.account_asset.AccountAssetManagerFinancial()
    real = managers.account_asset.AccountAssetManagerReal()

    class Meta:
        verbose_name = 'Account::Asset'
        verbose_name_plural = verbose_name


class AccountAssetFinancial(BaseAuditable):
    """An asset which is monetary.

    Examples: a cash or checking account.
    """

    account_asset_id: int

    account_asset = OneToOneField(
        AccountAsset, on_delete=CASCADE, primary_key=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )
    account_number = CharField(max_length=63, null=True, blank=True)
    institution = None  # TODO 2023-12-12

    class Meta:
        verbose_name = 'Account::Asset::Financial'
        verbose_name_plural = verbose_name


class AccountAssetReal(BaseAuditable):
    """A real asset.

    Examples: a vehicle, or real estate.
    Implies inherent value, and may be subject to depreciation.
    """

    account_asset_id: int

    account_asset = OneToOneField(
        AccountAsset, on_delete=CASCADE, primary_key=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )

    class Meta:
        verbose_name = 'Account::Asset::Real'
        verbose_name_plural = verbose_name


class AccountAssetRealXAssetDiscrete(BaseAuditable):
    """Relationship between discrete possessions and their financial 'bucket'.

    This works around generalized accounts like 'Tools' or 'Furniture'. For the
    sake of accounting, they are still 'Real Assets', but a discrete asset may
    not be duplicated in multiple accounts.
    """

    account_asset_real = ForeignKey(
        AccountAssetReal, on_delete=CASCADE,
        **default_related_names(__qualname__)
    )
    asset_discrete = OneToOneField(
        'AssetDiscrete', on_delete=PROTECT, primary_key=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )

    class Meta:
        verbose_name = 'Account::Asset::Real <-> Asset::Discrete'
        verbose_name_plural = verbose_name


class AccountEquity(BaseAuditable):
    """A business model included for completeness

    Examples: Common Stock, Paid-In Capital.
    """

    account_id: int

    account = OneToOneField(
        Account, on_delete=CASCADE, primary_key=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )

    class Meta:
        verbose_name = 'Account::Equity'
        verbose_name_plural = verbose_name


class AccountExpense(BaseAuditable):
    """An expense account.

    Examples: Utilities, Rent, or Fuel.
    """

    account_id: int

    account = OneToOneField(
        Account, on_delete=CASCADE, primary_key=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )

    class Meta:
        verbose_name = 'Account::Expense'
        verbose_name_plural = verbose_name


class AccountIncome(BaseAuditable):
    """An income account.

    Examples: Salary, dividends
    """

    account_id: int

    account = OneToOneField(
        Account, on_delete=CASCADE, primary_key=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )

    class Meta:
        verbose_name = 'Account::Income'
        verbose_name_plural = verbose_name


class AccountLiability(BaseAuditable):
    """A liability account.

    Examples: a loan, mortgage, or credit card
    Notes:
        Secured vs Unsecured
        Revolving vs Non-Revolving
        - Credit card is Unsecured, Revolving
        - Mortgage is Secured, Non-Revolving
        - Car Loan is Secured, Non-Revolving
        - HELOC is Secured (by equity)
            - somewhat revolving? Open term with a limit?
    """

    class Subtype(TextChoices):
        SECURED = 'SECURED', 'SECURED'
        OTHER = 'OTHER', 'OTHER'

    account_id: int

    account = OneToOneField(
        Account, on_delete=CASCADE, primary_key=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )
    account_number = CharField(max_length=63, null=True, blank=True)
    lender = None  # TODO 2023-12-12
    subtype = CharField(
        max_length=15, choices=Subtype.choices, default=Subtype.OTHER
    )

    class Meta:
        verbose_name = 'Account::Liability'
        verbose_name_plural = verbose_name


class AccountLiabilitySecured(BaseAuditable):
    """A liability account that is held against an asset."""

    account_liability_id: int
    asset_id: int

    account_liability = OneToOneField(
        AccountLiability, on_delete=CASCADE, primary_key=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )
    asset = ForeignKey(
        'Asset', on_delete=PROTECT,
        **default_related_names(__qualname__)
    )

    class Meta:
        verbose_name = 'Account::Liability::Secured'
        verbose_name_plural = verbose_name
