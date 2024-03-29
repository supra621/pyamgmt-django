from django.db.models import (
    CharField, DateField, ForeignKey,
    CASCADE, PROTECT, SET_NULL, UniqueConstraint, ManyToManyField, PositiveSmallIntegerField, TextField,
)

from django_base.models import BaseAuditable
from django_base.validators import (
    validate_date_not_future,
    validate_year_not_future
)
from django_base.utils import default_related_names

from . import _enums


class VideoGame(BaseAuditable):
    """
    developer(s) - person or company or other entity
    genre(s)
    language?
    platform: PC, PS4, NES, SNES - not mutually exclusive; m2m
    publisher(s) - usually a company, but could be independently published
    release date - different per platform, port, region, or market (part of m2m)
    tag(s)? Something looser than genre, though not required.
    title

    Could also relate to people:
        voice acting, developers, directors, composers, producers
    Relates to music via soundtracks (songs vs albums is debatable, like movies)
    Like, an "unofficial" OST is kind of an issue for copyright, but not every
    game was published alongside an OST
    Not every game is regionalized right? NTSC / PAL / JP was common for
    consoles. Region # is a thing for media.

    Video Games also are released under different editions.
    Sometimes editions are just bundles that include add-ons.
    Editions should not be used for remakes or remasters.
    """

    title = CharField(max_length=100)
    # developer = ForeignKey(
    #     'VideoGameDeveloper', on_delete=CASCADE,
    #     null=True, blank=True,
    #     **default_related_names(__qualname__)
    # )
    disambiguator = CharField(max_length=255, blank=True)
    series = ForeignKey(
        'VideoGameSeries', on_delete=SET_NULL,
        null=True, blank=True,
        **default_related_names(__qualname__)
    )
    year_first_published = PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[validate_year_not_future]
    )
    notes = TextField(blank=True)
    music_albums = ManyToManyField(
        'MusicAlbum', through='MusicAlbumXVideoGame',
        related_name='+', blank=True,
    )
    personnel = ManyToManyField(
        'Person', through='PersonXVideoGame',
        related_name='+', blank=True,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('title', 'disambiguator'),
                name='unique_video_game',
            )
        ]

    def __str__(self) -> str:
        return self.title


class VideoGameAddon(BaseAuditable):
    """DLC, Expansion pack, or other additional components that are optional.

    """
    # release date
    # type, such as DLC, expansion, addon, content, in-game something
    # (or tags may be appropriate)
    name = CharField(max_length=100)
    release_date = DateField(
        null=True, blank=True,
        validators=[validate_date_not_future]
    )
    video_game = ForeignKey(
        VideoGame, on_delete=PROTECT,
        **default_related_names(__qualname__)
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('name', 'video_game'),
                name='unique_video_game_addon',
            )
        ]

    def __str__(self) -> str:
        return self.name


class VideoGameDeveloper(BaseAuditable):
    name = CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class VideoGameEdition(BaseAuditable):
    """Deluxe, Supporters, Limited, etc.

    Some games that were released cross-platform have platform-specific content,
    like Soul Calibur and Terraria. These should be their own edition, e.g.,
    "Terraria PC Edition".
    """

    name = CharField(max_length=100)
    release_date = DateField(
        null=True, blank=True,
        validators=[validate_date_not_future]
    )
    video_game = ForeignKey(
        VideoGame, on_delete=PROTECT,
        **default_related_names(__qualname__)
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('name', 'video_game'),
                name='unique_video_game_edition',
            )
        ]

    def __str__(self) -> str:
        return self.name


class VideoGamePlatform(BaseAuditable):
    """
    May also be a commodity, asset, or catalog item, but keep
    this abstracted from the physical consoles or assemblies
    """

    name = CharField(max_length=31, unique=True)
    short_name = CharField(max_length=15, blank=True)

    def __str__(self) -> str:
        return self.name


class VideoGamePlatformEdition(BaseAuditable):
    name = CharField(max_length=31)
    video_game_platform = ForeignKey(
        VideoGamePlatform, on_delete=CASCADE,
        **default_related_names(__qualname__)
    )

    def __str__(self):
        return self.name


class VideoGamePlatformRegion(BaseAuditable):
    Region = _enums.Region

    region = CharField(
        max_length=2, choices=Region.choices,
        blank=True, default=''
    )
    release_date = DateField(
        null=True, blank=True,
        validators=[validate_date_not_future]
    )
    video_game_platform = ForeignKey(
        VideoGamePlatform, on_delete=CASCADE,
        **default_related_names(__qualname__)
    )


class VideoGameRole(BaseAuditable):
    """Credits to personnel."""

    name = CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class VideoGameSeries(BaseAuditable):
    """A grouping of related video games."""

    name = CharField(max_length=63, unique=True)
    parent_series = ForeignKey(
        'self', on_delete=SET_NULL,
        null=True, blank=True,
        related_name='sub_series',
    )

    class Meta:
        verbose_name_plural = 'video game series'

    def __str__(self) -> str:
        return self.name


class VideoGameXVideoGamePlatform:
    """
    This gets closer to the catalog item.

    Example:
        "I bought a [copy] of [game] on [platform]
        "I bought a [key] for [World of Final Fantasy] on [Steam/PC]
        "I bought a [blu-ray] of [World of Final Fantasy] on [PS4]

    TODO 2023-12-12: Console games were regionalized for PAL/NTSC
    """

    release_date = DateField(
        null=True, blank=True,
        validators=[validate_date_not_future]
    )
    video_game = ForeignKey(
        VideoGame, on_delete=PROTECT,
        **default_related_names(__qualname__)
    )
    video_game_platform = ForeignKey(
        VideoGamePlatform, on_delete=PROTECT,
        **default_related_names(__qualname__)
    )


class VideoGameEditionXVideoGamePlatform(BaseAuditable):
    video_game_edition = ForeignKey(
        VideoGameEdition, on_delete=PROTECT,
        **default_related_names(__qualname__)
    )
    video_game_platform = ForeignKey(
        VideoGamePlatform, on_delete=PROTECT,
        **default_related_names(__qualname__)
    )
    release_date = DateField(
        null=True, blank=True,
        validators=[validate_date_not_future]
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('video_game_edition', 'video_game_platform'),
                name='unique_video_game_edition_x_video_game_platform'
            )
        ]
