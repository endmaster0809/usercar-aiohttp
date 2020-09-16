from views import index, get_users, get_user, update_user, create_user, delete_user


def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get('/users', get_users)
    app.router.add_get('/user/{id}', get_user)
    app.router.add_put('/user/{id}', update_user)
    app.router.add_post('/user/', create_user)
    app.router.add_delete('/user/{id}', delete_user)
