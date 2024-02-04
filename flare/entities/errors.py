from dataclasses import dataclass


@dataclass
class SuccessMessage:
    title: str
    message: str


@dataclass
class ErrorMessage:
    title: str
    message: str
