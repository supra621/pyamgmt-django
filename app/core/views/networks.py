from collections import defaultdict

from django_ccbv.views import TemplateView

from schemaviz import Edge, EdgeColor, Node, VisNetwork, VisOptions

from ..models import (
    MusicAlbumXMusicTag,
    MusicAlbumEditionXSongRecording,
    MusicArtistXSong,
    MusicArtistXSongPerformance,
)
from ..utils import network


class NetworkIndex(TemplateView):
    template_name = 'core/network-index.html'


class MusicNetworkView(TemplateView):
    """Explores several edges of interest.

    Motion Picture <-> Music Album;
    Music Album <-> Music Artist;
    Music Album <-> Person;
    Music Album <-> Video Game;
    Music Artist <-> Person;
    """
    template_name = 'core/network.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        return context


class FilmGamesAndMusicNetworkView(TemplateView):
    template_name = 'core/network.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        vis_data = network.motion_picture_x_person()
        vis_data.extend(network.music_artist_x_person())
        vis_data.extend(network.music_album_x_music_artist())
        vis_data.extend(network.music_album_x_person())
        vis_data.extend(network.music_album_x_video_game())
        vis_data.extend(network.person_x_song())
        vis_data.extend(network.person_x_song_performance())
        vis_data.extend(network.person_x_video_game())
        vis_options = VisOptions(
            nodes=dict(
                font=dict(size=20),
                opacity=0.8,
                shape='dot',
            ),
            physics=dict(
                barnesHut=dict(
                    gravitationalConstant=-30000,
                    springLength=300,
                )
            )
        )
        context.update({
            'vis_data': vis_data.to_json(),
            'vis_options': vis_options.to_dict()
        })
        return context


class MusicArtistNetworkView(TemplateView):
    """Explores edges that relate Music Artists to people.

    Factors out specific albums and songs from display to reduce rendering.
    """
    template_name = 'core/network.html'

    @staticmethod
    def get_music_artist_x_person_edge_kwargs(edge) -> dict:
        dashes = None
        width = 3
        if edge.is_active is False:
            dashes = True
            width = 1
        return {
            'dashes': dashes,
            'width': width
        }

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        vis_data = network.music_artist_x_person(
            edge_kwargs=self.get_music_artist_x_person_edge_kwargs
        )
        vis_data.extend(network.music_album_x_music_artist(
            edge_kwargs={
                'width': 2,
            }
        ))
        vis_data.extend(network.music_album_x_person(
            edge_kwargs={
                'color': EdgeColor(color='66FF66'),
                'length': 600,
            }
        ))
        vis_data.extend(network.person_x_song(
            edge_kwargs={
                'color': EdgeColor(color='2266FF'),
                'length': 600,
            }
        ))
        vis_data.extend(network.person_x_song_performance(
            edge_kwargs={
                'color': EdgeColor(color='6688FF'),
            }
        ))
        vis_options = VisOptions(
            nodes=dict(
                font=dict(size=20),
                opacity=0.8,
                shape='box',
            ),
            physics=dict(
                barnesHut=dict(
                    gravitationalConstant=-30000,
                    springLength=300,
                )
            )
        )
        context.update({
            'vis_data': vis_data.to_json(),
            'vis_options': vis_options.to_dict(),
        })
        return context


