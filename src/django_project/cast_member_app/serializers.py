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


class ListCastMembersOutputSerializer(serializers.Serializer):
    data = CastMemberOutputSerializer(many=True)


class UpdateCastMemberInputSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    name = serializers.CharField(required=True)
    type = CastMemberTypeField(required=True)


class UpdateCastMemberOutputSerializer(serializers.Serializer):
    data = CastMemberOutputSerializer(source="*")


class DeleteCastMemberInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
