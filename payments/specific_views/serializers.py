import secrets
from rest_framework import serializers
from events.models import Event
from payments import models


class LuncheonSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Luncheon
        fields = "__all__"


class ExhibitionBootSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ExhibitionBoot
        exclude = ["writer"]


class ParticipantVerification(serializers.Serializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone_no = serializers.CharField(required=True)


class MembersAGMRegistrationSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(
        allow_null=False, required=True, queryset=Event.objects.filter(is_agm=True))
    participant = ParticipantVerification(
        many=True, required=True, allow_empty=False)

    class Meta:
        model = models.MembersAGMRegistration
        fields = "__all__"
        read_only_fields = ["ref", "amount_to_pay"]

    def create(self, validated_data):
        while True:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = models.MembersAGMRegistration.objects.filter(
                ref=ref).exists()
            if not object_with_similar_ref:
                validated_data["ref"] = ref
                break

        luncheon_price = models.Luncheon.objects.get(type="member").price

        no_of_participant = len(validated_data.get("participant", ""))
        validated_data["amount_to_pay"] = no_of_participant * luncheon_price

        agm_registration = models.MembersAGMRegistration.objects.create(
            **validated_data)
        return agm_registration


class ExhibitorsAGMRegistrationSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(
        allow_null=False, required=True, queryset=Event.objects.filter(is_agm=True))
    participant = ParticipantVerification(
        many=True, required=True, allow_empty=False)
    luncheon_covered_participants = serializers.IntegerField(required=True)

    class Meta:
        model = models.ExhibitorsAGMRegistration
        fields = "__all__"
        read_only_fields = ["ref", "amount_to_pay"]

    def create(self, validated_data):
        while True:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = models.ExhibitorsAGMRegistration.objects.filter(
                ref=ref).exists()
            if not object_with_similar_ref:
                validated_data["ref"] = ref
                break

        boot_list = validated_data.get("boot", "")
        luncheon_covered_participants = validated_data.get(
            "luncheon_covered_participants", "")

        luncheon_price = models.Luncheon.objects.get(type="exhibitor").price

        amount_to_pay = int(luncheon_covered_participants) * luncheon_price

        agm_registration = models.ExhibitorsAGMRegistration.objects.create(
            **validated_data)

        agm_registration = models.ExhibitorsAGMRegistration.objects.get(
            ref=agm_registration.ref)

        total_boot_price = 0

        for boot in boot_list:
            boot_instance = models.ExhibitionBoot.objects.get(pk=int(boot))
            if boot_instance.is_occupied == False:
                total_boot_price = total_boot_price + boot_instance.price
                boot_instance.is_occupied = True
                boot_instance.rented_by = agm_registration
                boot_instance.save()

        amount_to_pay = amount_to_pay + total_boot_price

        agm_registration.amount_to_pay = amount_to_pay
        agm_registration.save()

        return agm_registration


class OthersAGMRegistrationSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(
        allow_null=False, required=True, queryset=Event.objects.filter(is_agm=True))

    class Meta:
        model = models.OthersAGMRegistration
        fields = "__all__"
        read_only_fields = ["ref"]

    def create(self, validated_data):
        while True:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = models.OthersAGMRegistration.objects.filter(
                ref=ref).exists()
            if not object_with_similar_ref:
                validated_data["ref"] = ref
                break

        agm_registration = models.OthersAGMRegistration.objects.create(
            **validated_data)
        return agm_registration


class AGMInvitationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AGMInvitation
        fields = "__all__"
        read_only_fields = ["ref"]

    def create(self, validated_data):
        while True:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = models.OthersAGMRegistration.objects.filter(
                ref=ref).exists()
            if not object_with_similar_ref:
                validated_data["ref"] = ref
                break

        invitation = models.AGMInvitation.objects.create(**validated_data)
        return invitation


class AGMInvitationVerificationSerializer(serializers.Serializer):
    ref = serializers.CharField(required=True)


class QuickRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.QuickRegistration
        fields = "__all__"
