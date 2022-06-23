
from abc import ABC
import abc
from dataclasses import dataclass
from typing import Any, Dict, Generic, List, TypeVar

from .exceptions import ValidationException

@dataclass(frozen=True, slots=True)
class ValidatorRules:
    value: Any
    prop: str

    @staticmethod
    def values(value: Any, prop: str):
        return ValidatorRules(value, prop)

    def required(self) -> 'ValidatorRules':
        if self.value is None or self.value == "":
            raise ValidationException(f'Field {self.prop} is required')
        return self

    def string(self) -> 'ValidatorRules':
        if self.value is not None and not isinstance(self.value, str):
            raise ValidationException(f'Field {self.prop} must be a string')
        return self

    def max_length(self, max_len: int) -> 'ValidatorRules':
        if self.value is not None and len(self.value) > max_len:
            raise ValidationException(f'Field {self.prop} length should be smaller than {max_len}')
        return self

    def boolean(self) -> 'ValidatorRules':
        if self.value is not None and not isinstance(self.value, bool):
            raise ValidationException(f'The {self.prop} must be a bool value')
        return self


ErrorFields = Dict[str, List[str]]

PropsValidated = TypeVar('PropsValidated')

@dataclass(slots=True)
class ValidatorFieldsInterface(ABC, Generic[PropsValidated]):
    errors: ErrorFields = None
    validated_data: PropsValidated = None

    @abc.abstractmethod
    def validate(self, data: Any) -> bool:
        raise NotImplementedError()