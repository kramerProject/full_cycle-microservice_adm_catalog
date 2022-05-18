
from dataclasses import FrozenInstanceError, dataclass, is_dataclass
from abc import ABC
import unittest
from unittest.mock import patch
from __seedwork.domain import value_objects
from __seedwork.domain.value_objects import UniqueEntityId, ValueObject
from __seedwork.domain.exceptions import InvalidUuidException
import uuid

@dataclass(frozen=True)
class StubOneProp(ValueObject):
    prop: str

@dataclass(frozen=True)
class StubTwoProps(ValueObject):
    prop1: str
    prop2: str

class TestValueObjectUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(ValueObject))

    
    def test_if_is_abstract_class(self):
        self.assertIsInstance(ValueObject(), ABC)

    def test_init_prop(self):
        vo1 = StubOneProp(prop='value')
        self.assertEqual(vo1.prop, 'value')

        vo2 = StubTwoProps(prop1='value1', prop2='value2')
        self.assertEqual(vo2.prop1, 'value1')
        self.assertEqual(vo2.prop2, 'value2')

    def test_should_convert_to_string(self):
        vo1 = StubOneProp(prop='value')
        self.assertEqual(vo1.prop, str(vo1))

        vo2 = StubTwoProps(prop1='value1', prop2='value2')
        self.assertEqual('{"prop1": "value1", "prop2": "value2"}', str(vo2))

    def test_if_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = StubOneProp(prop="value")
            value_object.id = "Fake id"
class TestUniqueEntityIdUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(UniqueEntityId))

    def test_throw_exception_when_uuid_is_invalid(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:
            with self.assertRaises(InvalidUuidException) as assert_error:
                UniqueEntityId("Fake id")
            mock_validate.assert_called_once()
            self.assertEqual(assert_error.exception.args[0], 'ID must be a valid uuid')

    def test_accept_uuid_passed_in_contructor(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:
            value_object = UniqueEntityId('bb0e392e-dc7b-4d13-a22a-3dd6b9d1caf5')
            mock_validate.assert_called_once()
            self.assertEqual(value_object.id, 'bb0e392e-dc7b-4d13-a22a-3dd6b9d1caf5')
        
        uuid_value = uuid.uuid4()
        value_object = UniqueEntityId(uuid_value)
        self.assertEqual(value_object.id, str(uuid_value))

    def test_generate_id_when_not_passed_id_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:
            value_object = UniqueEntityId()
            uuid.UUID(value_object.id)
            mock_validate.assert_called_once()

    def test_if_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = UniqueEntityId()
            value_object.id = "Fake id"
