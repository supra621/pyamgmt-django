__all__ = [
    'Account', 'AccountAsset', 'AccountAssetFinancial', 'AccountAssetReal',
    'AccountEquity', 'AccountExpense', 'AccountIncome', 'AccountLiability',
    'Asset', 'AssetDiscrete', 'AssetDiscreteCatalogItem',
    'AssetDiscreteVehicle', 'AssetInventory', 'AssetType',
    'CatalogItem', 'CatalogItemDigitalSong',
    'CatalogItemToInvoiceLineItem', 'CatalogItemToOrderLineItem',
    'CatalogItemToPointOfSaleLineItem',
    'Invoice', 'InvoiceLineItem', 'InvoiceLineItemToNonCatalogItem',
    'MediaFormat',
    'MotionPicture',
    'MusicAlbum',
    'MusicAlbumArtwork',
    'MusicAlbumToMusicArtist',
    'MusicAlbumToSongRecording',
    'MusicArtist', 'MusicArtistToPerson', 'MusicArtistToSong',
    'MusicArtistToSongRecording',
    'NonCatalogItem',
    'Order', 'OrderLineItem',
    'Party', 'PartyBusiness', 'PartyPerson', 'PartyType', 'Payee', 'Person',
    'PointOfSale', 'PointOfSaleDocument', 'PointOfSaleLineItem',
    'Seller',
    'Song', 'SongRecording',  # 'SongToSong',
    'Txn', 'TxnLineItem',
    'Unit',
    'Vehicle', 'VehicleMake', 'VehicleMileage', 'VehicleModel', 'VehicleTrim',
    'VehicleYear',
]

import datetime
from typing import Optional

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db.models import (
    # Fields
    BooleanField, CharField, DateField, DecimalField, DurationField, FileField,
    ForeignKey,
    ImageField, IntegerField, JSONField,
    ManyToManyField,
    OneToOneField,
    PositiveIntegerField, PositiveSmallIntegerField, TextField,
    TimeField, URLField,
    # Indexes
    UniqueConstraint,
    # Model Managers
    Manager,
    # Enum
    TextChoices,
    # on_delete callbacks
    CASCADE, PROTECT, SET_DEFAULT, SET_NULL,
    # SQL
    F, Sum,
)
from django.utils import timezone
from django.utils.functional import cached_property

# from base.db.models.fields.related import (
#     ForeignKey,
#     OneToOneField,
#     ManyToManyField,
# )
from base.models import BaseAuditable
from base.models.fields import UpperCharField
from base.validators import (
    validate_alphanumeric,
    validate_date_not_future,
    validate_digit,
    validate_positive_timedelta,
    validate_year_not_future,
)

from core.models import managers, querysets
from core.models.fields import CurrencyField
from core.validators import (
    validate_isbn,
    validate_isbn_13_check_digit,
)


def get_default_mediaformat_audio():
    return MediaFormat.get_default_audio()


##########
# MODELS #
##########

class Account(BaseAuditable):
    """Double-entry style account.

    If money goes into it or comes out of it, literally or figuratively, it may
    be tracked as an account.
    Assets, Expenses, Dividends, Losses:
        increased by debit; decreased by credit
    Liabilities, Income, Capital, Revenue, Gains, Equity:
        decreased by debit; increased by credit
    """

    class Subtype(TextChoices):
        ASSET = 'ASSET'  # Checking, Savings, Real, Discrete, Inventory
        LIABILITY = 'LIABILITY'  # Loan, Mortgage, Credit Card
        EQUITY = 'EQUITY'  # Not sure yet
        INCOME = 'INCOME'  # Salary
        EXPENSE = 'EXPENSE'  # Rent, Utilities, Internet, Fees
        OTHER = 'OTHER'  # Not likely to use
    name = CharField(max_length=255, unique=True)
    parent_account = ForeignKey(
        'self', on_delete=SET_NULL, related_name='child_accounts', null=True,
        blank=True)
    subtype = CharField(
        max_length=9, choices=Subtype.choices, default=Subtype.OTHER)

    objects = managers.AccountManager()
    assets = managers.AccountManagerAsset()
    liabilities = managers.AccountManagerLiability()
    equities = managers.AccountManagerEquity()
    incomes = managers.AccountManagerIncome()
    expenses = managers.AccountManagerExpense()

    def __str__(self) -> str:
        return f'{self.name}'

    def clean(self) -> None:
        if self.parent_account == self:
            raise ValidationError("An account may not be its own parent.")

    @property
    def balance(self) -> int:
        return 0

    def debit_coef(self, debit: bool) -> int:
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

    account = OneToOneField(Account, on_delete=CASCADE, primary_key=True)
    account_id: int
    subtype = CharField(max_length=31, choices=Subtype.choices, default=Subtype.OTHER)

    objects = Manager()
    financials = managers.AccountAssetManagerFinancial()
    real = managers.AccountAssetManagerReal()


class AccountAssetFinancial(BaseAuditable):
    """An asset which is monetary.

    Examples: a cash or checking account.
    """
    account_asset = OneToOneField(AccountAsset, on_delete=CASCADE, primary_key=True)
    account_asset_id: int
    account_number = CharField(max_length=63, null=True, blank=True)
    institution = None  # TODO


class AccountAssetReal(BaseAuditable):
    """A real asset.

    Examples: a vehicle, or real estate.
    Implies inherent value, and may be subject to depreciation.
    """
    accountasset = OneToOneField(AccountAsset, on_delete=CASCADE, primary_key=True)
    accountasset_id: int
    # TODO: Decide if I want `limit_choices_to=` here. If so, needs a callback.
    asset = ForeignKey('Asset', on_delete=SET_NULL, null=True, blank=True)
    asset_id: int


