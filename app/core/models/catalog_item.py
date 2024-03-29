from decimal import Decimal

from django.core.validators import MinLengthValidator
from django.db.models import (
    CASCADE,
    CharField,
    DecimalField,
    ForeignKey,
    IntegerField,
    JSONField,
    OneToOneField,
    PROTECT,
    SET_NULL,
    UniqueConstraint,
    TextChoices,
)

from django_base.models import BaseAuditable
from django_base.models.fields import UpperCharField
from django_base.utils import default_related_names, pascal_case_to_snake_case
from django_base.validators import validate_alphanumeric, validate_digit

from core.validators import validate_isbn, validate_isbn_13_check_digit
from ._fields import CurrencyField


class CatalogItem(BaseAuditable):
    """An item with unique registries in other global systems.

    Can generally be ordered, purchased, re-sold, and accumulated as a discrete
    asset or inventory.
    Does not include concepts like labor hours, services, or warranties.

    My primary key is essentially *my* catalog number, despite the fact that my
    table doesn't get mailed out before the holidays.
    """

    class Subtype(TextChoices):
        DIGITAL_SONG = 'DIGITAL_SONG', 'DIGITAL_SONG'
        MANUFACTURED = 'MANUFACTURED', 'MANUFACTURED'
        MUSIC_ALBUM = 'MUSIC_ALBUM', 'MUSIC_ALBUM'

    asin = UpperCharField(
        max_length=10, unique=True,
        null=True, blank=True,
        validators=[MinLengthValidator(10), validate_alphanumeric],
        verbose_name="ASIN",
        help_text="Amazon Standard Identification Number"
    )
    ean_13 = CharField(
        max_length=13, unique=True,
        null=True, blank=True,
        validators=[MinLengthValidator(13), validate_digit],
        verbose_name="EAN-13",
        help_text="European Article Number"
    )
    eav = JSONField(null=True, blank=True)
    # isbn is also part of GSIN / gs1 spec now, apparently
    isbn = CharField(
        max_length=10, unique=True,
        null=True, blank=True,
        validators=[MinLengthValidator(10), validate_isbn],
        verbose_name="ISBN",
        help_text="International Standard Book Number"
    )
    isbn_13 = CharField(
        max_length=13, unique=True,
        null=True, blank=True,
        validators=[
            MinLengthValidator(13),
            validate_digit,
            validate_isbn_13_check_digit
        ],
        verbose_name="ISBN-13"
    )
    ismn = CharField(
        max_length=13, unique=True,
        null=True, blank=True,
        validators=[MinLengthValidator(13)],
        verbose_name="ISMN",
        help_text="International Standard Music Number"
    )
    name = CharField(max_length=255)
    subtype = CharField(
        max_length=31, choices=Subtype.choices, blank=True, default='',
    )
    upc_a = CharField(
        max_length=12, unique=True, null=True, blank=True,
        validators=[MinLengthValidator(12), validate_digit]
    )

    class Meta:
        verbose_name = 'CatalogItem'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name}'

    @property
    def amazon_url(self) -> str:
        if self.asin:
            return f'https://www.amazon.com/dp/{self.asin}'
        else:
            return ''


class CatalogItemBookPublication(BaseAuditable):
    catalog_item = OneToOneField(
        CatalogItem, on_delete=CASCADE, primary_key=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )
    book_publication = ForeignKey(
        'BookPublication', on_delete=PROTECT,
        **default_related_names(__qualname__)
    )


class CatalogItemDigitalSong(BaseAuditable):
    """Digital songs.

    Unlike Music albums, can be distributed individually absent of other medium.
    - Even if a song is released as a "Single", that "Single" still requires a
      medium for physical distribution, which makes it a "Single Album"
    """

    catalog_item_id: int

    catalog_item = OneToOneField(
        CatalogItem, on_delete=CASCADE, primary_key=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )
    song_recording = OneToOneField(
        'SongRecording', on_delete=CASCADE, null=True, blank=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )


class CatalogItemManufactured(BaseAuditable):
    """Items that are characterized by a manufacturer and part number.

    This is one of the most general subtypes of catalog items. Favor the use of
    other subtypes if they describe the item more specifically.
    """

    catalog_item = OneToOneField(
        CatalogItem, on_delete=CASCADE, primary_key=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )
    manufacturer = ForeignKey(
        'Manufacturer', on_delete=PROTECT,
        null=True, blank=True,
        **default_related_names(__qualname__)
    )
    part_number = CharField(
        max_length=255, blank=True,
        help_text="Model or Part Number"
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('manufacturer', 'part_number'),
                name='unique_catalog_item_manufactured',
                nulls_distinct=False,
            )
        ]


