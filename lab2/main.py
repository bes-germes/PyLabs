import math
import time
from datetime import datetime
import os.path


class my_vector:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def __str__(self):
        return "<{0}; {1}>".format(self.x, self.y)

    def __repr__(self):
        return str(self)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y

    def __add__(self, other_vec):
        x = self.x + other_vec.x
        y = self.y + other_vec.y
        return my_vector(x, y)

    def __sub__(self, other_vec):
        x = self.x - other_vec.x
        y = self.y - other_vec.y
        return my_vector(x, y)

    def __eq__(self, other_vec):
        return self.x == other_vec.x and self.y == other_vec.y

    def __ne__(self, other_vec):
        return not self == other_vec

    def __mul__(self, other):
        if (type(other) == int):
            x = self.x * other
            y = self.y * other
            return my_vector(x, y)
        elif (type(other) == my_vector):
            return self.x * other.x + self.y * other.y

    def __rmul__(self, other):
        return self * other


class my_figure:

    def info(self):
        return "base"

    def square(self):
        return "tyt pydet ploshad'"


class my_rectangle(my_figure):
    def __init__(self, width, height):
        self.__width = width
        self.__height = height

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, w):
        if w > 0:
            self.__width = w
        else:
            raise ValueError

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, h):
        if h > 0:
            self.__height = h
        else:
            raise ValueError

    def info(self):
        return "rectangle"

    def square(self):
        return self.__width * self.__height


class my_triangle(my_figure):
    def __init__(self, vec1: my_vector, vec2: my_vector):
        self.__vec1 = vec1
        self.__vec2 = vec2

    @property
    def vec1(self):
        return self.__vec1

    @vec1.setter
    def vec1(self, vec1):
        self.__vec1 = vec1

    @property
    def vec2(self):
        return self.__vec2

    @vec2.setter
    def vec2(self, vec2):
        self.__vec2 = vec2

    def info(self):
        return "triangle"

    def square(self):
        return (self.vec1.x * self.vec2.y - self.vec1.y * self.vec2.x) / 2


class my_cyrcle(my_figure):
    def __init__(self, r):
        self.__r = r

    @property
    def r(self):
        return self.__r

    @r.setter
    def vec1(self, r):
        self.__r = r

    def info(self):
        return "cyrcle"

    def square(self):
        return math.pi * (self.r ** 2)


class timer:
    def __init__(self, my_function):
        self.my_function = my_function
        self.starttime = 0
        self.runtime = 0
        self.name = ""

    @property
    def __name__(self):
        return self.my_function.__name__

    def __call__(self, *args, **kwargs):
        self.starttime = time.perf_counter()
        result = self.my_function(*args, **kwargs)
        self.runtime = time.perf_counter() - self.starttime
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"{current_time}: function {self.my_function.__name__} called with arguments {args}----timer")
        return result
        # print(f"{self.runtime:.10f}")


class HTML_printer:
    def __init__(self, my_function):
        self.my_function = my_function

    def __call__(self, *args, **kwargs):
        result = self.my_function(*args, **kwargs)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(
            f"{current_time}: function {self.my_function.__name__} called with arguments {args}----HTML_printer")
        print(f"<html><body>{self.my_function.runtime:.10f}</body></html>")
        return result


@HTML_printer
@timer
def to_power_numbers(list_of_numbers: list):
    j = 0
    for i in list_of_numbers:
        list_of_numbers[j] *= i
        j += 1
    return list_of_numbers


@HTML_printer
@timer
def list_comprehension(list_of_numbers: list):
    squares = [n * n for n in list_of_numbers]
    return squares


@HTML_printer
@timer
def map_power(list_of_numbers: list):
    return list(map(lambda x: x * x, list_of_numbers))


class my_logger(object):
    def __init__(self, status: str, message: str):
        self.__status = status
        self.__message = message

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(my_logger, cls).__new__(cls)
        return cls.instance

    @property
    def status(self):
        return self.__status

    @status.setter
    def vestatusc1(self, status):
        self.__status = status

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, message):
        self.__message = message

    def get_cur_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    def write_to_log(self):
        # if os.path.exists("log.txt"):
        with open("log.txt", "a", encoding='utf-8') as write_file:
            write_file.write(f"[{self.status}] {self.get_cur_time()}: {self.message},\n")
        self.print_from_file()
        # else:
        #     self.make_new_file()

    def make_new_file(self):
        open("log.txt", "w", encoding='utf-8').close()
        self.write_to_log()

    def print_from_file(self):
        with open("log.txt", "r", encoding="utf-8") as f:
            text = f.readlines()
            for line in text:
                print(line, end='')

    def debug(self, message: str):
        self.__status = "debug"
        self.__message = message
        self.write_to_log()


    def info(self, message: str):
        self.__status = "indo"
        self.__message = message
        self.write_to_log()


    def warn(self, message: str):
        self.__status = "warn"
        self.__message = message
        self.write_to_log()


    def error(self, message: str):
        self.__status = "error"
        self.__message = message
        self.write_to_log()


    def critical(self, message: str):
        self.__status = "critical"
        self.__message = message
        self.write_to_log()


if __name__ == "__main__":
    # new_vec = my_vector(3123, 677)
    # print(2 * new_vec)
    # new_vec1 = my_vector(654, 234)
    # print(new_vec.x)
    # new_fig = my_figure()
    # new_rec = my_rectangle(5, 5)
    # new_tri = my_triangle(new_vec, new_vec1)
    # new_cyr = my_cyrcle(2)
    # print(new_cyr.info())

    # l = [1, 2, 3, 4, 5, 5344234234234682364482348247422345]
    # to_power_numbers(l)
    # list_comprehension(l)
    # map_power(l)

    new_log = my_logger("init", "init")

    new_log.critical("dfgdgd")
