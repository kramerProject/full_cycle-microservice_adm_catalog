from dataclasses import FrozenInstanceError, is_dataclass
from datetime import date, datetime
import unittest
from category.domain.entities import Category


class TestCategoryUnit(unittest.TestCase):

    def test_if_is_dataclass(self):
        self.assertTrue(is_dataclass(Category))

        
    def test_constructor(self):
        category = Category(name="Movie")
        self.assertEqual(category.name,  "Movie")
        self.assertEqual(category.description, None)
        self.assertTrue(category.is_active)
        self.assertIsInstance(category.created_at, datetime)

        created_at = datetime.now()
        category = Category(
            name="Movie",
            description="some other description",
            is_active=False, 
            created_at=created_at
        )
        self.assertEqual(category.name,  "Movie")
        self.assertEqual(category.description, "some other description")
        self.assertFalse(category.is_active)
        self.assertIsInstance(category.created_at, datetime)

    def test_if_created_is_generated_in_constructor(self):
        category_1 = Category(name="Movie 1")
        category_2 = Category(name="Movie 2")
        self.assertNotEqual(
            category_1.created_at.timestamp(),
            category_2.created_at.timestamp()
        )

    def test_if_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = Category(name='Test')
            value_object.name = "Another name"