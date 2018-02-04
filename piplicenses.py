#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8 ff=unix ft=python ts=4 sw=4 sts=4 si et
"""
pip-licenses

MIT License

Copyright (c) 2018 raimon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from __future__ import (division, print_function,
                        absolute_import, unicode_literals)
import sys
import argparse
from email.parser import FeedParser

import pip
from prettytable import PrettyTable

__version__ = '0.1.0'
__author__ = 'raimon'
__license__ = 'MIT License'
__summary__ = 'Dump the license list of packages installed with pip.'
__url__ = 'https://github.com/raimon49/pip-licenses'


METADATA_KEYS = (
    'home-page',
    'author',
    'license',
)


SYSTEM_PACKAGES = (
    'pip',
    'PTable',
    'setuptools',
    'wheel',
)


def get_licenses(with_authors=False, with_system=False, with_urls=False):
    pkgs = pip.get_installed_distributions()
    table = PrettyTable()
    table.field_names = ['Package', 'License', 'Author', 'URL', ]
    table.align = 'l'
    for pkg in pkgs:
        pkg_info = get_pkg_info(pkg)

        if not with_system and pkg_info['name'] in SYSTEM_PACKAGES:
            continue

        table.add_row([pkg_info['namever'],
                       pkg_info['license'],
                       pkg_info['author'],
                       pkg_info['home-page'], ])

    print(table.get_string(fields=['Package', 'License', ]))


def get_pkg_info(pkg):
    pkg_info = {
        'name': pkg.project_name,
        'version': pkg.version,
        'namever': str(pkg),
    }
    metadata = None
    if pkg.has_metadata('METADATA'):
        metadata = pkg.get_metadata('METADATA')

    if pkg.has_metadata('PKG-INFO'):
        metadata = pkg.get_metadata('PKG-INFO')

    if metadata is None:
        for key in METADATA_KEYS:
            pkg_info[key] = 'UNKNOWN'

    feed_parser = FeedParser()
    feed_parser.feed(metadata)
    parsed_metadata = feed_parser.close()

    for key in METADATA_KEYS:
        pkg_info[key] = parsed_metadata.get(key, 'UNKNOWN')

    return pkg_info


def create_parser():
    parser = argparse.ArgumentParser(
        description=__summary__)
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s ' + __version__)
    parser.add_argument('-s', '--with-system',
                        action='store_true',
                        default=False,
                        help='dump with system packages')
    parser.add_argument('-a', '--with-authors',
                        action='store_true',
                        default=False,
                        help='dump with package authors')
    parser.add_argument('-u', '--with-urls',
                        action='store_true',
                        default=False,
                        help='dump with package urls')

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    get_licenses(args.with_system,
                 args.with_authors,
                 args.with_urls)


if __name__ == '__main__':
    main()
