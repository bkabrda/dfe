import argparse

from dfe.configurations import Configurations
from dfe.renderer import Renderer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--configurations', default='configurations.yml')
    parser.add_argument('-i', '--input-dir', default='.')
    parser.add_argument('-o', '--output-dir', default='.')
    subp = parser.add_subparsers(dest='subparser')
    subp.add_parser('list-configs')
    val = subp.add_parser('config-value')
    val.add_argument('config')
    val.add_argument('value')
    rend = subp.add_parser('render')
    rend.add_argument('config')
    args = parser.parse_args()
    configs = Configurations.from_file(args.configurations, args.output_dir)
    if args.subparser == 'list-configs':
        for c in sorted(configs.configs_names):
            print(c)
    elif args.subparser == 'config-value':
        # TODO: nice formatting
        print(
            configs.\
            get_expanded_config(args.config).\
            get_value(args.value)
        )
    elif args.subparser == 'render':
        renderer = Renderer(
            configs.get_expanded_config(args.config),
            input_dir = args.input_dir,
        )
        renderer.render()

if __name__ == '__main__':
    main()
