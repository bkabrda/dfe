import jinja2


class Renderer(object):
    def __init__(self, df_path, args):
        self.df_path = df_path
        self.args = args
        self.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))

    def render(self):
        tpl = self.jinja_env.get_template(self.df_path)
        return tpl.render(**self.args)
