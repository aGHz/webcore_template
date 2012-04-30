#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages


setup(
        name = "Project",
        version = "0.1",
        description = "",
        author = "Adrian Ghizaru",
        author_email = "adrian.ghizaru@gmail.com",
        url = "http://aghz.ca/",

        install_requires = [
            'WebCore < 2.0',
            'jinja2',
            'IPython==0.10'
            ],
        packages = find_packages(exclude=[
            'schema'
            ]),

        zip_safe = False,
        include_package_data = True,
        package_data = {
                '': ['README.textile', 'LICENSE'],
                '__project__': ['templates/*']
            },

        paster_plugins = ['PasteScript', 'WebCore'],
        entry_points = {
            'paste.paster_command': [
                'manage = __project__.commands.manage:ManageCommand',
                'admin = __project__.commands.admin:AdminCommand'
                ]
            }
    )
