
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
try:
    from city.person import Person
except Exception:
    class Person:
        def __init__(self, _name='Ivan', _surname='Ivanov', _midname='Ivanovich'):
            self._name = _name
            self._surname = _surname
            self._middle_name = _midname
        def __str__(self) -> str:
            return f"{self._surname} {self._name} {self._middle_name}"


class Male(Person):
    pass


class Female(Person):
    pass


def patronymic_from_father(father_first_name: str, gender: str) -> str:
    name = father_first_name.strip()
    lower = name.lower()
    if lower.endswith("a") or lower.endswith("я") or lower.endswith("й"):
        root = name[:-1]
    else:
        root = name
    if gender.upper().startswith("M"):
        return root + "ovich"
    else:
        return root + "ovna"


@dataclass
class Child(Person):
    gender: str = "M"  # "M" or "F"
    father: Optional[Male] = None
    use_new_branch: bool = False
    custom_middle_name: Optional[str] = None

    def __init__(self, name: str, surname: str, gender: str, father: Optional[Male] = None,
                 use_new_branch: bool = False, custom_middle_name: Optional[str] = None):
        self.gender = gender
        self.father = father
        self.use_new_branch = use_new_branch
        if use_new_branch and custom_middle_name:
            mid = custom_middle_name
        elif father is not None:
            mid = patronymic_from_father(father._name, gender)
        else:
            mid = "Unknown"
        super().__init__(name, surname, mid)

    def __str__(self) -> str:
        return f"{self._surname} {self._name} {self._middle_name} ({'boy' if self.gender.upper().startswith('M') else 'girl'})"


@dataclass
class Family:
    surname: str
    father: Optional[Male] = None
    mother: Optional[Female] = None
    children: List[Child] = field(default_factory=list)

    def all_members(self) -> List[Person]:
        members: List[Person] = []
        if self.father: members.append(self.father)
        if self.mother: members.append(self.mother)
        members.extend(self.children)
        return members

    @staticmethod
    def new(father_name: str, mother_name: str, surname: str) -> "Family":
        return Family(
            surname=surname,
            father=Male(father_name, surname, "—"),
            mother=Female(mother_name, surname, "—"),
        )

    def add_child(self, name: str, gender: str, use_new_branch: bool = False, custom_middle_name: Optional[str] = None) -> "Family":
        ch = Child(
            name=name,
            surname=self.surname,
            gender=gender,
            father=self.father,
            use_new_branch=use_new_branch,
            custom_middle_name=custom_middle_name
        )
        self.children.append(ch)
        return self