class AccountEquity(BaseAuditable):
    """A business model included for completeness

    Examples: Common Stock, Paid-In Capital.
    """
    account = OneToOneField(Account, on_delete=CASCADE, primary_key=True)
    account_id: int


class AccountExpense(BaseAuditable):
    """An expense account.

    Examples: Utilities, Rent, or Fuel.
    """
    account = OneToOneField(Account, on_delete=CASCADE, primary_key=True)
    account_id: int


class AccountIncome(BaseAuditable):
    """An income account.

    Examples: Salary, dividends
    """
    account = OneToOneField(Account, on_delete=CASCADE, primary_key=True)
    account_id: int


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
    account = OneToOneField(Account, on_delete=CASCADE, primary_key=True)
    account_id: int
    account_number = CharField(max_length=63, null=True, blank=True)
    lender = None  # TODO
    subtype = CharField(max_length=15, choices=Subtype.choices, default=Subtype.OTHER)


class AccountLiabilitySecured(BaseAuditable):
    """A liability account that is held against an asset."""
    accountliability = OneToOneField(AccountLiability, on_delete=CASCADE, primary_key=True)
    accountliability_id: int
    asset = ForeignKey('Asset', on_delete=PROTECT)
    asset_id: int


class Asset(BaseAuditable):
    """Any item which implies ownership."""
    class Subtype(TextChoices):
        DISCRETE = 'DISCRETE', 'DISCRETE'
        INVENTORY = 'INVENTORY', 'INVENTORY'
    description = TextField(null=True, blank=True)
    subtype = CharField(max_length=31, choices=Subtype.choices)

    def __str__(self):
        return f'Asset {self.pk}'


class AssetDiscrete(BaseAuditable):
    """An item that is uniquely identifiable.

    Examples: A vehicle, serialized equipment, or property
    """
    class Subtype(TextChoices):
        CATALOG_ITEM = 'CATALOG_ITEM', 'CATALOG_ITEM'
        VEHICLE = 'VEHICLE', 'VEHICLE'
    asset = OneToOneField(Asset, on_delete=CASCADE, primary_key=True)
    asset_id: int
    date_acquired = DateField(null=True, blank=True)
    date_withdrawn = DateField(null=True, blank=True)
    subtype = CharField(max_length=31, choices=Subtype.choices, default='NONE')


class AssetDiscreteCatalogItem(BaseAuditable):
    """A discrete asset that can relate to a CatalogItem."""
    assetdiscrete = OneToOneField(AssetDiscrete, on_delete=CASCADE, primary_key=True)
    assetdiscrete_id: int
    catalog_item = ForeignKey('CatalogItem', on_delete=PROTECT)
    catalog_item_id: int


class AssetDiscreteVehicle(BaseAuditable):
    """A discrete asset that can be associated with a unique vehicle."""
    assetdiscrete = OneToOneField(AssetDiscrete, on_delete=CASCADE, primary_key=True)
    assetdiscrete_id: int
    vehicle = OneToOneField('Vehicle', on_delete=PROTECT)
    vehicle_id: int

    def __str__(self):
        return f'AssetDiscreteVehicle {self.pk}: {self.vehicle_id}'


class AssetInventory(BaseAuditable):
    """An item that is not uniquely identifiable.

    Example: Copies of DVDs, un-serialized items.
    """
    asset = OneToOneField(Asset, on_delete=CASCADE, primary_key=True)
    asset_id: int
    # CatalogItem is OneToOne because inventory should accumulate
    catalogitem = OneToOneField('CatalogItem', on_delete=PROTECT)
    catalogitem_id: int
    quantity = IntegerField(default=1)


class AssetType(BaseAuditable):
    """Expandable type to support hierarchy

    Not to be confused with AssetSubtype.
    """
    # TODO: Do I care about this?
    name = CharField(max_length=255)
    parent_asset_type = ForeignKey(
        'self', on_delete=SET_NULL, related_name='child_asset_types',
        null=True, blank=True,
    )

    def __str__(self):
        return f'AssetType {self.pk}: {self.name}'


class Book(BaseAuditable):
    """Every CRUD app needs a book model."""
    title = CharField(max_length=255)
    # publisher
    # authors

    def __str__(self):
        return f'{self.title}'


class BookEdition(BaseAuditable):
    """Version/printing of a book.

    As books may have revisions or updates, this is how they are tracked in the
    database under the same body of work.
    """
    book = ForeignKey(Book, on_delete=PROTECT)
    edition = PositiveSmallIntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=('book', 'edition'), name='unique_bookedition')
        ]


class BookPublication(BaseAuditable):
    """Not sure about this one.

    - the distributed work, in print, ebook, audio
    - audiobooks present a complication. Similar to music, they are a recorded
    performance with one or more narrators
    - This is where hardcover / paperback would live, I think
        - The ISBN is usually different between the two
    """
    bookedition = ForeignKey(BookEdition, on_delete=PROTECT)
    format = None  # TODO
    publisher = None  # TODO


class BookToMotionPicture(BaseAuditable):
    """Loose relationship between a book and an adapted film.

    The edition of the book doesn't really matter.
    """
    book = ForeignKey(Book, on_delete=CASCADE)
    motionpicture = ForeignKey("MotionPicture", on_delete=CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=('book', 'motionpicture'), name='unique_booktomotionpicture')
        ]


