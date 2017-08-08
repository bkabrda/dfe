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
        for c in sorted(configs.configs_list):
            print(c)
    elif args.config_as_env_vars:
        print(configs.config_as_env_vars(args.config_as_env_vars))
    elif args.render_with_config:
        print(
            Renderer(args.dockerfile, configs.expanded_configs[args.render_with_config]).render()
        )

if __name__ == '__main__':
    main()
