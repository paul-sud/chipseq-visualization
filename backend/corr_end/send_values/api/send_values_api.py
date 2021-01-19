from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from ..models import Correlations, Link, Researcher


class ResearcherSerializer(ModelSerializer):
    class Meta:
        model = Researcher
        fields = ["name", "institution", "link"]

    def validate(self, user_data):
        if not (user_data["name"]):
            print("One or more of the fields is missing.")
            return ValidationError
        return user_data

    def create(self, user_data):
        new_researcher = Researcher.objects.create(**user_data)
        new_researcher.save()
        return new_researcher

    def update(self, existing_researcher, user_data):
        fields = ["name", "institution", "link"]
        for i in fields:
            field_value = user_data.get(i, getattr(existing_researcher, i))
            setattr(existing_researcher, i, field_value)
        existing_researcher.save()
        return existing_researcher


class LinkSerializer(ModelSerializer):
    """
    Parent Model is Link, Child Model is Researcher
    """

    researchers = ResearcherSerializer(many=True, read_only=True)

    class Meta:
        model = Link
        fields = ["encode_url", "submitted_by", "researchers"]

    def validate(self, user_data):
        if not (user_data["encode_url"]):
            print("One or more of the fields is missing.")
            return ValidationError
        return user_data

    def create(self, user_data):
        new_link = Link.objects.create(**user_data)
        new_link.save()
        return new_link

    def update(self, existing_link, user_data):
        fields = ["encode_url", "submitted_by"]
        for i in fields:
            field_value = user_data.get(i, getattr(existing_link, i))
            setattr(existing_link, i, field_value)
        existing_link.save()
        return existing_link


class CorrelationsSerializer(ModelSerializer):
    class Meta:
        model = Correlations
        fields = [
            "experiment_name",
            "row_num",
            "col_num",
            "row_label",
            "col_label",
            "corr_value",
        ]

    def validate(self, user_data):
        if not (
            user_data["experiment_name"]
            or user_data["row_num"]
            or user_data["col_num"]
            or user_data["row_label"]
            or user_data["col_label"]
            or user_data["corr_value"]
        ):
            print("One or more of the fields is missing.")
            return ValidationError
        return user_data

    def create(self, user_data):
        new_correlation = Correlations.objects.create(**user_data)
        new_correlation.save()
        return new_correlation

    def update(self, existing_correlation, user_data):
        fields = [
            "experiment_name",
            "row_num",
            "col_num",
            "row_label",
            "col_label",
            "corr_value",
        ]
        for i in fields:
            field_value = user_data.get(i, getattr(existing_correlation, i))
            setattr(existing_correlation, i, field_value)
        existing_correlation.save()
        return existing_correlation


class LinksViewSet(ModelViewSet):
    serializer_class = LinkSerializer
    http_method_names = ["get", "post", "put", "delete", "options"]
    queryset = Link.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ["encode_url", "submitted_by"]


class ResearcherViewSet(ModelViewSet):
    serializer_class = ResearcherSerializer
    http_method_names = ["get", "post", "put", "delete", "options"]
    queryset = Researcher.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ["name", "institution", "link"]


class CorrelationsViewSet(ModelViewSet):
    serializer_class = CorrelationsSerializer
    http_method_names = ["get", "post", "put", "delete", "options"]
    queryset = Correlations.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("experiment_name", "row_label", "col_label", "corr_value")
