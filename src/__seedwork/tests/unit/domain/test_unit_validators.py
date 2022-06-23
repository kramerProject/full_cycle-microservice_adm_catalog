

import unittest
from __seedwork.domain.validators import ValidatorRules
from __seedwork.domain.exceptions import ValidationException
from __seedwork.domain.validators import ValidatorFieldsInterface
from dataclasses import fields


class TestValidators(unittest.TestCase):

    def test_values_method(self):
        validator = ValidatorRules.values('some value', 'prop 1')
        self.assertIsInstance(validator, ValidatorRules)
        self.assertEqual(validator.value, 'some value')
        self.assertEqual(validator.prop, 'prop 1')

    def test_required_rule(self):
        invalid_data = [
            {'value': None, 'prop': 'prop'},
            {'value': "", 'prop': 'prop2'},
        ]
        for data in invalid_data:
            msg = f'value: {data["value"]}, prop: {data["prop"]}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                ValidatorRules.values(data['value'], data['prop']).required()

            self.assertEqual(
                f'Field {data["prop"]} is required',
                assert_error.exception.args[0]
            )
        valid_data = [
            {'value': 'test', 'prop': 'prop1'},
            {'value': 5, 'prop': 'prop2'},
            {'value': 0, 'prop': 'prop3'},
            {'value': False, 'prop': 'prop4'}
        ]
        for data in valid_data:
            self.assertIsInstance(
                ValidatorRules.values(data['value'], data['prop']).required(),
                ValidatorRules
            )

    def test_string(self):
        
        invalid_data = [
            {'value': 5, 'prop': 'prop'},
            {'value': True, 'prop': 'prop2'},
            {'value': {}, 'prop': 'prop2'},
        ]
        for data in invalid_data:
            with self.assertRaises(ValidationException) as assert_error:
                ValidatorRules.values(data['value'], data['prop']).string()

            self.assertEqual(
                    f'Field {data["prop"]} must be a string',
                    assert_error.exception.args[0]
            )

        valid_data = [
            {'value': None, 'prop': 'prop'},
            {'value': "", 'prop': 'prop2'},
            {'value': 'some value', 'prop': 'prop2'}
        ]

        for data in valid_data:
            self.assertIsInstance(
                ValidatorRules.values(data['value'], data['prop']).string(),
                ValidatorRules
            )

    def test_max_length_rule(self):
        
        invalid_data = [
            {'value': 5 * "t", 'prop': 'prop'}
        ]
        for data in invalid_data:
            with self.assertRaises(ValidationException) as assert_error:
                ValidatorRules.values(data['value'], data['prop']).max_length(4)

            self.assertEqual(
                    f'Field {data["prop"]} length should be smaller than 4',
                    assert_error.exception.args[0]
            )

        valid_data = [
            {'value': None, 'prop': 'prop'},
            {'value': "t" * 5, 'prop': 'prop2'}
        ]

        for data in valid_data:
            self.assertIsInstance(
                ValidatorRules.values(data['value'], data['prop']).max_length(5),
                ValidatorRules
            )

    def test_boolean_rule(self):
        
        invalid_data = [
            {'value': "not bool", 'prop': 'prop'},
            {'value': "", 'prop': 'prop'}
        ]
        for data in invalid_data:
            with self.assertRaises(ValidationException) as assert_error:
                ValidatorRules.values(data['value'], data['prop']).boolean()

            self.assertEqual(
                    f'The {data["prop"]} must be a bool value',
                    assert_error.exception.args[0]
            )

        valid_data = [
            {'value': None, 'prop': 'prop'},
            {'value': True, 'prop': 'prop2'},
            {'value': False, 'prop': 'prop2'}
        ]

        for data in valid_data:
            self.assertIsInstance(
                ValidatorRules.values(data['value'], data['prop']).boolean(),
                ValidatorRules
            )


    def test_should_throw_error_when_combining_two_or_more_rules(self):
        with self.assertRaises(ValidationException) as assert_error:
                ValidatorRules.values("", "prop").required().string()

        self.assertEqual(
                'Field prop is required',
                assert_error.exception.args[0]
        )

        with self.assertRaises(ValidationException) as assert_error:
                ValidatorRules.values("Not bool", "prop").required().boolean()

        self.assertEqual(
                'The prop must be a bool value',
                assert_error.exception.args[0]
        )

        with self.assertRaises(ValidationException) as assert_error:
                ValidatorRules.values(5, "prop").required().string()

        self.assertEqual(
                'Field prop must be a string',
                assert_error.exception.args[0]
        )

        with self.assertRaises(ValidationException) as assert_error:
                ValidatorRules.values(6 * "T", "prop").required().string().max_length(5)

        self.assertEqual(
                'Field prop length should be smaller than 5',
                assert_error.exception.args[0]
        )

    def test_should_be_valid_when_combined(self):
        ValidatorRules("string", "prop").required().string()
        ValidatorRules(False, "prop").required().boolean()
        ValidatorRules("ttt", "prop").required().string().max_length(3)
        self.assertTrue(True)



class TestValidatorFieldsInterfaceUnit(unittest.TestCase):
    
    def test_throw_error_when_validate_method_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            ValidatorFieldsInterface()  # pylint: disable=abstract-class-instantiated
        self.assertEqual(
            assert_error.exception.args[0],
            "Can't instantiate abstract class ValidatorFieldsInterface " +
            "with abstract method validate"
        )

    def test_qualquer(self):
        fields_class = fields(ValidatorFieldsInterface)
        errors_field = fields_class[0]
        self.assertEqual(errors_field.name, 'errors')
        self.assertIsNone(errors_field.default)

        validated_data_field = fields_class[1]
        self.assertEqual(validated_data_field.name, 'validated_data')
        self.assertIsNone(validated_data_field.default)