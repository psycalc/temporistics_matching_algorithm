import unittest

class TestTypologyTemporistics(unittest.TestCase):
    def setUp(self):
        from app import create_app  # Import here to avoid premature Flask context usage
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        # Importing here ensures it's within a context
        from app.typologies.typology_temporistics import TypologyTemporistics
        self.typology = TypologyTemporistics()

    def tearDown(self):
        self.app_context.pop()

    # Your tests here...