class CatalogItem(BaseAuditable):
    """An item with unique registries in other global systems.

    Can generally be ordered, purchased, re-sold, and accumulated as a discrete
    asset or inventory.
    Does not include concepts like labor hours, services, or warranties.
    """
    class Subtype(TextChoices):
        DIGITAL_SONG = 'DIGITAL_SONG', 'DIGITAL_SONG'
        MUSIC_ALBUM = 'MUSIC_ALBUM', 'MUSIC_ALBUM'
    asin = UpperCharField(
        max_length=10, unique=True, null=True, blank=True,
        validators=[MinLengthValidator(10), validate_alphanumeric],
        verbose_name="ASIN",
        help_text="Amazon Standard Identification Number"
    )
    ean_13 = CharField(
        max_length=13, unique=True, null=True, blank=True,
        validators=[MinLengthValidator(13), validate_digit],
        verbose_name="EAN-13",
        help_text="European Article Number"
    )
    eav = JSONField(null=True, blank=True)
    # isbn is also part of gsin / gs1 spec now, apparently
    isbn = CharField(
        max_length=10, unique=True, null=True, blank=True,
        validators=[MinLengthValidator(10), validate_isbn],
        verbose_name="ISBN",
        help_text="International Standard Book Number"
    )
    isbn_13 = CharField(
        max_length=13, unique=True, null=True, blank=True,
        validators=[MinLengthValidator(13), validate_digit, validate_isbn_13_check_digit]
    )
    ismn = CharField(
        max_length=13, unique=True, null=True, blank=True,
        validators=[MinLengthValidator(13)],
        verbose_name="ISMN",
        help_text="International Standard Music Number"
    )
    name = CharField(max_length=255)
    subtype = CharField(max_length=31, choices=Subtype.choices, null=True, blank=True)
    upc_a = CharField(
        max_length=12, unique=True, null=True, blank=True,
        validators=[MinLengthValidator(12), validate_digit]
    )


class CatalogItemDigitalSong(BaseAuditable):
    """Digital songs.

    Unlike Music albums, can be distributed individually absent of other medium.
    - Even if a song is released as a "Single", that "Single" still requires a
      medium for physical distribution, which makes it a "Single Album"
    """
    catalogitem = OneToOneField(CatalogItem, on_delete=CASCADE, primary_key=True)
    catalogitem_id: int


class CatalogItemMusicAlbumProduction(BaseAuditable):
    """A produced Music Album distributed in a particular format."""
    catalogitem = OneToOneField(CatalogItem, on_delete=CASCADE, primary_key=True)
    catalogitem_id: int
    # Does
    mediaformat = ForeignKey('MediaFormat', on_delete=SET_DEFAULT, default=get_default_mediaformat_audio)
    mediaformat_id: int
    # musicalbumproduction = ForeignKey('MusicAlbumProduction')


class CatalogItemToCatalogItem(BaseAuditable):
    """Holds relationships between CatalogItems to account for bundles."""
    catalogitem_a = ForeignKey(CatalogItem, on_delete=CASCADE, related_name='+')
    catalogitem_b = ForeignKey(CatalogItem, on_delete=CASCADE, related_name='+')
    relationship = None


class CatalogItemToInvoiceLineItem(BaseAuditable):
    """Relates a CatalogItem record to an InvoiceLineItem record."""
    invoicelineitem = OneToOneField('InvoiceLineItem', on_delete=CASCADE, primary_key=True)
    invoicelineitem_id: int
    catalogitem = ForeignKey(CatalogItem, on_delete=PROTECT)
    catalogitem_id: int
    unit_price = CurrencyField()
    # seller?
    quantity = IntegerField()

    def __str__(self):
        return f'CatalogItemToInvoiceLineItem {self.pk}: {self.catalogitem_id}'


class CatalogItemToOrderLineItem(BaseAuditable):
    """Relates a CatalogItem record to an OrderLineItem record."""
    orderlineitem = OneToOneField('OrderLineItem', on_delete=CASCADE, primary_key=True)
    orderlineitem_id: int
    catalogitem = ForeignKey(CatalogItem, on_delete=PROTECT)
    catalogitem_id: int

    def __str__(self):
        return f'CatalogItemToOrderLineItem {self.pk}: {self.catalogitem_id}'


class CatalogItemToPointOfSaleLineItem(BaseAuditable):
    """Relates a CatalogItem record to a PointOfSaleLineItem record"""
    pointofsalelineitem = OneToOneField('PointOfSaleLineItem', on_delete=CASCADE, primary_key=True)
    pointofsalelineitem_id: int
    catalogitem = ForeignKey(CatalogItem, on_delete=PROTECT)
    catalogitem_id: int
    quantity = DecimalField(max_digits=19, decimal_places=5, default=1)
    unit_price = CurrencyField()
    unit = ForeignKey('Unit', on_delete=SET_NULL, null=True, blank=True)
    unit_id: int

    def __str__(self):
        return f'CatalogItemToPointOfSaleLineItem {self.pk}: {self.catalogitem_id}'

    @property
    def price(self):
        return self.quantity * self.unit_price


class Invoice(BaseAuditable):
    """Payment due to a party for a good or service."""
    # party_id = ForeignKey()
    invoice_date = DateField()
    invoice_number = CharField(max_length=255)


