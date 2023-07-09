from rest_framework import serializers
from elevator.models import Elevator, UserRequest
from utils.redis_conn import redis_utils
from collections import OrderedDict


class ElevatorSerializer(serializers.ModelSerializer):
    """Serializer for Elevator model"""

    def to_representation(self, instance):
        # Remove 'elevator_number' field from representation
        self.fields.pop("elevator_number", None)
        representation_data = super().to_representation(instance)

        # Retrieve user requests associated with the elevator
        instance_user_requests = UserRequestSerializer(
            instance.user_requests.all().order_by("created_at"),
            many=True,
        ).data

        # Retrieve available moves from Redis
        all_available_moves_str = redis_utils.get_elevators_moves(
            elevator_number=instance.number
        )
        all_available_moves = map(int, all_available_moves_str)

        # Categorize user requests as completed or not completed based on available moves
        representation_data["user_request_not_completed"] = []
        representation_data["user_request_completed"] = []

        for instance_user_request in instance_user_requests:
            if instance_user_request["floor"] in all_available_moves:
                representation_data["user_request_not_completed"].append(
                    instance_user_request
                )
            else:
                representation_data["user_request_completed"].append(
                    instance_user_request
                )

        return representation_data

    class Meta:
        model = Elevator
        fields = "__all__"


class UserRequestSerializer(serializers.ModelSerializer):
    """Serializer for UserRequest model"""

    elevator_number = serializers.IntegerField(required=True)

    def to_internal_value(self, data):
        internal_data = super().to_internal_value(data)

        # Remove 'elevator_number' from internal data
        internal_data.pop("elevator_number", None)

        elevator_number = self.initial_data.get("elevator_number")
        if not elevator_number:
            raise serializers.ValidationError(
                {"elevator_number": "elevator_number is required."}
            )

        # Retrieve the elevator instance based on 'elevator_number'
        elevator = Elevator.objects.get(number=elevator_number, is_active=True)
        internal_data["elevator"] = elevator
        return internal_data

    def to_representation(self, instance):
        # Remove 'elevator_number' field from representation
        self.fields.pop("elevator_number", None)
        representation_data = super().to_representation(instance)

        # Set 'elevator_number' as a field in the representation
        representation_data.setdefault("elevator_number", instance.elevator.number)
        representation_data.pop("elevator")
        return representation_data

    class Meta:
        model = UserRequest
        fields = "__all__"
