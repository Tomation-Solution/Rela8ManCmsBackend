from rest_framework import serializers, exceptions
from events.models import Event


class EventsSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False)

    def validate(self, attrs):
        is_paid = attrs.get("is_paid", "")
        price = attrs.get("price", "")

        if is_paid == True:
            if not price:
                raise exceptions.ValidationError(
                    "price must be provided on paid events.")
        elif is_paid == False:
            if price:
                raise exceptions.ValidationError(
                    "price must not be provided on free events.")

        return super().validate(attrs)

    def update(self, instance, validated_data):
        is_paid = validated_data.get('is_paid', instance.is_paid)

        if is_paid == False:
            instance.price = 0.00

        return super().update(instance, validated_data)

    class Meta:
        model = Event
        exclude = ["writer"]
