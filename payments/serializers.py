# import secrets
# from rest_framework import serializers, exceptions
# from payments.models import PublicationPayment, EventTrainingRegistration
# from publications.models import Publication
# from events.models import Event
# from trainings.models import Training


# class PublicationPaymentSerailzer(serializers.ModelSerializer):
#     publication = serializers.PrimaryKeyRelatedField(
#         allow_null=False, queryset=Publication.objects.filter(is_paid=True), required=True)

#     class Meta:
#         model = PublicationPayment
#         fields = "__all__"
#         read_only_fields = ["ref", "amount_to_pay"]

#     def create(self, validated_data):
#         while True:
#             ref = secrets.token_urlsafe(20)
#             object_with_similar_ref = PublicationPayment.objects.filter(
#                 ref=ref).exists()
#             if not object_with_similar_ref:
#                 validated_data["ref"] = ref
#                 break

#         publication_id = validated_data.get("publication", "")
#         amount_to_pay = publication_id.price

#         if publication_id:
#             validated_data["amount_to_pay"] = amount_to_pay

#         paid_publication = PublicationPayment.objects.create(**validated_data)
#         return paid_publication


# class EventTrainingRegistrationSerializer(serializers.ModelSerializer):
#     training = serializers.PrimaryKeyRelatedField(
#         allow_null=True, queryset=Training.objects.all(), required=False)
#     event = serializers.PrimaryKeyRelatedField(
#         allow_null=True, queryset=Event.objects.all(), required=False)

#     class Meta:
#         model = EventTrainingRegistration
#         fields = "__all__"
#         read_only_fields = ["ref", "amount_to_pay"]

#     def validate(self, attrs):
#         type = attrs.get("type", None)
#         training = attrs.get("training", None)
#         event = attrs.get("event", None)

#         if type == "TRAINING":
#             if not training:
#                 raise exceptions.ValidationError(
#                     "a valid training must be provided if type is TRAINING")
#         elif type == "EVENT":
#             if not event:
#                 raise exceptions.ValidationError(
#                     "a valid event must be provided if type is EVENT")

#         return super().validate(attrs)

#     def create(self, validated_data):
#         while True:
#             ref = secrets.token_urlsafe(20)
#             object_with_similar_ref = EventTrainingRegistration.objects.filter(
#                 ref=ref).exists()
#             if not object_with_similar_ref:
#                 validated_data["ref"] = ref
#                 break

#         if validated_data.get("type") == "TRAINING":
#             training_id = validated_data.get("training", "")
#             is_paid = training_id.is_paid
#             amount_to_pay = training_id.price

#             if training_id:
#                 validated_data["amount_to_pay"] = amount_to_pay

#         elif validated_data.get("type") == "EVENT":
#             event_id = validated_data.get("event", "")
#             is_paid = event_id.is_paid
#             amount_to_pay = event_id.price

#             if event_id:
#                 validated_data["amount_to_pay"] = amount_to_pay

#         if not is_paid:
#             validated_data["is_verified"] = True

#         registration = EventTrainingRegistration.objects.create(
#             **validated_data)

#         return registration

from rest_framework import serializers

from events.models import Event
from trainings.models import Training
from .models import PublicationPayment, EventTrainingRegistration, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "payment_ref",
            "amount",
            "payment_method",
            "access_code",
            "status",
            "created_at",
            "updated_at",
        ]


class PublicationPaymentSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer()  # Nested payment serializer

    class Meta:
        model = PublicationPayment
        fields = [
            "payment",  # This will return all the details from the Payment model
            "publication",  # Assuming this field is needed, it wasn't included in the example serializer
            "fullname",
            "email",
            "phone_number",
            "company_name",
            "amount_to_pay",
            "is_verified",
            "file_received",
            "created_at",
            "updated_at",
        ]

    def get_payment_method(self, instance):
        # Safely access payment method
        payment = instance.payment
        return getattr(payment, "payment_method", None) if payment else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation


class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = [
            "id",
            "name",
            "training_type",
            "group_type",
            "location",
            "start_date",
            "end_date",
            "is_paid",
            "price",
            "image",
        ]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "is_agm",
            "group_type",
            "location",
            "start_date",
            "end_date",
            "is_paid",
            "price",
            "image",
        ]


class EventTrainingRegistrationSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer()
    training = TrainingSerializer()
    event = EventSerializer()

    class Meta:
        model = EventTrainingRegistration
        fields = [
            "payment",
            "fullname",
            "email",
            "phone_number",
            "company_name",
            "event_type",
            "training",
            "event",
            "amount_to_pay",
            "is_verified",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Optional: You can clean up null values if you like
        if not instance.training:
            representation.pop("training")
        if not instance.event:
            representation.pop("event")
        return representation

    def get_payment_method(self, instance):
        # Safely access payment method
        payment = instance.payment
        return getattr(payment, "payment_method", None) if payment else None