class InvoiceLineItem(BaseAuditable):
    """A line item related to an Invoice."""
    class Subtype(TextChoices):
        CATALOGUE_ITEM = 'CATALOGUE_ITEM', 'CATALOGUE_ITEM'
        NON_CATALOGUE_ITEM = 'NON_CATALOGUE_ITEM', 'NON_CATALOGUE_ITEM'
    invoice = ForeignKey(Invoice, on_delete=CASCADE)
    invoice_id: int
    subtype = CharField(max_length=31, choices=Subtype.choices)

    def __str__(self):
        return f'InvoiceLineItem {self.pk}: {self.invoice_id}'


class InvoiceLineItemToNonCatalogItem(BaseAuditable):
    """Relates a NonCatalogItem record to an InvoiceLineItem record."""
    invoicelineitem = OneToOneField(InvoiceLineItem, on_delete=CASCADE, primary_key=True)
    invoicelineitem_id: int
    noncatalogitem = ForeignKey('NonCatalogItem', on_delete=CASCADE)
    noncatalogitem_id: int

    def __str__(self):
        return f'InvoiceLineItemToNonCatalogItem {self.invoicelineitem_id}: {self.noncatalogitem_id}'


class MediaFormat(BaseAuditable):
    name = CharField(max_length=255, unique=True)

    @classmethod
    def get_default_audio(cls):
        obj, _ = cls.objects.get_or_create(name='Audio')
        return obj.pk


class MotionPicture(BaseAuditable):
    title = CharField(max_length=255)
    year_produced = PositiveSmallIntegerField(
        null=True, blank=True, validators=[validate_year_not_future])

    def __str__(self):
        return f'{self.title}'


class MotionPictureRecording(BaseAuditable):
    """Released edition of a motion picture.

    Takes into account media (digital, DVD, maybe even distributor)"""
    motionpicture = ForeignKey(MotionPicture, on_delete=PROTECT)


class MotionPictureToMusicAlbum(BaseAuditable):
    """Relates a motion picture to its soundtrack and/or score."""
    motionpicture = ForeignKey(MotionPicture, on_delete=CASCADE)
    motionpicture_id: int
    musicalbum = ForeignKey('MusicAlbum', on_delete=CASCADE)
    musicalbum_id: int


class MotionPictureToSong(BaseAuditable):
    """Not sure if needed, but would account for one-off non-score non-soundtrack songs.
    There are some conventions here. "Original Soundtrack" and "Music from the Motion Picture" sometimes imply
     different meanings. I don't know if soundtracks or film scores are always published, either.
    """
    motionpicture = ForeignKey(MotionPicture, on_delete=CASCADE)
    motionpicture_id: int
    song = ForeignKey("Song", on_delete=CASCADE)
    song_id: int


class MusicAlbum(BaseAuditable):
    """An individual Music album production."""
    # TODO: MusicAlbums can also have different "editions", like special or remastered
    #  They would still group together under the same title. Usually they share tracks.
    # TODO: Move media format? Or would be treat albums as being different productions?
    is_compilation = BooleanField(
        default=False,
        help_text="Album is a compilation of other songs, such as a Greatest Hits album."
    )
    # mediaformat = ForeignKey(MediaFormat, on_delete=SET_DEFAULT, default=get_default_mediaformat_audio)  # TODO
    # mediaformat_id: int
    title = CharField(max_length=255, unique=True)  # Temporary unique constraint
    total_discs = PositiveSmallIntegerField(default=1)  # TODO
    year_copyright = PositiveSmallIntegerField(null=True, blank=True, validators=[validate_year_not_future])
    year_produced = PositiveSmallIntegerField(null=True, blank=True, validators=[validate_year_not_future])
    # Relationships
    musicartists = ManyToManyField(
        'MusicArtist',
        through='MusicAlbumToMusicArtist',
        related_name='music_albums',
        blank=True)
    # songrecordings = ManyToManyField(
    #     'SongRecording', through='MusicAlbumToSongRecording',
    #     blank=True)

    def __str__(self):
        return f'{self.title}'

    @cached_property
    def duration(self):
        return self.songrecordings.aggregate(Sum('duration'))['duration__sum']

    @cached_property
    def total_songs(self):
        return self.songrecordings.count()


class MusicAlbumArtwork(BaseAuditable):
    """Holds zero or many images relating to a MusicAlbum."""
    musicalbum = ForeignKey(MusicAlbum, on_delete=CASCADE)
    musicalbum_id: int
    image = ImageField()

    def __str__(self):
        return f'MusicAlbumArtwork {self.pk}: {self.musicalbum_id}'


class MusicAlbumEdition(BaseAuditable):
    """Further classification of different releases of an album.

    TODO: Format here? Probably, or model it after books, e.g., "Production"
     Although formats are sometimes linked to editions. "DigiPak", "Bonus track"
     Remastered albums contain remastered tracks, maybe bonuses
    """
    musicalbum = ForeignKey(MusicAlbum, on_delete=PROTECT)
    total_discs = PositiveSmallIntegerField(default=1)  # TODO
    year_copyright = PositiveSmallIntegerField(null=True, blank=True, validators=[validate_year_not_future])
    year_produced = PositiveSmallIntegerField(null=True, blank=True, validators=[validate_year_not_future])


class MusicAlbumProduction(BaseAuditable):
    """This resolves media formats for album releases.


    """
    musicalbumedition = ForeignKey(MusicAlbumEdition, on_delete=PROTECT)
    total_discs = PositiveSmallIntegerField(default=1)
    year_produced = PositiveSmallIntegerField(null=True, blank=True, validators=[validate_year_not_future])


