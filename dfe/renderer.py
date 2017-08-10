import jinja2

from dfe.exceptions import DFETemplateNotFoundException


class Renderer(object):
    def __init__(self, cfg, input_dir):
        self.cfg = cfg
        self.input_dir = input_dir
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(input_dir),
            undefined=jinja2.StrictUndefined
        )

    def render_file(self, f):
        try:
            tpl = self.jinja_env.get_template(f)
        except jinja2.exceptions.TemplateNotFound:
            raise DFETemplateNotFoundException(f, self.input_dir)
        return tpl.render(**self.cfg.vars)

    def render(self):
        for f, v in self.cfg.files.items():
            rendered = self.render_file(v['path'])
            with open(v['outpath'], 'w') as fp:
                fp.write(rendered)
