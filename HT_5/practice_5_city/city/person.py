
class Person:
    def __init__(self, _name = 'Ivan', _surname = 'Ivanov',_midname = 'Ivanovich'):
        print("Creation person with name {} {} {} is in process".format(_name, _surname, _midname))
        self._name = _name
        self._surname = _surname
        self._middle_name = _midname

    def __str__(self) -> str:
        str = ''
        for key,val in self.__dict__.items():
            str = str + '{} = {} \n'.format(key, val)
        #return "{} {} {}".format(self._name, self._surname, self._middle_name)
        return str

    def __del__(self) -> None:
        print("Person {} {} {} was removed".format(self._name, self._surname, self._middle_name))

