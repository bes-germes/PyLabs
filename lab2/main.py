import math
import time
from datetime import datetime
from abc import ABC, abstractmethod
import os.path
from typing import Any


class MyVector:
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
        return MyVector(x, y)

    def __sub__(self, other_vec):
        x = self.x - other_vec.x
        y = self.y - other_vec.y
        return MyVector(x, y)

    def __eq__(self, other_vec):
        return self.x == other_vec.x and self.y == other_vec.y

    def __ne__(self, other_vec):
        return not self == other_vec

    def __mul__(self, other):
        if type(other) == int:
            x = self.x * other
            y = self.y * other
            return MyVector(x, y)
        elif type(other) == MyVector:
            return self.x * other.x + self.y * other.y

    def length(self):
        return (self.x**2 + self.y**2) ** 0.5

    def __rmul__(self, other):
        return self * other


class MyFigure(ABC):
    @abstractmethod
    def info(self):
        return "base"

    @abstractmethod
    def square(self):
        return "tyt pydet ploshad'"


class MyRectangle(MyFigure):
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


class MyTriangle(MyFigure):
    def __init__(self, vec1: MyVector, vec2: MyVector):
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


class MyCyrcle(MyFigure):
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
        return math.pi * (self.r**2)


class BaseDecor:
    def __init__(self, my_function):
        self.my_function = my_function

        self.infoList = list()

    # @abstractmethod
    # def __call__(self, *args: Any, **kwds: Any) -> Any:
    #     return super().__call__(*args, **kwds)

    def _logInfo(self, *args):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.infoList.append(
            f"{current_time}: function {self.my_function.__name__} called with arguments {args}"
        )
        print(self.infoList)


class Timer(BaseDecor):
    # self.starttime = 0
    # self.runtime = 0
    # self.name = ""
    # /
    @property
    def __name__(self):
        return self.my_function.__name__

    def __call__(self, *args, **kwargs):
        self.starttime = time.perf_counter()
        result = self.my_function(*args, **kwargs)
        self.runtime = time.perf_counter() - self.starttime
        self._logInfo(*args)
        return result

        # print(f"{self.runtime:.10f}")


class HtmlPrinter(BaseDecor):
    # def __init__(self, my_function):
    #     self.my_function = my_function

    def __call__(self, *args, **kwargs):
        result = self.my_function(*args, **kwargs)
        self._logInfo(*args)
        print(f"<html><body>{self.my_function.runtime:.10f}</body></html>")
        return result


@HtmlPrinter
@Timer
def to_power_numbers(list_of_numbers: list):
    j = 0
    print(list_of_numbers)
    for i in list_of_numbers:
        list_of_numbers[j] *= i
        j += 1
    return list_of_numbers


@HtmlPrinter
@Timer
def list_comprehension(list_of_numbers: list):
    squares = [n * n for n in list_of_numbers]
    return squares


@HtmlPrinter
@Timer
def map_power(list_of_numbers: list):
    return list(map(lambda x: x * x, list_of_numbers))


class MyLogger(object):
    def __init__(self, path: str):
        self.write_file = open(path, "a", encoding="utf-8")

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(MyLogger, cls).__new__(cls)
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

    def __write_to_log(self, message: str, status: str):
        self.write_file.write(f"[{status}] {self.get_cur_time()}: {message},\n")

    def __del__(self):
        self.write_file.close()

    def debug(self, message: str):
        self.__write_to_log(message, "debug")

    def info(self, message: str):
        self.__write_to_log(message, "indo")

    def warn(self, message: str):
        self.__write_to_log(message, "warn")

    def error(self, message: str):
        self.__write_to_log(message, "error")

    def critical(self, message: str):
        self.__write_to_log(message, "critical")


if __name__ == "__main__":
    new_vec = MyVector(1, 2)
    print(new_vec.length())
    # new_vec1 = my_vector(654, 234)
    # print(new_vec.x)
    # new_fig = my_figure()
    # new_rec = my_rectangle(5, 5)
    # new_tri = my_triangle(new_vec, new_vec1)
    # new_cyr = my_cyrcle(2)
    # print(new_cyr.info())
    #
    l = [1, 2, 3, 4, 5, 5344234234234682364482348247422345]
    to_power_numbers(l)
    list_comprehension(l)
    map_power(l)

    # new_log = MyLogger("log.txt")

    # new_log.critical("dfgdgd")
