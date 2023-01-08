from __future__ import annotations

from enum import Enum


class Reference(Enum):
    def as_key(self) -> str:
        return self.name.lower()

    def index(self) -> int:
        ref_list = list(self.__class__)
        return ref_list.index(self)

    @classmethod
    def at(cls, index: int) -> Reference:
        ref_list = list(cls)
        return ref_list[index]
