import argparse
import asyncio
import aiohttp
import csv
import json

def csv_write(path, html_response):

    html_response = json.loads(html_response)

    if not "labs" in html_response:
        return print("Нет лаб")    
        
    with open(path, mode="w+", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
        file_writer.writerow(["Имя лабы", "дедлайн"])
        for lab_name in html_response['labs'].keys():
            file_writer.writerow([lab_name, html_response['labs'][lab_name]['deadline']])

    
        

async def main(method=None, link=None):
    async with aiohttp.ClientSession() as session:
        html = ""
        match str(method).upper():
            case "GET":
                async with session.get(link) as response:
                    html = await response.text()
                    print(html)
            case "POST":
                async with session.post(link) as response:
                    html = await response.text()
                    print(html)
            case "DELETE":
                async with session.delete(link) as response:
                    html = await response.text()
                    print(html)
            case "PATCH":
                async with session.patch(link) as response:
                    html = await response.text()
                    print(html)
            case _:
                return print("Неизвестный метод...")
        csv_write("C:/Users/olezh/PyProjects/labs.csv", html)
        

parser = argparse.ArgumentParser(description="storage script")

parser.add_argument("--method", dest="method", type=str)
parser.add_argument("--link", dest="link", type=str)

args = parser.parse_args()

asyncio.run(main(args.method, args.link))