class MusicAlbumToMusicArtist(BaseAuditable):
    """Relates a MusicAlbum to a MusicArtist; Album Artist.

    This is assuming that while most albums are released under one artist, there
    are cases where there are actually two artists that collaborate on a single
    album, e.g., "Hans Zimmer & James Newton Howard" for the Christopher Nolan
    Batman movies. Both artists are credited on the soundtrack for composition.
    This does not replace individual song artists, as there are "featured"
    tracks, or compilation albums.
    """
    musicalbum = ForeignKey(MusicAlbum, on_delete=CASCADE)
    musicalbum_id: int
    musicartist = ForeignKey('MusicArtist', on_delete=CASCADE)
    musicartist_id: int

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('musicalbum', 'musicartist'),
                name='unique_musicalbumtomusicartist')
        ]

    def __str__(self):
        return f'MusicAlbumToMusicArtist {self.pk}: {self.musicalbum_id}-{self.musicartist_id}'


class MusicAlbumToSongRecording(BaseAuditable):
    disc_number = PositiveSmallIntegerField(null=True, blank=True)
    musicalbum = ForeignKey(MusicAlbum, on_delete=CASCADE)
    musicalbum_id: int
    songrecording = ForeignKey('SongRecording', on_delete=CASCADE)
    songrecording_id: int
    track_number = PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('musicalbum', 'songrecording'),
                name='unique_musicalbumtosongrecording'
            ),
            UniqueConstraint(
                fields=('musicalbum', 'disc_number', 'track_number'),
                name='unique_musicalbumtosongrecording_disc_track'
            )
        ]

    def __str__(self):
        return f'MusicAlbumToSongRecording {self.pk}: {self.musicalbum_id}-{self.songrecording_id}'


class MusicArtist(BaseAuditable):
    """An individual musician or a group of musicians."""
    name = CharField(max_length=255, unique=True)
    website = URLField(
        null=True, blank=True,
        help_text="Website or homepage for this music artist."
    )
    # Relationships
    # songs = ManyToManyField('Song', through='MusicArtistToSong', related_name='+', blank=True)

    def __str__(self):
        return f'{self.name}'

    @cached_property
    def total_albums(self):
        return self.musicalbums.count()

    @cached_property
    def total_songs(self):
        return self.songs.count()


class MusicArtistActivity(BaseAuditable):
    """Dates for MusicArtist activity, as bands can go on hiatus."""
    musicartist = ForeignKey(MusicArtist, on_delete=CASCADE)
    musicartist_id: int
    year_active = PositiveSmallIntegerField(validators=[validate_year_not_future])
    year_inactive = PositiveSmallIntegerField(null=True, blank=True, validators=[validate_year_not_future])

    class Meta:
        constraints = [
            UniqueConstraint(fields=('musicartist', 'year_active'), name='unique_musicartistactivity')
        ]


class MusicArtistToPerson(BaseAuditable):
    """Relates a MusicArtist to a Person.

    A MusicArtist may be one or many persons, e.g., solo artists, composers,
    bands, etc.
    These are also optionally bound by time. Band members can leave and re-join
    a group.
    Only "official" members of a band are considered.
    """
    musicartist = ForeignKey(MusicArtist, on_delete=CASCADE)
    musicartist_id: int
    person = ForeignKey('Person', on_delete=CASCADE)
    person_id: int

    objects = Manager()
    with_related = managers.MusicArtistToPersonManager()

    class Meta:
        constraints = [
            UniqueConstraint(fields=('musicartist', 'person'), name='unique_musicartisttoperson')
        ]

    def __str__(self):
        return f'MusicArtistToPerson {self.pk}: {self.musicartist_id}-{self.person_id}'

    @property
    def is_active(self) -> Optional[bool]:
        activity = self.musicartisttopersonactivity_set.order_by('date_active').first()
        if activity is None:
            return None
        if activity.date_inactive is None:
            return True
        if activity.date_inactive >= timezone.now():
            return False


class MusicArtistToPersonActivity(BaseAuditable):
    """Holds records of when a person was part of a group or act."""
    musicartisttoperson = ForeignKey(MusicArtistToPerson, on_delete=CASCADE)
    musicartisttoperson_id: int
    date_active = DateField(validators=[validate_date_not_future])
    date_inactive = DateField(null=True, blank=True, validators=[validate_date_not_future])


class MusicArtistToSong(BaseAuditable):
    """Relates a MusicArtist to a Song"""
    musicartist = ForeignKey(MusicArtist, on_delete=CASCADE)
    musicartist_id: int
    song = ForeignKey('Song', on_delete=CASCADE)
    song_id: int
    # role?

    class Meta:
        constraints = [
            UniqueConstraint(fields=('musicartist', 'song'), name='unique_musicartisttosong')
        ]

    def __str__(self):
        return f'MusicArtistToSong {self.pk}: {self.musicartist_id}-{self.song_id}'


class MusicArtistToSongRecording(BaseAuditable):
    musicartist = ForeignKey(MusicArtist, on_delete=CASCADE)
    musicartist_id: int
    songrecording = ForeignKey('SongRecording', on_delete=CASCADE)
    songrecording_id: int

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('musicartist', 'songrecording'),
                name='unique_musicartisttosongrecording'
            )
        ]

    def __str__(self):
        return f'MusicArtistToSongRecording {self.pk}: {self.musicartist_id}-{self.songrecording_id}'


class NonCatalogItem(BaseAuditable):
    """A non-tangible or generic item, such as a tax levied."""
    name = CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'


