import re


class ParseError(ValueError):
    pass


class Symbol:
    REGEX = re.compile(r'.*')

    def __init__(self, string: str) -> None:
        match = self.REGEX.match(string)

        if match:
            string = match.group()
        else:
            class_name = type(self).__name__
            raise ParseError(f"'{string}' is not a valid {class_name}")

        self.value = string

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}('{self.value}')"

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Symbol):
            raise NotImplemented

        return self.value == other.value


class NonTerminal(Symbol):
    REGEX = re.compile(r'^([A-Z]\d*)$')


class Terminal(Symbol):
    REGEX = re.compile(r'^([^A-Z&$\s]+)$')


class Epsilon(Symbol):
    REGEX = re.compile(r'^&$')


class EoS(Symbol):
    REGEX = re.compile(r'^\$$')


def symbol_from_string(string: str) -> Symbol:
    try:
        return NonTerminal(string)
    except ParseError:
        try:
            return Terminal(string)
        except ParseError:
            try:
                return Epsilon(string)
            except ParseError:
                raise ParseError(f"Invalid symbol {string}")
