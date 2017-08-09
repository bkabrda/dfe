import jinja2


class Renderer(object):
    def __init__(self, cfg):
        self.cfg = cfg
        self.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))

    def render(self):
        tpl = self.jinja_env.get_template(self.cfg.dockerfile)
        return tpl.render(**self.cfg.vars)
