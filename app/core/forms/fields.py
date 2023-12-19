__all__ = [
    'MusicAlbumEditionChoiceField',
    'SongRecordingChoiceField',
    'VehicleYearChoiceField',
]

from django.forms import ModelChoiceField


class MusicAlbumEditionChoiceField(ModelChoiceField):
    def __init__(self, queryset, **kwargs):
        if queryset is not None:
            queryset = (
                queryset
                .select_related('music_album')
            )
        super().__init__(queryset, **kwargs)

    def label_from_instance(self, obj) -> str:
        return f'{obj.music_album.title} ({obj.name})'


class SongRecordingChoiceField(ModelChoiceField):
    def __init__(self, queryset, **kwargs):
        if queryset is not None:
            queryset = (
                queryset
                .select_related('song')
            )
        super().__init__(queryset, **kwargs)

    def label_from_instance(self, obj) -> str:
        label = f'{obj.song.title}'
        if obj.description:
            label += f' ({obj.description})'
        return f'{label} [{obj.recording_type}]'


class VehicleYearChoiceField(ModelChoiceField):
    def __init__(self, queryset, **kwargs):
        if queryset is not None:
            queryset = (
                queryset
                .select_related('vehicle_trim__vehicle_model__vehicle_make')
                .order_by(
                    '-year',
                    'vehicle_trim__vehicle_model__vehicle_make__name',
                    'vehicle_trim__vehicle_model__name',
                    'vehicle_trim__name'
                )
            )
        super().__init__(queryset, **kwargs)

    def label_from_instance(self, obj) -> str:
        vehicle_year = obj.year
        vehicle_trim = obj.vehicletrim.name
        vehicle_model = obj.vehicletrim.vehiclemodel.name
        vehicle_make = obj.vehicletrim.vehiclemodel.vehiclemake.name
        return f'{vehicle_year} {vehicle_make} {vehicle_model} {vehicle_trim}'
