from rest_framework import serializers, exceptions
from trainings.models import Training


class TrainingsSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        is_paid = attrs.get("is_paid", "")
        price = attrs.get("price", "")

        if is_paid == True:
            if not price:
                raise exceptions.ValidationError(
                    "price must be provided on paid trainings.")
        elif is_paid == False:
            if price:
                raise exceptions.ValidationError(
                    "price must be provided on free trainings.")

        return super().validate(attrs)
    
    def update(self, instance, validated_data):
        is_paid = validated_data.get('is_paid', instance.is_paid)

        if is_paid == False:
            instance.price = 0.00

        return super().update(instance, validated_data)

    class Meta:
        model = Training
        exclude = ["writer"]
