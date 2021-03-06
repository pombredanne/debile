# Copyright (c) 2012-2013 Paul Tagliamonte <paultag@debian.org>
# Copyright (c) 2013 Leo Cavaille <leo@cavaille.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from debile.slave.wrappers.cppcheck import parse_cppcheck
from debile.slave.utils import cd
from debile.utils.commands import run_command


def cppcheck(dsc, analysis):
    run_command(["dpkg-source", "-x", dsc, "source"])
    with cd('source'):
        out, err, ret = run_command([
            'cppcheck', '-j8', '--enable=all', '.', '--xml'
        ])

        xmlbytes = err.encode()

        failed = False
        if err.strip() == '':
            return (analysis, err, failed)

        for issue in parse_cppcheck(xmlbytes):
            analysis.results.append(issue)
            if not failed and issue.severity in [
                'performance', 'portability', 'error', 'warning'
            ]:
                failed = True

        return (analysis, err, failed, None)


def version():
    out, err, ret = run_command([
        'cppcheck', '--version'
    ])
    if ret != 0:
        raise Exception("cppcheck is not installed")
    name, version = out.split(" ")
    return (name, version.strip())
