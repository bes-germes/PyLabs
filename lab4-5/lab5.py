import aiohttp
import asyncio
import argparse
import json
import csv


class Client:
    """Класс клиента"""

    def __init__(self, url):
        self.url = url

    @staticmethod
    async def print_response(response):
        """Распечатать ответ сервера"""
        print(f"Response status: {response.status}")
        text = await response.text()
        if not len(text) == 0:
            print(text)
            print(response.headers)

    @staticmethod
    async def export_labs(res, name):
        """Экспортировать лабораторные в файл"""
        with open(f'{name}.csv', 'w', newline='') as csvfile:
            lab_writer = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            # for i in res.keys():
            lab_writer.writerow(['Имя лабораторной'] + [i for i in res])
            lab_writer.writerow(['Дедлайн'] + [res[i]['date'] for i in res])
            descr = []
            for i in res:
                if 'description' in res[i]:
                    descr.append(res[i]['description'])
                else:
                    descr.append(None)
            lab_writer.writerow(['Описание'] + descr)

            students = set()
            for i in res:
                if 'students' in res[i]:
                    for stud in res[i]['students'].strip().split(','):
                        students.add(stud)

            for stud in students:
                done_labs = []
                for i in res:
                    if 'students' not in res[i]:
                        done_labs.append(None)
                        continue
                    if stud not in res[i]['students'].strip().split(','):
                        done_labs.append(None)
                        continue
                    done_labs.append('+')
                lab_writer.writerow([stud] + done_labs)

        # print("Status:", response.status)
        # print("Content-type:", response.headers['content-type'])
        # text = await response.text()
        # print("Body:", text)

    async def add_lab(self, lab, date):
        """Добавить новую лабораторную работу"""
        async with aiohttp.ClientSession() as session:
            request = {'name': lab, 'date': date}
            async with session.post(url="{}/{}".format(self.url, 'labs'), data=json.dumps(request)) as response:
                await self.print_response(response)

    async def get_lab(self, text):
        """Получить лабораторную работу"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url="{}/{}/{}".format(self.url, 'labs', text)) as response:
                await self.print_response(response)
                if response.status == 200:
                    try:
                        res = await response.json()
                        await self.export_labs({text: res}, text)
                    except Exception as inst:
                        print(type(inst))  # the exception type
                        print(inst.args)  # arguments stored in .args
                        print(inst)  # __str__ allows args to be printed directly,

    async def get_labs(self):
        """Получить список всех лабораторных работ"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url="{}/{}".format(self.url, 'labs')) as response:
                await self.print_response(response)
                if response.status == 200:
                    try:
                        res = await response.json()
                        await self.export_labs(res, 'all_labs')
                    except Exception as inst:
                        print(type(inst))  # the exception type
                        print(inst.args)  # arguments stored in .args
                        print(inst)  # __str__ allows args to be printed directly,

    async def edit_lab(self, lab, date, description, students):
        """Изменить лабоработрую работу"""
        async with aiohttp.ClientSession() as session:
            request = {}
            if date is not None:
                request['date'] = date
            if description is not None:
                request['description'] = description
            if students is not None:
                request['students'] = students

            async with session.patch(url="{}/{}/{}".format(self.url, 'labs', lab),
                                     data=json.dumps(request)) as response:
                await self.print_response(response)

    async def remove_lab(self, lab):
        """Удалить лабораторную работу"""
        async with aiohttp.ClientSession() as session:
            async with session.delete(url="{}/{}/{}".format(self.url, 'labs', lab)) as response:
                await self.print_response(response)


async def main(cli_args):
    client = Client('http://localhost:8080')

    if cli_args.get_all:
        await client.get_labs()

    if cli_args.get:
        await client.get_lab(cli_args.get)

    if cli_args.add and not cli_args.date:
        print("Для добавления лабораторной работы требуется дедлайн(--date)")
    elif cli_args.add and cli_args.date:
        await client.add_lab(cli_args.add, cli_args.date)

    if cli_args.edit and not (cli_args.date or cli_args.description or cli_args.students):
        print("Для изменения лабораторной работы требуется изменяемый параметр --date --description или --students")
    elif cli_args.edit:
        await client.edit_lab(cli_args.edit, cli_args.date, cli_args.description, cli_args.students)

    if cli_args.remove:
        await client.remove_lab(cli_args.remove)  # переделать на один цикл


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Обращения к серверу хранения лабораторных работ')

    # Параметры лабораторной работы
    parser.add_argument('--date', type=str, help="Дата лабораторной работы в формате \"день.месяц.год\"")
    parser.add_argument('--description', type=str, help="Описание лабораторной работы")
    parser.add_argument('--students', type=str, help="Студенты выполняющие лабораторную работу")

    # Чтобы можно было выполнить только одно действие за раз
    group = parser.add_mutually_exclusive_group(required=True)

    #   Запрос для внесения лабораторной работы в расписание на http://<адрес>:<port>/labs
    #      На данном этапе лабораторная работа ещё не выдана, и список студентов пуст.
    #      В ответе возвращается URL для дальнейшей работы с данной лабораторной: http://<адрес>:<port>/labs/<название>
    group.add_argument('--add', type=str, help="Запрос для внесения лабораторной работы в расписание")

    # Запрос для изменения всех полей лабораторной работы, кроме её названия,
    # на http://<адрес>:<port>/labs/<название>. Название изменять нельзя
    group.add_argument('--edit', type=str,
                       help="Запрос для изменения всех полей лабораторной работы, кроме её названия")

    #   Запрос для удаления лабораторной работы на http://<адрес>:<port>/labs/<название>
    group.add_argument('--remove', type=str, help="Запрос для удаления лабораторной работы")

    #   Запрос для получения данных о лабораторной работе на http://<адрес>:<port>/labs/<название>
    group.add_argument('--get', type=str, help="Запрос для получения данных о лабораторной работе")

    #   Запрос для получения данных обо всех лабораторных работах на http://<адрес>:<port>/labs
    group.add_argument('--get_all', action='store_true',
                       help="Запрос для получения данных обо всех лабораторных работах")

    args = parser.parse_args()
    asyncio.run(main(args))
