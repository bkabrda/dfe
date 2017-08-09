# dfe - Dockerfile Expand

`dfe` provides a simple templating engine that allows for writing a
`Dockerfile` as a [Jinja2 template](http://jinja.pocoo.org/) and provide
multiple configurations to render it in.

## Dockerfile

A `Dockerfile` written for usage by `dfe` might look like this:

    FROM {{ base_img_reg }}/{{ base_img_name }}:{{ base_img_tag }}
    
    RUN {{ installer }} install httpd && \
        {{ installer }} clean all
    
    COPY {{ configfile }} /etc/httpd/conf.d
    
    EXPOSE 80
    
    CMD exec /usr/sbin/apachectl -DFOREGROUND

## configurations.yml

`dfe` requires a `configurations.yml` file as input. A `configurations.yml`
file used with the above `Dockerfile` might look like this:

    version: '1'
    
    defaults:
      vars:
        configfile: config-rhel_centos
    
    configurations:
      - name: fedora-26
        vars:
          base_img_reg: some.registry.fedoraproject.org
          base_img_name: fedora
          base_img_tag: 26
          configfile: config-fedora

      - name: centos-7
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
* There are some `defaults` defined

When `dfe is executed, configurations will be expanded in the following way:

* For each `configurations` entry, `defaults` is taken as the base
* Value from the `configurations` entry are then taken and added
  (these values can override the defaults)
* Some values are added automatically. Currently, these are:
  * `vars.installer` - equals to `dnf` if `base_img_name` is `fedora`;
    `yum` if `base_img_name` is `centos` or `rhel`
  * `dockerfile` - equals to `Dockerfile`

Taking the example above, these would be the expanded configurations:

    - name: fedora-26
      dockerfile: Dockerfile
      vars:
        base_img_reg: some.registry.fedoraproject.org
        base_img_name: fedora
        base_img_tag: 26
        configfile: config-fedora
        installer: dnf

    - name: centos-7
      dockerfile: Dockerfile
      vars:
        base_img_reg: some.registry.centos.org
        base_img_name: centos
        base_img_tag: 7
        configfile: config-rhel_centos
        installer: yum

## Dockerfile Expansion

`Dockerfile` rendering by `dfe` for specific `configurations` entry:

* The `configurations` entry is expanded (see above)
* The `dockerfile` attribute is taken from given entry and used as a template
  (current directory is used as a base to search for this file)
* The template is rendered using values from entry's `vars`

## Config as Environment Variables

In some cases, it might be useful to be able to print values from an expanded
`configurations` entry as shell environment variables. For example,
when running tests via
[MTF](https://github.com/fedora-modularity/meta-test-family/), you might want
to have information such as `base_img_name` available in the test suite.

`dfe` allows doing this via the `-e` switch(see below). This will print
all the values from an expanded `vars` section of given `configurations` item.
An example output follows (note that variable names are capitalized):

    BASE_IMG_REG=some.registry.fedoraproject.org INSTALLER=dnf CONFIGFILE=config-rhel_centos BASE_IMG_NAME=fedora BASE_IMG_TAG=26

## Usage

* `dfe -h` - Print help
* `dfe -c <configurations> -l` - List names of configurations entries
* `dfe -c <configurations> -e <configuration_item>` - Output given item as
  env vars to stdout
* `dfe -c <configurations> -r <configuration_item>` - Output rendered
  Dockerfile to stdout

# Example

To run `dfe` from git source on the example in `example` directory, you need
to change dir there and run:

    PYTHONPATH=.. python ../dfe/bin.py -c configurations.yml <your_command>
