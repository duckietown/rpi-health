#!/usr/bin/env python

##
##  Do not modify!
##
##

import datetime
import getpass
import json
import os
import platform
import subprocess
from collections import OrderedDict


def go():
    labels = OrderedDict()

    def add_label(lname, value):
        labels[lname] = value

    def run(x):
        return subprocess.check_output(x)

    _ = run(['git', 'status', '--porcelain', '--untracked-files=no'])
    nmodified = len(_.strip().split('\n'))
    _ = run(['git', 'status', '--porcelain'])
    nadded = len(_.strip().split('\n'))
    add_label('nmodified', nmodified)
    add_label('nadded', nadded)
    add_label('user', getpass.getuser())
    add_label('platform_machine', platform.machine())
    add_label('platform_node', platform.node())
    # add_label('platform_release', platform.release())
    add_label('platform_system', platform.system())
    # add_label('platform_version', platform.version())
    # add_label('platform_processor', platform.processor())
    add_label('build_timestamp', datetime.datetime.now().isoformat())

    d = os.path.basename(os.path.realpath(os.getcwd()))
    prefix = 'duckietown/dt18/%s/' % d
    args = []
    for k, v in labels.items():
        j = json.dumps(v)
        k0 = prefix + k

        args.append('--label')
        args.append('%s=%s' % (k0, j))

    print(" ".join(args))


if __name__ == '__main__':
    go()
