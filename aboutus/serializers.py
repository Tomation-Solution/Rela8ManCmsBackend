from aboutus import models
from rest_framework import serializers
from rest_framework import exceptions


class AboutContactUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AboutContactUs
        fields = "__all__"


class AboutHistorySerializer(serializers.ModelSerializer):
    history_paragraphs = serializers.JSONField(required=True)
    core_values = serializers.JSONField(required=True)
    vision = serializers.JSONField(required=True)
    mission = serializers.JSONField(required=True)
    objectives = serializers.JSONField(required=True)
    extras = serializers.JSONField(required=True)

    class Meta:
        model = models.AboutHistory
        exclude = ["writer"]


class AboutAdvocacySerializer(serializers.ModelSerializer):
    main_achievements = serializers.JSONField(required=True)

    class Meta:
        model = models.AboutAdvocacy
        exclude = ["writer"]


class AboutAffilliateSerializer(serializers.ModelSerializer):
    ops = serializers.JSONField(required=True)
    international_partners = serializers.JSONField(required=True)

    class Meta:
        model = models.AboutAffilliate
        exclude = ["writer"]


class AboutHowWeWorkSerializer(serializers.ModelSerializer):
    how_we_work = serializers.JSONField(required=True)
    how_we_work_details = serializers.JSONField(required=True)
    committees = serializers.JSONField(required=True)
    committee_details = serializers.JSONField(required=True)
    adhoc = serializers.JSONField(required=True)
    spvehicles = serializers.JSONField(required=True)
    spgroups = serializers.JSONField(required=True)
    conduct = serializers.JSONField(required=True)
    conduct_listing = serializers.JSONField(required=True)

    class Meta:
        model = models.AboutHowWeWork
        exclude = ["writer"]


class AboutWhereWeOperateSerializer(serializers.ModelSerializer):
    national_secretariat = serializers.CharField(required=True)
    coorprate_office = serializers.CharField(required=True)
    branch_text = serializers.CharField(required=True)

    class Meta:
        model = models.AboutWhereWeOperate
        exclude = ["writer"]


class AboutWhereWeOperateOfficeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=300, required=True)
    email = serializers.JSONField(required=True)
    phone_no = serializers.JSONField(required=True)
    address = serializers.CharField(max_length=300, required=True)
    website = serializers.URLField(required=False)

    class Meta:
        model = models.AboutWhereWeOperateOffice
        exclude = ["writer"]


class AboutWhereWeOperateBranchSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=300, required=True)
    manager_name = serializers.CharField(max_length=300, required=True)
    title = serializers.CharField(max_length=300, required=True)
    email = serializers.JSONField(required=True)
    address = serializers.CharField(max_length=300, required=True)

    class Meta:
        model = models.AboutWhereWeOperateBranch
        exclude = ["writer"]


class AboutOurExecutivesSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    name = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    extra_title1 = serializers.CharField(required=False)
    extra_title2 = serializers.CharField(required=False)
    type = serializers.CharField(required=True)
    tenor = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = models.AboutOurExecutives
        exclude = ["writer"]