class MusicArtistDetailedNetworkView(TemplateView):
    template_name = 'core/music-artist-network.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        vis_data = network.music_artist_x_person()
        album_to_artist_map = defaultdict(list)
        artist_to_song_arrangement_set = set()
        nodes = {}
        edges = []

        vis_data.extend(network.music_album_x_music_artist())

        # Album <-> Song
        # If Artist connects through a song, ignore additional edges
        # later on
        qs = (
            MusicAlbumEditionXSongRecording.objects
            .select_related(
                'music_album_edition__music_album',
                'song_recording__song_performance__song_arrangement',
            )
        )
        for edge in qs:
            music_album = edge.music_album_edition.music_album
            song_arrangement = edge.song_recording.song_performance.song_arrangement
            music_album_key = f'music_album-{music_album.pk}'
            song_arrangement_key = f'song_arrangement-{song_arrangement.pk}'
            if music_album_key not in nodes:
                nodes[music_album_key] = Node(
                    id=music_album_key,
                    label=music_album.title,
                    group='music_album',
                )
            if song_arrangement_key not in nodes:
                nodes[song_arrangement_key] = Node(
                    id=song_arrangement_key,
                    label=song_arrangement.title,
                    group='song',
                )
            edges.append(Edge(
                from_=music_album_key,
                to=song_arrangement_key,
            ))
            # music_artist_key = album_to_artist_map.get(music_album_key, None)
            music_artist_keys = album_to_artist_map.get(music_album_key, [])
            for music_artist_key in music_artist_keys:
                t = music_artist_key, song_arrangement_key
                artist_to_song_arrangement_set.add(t)
        # Artist <-> Song
        qs = (
            MusicArtistXSongPerformance.objects
            .select_related(
                'music_artist', 'song_performance__song_arrangement'
            )
        )
        for edge in qs:
            music_artist = edge.music_artist
            music_artist_node = Node.from_music_artist(music_artist)
            if music_artist_node.id not in nodes:
                nodes[music_artist_node.id] = music_artist_node
            song_arrangement = edge.song_performance.song_arrangement
            song_arrangement_key = f'song_arrangement-{song_arrangement.pk}'
            if song_arrangement_key not in nodes:
                nodes[song_arrangement_key] = Node(
                    id=song_arrangement_key,
                    label=song_arrangement.title,
                    group='song',
                )
            t = music_artist_node.id, song_arrangement_key
            if t not in artist_to_song_arrangement_set:
                edges.append(Edge(
                    from_=music_artist_node.id,
                    to=song_arrangement_key,
                ))
                artist_to_song_arrangement_set.add(t)
        # Artist <-> Song
        qs = (
            MusicArtistXSong.objects
            .select_related('music_artist', 'song')
        )
        for edge in qs:
            music_artist = edge.music_artist
            music_artist_node = Node.from_music_artist(music_artist)
            if music_artist_node.id not in nodes:
                nodes[music_artist_node.id] = music_artist_node
            song = edge.song
            song_node = Node.from_song(song)
            if song_node.id not in nodes:
                nodes[song_node.id] = song_node
            t = music_artist_node.id, song_node.id
            if t not in artist_to_song_arrangement_set:
                edges.append(Edge(
                    from_=music_artist_node.id,
                    to=song_node.id,
                ))
                artist_to_song_arrangement_set.add(t)
        vis_data = VisNetwork(nodes, edges)
        context.update({
            'vis_data': vis_data.to_json(),
        })
        return context


class MusicTagNetworkView(TemplateView):
    template_name = 'core/network.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        qs = (
            MusicAlbumXMusicTag.objects
            .select_related('music_album', 'music_tag')
        )
        nodes = {}
        edges = []
        for edge in qs:
            music_album = edge.music_album
            music_tag = edge.music_tag
            music_album_key = f'music_album-{music_album.pk}'
            music_tag_key = music_tag.name
            if music_album_key not in nodes:
                nodes[music_album_key] = Node(
                    id=music_album_key,
                    label=music_album.title,
                    group='music_album',
                )
            if music_tag_key not in nodes:
                nodes[music_tag_key] = Node(
                    id=music_tag_key,
                    label=music_tag.name,
                    group='music_tag',
                )
            edges.append(Edge(
                from_=music_album_key,
                to=music_tag_key,
            ))
        vis_data = VisNetwork(nodes, edges)
        context.update({
            'vis_data': vis_data.to_json(),
        })
        return context


class PersonRelationView(TemplateView):
    template_name = 'core/network.html'

    @staticmethod
    def get_person_x_person_relation_edge_kwargs(edge) -> dict:
        color = EdgeColor(color='#4488FF')
        width = 3
        length = None
        if edge.relation in edge.Relation.get_sibling_members():
            color = EdgeColor(color='#BB0000')
            width = 2
            length = 600
        return {
            'color': color,
            'length': length,
            'width': width,
        }

    @staticmethod
    def get_person_x_person_relationship_edge_kwargs(edge) -> dict:
        color = EdgeColor(color='#00FF00')
        width = 1
        length = None
        if edge.relationship in edge.Relationship.get_partner_members():
            color = EdgeColor(color='#FF00FF')
            width = 3
            length = None
        return {
            'color': color,
            'width': width,
            'length': length,
        }

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        vis_data = network.person_x_person_relation(
            edge_kwargs=self.get_person_x_person_relation_edge_kwargs)
        vis_data.extend(
            network.person_x_person_relationship(
                edge_kwargs=self.get_person_x_person_relationship_edge_kwargs
            ), duplicate_edges=True)
        context['vis_data'] = vis_data.to_json()
        return context


class SongNetworkView(TemplateView):
    template_name = 'core/network.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        return context
