from tank import Direction
from shot import Shot


class Action:
    def __init__(self, tank):
        self.tank = tank

    def __call__(self, *args, **kwargs):
        pass


class Forward(Action):
    def __init__(self, tank):
        super().__init__(tank)

    def __call__(self, *args, **kwargs):
        self.tank.movement(Direction.FORWARD)


class Backward(Action):
    def __init__(self, tank):
        super().__init__(tank)

    def __call__(self, *args, **kwargs):
        self.tank.movement(Direction.BACKWARD)


class Left(Action):
    def __init__(self, tank):
        super().__init__(tank)

    def __call__(self, *args, **kwargs):
        self.tank.movement(Direction.LEFT)


class Right(Action):
    def __init__(self, tank):
        super().__init__(tank)

    def __call__(self, *args, **kwargs):
        self.tank.movement(Direction.RIGHT)


class Aim(Action):
    def __init__(self, tank):
        super().__init__(tank)

    def __call__(self, *args, **kwargs):
        self.tank.aim(*args)


class Fire(Action):
    def __init__(self, tank):
        super().__init__(tank)

    def __call__(self, *args, **kwargs):
        # Check if tank can fire
        self.tank.fire()
        # Create and link new shot
        shot = Shot(self.tank.position, self.tank.orientation)
