from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from elevator.models import Elevator, UserRequest
from elevator.serializers import UserRequestSerializer, ElevatorSerializer
from utils.redis_conn import redis_utils
from rest_framework.decorators import action
from elevator.models_choices import ElevatorDirections


class ElevatorViewSet(viewsets.ModelViewSet):
    serializer_class = ElevatorSerializer

    def get_queryset(self):
        # Retrieve active, operational, and non-maintenance elevators
        queryset = Elevator.objects.filter(
            is_active=True, number__gt=0, is_operational=True, is_maintenance=False
        )
        return queryset

    def create(self, request):
        try:
            # Disable all active elevators
            all_active_elevators = Elevator.objects.filter(is_active=True, number__gt=0)
            all_active_elevators.update(is_active=False, number=None)

            num_elevators = int(request.data.get("num_elevators"))
            # Initialize the elevator system with 'num_elevators' elevators
            elevators = [Elevator(number=index + 1) for index in range(num_elevators)]

            Elevator.objects.bulk_create(elevators)
            redis_utils.update_redis_for_new_elevators(num_elevators=num_elevators)
            return Response(
                {"message": f"Successfully created {num_elevators} elevators."},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=["POST"])
    def move_elevator(self, request, pk):
        # Retrieve the specific elevator instance
        elevator_instance = Elevator.objects.filter(
            number=pk, is_active=True, is_maintenance=False, is_operational=True
        ).first()

        if not elevator_instance:
            return Response({"message": "Elevator is not functional"})

        elevator_moves = redis_utils.get_elevators_moves(
            elevator_number=elevator_instance.number
        )

        if elevator_moves:
            next_floor = int(elevator_moves[0])

            current_floor = elevator_instance.current_floor

            # Determine the direction of the elevator
            elevator_instance.direction = (
                ElevatorDirections.UP
                if current_floor < next_floor
                else ElevatorDirections.DOWN
            )

            elevator_instance.is_running = True
            elevator_instance.current_floor = next_floor

            # Update the elevator's movement in Redis
            redis_utils.move_elevator(elevator_number=elevator_instance.number)

            total_moves_left = redis_utils.conn.llen(
                f"elevator_{elevator_instance.number}"
            )

            if not total_moves_left:
                # Set elevator as idle and not running if no more moves are left
                elevator_instance.direction = ElevatorDirections.IDLE
                elevator_instance.is_running = False

            elevator_instance.save()

            return Response(
                {"message": f"Elevator moved to {elevator_instance.current_floor}"}
            )
        return Response({"message": "No moves available"})


class UserRequestViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = UserRequest.objects.all()
    serializer_class = UserRequestSerializer

    def create(self, request, *args, **kwargs):
        # Create a new user request
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_request_instance = serializer.save()
        redis_utils.add_request_to_elevator(
            elevator_number=new_request_instance.elevator.number,
            requested_floor=new_request_instance.floor,
        )
        response_data = self.serializer_class(new_request_instance).data
        return Response(response_data, status=status.HTTP_201_CREATED)