class Order(BaseAuditable):
    """A purchase record which is usually paid in advance, but not immediately fulfilled"""
    # party = ForeignKey()
    order_date = DateField()
    order_number = CharField(max_length=255)

    def __str__(self):
        return f'Order {self.pk}: {self.order_number}'


class OrderLineItem(BaseAuditable):
    class Subtype(TextChoices):
        CATALOGUE_ITEM = 'CATALOG_ITEM', 'CATALOG_ITEM'
        NON_CATALOGUE_ITEM = 'NON_CATALOG_ITEM', 'NON_CATALOG_ITEM'
    order = ForeignKey(Order, on_delete=CASCADE)
    order_id: int
    subtype = CharField(max_length=31, choices=Subtype.choices)

    def __str__(self):
        return f'OrderLineItem {self.pk}: {self.order_id}'


class Party(BaseAuditable):
    class Subtype(TextChoices):
        COMPANY = 'BUSINESS'
        PERSON = 'PERSON'
    name = CharField(max_length=255)
    partytype = ForeignKey('PartyType', on_delete=SET_NULL, null=True, blank=True)
    subtype = CharField(max_length=31, choices=Subtype.choices)

    def __str__(self):
        return f'{self.name}'


class PartyBusiness(BaseAuditable):
    """A business or corporate entity."""
    party = OneToOneField(Party, on_delete=CASCADE, primary_key=True)
    party_id: int
    trade_name = CharField(max_length=255)

    def __str__(self):
        return f'PartyCompany {self.pk}: {self.trade_name}'


class PartyPerson(BaseAuditable):
    """An individual person."""
    party = OneToOneField(Party, on_delete=CASCADE, primary_key=True)
    party_id: int
    person = OneToOneField('Person', on_delete=CASCADE)
    person_id: int


class PartyType(BaseAuditable):
    name = CharField(max_length=255)
    parent_partytype = ForeignKey(
        'self', on_delete=SET_NULL, null=True, blank=True, related_name='child_party_types'
    )

    def __str__(self):
        return f'{self.name}'


class Payee(BaseAuditable):
    """Within scope of transaction, the entity receiving payment."""
    memo = TextField(null=True, blank=True)
    name = CharField(max_length=255, unique=True, help_text="Name as displayed on transaction ledger.")
    party = ForeignKey(Party, on_delete=PROTECT, null=True, blank=True)
    party_id: int

    def __str__(self):
        return f'{self.name}'


class Person(BaseAuditable):
    """A person. Generally self-explanatory as an entity.
    Maybe a personal acquaintance, and/or a notable individual with some level of fame.
    """
    first_name = CharField(max_length=255)
    middle_name = CharField(max_length=255, blank=True)
    last_name = CharField(max_length=255)
    date_of_birth = DateField(null=True, blank=True)
    date_of_death = DateField(null=True, blank=True)
    subtype_acquaintance = BooleanField()
    subtype_notable = BooleanField()
    notes = TextField(blank=True)

    def __str__(self):
        return f'{self.full_name}'

    @property
    def age(self) -> Optional[int]:
        if self.date_of_birth is None:
            return None
        reference_date = self.date_of_death or datetime.date.today()
        years = reference_date.year - self.date_of_birth.year
        months = reference_date.month - self.date_of_birth.month
        if months < 0:
            return years - 1
        if months == 0:
            days = reference_date.day - self.date_of_birth.day
            if days < 0:
                return years - 1
        return years

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'


class PointOfSale(BaseAuditable):
    """A PointOfSale transaction, usually accompanied by a physical receipt.
    Similar to an invoice or order, but is typically both paid and fulfilled at the time of the transaction.
    """
    barcode = CharField(max_length=255, null=True, blank=True)
    party = ForeignKey(Party, on_delete=PROTECT)  # Business, retailer...
    party_id: int
    point_of_sale_date = DateField()
    point_of_sale_time = TimeField(null=True, blank=True)
    txn = OneToOneField('Txn', on_delete=SET_NULL, null=True, blank=True)  # TODO

    @property
    def line_item_total(self):
        qs = (
            self.line_items.all()
            .aggregate(
                total=Sum(
                    F('catalogitemtopointofsalelineitem__quantity') *
                    F('catalogitemtopointofsalelineitem__unit_price')
                )
            )
        )
        return qs['total']


class PointOfSaleDocument(BaseAuditable):
    """Scanned document(s) related to a PointOfSale transaction."""
    pointofsale = ForeignKey(PointOfSale, on_delete=PROTECT)
    pointofsale_id: int
    document = FileField()


class PointOfSaleLineItem(BaseAuditable):
    """Line items of a PointOfSale transaction."""
    class Subtype(TextChoices):
        CATALOGUE_ITEM = 'CATALOGUE_ITEM', 'CATALOGUE_ITEM'
        NON_CATALOGUE_ITEM = 'NON_CATALOGUE_ITEM', 'NON_CATALOGUE_ITEM'
    pointofsale = ForeignKey(PointOfSale, on_delete=PROTECT, related_name='line_items')
    pointofsale_id: int
    short_memo = CharField(max_length=255, null=True)
    subtype = CharField(max_length=31, choices=Subtype.choices)

    def __str__(self):
        return f'PointOfSaleLineItem {self.pk}: {self.pointofsale_id}'


