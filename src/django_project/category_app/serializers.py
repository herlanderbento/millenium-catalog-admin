from rest_framework import serializers


class CreateCategoryInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(
        max_length=255, required=False, allow_blank=True, allow_null=False
    )
    is_active = serializers.BooleanField(default=True)


class GetCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateCategoryInputSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(
        required=True, allow_blank=True, allow_null=False
    )
    is_active = serializers.BooleanField(required=True)


class DeleteCategoryInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
