import argparse

from dfe.configurations import Configurations
from dfe.renderer import Renderer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--configurations', default='configurations.yml')
    parser.add_argument('-d', '--dockerfile', default='Dockerfile.template')
    meg = parser.add_mutually_exclusive_group(required=True)
    meg.add_argument('-l', '--list-configurations', action='store_true')
    meg.add_argument('-e', '--config-as-env-vars')
    meg.add_argument('-r', '--render-with-config')
    args = parser.parse_args()
    configs = Configurations.from_file(args.configurations)
    if args.list_configurations:
        for c in sorted(configs.configs_names):
            print(c)
    elif args.config_as_env_vars:
        print(configs.get_expanded_config(args.config_as_env_vars).as_env_vars())
    elif args.render_with_config:
        print(Renderer(configs.get_expanded_config(args.render_with_config)).render())

if __name__ == '__main__':
    main()
