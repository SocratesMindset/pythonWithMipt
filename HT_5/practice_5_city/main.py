
import sys

from city.person import Person
from city.city import  City
from city.city_list import CityList

def person_test() -> None:
    p = Person('a', 'b', 'c')
    help(p)

    #print(dir(p))
    print(p)


def city_test() -> None:
    c1 = City("City1", 10)
    print(c1)
    c2 = City("City2", 50)
    print(c2)

    for i in range(15):
        c1.add_person()

    for i in range(5):
        c1.remove_person()
        c2.remove_person()

    print(c1)
    print(c2)

    #print(c1)

    c2.tmp1 = 10
    c2.tmp2 = 20

    print(c1.__dict__)
    print(c2.__dict__)

    print(dir(c1))
    print(dir(c2))

    print(hasattr(c2, 'tmp3' ))

    print(c1)
    print(c2)


def city_list_test() -> None:

    c3 = CityList("City_with_named_persons", 10)

    for i in range(15):
        s = str(i)
        c3.add_person(Person(s,s+s, s+s+s))

    #print(c3)

    for i in range(2,10,2):
        c3.remove_person(i)

    print(c3)

def cls_method(cls) -> None:
    print('This classmethod was added to {} \n'.format(cls))

def stat_method() -> None:
    print('This staticmethod was added \n')

# dynamical + attr
def add_attr() -> None:
    pers_1 = Person()

    setattr(pers_1, 'age', '135')
    pers_1.__dict__['gneder'] = 'male'
    
    setattr(Person, 'cls_method', classmethod(cls_method))
    setattr(Person, 'stat_method', staticmethod(stat_method))

    Person.cls_method()
    Person.stat_method()
    
    print(pers_1)

    pers_2 = Person("Vasil", "Vasiliev", "Vas.")

    print(pers_2)
    

if __name__ == '__main__':

    print("Program is started \n")

    test = int(sys.argv[1])

    match test:
        case 1:
            person_test()
        case 2: 
            city_test()
        case 3:
            city_list_test()
        case 4:
            add_attr()
        case _ :
            print("Error: wrong test number\n")


    print("Program is finished \n")


