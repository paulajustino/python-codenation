from abc import ABC, abstractmethod


class Department:
    def __init__(self, name, code):
        self.name = name
        self.code = code


# classe abstrata
class Employee(ABC):
    def __init__(self, code, name, salary, departament):
        self.code = code
        self.name = name
        self.salary = salary
        self.__department = departament
        self.HOURS = 8
        self.RATE = 0.15

    # implementacao obrigatoria de quem herda a classe
    @abstractmethod
    def calc_bonus(self):
        pass

    def get_hours(self):
        return self.HOURS

    def get_department(self):
        return self.__department.name

    def set_department(self, departament_name):
        self.__department.name = departament_name


class Manager(Employee):
    def __init__(self, code, name, salary):
        super().__init__(code, name, salary, Department('managers', 1))

    def calc_bonus(self):
        return self.salary * self.RATE


class Seller(Employee):
    def __init__(self, code, name, salary):
        super().__init__(code, name, salary, Department('sellers', 2))
        self.__sales = 0.0

    def calc_bonus(self):
        return self.get_sales() * self.RATE

    def get_sales(self):
        return self.__sales

    def put_sales(self, sales):
        self.__sales += sales
