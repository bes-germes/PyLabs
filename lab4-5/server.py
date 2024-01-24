# Разработать сервер REST API для учёта лабораторных работ студентов с использованием библиотеки aiohttp.
# Сервер должен хранить следующие данные о лабораторных работах:
#   Название лабораторной (обязательно, уникальное поле)
#   Дедлайн (дата в формате день.месяц. год) (обязательно)
#   Описание (опционально)
#   Список студентов, сдавших данную лабораторную работу (опционально)
# Сервер должен поддерживать запросы:
#   Запрос для внесения лабораторной работы в расписание на http://<адрес>:<port>/labs
#      На данном этапе лабораторная работа ещё не выдана, и список студентов пуст.
#      В ответе возвращается URL для дальнейшей работы с данной лабораторной: http://<адрес>:<port>/labs/<название>
#   Запрос для изменения всех полей лабораторной работы, кроме её названия, на http://<адрес>:<port>/labs/<название>.
#      Название изменять нельзя
#   Запрос для удаления лабораторной работы на http://<адрес>:<port>/labs/<название>
#   Запрос для получения данных о лабораторной работе на http://<адрес>:<port>/labs/<название>
#   Запрос для получения данных обо всех лабораторных работах на http://<адрес>:<port>/labs

from aiohttp import web
import json
import datetime
import multidict

dateformat = '%d.%m.%Y'


class Lab:
    """Лабораторная работа"""

    def __init__(self, name, date):
        self.__name = name  # Название лабораторной (обязательно, уникальное поле)
        self.date = datetime.datetime.strptime(date, dateformat)  # Дедлайн (дата в формате день.месяц. год)
        self.description = None  # Описание (опционально)
        self.students = None  # Список студентов, сдавших данную лабораторную работу (опционально)

    @property
    def name(self):
        """Неизменяемое имя"""
        return self.__name

    @staticmethod
    def check_date_format(date):
        """Проверить формат даты"""
        try:
            datetime.datetime.strptime(date, dateformat)  # Дедлайн (дата в формате день.месяц. год)
            return True
        except Exception as inst:
            print(type(inst))  # the exception type
            print(inst)  # __str__ allows args to be printed directly,
            return False

    def get_dict(self):
        """Получить в виде словаря для отправки по сети"""
        res = {'name': self.__name, 'date': self.date.strftime(dateformat)}
        if self.description is not None:
            res['description'] = self.description
        if self.students is not None:
            res['students'] = ','.join(self.students)
        return res

    def edit_lab(self, new_lab):
        """Изменить лабораторнуб работу"""
        if 'date' in new_lab:  # todo проверка формата дата
            self.date = datetime.datetime.strptime(new_lab['date'], dateformat)  # Хранить в виде datetime для удобства
        if 'description' in new_lab:
            self.description = new_lab['description']
        if 'students' in new_lab:
            self.students = new_lab['students'].strip().split(',')  # Хранить в виде списка для удобства


class Server:
    """Класс сервера"""

    def __init__(self):
        self.app = web.Application()
        self.url = "http://localhost:8080"
        self.labs = dict()

        routes = web.RouteTableDef()
        self.app.router.add_post('/labs', self.add_lab)
        self.app.router.add_get('/labs', self.get_labs)
        self.app.router.add_get('/labs/{lab_name}', self.get_lab)
        self.app.router.add_patch('/labs/{lab_name}', self.edit_lab)
        self.app.router.add_delete('/labs/{lab_name}', self.delete_lab)

    # @routes.post('/labs') # почему-то как метод класса не работает ;(
    async def add_lab(self, request):
        """Добавление лабораторной на сервер"""
        try:
            req = await request.json()
        except Exception as inst:
            print(type(inst))  # the exception type
            print(inst.args)  # arguments stored in .args
            print(inst)  # __str__ allows args to be printed directly,
            return web.Response(status=400, text=str(inst))

        if ('name' not in req) or ('date' not in req):
            return web.Response(status=400, text="Недостаточно аргументов для создания лабораторной работы")

        if req['name'] in self.labs:
            # лабораторная уже существует
            return web.Response(status=409, text="Лабораторная уже существует")

        if not Lab.check_date_format(req['date']):
            # неправильный формат даты
            return web.Response(status=400, text="Некорректный формат даты")

        self.labs[req['name']] = Lab(name=req['name'], date=req['date'])
        return web.Response(status=201,
                            headers=multidict.MultiDict({'Location': "{}/{}".format(self.url, req['name'])}))

    async def get_labs(self, request):
        """Получить все лабораторные"""
        resp = dict()
        for i in self.labs:
            resp[i] = self.labs[i].get_dict()
        return web.json_response(status=200, data=resp)

    async def get_lab(self, request):
        """Получить конкретную лабораторную"""
        lab_name = request.match_info['lab_name']
        if lab_name not in self.labs:
            return web.Response(status=404, text="Лабораторная работа не найдена")
        else:
            return web.json_response(status=200, data=self.labs[lab_name].get_dict())

    async def edit_lab(self, request):
        """Редактирование лабораторной"""
        lab_name = request.match_info['lab_name']
        if lab_name not in self.labs:
            return web.Response(status=404, text="Лабораторная работа не найдена")
        try:
            req = await request.json()

            if ('date' in req) and not (Lab.check_date_format(req['date'])):
                return web.Response(status=400, text="Неверный формат даты")

            self.labs[lab_name].edit_lab(req)
            return web.json_response(status=200, text="Лабораторная изменена")
        except Exception as inst:
            print(type(inst))  # the exception type
            print(inst.args)  # arguments stored in .args
            print(inst)  # __str__ allows args to be printed directly,
            return web.Response(status=400, text=str(inst))

    async def delete_lab(self, request):
        """Удалить лабораторную"""
        lab_name = request.match_info['lab_name']
        if lab_name not in self.labs:
            return web.Response(status=404, text="Лабораторная работа не найдена")
        else:
            del self.labs[lab_name]
            return web.Response(status=200, text="Лабораторная удалена")


if __name__ == '__main__':
    serv = Server()
    web.run_app(serv.app)