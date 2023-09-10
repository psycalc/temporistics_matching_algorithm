class TypologyAspect:
    def __init__(self, aspect_name: str, position: int):
        """
        Initializes a new instance of the TypologyAspect class.

        :param aspect_name: The name of the aspect.
        :param position: The position of the aspect in the typology.
        """
        self.aspect_name = aspect_name
        self.position = position

    def __str__(self):
        """
        Returns a string representation of the TypologyAspect instance.

        :return: A string representation of the TypologyAspect instance.
        """
        return self.aspect_name

    def __repr__(self):
        """
        Returns a string representation of the TypologyAspect instance.

        :return: A string representation of the TypologyAspect instance.
        """
        return f"TypologyAspect({self.aspect_name!r}, {self.position})"
