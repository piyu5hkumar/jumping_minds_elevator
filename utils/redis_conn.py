import redis
from django.conf import settings


class RedisUtils:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.conn = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True,
        )

    def update_redis_for_new_elevators(self, num_elevators=0):
        all_elevators_in_redis = self.conn.lrange("all_available_elevators", 0, -1)

        for elevator_in_redis in all_elevators_in_redis:
            self.conn.delete(elevator_in_redis)
        self.conn.delete("all_available_elevators")

        self.conn.lpush(
            "all_available_elevators",
            *[f"elevator_{index + 1}" for index in range(num_elevators)],
        )

    def add_request_to_elevator(self, elevator_number, requested_floor):
        self.conn.rpush(
            f"elevator_{elevator_number}",
            requested_floor,
        )

    def get_elevators_moves(self, elevator_number):
        return self.conn.lrange(f"elevator_{elevator_number}", 0, -1)

    def move_elevator(self, elevator_number):
        redis_utils.conn.lpop(f"elevator_{elevator_number}")


redis_utils = RedisUtils()
