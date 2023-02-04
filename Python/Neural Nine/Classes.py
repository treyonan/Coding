# Parent Classes (virtual) -------------------------------

class Language:
    def __init__(self, name):
        self.name = name
    def get_name(self):
        return self.name
    def message(self):
        print("My name is " + self.name)

languages = [Language("Python"), Language("JavaScript")]

for language in languages:
    language.message()



class machine():
    def __init__(self):
        pass

    def comm(self, comm_type):
        pass


class comm():
    def __init__(self):
        pass   

    def show(self):
        pass

# Child classes -------------------------------------------

class test_machine(machine):
    def __init__(self):
        self.machine_type = "I am a Test Machine"

    def comm(self, comm):
        self.comm = comm        


class Ethernet(comm):
    def __init__(self):
        self.comm = "My comm protocol is Ethernet"

    def show(self):
        print(self.comm)

class Modbus(comm):
    def __init__(self):
        self.comm = "My comm protocol is Modubs"

    def show(self):
        print(self.comm)


# Object instances -----------------------------------------------

test_machine1 = test_machine()
test_machine1.comm(Ethernet())

test_machine2 = test_machine()
test_machine2.comm(Modbus())

print(test_machine1.machine_type)
test_machine1.comm.show()

print(test_machine2.machine_type)
test_machine2.comm.show()