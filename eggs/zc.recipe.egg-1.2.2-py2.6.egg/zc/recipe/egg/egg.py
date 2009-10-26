##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Install packages as eggs

$Id: egg.py 98177 2009-03-17 13:09:25Z jim $
"""

import logging, os, re, zipfile
import zc.buildout.easy_install

class Eggs(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        links = options.get('find-links',
                            buildout['buildout'].get('find-links'))
        if links:
            links = links.split()
            options['find-links'] = '\n'.join(links)
        else:
            links = ()
        self.links = links

        index = options.get('index', buildout['buildout'].get('index'))
        if index is not None:
            options['index'] = index
        self.index = index

        allow_hosts = buildout['buildout'].get('allow-hosts', '*')
        allow_hosts = tuple([host.strip() for host in allow_hosts.split('\n')
                               if host.strip()!=''])
        self.allow_hosts = allow_hosts 

        options['eggs-directory'] = buildout['buildout']['eggs-directory']
        options['_e'] = options['eggs-directory'] # backward compat.
        options['develop-eggs-directory'
                ] = buildout['buildout']['develop-eggs-directory']
        options['_d'] = options['develop-eggs-directory'] # backward compat.

        assert options.get('unzip') in ('true', 'false', None)

        python = options.get('python', buildout['buildout']['python'])
        options['executable'] = buildout[python]['executable']

    def working_set(self, extra=()):
        """Separate method to just get the working set

        This is intended for reuse by similar recipes.
        """
        options = self.options

        distributions = [
            r.strip()
            for r in options.get('eggs', self.name).split('\n')
            if r.strip()]
        orig_distributions = distributions[:]
        distributions.extend(extra)

        if self.buildout['buildout'].get('offline') == 'true':
            ws = zc.buildout.easy_install.working_set(
                distributions, options['executable'],
                [options['develop-eggs-directory'], options['eggs-directory']]
                )
        else:
            kw = {}
            if options.get('unzip'):
                kw['always_unzip'] = get_bool(options, 'unzip')

            ws = zc.buildout.easy_install.install(
                distributions, options['eggs-directory'],
                links = self.links,
                index = self.index, 
                executable = options['executable'],
                path=[options['develop-eggs-directory']],
                newest=self.buildout['buildout'].get('newest') == 'true',
                allow_hosts=self.allow_hosts,
                **kw)

        return orig_distributions, ws

    def install(self):
        reqs, ws = self.working_set()
        return ()

    update = install

class Scripts(Eggs):

    def __init__(self, buildout, name, options):
        super(Scripts, self).__init__(buildout, name, options)

        options['bin-directory'] = buildout['buildout']['bin-directory']
        options['_b'] = options['bin-directory'] # backward compat.

        self.extra_paths = [
            os.path.join(buildout['buildout']['directory'], p.strip())
            for p in options.get('extra-paths', '').split('\n')
            if p.strip()
            ]
        if self.extra_paths:
            options['extra-paths'] = '\n'.join(self.extra_paths)


        relative_paths = options.get(
            'relative-paths', 
            buildout['buildout'].get('relative-paths', 'false')
            )
        if relative_paths == 'true':
            options['buildout-directory'] = buildout['buildout']['directory']
            self._relative_paths = options['buildout-directory']
        else:
            self._relative_paths = ''
            assert relative_paths == 'false'

    parse_entry_point = re.compile(
        '([^=]+)=(\w+(?:[.]\w+)*):(\w+(?:[.]\w+)*)$'
        ).match
    def install(self):
        reqs, ws = self.working_set()
        options = self.options

        scripts = options.get('scripts')
        if scripts or scripts is None:
            if scripts is not None:
                scripts = scripts.split()
                scripts = dict([
                    ('=' in s) and s.split('=', 1) or (s, s)
                    for s in scripts
                    ])

            for s in options.get('entry-points', '').split():
                parsed = self.parse_entry_point(s)
                if not parsed:
                    logging.getLogger(self.name).error(
                        "Cannot parse the entry point %s.", s)
                    raise zc.buildout.UserError("Invalid entry point")
                reqs.append(parsed.groups())

            if get_bool(options, 'dependent-scripts'):
                # generate scripts for all packages in the working set,
                # except setuptools.
                reqs = list(reqs)
                for dist in ws:
                    name = dist.project_name
                    if name != 'setuptools' and name not in reqs:
                        reqs.append(name)

            return zc.buildout.easy_install.scripts(
                reqs, ws, options['executable'],
                options['bin-directory'],
                scripts=scripts,
                extra_paths=self.extra_paths,
                interpreter=options.get('interpreter'),
                initialization=options.get('initialization', ''),
                arguments=options.get('arguments', ''),
                relative_paths=self._relative_paths,
                )

        return ()

    update = install

def get_bool(options, name, default=False):
    value = options.get(name)
    if not value:
        return default
    if value == 'true':
        return True
    elif value == 'false':
        return False
    else:
        raise zc.buildout.UserError(
            "Invalid value for %s: %s" % (name, value))

Egg = Scripts
