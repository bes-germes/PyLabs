import copy
import time
import functools


##############lensort##################################
def lensort_without_sort(list_of_words: list):
    new_list_of_words = copy.deepcopy(list_of_words)

    if type(new_list_of_words) is list:
        for word in new_list_of_words:
            if type(word) is str:
                continue
            else:
                return "only for str"

        for i in range(len(new_list_of_words) - 1):
            for j in range(len(new_list_of_words) - i - 1):
                if len(new_list_of_words[j]) > len(new_list_of_words[j + 1]):
                    new_list_of_words[j], new_list_of_words[j + 1] = (
                        new_list_of_words[j + 1],
                        new_list_of_words[j],
                    )

        return new_list_of_words
    else:
        return "Wrong arg"


def lensort_with_sorted(list_of_words: list):
    return sorted(list_of_words)


def lensort_with_sort(list_of_words: list):
    new_list_of_words = copy.deepcopy(list_of_words)
    new_list_of_words.sort()
    return new_list_of_words


def lensort_with_lambda_and_sort(list_of_words: list):
    new_list_of_words = copy.deepcopy(list_of_words)
    new_list_of_words.sort(key=lambda x: len(x))
    return new_list_of_words


def lensort_with_lambda_and_sorted(list_of_words: list):
    return sorted(list_of_words, key=lambda x: len(x))


########unique################


def unique(list_of_something: list):
    new_set = set(list_of_something)
    new_list = []
    for i in new_set:
        new_list.append(i)
    return new_list


#########my_enumerate##################


def my_enumerate(list_of_something: list):
    new_list_idx = []
    for i in range(len(list_of_something)):
        new_list_idx.append(i)
    list_zip = list(zip(new_list_idx, list_of_something))
    return list_zip


def input_txt_and_count_words(file_name: str):
    d = {}

    with open(file_name, "r", encoding="utf-8") as f:
        text = f.readlines()

    # return text
    for line in text:
        for word in line.split():
            if word in d.keys():
                d[word] += 1
            else:
                d[word] = 1
    return d


def timer(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        runtime = time.perf_counter() - start
        print(f"{func.__name__} took {runtime:.10f} secs")
        return result

    return _wrapper


@timer
def to_power_numbers(list_of_numbers: list):
    j = 0
    for i in list_of_numbers:
        list_of_numbers[j] *= i
        j += 1
    return list_of_numbers


@timer
def list_comprehension(list_of_numbers: list):
    squares = [n * n for n in list_of_numbers]
    return squares


@timer
def map_power(list_of_numbers: list):
    return list(map(lambda x: x * x, list_of_numbers))


# l = ["python", "perl", "java", "c", "haskell", "ruby"]
# print(lensort_with_lambda_and_sorted(l))
# print(l)

# l = [1, 2, 1, 3, 2, 5]
# print(unique(l))
# print(l)

# l = ["a", "b", "c"]
# print(my_enumerate(l))

# print(input_txt_and_count_words("test.txt"))

# l = [1, 2, 3, 4, 5, 6]
# print(to_power_numbers(l))
# print(list_comprehension(l))
# print(map_power(l))