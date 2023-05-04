import secrets
from rest_framework import serializers, exceptions
from payments.models import PublicationPayment, EventTrainingRegistration, AGMRegistration
from publications.models import Publication
from events.models import Event
from trainings.models import Training


class PublicationPaymentSerailzer(serializers.ModelSerializer):
    publication = serializers.PrimaryKeyRelatedField(
        allow_null=False, queryset=Publication.objects.all(), required=True)

    class Meta:
        model = PublicationPayment
        fields = "__all__"
        read_only_fields = ["ref", "amount_to_pay"]

    def create(self, validated_data):
        while True:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = PublicationPayment.objects.filter(
                ref=ref).exists()
            if not object_with_similar_ref:
                validated_data["ref"] = ref
                break

        publication_id = validated_data.get("publication", "")
        amount_to_pay = publication_id.price

        if publication_id:
            validated_data["amount_to_pay"] = amount_to_pay

        paid_publication = PublicationPayment.objects.create(**validated_data)
        return paid_publication


class EventTrainingRegistrationSerializer(serializers.ModelSerializer):
    training = serializers.PrimaryKeyRelatedField(
        allow_null=True, queryset=Training.objects.all(), required=False)
    event = serializers.PrimaryKeyRelatedField(
        allow_null=True, queryset=Event.objects.all(), required=False)

    class Meta:
        model = EventTrainingRegistration
        fields = "__all__"
        read_only_fields = ["ref", "amount_to_pay"]

    def validate(self, attrs):
        type = attrs.get("type", None)
        training = attrs.get("training", None)
        event = attrs.get("event", None)

        if type == "TRAINING":
            if not training:
                raise exceptions.ValidationError(
                    "a valid training must be provided if type is TRAINING")
        elif type == "EVENT":
            if not event:
                raise exceptions.ValidationError(
                    "a valid event must be provided if type is EVENT")

        return super().validate(attrs)

    def create(self, validated_data):
        while True:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = EventTrainingRegistration.objects.filter(
                ref=ref).exists()
            if not object_with_similar_ref:
                validated_data["ref"] = ref
                break

        if validated_data.get("type") == "TRAINING":
            training_id = validated_data.get("training", "")
            is_paid = training_id.is_paid
            amount_to_pay = training_id.price

            if training_id:
                validated_data["amount_to_pay"] = amount_to_pay

        elif validated_data.get("type") == "EVENT":
            event_id = validated_data.get("event", "")
            is_paid = event_id.is_paid
            amount_to_pay = event_id.price

            if event_id:
                validated_data["amount_to_pay"] = amount_to_pay

        if not is_paid:
            validated_data["is_verified"] = True

        registration = EventTrainingRegistration.objects.create(
            **validated_data)

        return registration


class AGMParticipantVerification(serializers.Serializer):
    designation_choices = [
        ("memeber", "memeber"),
        ("exhibitor", "exhibitor"),
        ("exhibitor-participant", "exhibitor-participant"),
        ("guest", "guest"),
        ("media", "media"),
        ("staff", "staff"),
    ]

    name = serializers.CharField(required=True)
    designation = serializers.ChoiceField(
        required=True, choices=designation_choices)
    email = serializers.EmailField(required=True)
    phone_no = serializers.CharField(required=True)


class AGMRegistrationSerailizer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(
        allow_null=False, required=True, queryset=Event.objects.filter(is_agm=True))
    participant_details = AGMParticipantVerification(
        many=True, required=True, allow_empty=False)

    class Meta:
        model = AGMRegistration
        fields = "__all__"
        read_only_fields = ["ref", "amount_to_pay"]

    def create(self, validated_data):
        while True:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = AGMRegistration.objects.filter(
                ref=ref).exists()
            if not object_with_similar_ref:
                validated_data["ref"] = ref
                break

        event_price = validated_data.get("event", "").price
        validated_data["amount_to_pay"] = event_price

        agm_registration = AGMRegistration.objects.create(**validated_data)
        return agm_registration
