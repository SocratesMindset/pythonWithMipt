from city.city import City
import random
from city.person import Person

class CityList(City):

    def __init__(self, name: str, count: int):
        super(CityList, self).__init__(name, count)
        self.__person_list = []


    def add_person(self, p: Person) -> None:
        if super(CityList, self).add_person():
            self.__person_list.append(p)


    def add_person(self, *args: list) -> None:
        p = random.randint(1,100)
        s = str(p)
        if super().add_person():
            self.__person_list.append(Person(s,s+s, s+s+s))


    def remove_person(self, i: int) -> None:
        if super(CityList,self).remove_person():
            i = i % len(self.__person_list)
            del self.__person_list[i]

    def __str__(self) -> str:
        s1 = super(CityList, self).__str__()
        s = []
        s.append(s1)
        s.append("List of residents \n")

        for (i,v) in enumerate(self.__person_list):
            s.append(" - {} - {} \n".format(i,v))

        return ''.join(s)

    def __del__(self) -> None:
        print("The city {} was deleted from agglomeration".format(self._name))
