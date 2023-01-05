# proxy design pattern is similar to decorators by adding additional functionality as a wrapper function

from abc import ABCMeta, abstractclassmethod, abstractstaticmethod

class IPerson(metaclass=ABCMeta):
    @abstractstaticmethod
    def person_method():
        """ Interface Method """

class Person(IPerson):
    def person_method(self):
        print("I am a person")

class ProxyPerson(IPerson):
    def __init__(self):
        self.person = Person()

    def person_method(self):
        print("I am the proxy functionality")
        self.person.person_method()

p1 = Person()
p1.person_method()

p2 = ProxyPerson()
p2.person_method()
