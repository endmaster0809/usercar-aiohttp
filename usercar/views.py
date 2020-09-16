from aiohttp import web
import db
import json
from django.core.serializers.json import DjangoJSONEncoder


async def index(request):
    return web.Response(text="usercar api")


async def get_users(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.user.select())
        records = await cursor.fetchall()
        users = [dict(q) for q in records]
        response_obj = {'status': 'success', 'users': users}
        return web.Response(text=json.dumps(response_obj,
                                            sort_keys=True,
                                            indent=1,
                                            cls=DjangoJSONEncoder))


async def get_user(request):
    try:
        id = request.match_info.get('id', None)
        async with request.app['db'].acquire() as conn:
            cursor = await conn.execute(db.user.select().where(db.user.c.id == id))
            record = await cursor.fetchone()
            if record is not None:
                user = [dict(record)]
                response_obj = {'status': 'success', 'user': user}
                return web.Response(text=json.dumps(response_obj,
                                                    sort_keys=True,
                                                    indent=1,
                                                    cls=DjangoJSONEncoder))
            else:
                response_obj = {'status': 'success', 'user': None}
                return web.Response(text=json.dumps(response_obj), status=500)
    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        return web.Response(text=json.dumps(response_obj), status=500)


async def update_user(request):
    try:
        id = request.match_info.get('id', None)
        data = await request.json()
        user_name = data['user_name']
        email = data['email']
        async with request.app['db'].acquire() as conn:
            cursor = await conn.execute(db.user.select().where(db.user.c.id == id))
            record = await cursor.fetchone()
            if record is not None:
                await conn.execute(db.user.update().where(db.user.c.id == id).values(user_name=user_name, email=email))
                response_obj = {'status': 'success'}
                return web.Response(text=json.dumps(response_obj,
                                                    sort_keys=True,
                                                    indent=1,
                                                    cls=DjangoJSONEncoder))
            else:
                response_obj = {'status': 'failed', 'reason': f'there is no user with id:{id}.'}
                return web.Response(text=json.dumps(response_obj), status=500)
    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        return web.Response(text=json.dumps(response_obj), status=500)


async def create_user(request):
    try:
        data = await request.json()
        user_name = data['user_name']
        email = data['email']
        async with request.app['db'].acquire() as conn:
            await conn.execute(db.user.insert().values(user_name=user_name, email=email))
            response_obj = {'status': 'success'}
            return web.Response(text=json.dumps(response_obj,
                                                sort_keys=True,
                                                indent=1,
                                                cls=DjangoJSONEncoder))
    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        return web.Response(text=json.dumps(response_obj), status=500)


async def delete_user(request):
    try:
        id = request.match_info.get('id', None)
        async with request.app['db'].acquire() as conn:
            cursor = await conn.execute(db.user.select().where(db.user.c.id == id))
            record = await cursor.fetchone()
            if record is not None:
                await conn.execute(db.user.delete().where(db.user.c.id == id))
                response_obj = {'status': 'success'}
                return web.Response(text=json.dumps(response_obj,
                                                    sort_keys=True,
                                                    indent=1,
                                                    cls=DjangoJSONEncoder))
            else:
                response_obj = {'status': 'failed', 'reason': f'there is no user with id:{id}.'}
                return web.Response(text=json.dumps(response_obj), status=500)
    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        return web.Response(text=json.dumps(response_obj), status=500)
