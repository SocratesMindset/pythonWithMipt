
from city.city_families import CityWithFamilies
from city.family import Family

def main():
    c = CityWithFamilies("Moscow", 10)
    fam = Family.new(father_name="Pavel", mother_name="Anna", surname="Sidorov")
    fam.add_child("Ilya", "M")
    fam.add_child("Olga", "F")
    c.add_family(fam)

    fam2 = Family.new(father_name="Roman", mother_name="Elena", surname="Kuznetsov")
    fam2.add_child("Nikita", "M", use_new_branch=True, custom_middle_name="Petrovich")
    c.add_family(fam2)

    print(c)

if __name__ == "__main__":
    main()
