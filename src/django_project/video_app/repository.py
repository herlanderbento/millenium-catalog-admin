from typing import List, Set
import uuid

from django.core.paginator import Paginator
from django.db import models

from src.core._shared.domain.search_params import SortDirection
from src.core._shared.domain.exceptions import NotFoundException
from src.core.video.domain.video import Video, VideoId
from src.core.video.domain.video_repository import (
    IVideoRepository,
    VideoSearchParams,
    VideoSearchResult,
)

from src.django_project.video_app.mappers import VideoModelMapper
from src.django_project.video_app.models import AudioVideoMediaModel, VideoModel
from src.django_project.category_app.models import CategoryModel
from src.django_project.cast_member_app.models import CastMemberModel
from src.django_project.genre_app.models import GenreModel


class VideoDjangoRepository(IVideoRepository):
    sortable_fields: List[str] = ["title", "created_at"]

    def insert(self, entity: Video) -> None:
        model, relations = VideoModelMapper.to_model(entity)
        model.save()

        model.categories.set(relations.categories_ids)
        model.genres.set(relations.genres_ids)
        model.cast_members.set(relations.cast_members_ids)

    def bulk_insert(self, entities: List[Video]) -> None:
        VideoModel.objects.bulk_create(list(map(VideoModelMapper.to_model, entities)))

    def find_by_id(self, entity_id: VideoId) -> Video | None:
        model = VideoModel.objects.filter(id=entity_id).first()
        return VideoModelMapper.to_entity(model) if model else None

    def find_by_ids(self, entity_ids: Set[VideoId]) -> List[Video]:
        models = VideoModel.objects.filter(
            id__in=[str(video_id) for video_id in entity_ids]
        )
        return [VideoModelMapper.to_entity(model) for model in models]

    def find_all(self) -> List[Video]:
        models = VideoModel.objects.all()
        return [VideoModelMapper.to_entity(model) for model in models]

    def update(self, entity: Video) -> None:
        model = VideoModel.objects.filter(pk=entity.id.value).update(
            title=entity.title,
            description=entity.description,
            launch_year=entity.launch_year,
            duration=entity.duration,
            rating=entity.rating,
            opened=entity.opened,
            published=entity.published,
            created_at=entity.created_at,
        )

        if not model:
            raise NotFoundException(entity.id.value, self.get_entity())

        AudioVideoMediaModel.objects.filter(id=model.video_id).delete()

        model.video = (
            AudioVideoMediaModel.objects.create(
                name=entity.video.name,
                raw_location=entity.video.raw_location,
                encoded_location=entity.video.encoded_location,
                status=entity.video.status,
            )
            if entity.video
            else None
        )

        categories_set = VideoModel.objects.get(pk=entity.id.value).categories
        categories_set.clear()
        categories_set.add(
            *[category_id.value for category_id in entity.categories_id],
        )

        genres_set = VideoModel.objects.get(pk=entity.id.value).genres
        genres_set.clear()
        genres_set.add(
            *[genre_id.value for genre_id in entity.genres_id],
        )

        cast_members_set = VideoModel.objects.get(pk=entity.id.value).cast_members
        cast_members_set.clear()
        cast_members_set.add(
            *[cast_member_id.value for cast_member_id in entity.cast_members_id],
        )

    def delete(self, entity_id: VideoId) -> None:
        VideoModel.objects.filter(id=entity_id).delete()

    def search(self, props: VideoSearchParams) -> VideoSearchResult:
        query = (
            VideoModel.objects.all()
            .distinct()
            .prefetch_related(
                self._prefetch_categories(),
                self._prefetch_genres(),
                self._prefetch_cast_members(),
            )
        )

        if props.filter:
            if props.filter.title:
                query = query.filter(title__icontains=props.filter.title)

            if props.filter.categories_id:
                query = query.filter(
                    categories__id__in=self._filter_valid_uuids(
                        props.filter.categories_id
                    )
                )

            if props.filter.genres_id:
                query = query.filter(
                    genres__id__in=self._filter_valid_uuids(props.filter.genres_id),
                )
            if props.filter.cast_members_id:
                query = query.filter(
                    cast_members__id__in=self._filter_valid_uuids(
                        props.filter.cast_members_id
                    )
                )

        if props.sort and props.sort in self.sortable_fields:
            if props.sort_dir == SortDirection.DESC:
                props.sort = f"-{props.sort}"
            query = query.order_by(props.sort)
        else:
            query = query.order_by("-created_at")

        paginator = Paginator(query, props.per_page)

        if props.page <= paginator.num_pages:
            page_obj = paginator.page(props.page)
        else:
            page_obj = paginator.page(paginator.num_pages)
            page_obj.object_list = []

        return VideoSearchResult(
            items=[VideoModelMapper.to_entity(model) for model in page_obj.object_list],
            total=paginator.count,
            current_page=props.page,
            per_page=props.per_page,
        )

    def get_entity(self) -> Video:
        return Video

    def _prefetch_categories(self):
        return models.Prefetch("categories", queryset=CategoryModel.objects.only("id"))

    def _prefetch_genres(self):
        return models.Prefetch("genres", queryset=GenreModel.objects.only("id"))

    def _prefetch_cast_members(self):
        return models.Prefetch(
            "cast_members", queryset=CastMemberModel.objects.only("id")
        )

    def _filter_valid_uuids(self, entity_ids: List[str]) -> List[str]:
        if isinstance(entity_ids, str):
            entity_ids = [entity_ids]

        valid_uuids = []
        for entity_id in entity_ids:
            try:
                uuid_obj = uuid.UUID(entity_id)
                valid_uuids.append(str(uuid_obj))
            except ValueError:
                print(f"Invalid UUID encountered: {entity_id}")
                continue
        return valid_uuids
