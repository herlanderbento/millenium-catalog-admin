from rest_framework import serializers

from src.core.video.domain.audio_video_media import Rating


class SetField(serializers.ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))

    def to_representation(self, value):
        return list(super().to_representation(value))


class CreateVideoInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=1024)
    launch_year = serializers.IntegerField()
    duration = serializers.DecimalField(max_digits=5, decimal_places=2)
    rating = serializers.ChoiceField(choices=[(r.value, r.name) for r in Rating])
    opened = serializers.BooleanField()
    categories_id = SetField(
        child=serializers.UUIDField(), required=True, allow_empty=True
    )
    genres_id = SetField(child=serializers.UUIDField(), required=True, allow_empty=True)
    cast_members_id = SetField(
        child=serializers.UUIDField(), required=True, allow_empty=True
    )


class GetVideoInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class DeleteVideoInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class UploadVideoInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
