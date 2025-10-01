
from typing import List
from city.city_list import CityList
from city.person import Person
from city.family import Family

class CityWithFamilies(CityList):
    def __init__(self, name: str, count: int):
        super().__init__(name, count)

    def add_family(self, family: Family) -> bool:
        members: List[Person] = family.all_members()
        if self._cur_count + len(members) > self._max_count:
            return False
        for p in members:
            super(CityWithFamilies, self).add_person(p)  # use parent add_person(Person)
        return True
