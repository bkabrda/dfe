import os

import jinja2


class Renderer(object):
    def __init__(self, cfg, input_dir, output_dir):
        self.cfg = cfg
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(input_dir),
            undefined=jinja2.StrictUndefined
        )

    def render_file(self, f):
        tpl = self.jinja_env.get_template(f)
        return tpl.render(**self.cfg.vars)

    def render(self):
        df = self.render_file(self.cfg.dockerfile)
        target = os.path.join(self.output_dir,
                              self._rendered_fname(self.cfg.dockerfile, self.cfg)
                              )
        with open(target, 'w') as f:
            f.write(df)

    @staticmethod
    def _rendered_fname(original_fname, cfg):
        return '{orig}.{name}'.format(orig=original_fname, name = cfg.name)
