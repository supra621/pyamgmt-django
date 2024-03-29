import datetime

from django.db.models import (
    CharField, DateField, ForeignKey, IntegerField, PositiveIntegerField,
    TimeField,
    UniqueConstraint,
    CASCADE, PROTECT, SET_NULL,
)
from django.utils.functional import cached_property
from django.core.validators import MinLengthValidator, MinValueValidator

from django_base.models import BaseAuditable
from django_base.models.fields import UpperCharField
from django_base.utils import default_related_names
from django_base.validators import validate_date_not_future, validate_year_not_future


class Vehicle(BaseAuditable):
    """An individual, uniquely identifiable vehicle.

    Accounting reached via Vehicle -> Asset -> Account
    """

    vehicle_year_id: int

    vehicle_year = ForeignKey(
        'VehicleYear', on_delete=PROTECT,
        **default_related_names(__qualname__)
    )
    vin = UpperCharField(
        max_length=17, unique=True, validators=[MinLengthValidator(11)]
    )
    # TODO 2023-12-12: VIN Validator based on year + date
    # NHTSA vPIC data could go in a JSON format

    def __str__(self) -> str:
        return f'Vehicle {self.pk}: {self.vin}'

    @cached_property
    def admin_description(self) -> str:
        return (
            f'{self.vehicle_year.year}'
            f' {self.vehicle_year.vehicle_trim.vehicle_model.vehicle_make.name}'
            f' {self.vehicle_year.vehicle_trim.vehicle_model.name}'
            f' VIN: {self.vin}'
        )


class VehicleMake(BaseAuditable):
    """The make/brand/marque of a vehicle."""

    name = CharField(max_length=255, unique=True, help_text="Make/Brand/Marque")
    manufacturer = ForeignKey(
        'Manufacturer', on_delete=SET_NULL,
        null=True,
        **default_related_names(__qualname__)
    )

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.pk}: {self.name}'


class VehicleMileage(BaseAuditable):
    """A mileage record for a Vehicle at a given point in time."""

    vehicle_id: int

    vehicle = ForeignKey(
        'Vehicle', on_delete=PROTECT,
        **default_related_names(__qualname__)
    )
    odometer_date = DateField(
        validators=[validate_date_not_future],
        help_text="Date on which this odometer reading was captured"
    )
    odometer_miles = PositiveIntegerField(help_text="Odometer reading in miles")
    odometer_time = TimeField(
        null=True, blank=True, help_text="Time of this reading, if available"
    )

    class Meta:
        constraints = [
            # Sanity date/time constraint
            UniqueConstraint(
                fields=('vehicle', 'odometer_date', 'odometer_time'),
                name='unique_vehicle_mileage'
            )
        ]

    @property
    def odometer_datetime(self) -> datetime.datetime:
        return datetime.datetime.combine(self.odometer_date, self.odometer_time)


class VehicleModel(BaseAuditable):
    """The model of a vehicle, e.g., Supra."""

    vehicle_make_id: int

    name = CharField(
        max_length=255,
        help_text="Model name, such as 3000GT, Forte, Supra"
    )
    vehicle_make = ForeignKey(
        VehicleMake, on_delete=PROTECT,
        **default_related_names(__qualname__)
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('name', 'vehicle_make'),
                name='unique_vehicle_model'
            )
        ]

    def __str__(self) -> str:
        return f'VehicleModel {self.pk}: {self.vehicle_make_id}-{self.name}'


class VehicleService(BaseAuditable):
    """Preventative maintenance or repair.

    Usually encompasses multiple service items.
    """

    vehicle_id: int

    date_in = DateField()
    date_out = DateField(null=True, blank=True)
    mileage_in = IntegerField()
    mileage_out = IntegerField()
    vehicle = ForeignKey(
        Vehicle, on_delete=PROTECT,
        **default_related_names(__qualname__)
    )


class VehicleServiceItem(BaseAuditable):  # Line item
    """Individual maintenance items from a service."""
    # TODO: Should have foreign keys for service types, like oil change,
    #  oil filter, tire rotation, since those are standard across vehicles.
    vehicle_service_id: int

    description = CharField(max_length=255)
    vehicle_service = ForeignKey(
        VehicleService, on_delete=CASCADE,
        **default_related_names(__qualname__)
    )


class VehicleTrim(BaseAuditable):
    """An edition/trim of a vehicle model, such as EX, Turbo, Base."""

    vehicle_model_id: int

    name = CharField(max_length=255, help_text="Trim Level, such as EX, GT, SS")
    vehicle_model = ForeignKey(
        VehicleModel, on_delete=PROTECT,
        **default_related_names(__qualname__)
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('name', 'vehicle_model'),
                name='unique_vehicle_trim'
            )
        ]

    def __str__(self) -> str:
        return f'VehicleTrim {self.pk}: {self.vehicle_model_id}-{self.name}'


class VehicleYear(BaseAuditable):
    """Year that a Make/Model/Trim was actually produced."""

    vehicle_trim_id: int

    vehicle_trim = ForeignKey(
        VehicleTrim, on_delete=PROTECT,
        **default_related_names(__qualname__)
    )
    year = IntegerField(
        validators=[MinValueValidator(1886), validate_year_not_future],
        help_text="Production year"
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('vehicle_trim', 'year'),
                name='unique_vehicle_year'
            )
        ]

    def __str__(self) -> str:
        return f'VehicleYear {self.pk}: {self.vehicle_trim_id}-{self.year}'
