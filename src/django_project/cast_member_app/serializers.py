from rest_framework import serializers
from src.core.cast_member.domain.cast_member_type import CastMemberType


class CastMemberTypeField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        choices = [(type.name, type.value) for type in CastMemberType]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        return CastMemberType(super().to_internal_value(data))

    def to_representation(self, value):
        return str(super().to_representation(value))


class CastMemberOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    type = CastMemberTypeField(required=True)
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return obj.created_at.isoformat()


class CreateCastMemberInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    type = CastMemberTypeField(required=True)


class CreateCastMemberOutputSerializer(serializers.Serializer):
    data = CastMemberOutputSerializer(source="*")


class GetCastMemberInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class GetCastMemberOutputSerializer(serializers.Serializer):
    data = CastMemberOutputSerializer(source="*")


class ListCastMembersInputSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, allow_null=True)
    per_page = serializers.IntegerField(required=False, allow_null=True)
    sort = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    sort_dir = serializers.ChoiceField(
        choices=["asc", "desc"], required=False, allow_null=True
    )
    filter = serializers.JSONField(required=False, allow_null=True)


class ListCastMembersMetaSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()

class ListCastMembersOutputSerializer(serializers.Serializer):
    items = CastMemberOutputSerializer(many=True)  # Renomeado para 'data'
    meta = ListCastMembersMetaSerializer()  


class UpdateCastMemberInputSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    name = serializers.CharField(required=True)
    type = CastMemberTypeField(required=True)


class UpdateCastMemberOutputSerializer(serializers.Serializer):
    data = CastMemberOutputSerializer(source="*")


class DeleteCastMemberInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
