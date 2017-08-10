# dfe - Dockerfile Expand

`dfe` provides a simple templating engine that allows for writing a
`Dockerfile` as a [Jinja2 template](http://jinja.pocoo.org/) and provide
multiple configurations to render it in.

## Dockerfile

A `Dockerfile` written for usage by `dfe` might look like this:

    FROM {{ base_img_reg }}{{ base_img_name }}:{{ base_img_tag }}
    
    RUN {{ installer }} install httpd && \
        {{ installer }} clean all
    
    COPY {{ configfile }} /etc/httpd/conf.d
    COPY {{ files['helpmd']['outpath'] }} /usr/share/docs/{{ files['helpmd']['path'] }}
    
    EXPOSE 80
    
    CMD exec /usr/sbin/apachectl -DFOREGROUND

## configurations.yml

`dfe` requires a `configurations.yml` file as input. A `configurations.yml`
file used with the above `Dockerfile` might look like this:

    version: '1'
    
    defaults:
      files:
        # The help.md file is very similar for all combinations, so we provide just
        # one, which will also be rendered
        helpmd:
          path: help.md
      vars:
        # The configs for the service itself for centos vs fedora are very different,
        # therefore we provide different files
        configfile: config-rhel_centos
        installer: yum
    
    configurations:
      - name: fedora-26
        tag: "fedora/httpd:2.4"
        vars:
          base_img_reg: some.registry.fedoraproject.org
          base_img_name: fedora
          base_img_tag: 26
          configfile: config-fedora  # Override default config file
          installer: dnf

      - name: centos-7
        tag: "centos/httpd:2.4"
        vars:
          base_img_reg: some.registry.centos.org
          base_img_name: centos
          base_img_tag: 7

Things to note:

* This configuration file has `version: 1`. This is currently the only version;
  other versions might be added in the future
* There are 3 `configurations` defined, each has a `name` and `vars`.
  * Required values are `name`, `vars.base_img_reg`, `vars.base_img_name`
    and `vars.base_img_tag`
* There are some `defaults` defined; there is a `files` section in the defaults

When `dfe is executed, configurations will be expanded in the following way
(if some values already exist, from a previous step, they're overwritten):

* Some values are added automatically. Currently, these are:
  * `files.dockerfile` - equals to `{path: Dockerfile}`
  * `tag` - equals to `name`
  * If `base_img_reg` is present and non-empty, slash is appended;
    if `base_img_reg` is not present, it's added (empty)
* Values from `defaults` are added
* Values from the `configurations` entry are added
* `outpath` values are calculated for all `files` entries
* `name`, `tag` and `files` are added to `vars` to be accessbile
  while rendering

Taking the example above, these would be the expanded configurations
(assuming output path given to `dfe` is `.`):

    - name: fedora-26
      tag: "fedora/httpd:2.4"
      files:
        dockerfile:
          path: Dockerfile
          outpath: Dockerfile.fedora-26
        helpmd:
          path: help.md
          outpath: help.md.fedora-26
      vars:
        base_img_reg: some.registry.fedoraproject.org
        base_img_name: fedora
        base_img_tag: 26
        configfile: config-fedora
        installer: dnf

    - name: centos-7
      tag: "centos/httpd:2.4"
      files:
        dockerfile:
          path: Dockerfile
          outpath: Dockerfile.centos-7
        helpmd:
          path: help.md
          outpath: help.md.centos-7
      vars:
        base_img_reg: some.registry.centos.org
        base_img_name: centos
        base_img_tag: 7
        configfile: config-rhel_centos
        installer: yum

(Plus, the `files` section would also be appended under `vars`, but that is
omitted in this example.)

## Expansion (a.k.a. Rendering)

`Dockerfile` rendering by `dfe` for specific `configurations` entry:

* The `configurations` entry is expanded (see above)
* All files from the `files` item of given entry are traversed and rendered
* All templates are rendered using values from entry's expanded `vars`

## Printing expanded values

It's possible to print expanded values (or whole configs) to stdout
via the `-v` switch.

## Usage

* `dfe -h` - Print help
* `dfe [-c <configurations>] list-configs` - List names of configurations entries
* `dfe [-c <configurations>] [-i <dir>] [-o <dir>] render <configuration_item>`
  * Renders `Dockerfile`, from directory given by `-i` to directory
    given by `-o`
  * Name of the resulting files is `<original_filename>.<name>` (for `configurations`
    entry with given `name`)
* `dfe -c <configurations> expanded-value <configuration_item> <configuration_value>` -
   Output given value of given expanded configuration item to stdout (e.g.
   `tag` to print the tag; to print whole item, use `.`).

Default values:
* `-c`: `./configurations.yml`
* `-i`: `.`
* `-o`: `.`


# Example

To run `dfe` from git source on the example in `example` directory, run:

    PYTHONPATH=.. python ../dfe/bin.py -c configurations.yml -i example/ -o example/ <your_command>
