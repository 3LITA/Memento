import typing

from sqlalchemy.ext.mutable import Mutable


class MutableList(Mutable, list):
    def append(self, value: typing.Any) -> None:
        list.append(self, value)
        self.changed()
        return None

    @classmethod
    def coerce(cls: typing.Any, key: typing.Any, value: typing.Any) -> typing.Optional[typing.Union['MutableList', typing.Any]]:
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value