class PointOfSaleToTxn(BaseAuditable):
    """Relates a PointOfSale purchase to its correlated Transaction.

    In a PointOfSale scenario, these are settled paid in-full at the time of
    purchase.
    I would think that only one TXN record would relate to one PointOfSale
    record.
    By this logic, one of these tables MUST contain a reference to the other;
    however, this is intentionally modeled as a separate table for consistency
    and to avoid a refactor for any edge cases.
    """
    pointofsale = OneToOneField(PointOfSale, on_delete=CASCADE)  # maybe foreign key?
    pointofsale_id: int
    txn = OneToOneField('Txn', on_delete=CASCADE)  # definitely one-to-one
    txn_id: int


class Seller(BaseAuditable):
    name = CharField(max_length=255)


class Song(BaseAuditable):
    """A particular rendition of a song.

    This is a bit abstract, in that it does not fully represent the recordings
    or derivative works.
    """
    lyrics = TextField(blank=True, default='')
    title = CharField(max_length=255)
    # Relationships
    musicartists = ManyToManyField(
        MusicArtist, through='MusicArtistToSong',
        related_name='+'
    )

    def __str__(self):
        return f'{self.title}'


class SongRecording(BaseAuditable):
    """"""
    class RecordingType(TextChoices):
        LIVE = 'LIVE', 'Live Performance'
        STUDIO = 'STUDIO', 'Studio Recording'
    duration = DurationField(null=True, blank=True, validators=[validate_positive_timedelta])
    lyrics = TextField(blank=True, default='')
    song = ForeignKey(Song, on_delete=CASCADE)
    recording_type = CharField(max_length=6, choices=RecordingType.choices, default=RecordingType.STUDIO)
    # Relationships
    musicartists = ManyToManyField(
        MusicArtist, through='MusicArtistToSongRecording',
        related_name='+'
    )


class SongToSong(BaseAuditable):
    """Many to many for Songs.

    Includes covers, arrangements, or other derivative works.
    """
    # relationship: enum or foreign key lookup
    # tagging may play a part in this too (acoustic, instrumental)
    class SongRelationship(TextChoices):
        ARRANGEMENT = 'ARRANGEMENT'
        # COMPILATION = 'COMPILATION'
        COVER = 'COVER', 'Cover'
        # EDIT = 'EDIT'
        INSTRUMENTAL = 'INSTRUMENTAL'
        OVERTURE = 'OVERTURE'
        MASHUP = 'MASHUP', 'Mash-up'
        # REMASTER = 'REMASTER'
        REMIX = 'REMIX'
    song_derivative = ForeignKey(
        Song, on_delete=CASCADE,
        related_name='+'
    )
    song_derivative_id: int
    song_archetype = ForeignKey(
        Song, on_delete=CASCADE,
        related_name='+'
    )
    song_archetype_id: int
    song_relationship = CharField(max_length=15, choices=SongRelationship.choices)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('song_derivative', 'song_original'),
                name='unique_songtosong'
            )
        ]

    def clean(self):
        if self.song_archetype == self.song_derivative:
            raise ValidationError("Original and derivative must be different.")


class Txn(BaseAuditable):
    """A (financial) transaction.

    Should have properties for "total debit" and "total credit" derived from its
    line items, and those values should be equal.
    """
    memo = TextField(null=True, blank=True)
    payee = ForeignKey(Payee, on_delete=PROTECT)
    payee_id: int
    ref_total = CurrencyField(
        null=True, blank=True,
        verbose_name="Reference Total",
        help_text="Total transaction amount reflected on statement."
    )
    txn_date = DateField()

    objects = querysets.TxnQuerySet.as_manager()

    @property
    def _is_balanced(self) -> bool:
        return self._total_debits == self._total_credits

    @property
    def _total_credits(self):
        qs = (
            self.line_items.filter(debit=False)
            .aggregate(
                total_credits=Sum('amount')
            )
        )
        return qs['total_credits'] or 0

    @property
    def _total_debits(self):
        qs = (
            self.line_items.filter(debit=True)
            .aggregate(
                total_debits=Sum('amount')
            )
        )
        return qs['total_debits'] or 0


class TxnLineItem(BaseAuditable):
    """A line item of a Transaction.

    To support double-entry style accounting, this is where different accounts
    are related to individual debits/credits, and the outer "Transaction" groups
    them together as a total.
    Every transaction should have at least two line items representing the
    "from" and "to" accounts.
    """
    account = ForeignKey(Account, on_delete=PROTECT)
    account_id: int
    amount = CurrencyField()
    debit = BooleanField(default=False)
    memo = TextField(null=True, blank=True)
    txn = ForeignKey(Txn, on_delete=PROTECT, related_name='line_items')
    txn_id: int

    def __str__(self):
        return f'TxnLineItem {self.pk}: {self.txn_id}'


class Unit(BaseAuditable):
    """Unit table."""
    class Dimension(TextChoices):
        AREA = 'AREA', 'AREA'
        CURRENT = 'CURRENT', 'CURRENT'
        LENGTH = 'LENGTH', 'LENGTH'
        LIGHT = 'LIGHT', 'LIGHT'
        MASS = 'MASS', 'MASS'
        MATTER = 'MATTER', 'MATTER'
        TEMPERATURE = 'TEMPERATURE', 'TEMPERATURE'
        TIME = 'TIME', 'TIME'
        VOLUME = 'VOLUME', 'VOLUME'

    class System(TextChoices):
        SI = 'SI', 'SI'
        US = 'US', 'US'

    abbr = CharField(max_length=15)
    name = CharField(max_length=63)
    dimension = CharField(max_length=15, choices=Dimension.choices, null=True)
    system = CharField(max_length=2, choices=System.choices, null=True)

    def __str__(self):
        return f'{self.name} ({self.abbr})'


