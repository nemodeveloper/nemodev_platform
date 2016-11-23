from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    # env.globals.update({
    #     'static': staticfiles_storage.url,
    #     'url': reverse,
    # })
    return env
