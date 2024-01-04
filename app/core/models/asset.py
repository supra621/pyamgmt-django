from django.db.models import (
    CharField, DateField, ForeignKey, IntegerField, OneToOneField, TextField,
    TextChoices,
    CASCADE, PROTECT, SET_NULL,
)

from django_base.models import BaseAuditable
from django_base.utils import default_related_names, pascal_case_to_snake_case


class Asset(BaseAuditable):
    """Any item which implies ownership."""

    class Subtype(TextChoices):
        DISCRETE = 'DISCRETE', 'DISCRETE'
        INVENTORY = 'INVENTORY', 'INVENTORY'

    account_asset_real_id: int

    account_asset_real = ForeignKey(
        'AccountAssetReal', on_delete=SET_NULL,
        null=True, blank=True,
        **default_related_names(__qualname__)
    )
    description = TextField(null=True, blank=True)
    subtype = CharField(max_length=31, choices=Subtype.choices)

    class Meta:
        verbose_name = 'Asset'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return f'Asset {self.pk}: {self.description[:30]}'


class AssetDiscrete(BaseAuditable):
    """An item that is uniquely identifiable.

    Examples: A vehicle, serialized equipment, or property
    """

    class Subtype(TextChoices):
        CATALOG_ITEM = 'CATALOG_ITEM', 'CATALOG_ITEM'
        MANUFACTURED = 'MANUFACTURED', 'MANUFACTURED'
        VEHICLE = 'VEHICLE', 'VEHICLE'

    asset_id: int

    asset = OneToOneField(
        Asset, on_delete=CASCADE, primary_key=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )
    date_acquired = DateField(null=True, blank=True)
    date_withdrawn = DateField(null=True, blank=True)
    subtype = CharField(max_length=31, choices=Subtype.choices, default='NONE')

    class Meta:
        verbose_name = 'Asset::Discrete'
        verbose_name_plural = verbose_name


# class AssetDiscreteManufactured(BaseAuditable):
#     asset = OneToOneField(
#         Asset, on_delete=CASCADE, primary_key=True,
#         related_name=pascal_case_to_snake_case(__qualname__)
#     )
#     manufacturer = ForeignKey(
#         'Manufacturer', on_delete=SET_NULL, null=True, blank=True,
#         **default_related_names(__qualname__)
#     )
#     serial = CharField(max_length=255, blank=True)


# class AssetDiscreteSerialized(BaseAuditable):
#     """An item that is uniquely identifiable by serial number."""
#     asset_discrete = OneToOneField(
#         AssetDiscrete, on_delete=CASCADE, primary_key=True,
#         related_name=pascal_case_to_snake_case(__qualname__)
#     )
#     serial = CharField(max_length=255)
#     out_of = CharField(max_length=255, blank=True)
#     notes = TextField(blank=True)
#
#     class Meta:
#         verbose_name = 'Asset::Discrete::Serialized'
#         verbose_name_plural = 'Asset::Discrete::Serialized'


class AssetDiscreteVehicle(BaseAuditable):
    """A discrete asset that can be associated with a unique vehicle."""

    asset_discrete_id: int
    vehicle_id: int

    asset_discrete = OneToOneField(
        AssetDiscrete, on_delete=CASCADE, primary_key=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )
    vehicle = OneToOneField(
        'Vehicle', on_delete=PROTECT,
        related_name=pascal_case_to_snake_case(__qualname__)
    )

    class Meta:
        verbose_name = 'Asset::Discrete::Vehicle'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return f'AssetDiscreteVehicle {self.pk}: {self.vehicle_id}'


class AssetDiscreteXCatalogItem(BaseAuditable):
    """A discrete asset that can relate to a CatalogItem.

    Although this looks like a subtype, it's joining domains.
    """

    asset_discrete_id: int
    catalog_item_id: int

    asset_discrete = OneToOneField(
        AssetDiscrete, on_delete=CASCADE, primary_key=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )
    catalog_item = ForeignKey(
        'CatalogItem', on_delete=PROTECT,
        **default_related_names(__qualname__)
    )

    class Meta:
        verbose_name = 'Asset::Discrete <-> CatalogItem'
        verbose_name_plural = verbose_name


class AssetInventory(BaseAuditable):
    """An item that is not uniquely identifiable.

    Example: Copies of DVDs, un-serialized items.
    """

    asset_id: int
    catalog_item_id: int

    asset = OneToOneField(
        Asset, on_delete=CASCADE, primary_key=True,
        related_name=pascal_case_to_snake_case(__qualname__)
    )
    # CatalogItem is OneToOne because inventory should accumulate
    catalog_item = OneToOneField(
        'CatalogItem', on_delete=PROTECT,
        related_name=pascal_case_to_snake_case(__qualname__)
    )
    quantity = IntegerField(default=1)

    class Meta:
        verbose_name = 'Asset::Inventory'
        verbose_name_plural = verbose_name


class AssetType(BaseAuditable):
    """Expandable type to support hierarchy

    Not to be confused with AssetSubtype.
    """
    # TODO 2023-12-12: Do I care about this?
    name = CharField(max_length=255)
    parent_asset_type = ForeignKey(
        'self',
        on_delete=SET_NULL,
        related_name='child_asset_types',
        null=True, blank=True,
    )

    def __str__(self) -> str:
        return f'AssetType {self.pk}: {self.name}'