class Vehicle(BaseAuditable):
    """An individual, uniquely identifiable vehicle."""
    vehicle_year = ForeignKey('VehicleYear', on_delete=PROTECT)
    vehicle_year_id: int
    vin = UpperCharField(max_length=17, unique=True, validators=[MinLengthValidator(11)])
    # TODO: VIN Validator based on year + date
    # NHTSA vPIC data could go in a JSON format

    def __str__(self):
        return f'Vehicle {self.pk}: {self.vin}'


class VehicleMake(BaseAuditable):
    """The make/brand/marque of a vehicle."""
    name = CharField(max_length=255, unique=True, help_text="Make/Brand/Marque")
    # manufacturer

    def __str__(self):
        return f'{self.__class__.__name__} {self.pk}: {self.name}'


class VehicleMileage(BaseAuditable):
    """A mileage record for a Vehicle at a given point in time."""
    vehicle = ForeignKey('Vehicle', on_delete=PROTECT)
    vehicle_id: int
    odometer_date = DateField(
        validators=[validate_date_not_future],
        help_text="Date on which this odometer reading was captured"
    )
    odometer_miles = PositiveIntegerField(help_text="Odometer reading in miles")
    odometer_time = TimeField(null=True, blank=True, help_text="Time of this reading, if available")

    class Meta:
        constraints = [
            # Sanity date/time constraint
            UniqueConstraint(fields=('vehicle', 'odometer_date', 'odometer_time'), name='unique_vehiclemileage')
        ]

    @property
    def odometer_datetime(self) -> datetime.datetime:
        return datetime.datetime.combine(self.odometer_date, self.odometer_time)


class VehicleModel(BaseAuditable):
    """The model of a vehicle, e.g., Supra."""
    name = CharField(max_length=255, help_text="Model name, such as 3000GT, Forte, Supra")
    vehicle_make = ForeignKey(VehicleMake, on_delete=PROTECT)
    vehicle_make_id: int

    class Meta:
        constraints = [
            UniqueConstraint(fields=('name', 'vehiclemake'), name='unique_vehiclemodel')
        ]

    def __str__(self):
        return f'VehicleModel {self.pk}: {self.vehicle_make_id}-{self.name}'


class VehicleService(BaseAuditable):
    """Preventative maintenance or repair. Usually encompasses multiple service items."""
    date_in = DateField()
    date_out = DateField(null=True, blank=True)
    mileage_in = IntegerField()
    mileage_out = IntegerField()
    vehicle = ForeignKey(Vehicle, on_delete=PROTECT)
    vehicle_id: int


class VehicleServiceItem(BaseAuditable):  # Line item
    """Individual maintenance items from a service."""
    # TODO: Should have foreign keys for service types, like oil change, oil filter, tire rotation, since those are
    #  standard across vehicles.
    description = CharField(max_length=255)
    vehicleservice = ForeignKey(VehicleService, on_delete=CASCADE)
    vehicleservice_id: int


class VehicleTrim(BaseAuditable):
    """An edition/trim of a vehicle model, such as EX, Turbo, Base."""
    name = CharField(max_length=255, help_text="Trim Level, such as EX, GT, SS")
    vehiclemodel = ForeignKey(VehicleModel, on_delete=PROTECT)
    vehiclemodel_id: int

    class Meta:
        constraints = [
            UniqueConstraint(fields=('name', 'vehiclemodel'), name='unique_vehicletrim')
        ]

    def __str__(self):
        return f'VehicleTrim {self.pk}: {self.vehiclemodel_id}-{self.name}'


class VehicleYear(BaseAuditable):
    """Year that a Make/Model/Trim was actually produced."""
    vehicletrim = ForeignKey(VehicleTrim, on_delete=PROTECT)
    vehicletrim_id: int
    year = IntegerField(
        validators=[MinValueValidator(1886), validate_year_not_future],
        help_text="Production year"
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=('vehicletrim', 'year'), name='unique_vehicleyear')
        ]

    def __str__(self):
        return f'VehicleYear {self.pk}: {self.vehicletrim_id}-{self.year}'


class VideoGame(BaseAuditable):
    """"""
    # developer(s) - person or company or other entity
    # genre(s)
    # language?
    # platform: PC, PS4, NES, SNES - not mutually exclusive; m2m
    # publisher(s) - usually a company, but could be independently published or n/a
    # release date - different per platform, port, region, or market (part of m2m)
    # tag(s)? Something looser than genre, though not required.
    # title

    # Could also relate to people: voice acting, developers, directors, composers, producers
    # Relates to music via soundtracks (songs vs albums is debatable, like movies)
    #  Like, an "unofficial" OST is kind of an issue for copyright, but not every game was published alongside an OST
    # Not every game is regionalized right? NTSC / PAL / JP was common for consoles. Region # is a thing for media.


class VideoGameAddon(BaseAuditable):
    """DLC, Expansion pack, or other additional components that are optional."""
    # videogame = ForeignKey
    # release date
    # title / name
    # type, such as DLC, expansion, addon, content, in-game something (or tags may be appropriate)


class VideoGamePlatform(BaseAuditable):
    """"""
    # May also be a commodity, asset, or catalogue item, but we will probably keep this abstracted from the physical
    #  consoles or assemblies
    name = CharField(max_length=31)
    short_name = CharField(max_length=15)


class VideoGameToVideoGamePlatform(BaseAuditable):
    """"""
    # release_date
    # videogame
    # videogameplatform
    # TODO: region...