class CatalogItemMotionPictureRecording(BaseAuditable):
    catalog_item = OneToOneField(
        CatalogItem, on_delete=CASCADE, primary_key=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )
    motion_picture_recording = ForeignKey(
        'MotionPictureRecording', on_delete=CASCADE,
        **default_related_names(__qualname__)
    )

    class Meta:
        verbose_name = 'CatalogItem <-> MotionPictureRecording'
        verbose_name_plural = verbose_name


class CatalogItemMusicAlbumProduction(BaseAuditable):
    """A produced Music Album distributed in a particular format."""

    catalog_item_id: int

    catalog_item = OneToOneField(
        CatalogItem, on_delete=CASCADE, primary_key=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )
    music_album_production = ForeignKey(
        'MusicAlbumProduction', on_delete=SET_NULL,
        null=True, blank=True,
        **default_related_names(__qualname__)
    )


class CatalogItemXCatalogItem(BaseAuditable):
    """Holds relationships between CatalogItems to account for bundles.

    A "bundle" can contain individual items that may be listed separately. A
    bundle probably shouldn't contain bundles, though there's no real
    enforcement mechanism for that.
    """

    catalog_item_a = ForeignKey(
        'CatalogItem', on_delete=CASCADE, related_name='+')
    catalog_item_b = ForeignKey(
        'CatalogItem', on_delete=CASCADE, related_name='+')
    relationship = None


class CatalogItemXInvoiceLineItem(BaseAuditable):
    """Relates a CatalogItem record to an InvoiceLineItem record.

    A properly formed invoice line item should only relate to a single catalog
    item.
    """

    invoice_line_item_id: int
    catalog_item_id: int

    invoice_line_item = OneToOneField(
        'InvoiceLineItem', on_delete=CASCADE, primary_key=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )
    catalog_item = ForeignKey(
        'CatalogItem', on_delete=PROTECT,
        **default_related_names(__qualname__)
    )
    unit_price = CurrencyField()
    # seller?
    quantity = IntegerField()

    def __str__(self) -> str:
        return f'CatalogItemXInvoiceLineItem {self.pk}: {self.catalog_item_id}'


class CatalogItemXOrderLineItem(BaseAuditable):
    """Relates a CatalogItem record to an OrderLineItem record.

    A properly formed order line item should only relate to a single catalog
    item.
    """

    order_line_item_id: int
    catalog_item_id: int

    order_line_item = OneToOneField(
        'OrderLineItem', on_delete=CASCADE, primary_key=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )
    catalog_item = ForeignKey(
        'CatalogItem', on_delete=PROTECT,
        **default_related_names(__qualname__)
    )

    def __str__(self) -> str:
        return f'CatalogItemXOrderLineItem {self.pk}: {self.catalog_item_id}'


class CatalogItemXPointOfSaleLineItem(BaseAuditable):
    """Relates a CatalogItem record to a PointOfSaleLineItem record.

    Only one relation should exist per line item.
    """

    catalog_item_id: int
    point_of_sale_line_item_id: int
    unit_id: int

    point_of_sale_line_item = OneToOneField(
        'PointOfSaleLineItem', on_delete=CASCADE, primary_key=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )
    catalog_item = ForeignKey(
        'CatalogItem', on_delete=PROTECT,
        **default_related_names(__qualname__)
    )
    quantity = DecimalField(max_digits=19, decimal_places=5, default=1)
    unit_price = CurrencyField()
    unit = ForeignKey(
        'Unit', on_delete=SET_NULL, null=True, blank=True,
        **default_related_names(__qualname__)
    )

    def __str__(self) -> str:
        return (
            f'CatalogItemXPointOfSaleLineItem {self.pk}:'
            f' {self.catalog_item_id}'
        )

    @property
    def price(self) -> Decimal:
        return self.quantity * self.unit_price


class CatalogItemXVideoGameEdition(BaseAuditable):
    catalog_item = ForeignKey(
        CatalogItem, on_delete=CASCADE,
        **default_related_names(__qualname__)
    )
    video_game_edition = ForeignKey(
        'VideoGameEdition', on_delete=CASCADE,
        **default_related_names(__qualname__)
    )


class CatalogItemXVideoGamePlatformEdition(BaseAuditable):
    catalog_item = ForeignKey(
        CatalogItem, on_delete=CASCADE,
        **default_related_names(__qualname__)
    )
    video_game_platform_edition = ForeignKey(
        'VideoGamePlatformEdition', on_delete=CASCADE,
        **default_related_names(__qualname__)
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('catalog_item', 'video_game_platform_edition'),
                name='unique_catalog_item_x_video_game_platform_edition'
            )
        ]
