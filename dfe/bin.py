import argparse

from dfe.configurations import Configurations
from dfe.renderer import Renderer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--configurations',
        default='configurations.yml',
        help='Path to configurations file, defaults to ./configurations.yml'
    )
    parser.add_argument(
        '-i', '--input-dir',
        default='.',
        help='Path to directory with templates, defaults to "."'
    )
    parser.add_argument(
        '-o', '--output-dir',
        default='.',
        help='Path to directory where to put rendered templates, defaults to "."'
    )
    subp = parser.add_subparsers(dest='subparser')
    subp.add_parser(
        'list-configs',
        help='List names of all configurations items'
    )
    val = subp.add_parser(
        'config-value',
        help='Print given value from given config item, e.g. '
        '`fedora-26 vars.base_img_name` or `fedora-26 tag`'
    )
    val.add_argument(
        'config',
        help='Name of configuration item to extract value from'
    )
    val.add_argument(
        'value',
        help='Name of item to extract value from. You can use dotted notation to access '
        'sub-mappings, e.g. `vars.base_img_name`'
    )
    rend = subp.add_parser(
        'render',
        help='Render all files for given config'
    )
    rend.add_argument(
        'config',
        help='Config item to render files for'
    )
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
