from aiohttp import web
import json
import datetime

labs = dict()
dateformat = '%d.%m.%Y'

def check_date_format(date):
        """Проверить формат даты"""
        try:
            datetime.datetime.strptime(date, dateformat)
            return True
        except Exception as inst:
            print(type(inst))  
            print(inst)
            return False
        
def add_lab(lab_name):

    current_date = datetime.datetime.now()
    lab = {
        "deadline": str(current_date.strftime(dateformat))
    }
    labs[lab_name] = lab
 
def is_lab_exist(lab_name):
    if labs.get(lab_name):
        return True
    else:
        return False

async def view_all_labs(request):
    response_obj = { 'status' : 'success', 'labs': labs}
    return web.Response(text=json.dumps(response_obj), status=200)

async def new_lab(request):
    try:

        lab = request.query['lab_name']

        print("Creating new lab with name: " , lab)
        if not is_lab_exist(lab):
            add_lab(lab)
            response_obj = { 'status' : 'success', 'link':  f'http://localhost:8080/labs/{lab}'}
        else: 
            response_obj = { 'status' : 'faild', 'message':  f'already exist'}

        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:

        response_obj = { 'status' : 'failed', 'reason': str(e) }

        return web.Response(text=json.dumps(response_obj), status=500)

async def get_lab_info(request):
        name = request.match_info.get('lab_name')
        if labs.get(name):
            response_obj = { 'status' : 'success', 'labs': labs}
            return web.Response(text=json.dumps(response_obj), status=200)
        else:
            response_obj = { 'status' : 'failed', 'message':  f"doesn't exist"}
            return web.Response(text=json.dumps(response_obj), status=500)
        
async def edit_lab(request):
    name = request.match_info.get('lab_name')
    deadline = request.query.get('deadline')

    if check_date_format(deadline):      
        if labs.get(name):
            labs[name]['deadline'] = deadline
            response_obj = { 'status' : 'success', 'labs': labs}
            return web.Response(text=json.dumps(response_obj), status=200)
        else: 
            response_obj = { 'status' : 'failed', 'message':  f"doesn't exist"}
            return web.Response(text=json.dumps(response_obj), status=500)
    else:
        response_obj = { 'status' : 'failed', 'message':  f"wrong data format"}
        return web.Response(text=json.dumps(response_obj), status=500)

async def delete_lab(request):
    name = request.match_info.get('lab_name')
    if labs.get(name):
        del labs[name]
        response_obj = { 'status' : 'success', 'labs': labs}
        return web.Response(text=json.dumps(response_obj), status=200)
    else:
        response_obj = { 'status' : 'failed', 'message':  f"smt wrong"}
        return web.Response(text=json.dumps(response_obj), status=500)
        


if __name__ == '__main__':
    app = web.Application()
    app.router.add_get('/labs', view_all_labs) 
    app.router.add_post('/labs', new_lab) 
    app.router.add_get('/labs/{lab_name}', get_lab_info) 
    app.router.add_patch('/labs/{lab_name}', edit_lab)
    app.router.add_delete('/labs/{lab_name}', delete_lab)
    web.run_app(app)