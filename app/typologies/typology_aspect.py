class TypologyAspect:
    def __init__(self, aspect_name: str, position: int):
        self.aspect_name = aspect_name
        self.position = position

    def __str__(self):
        return self.aspect_name

    def __repr__(self):
        return f"TypologyAspect({self.aspect_name!r}, {self.position})"
