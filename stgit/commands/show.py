__copyright__ = """
Copyright (C) 2006, Catalin Marinas <catalin.marinas@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2 as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
"""

import sys, os
from optparse import OptionParser, make_option
from pydoc import pager

from stgit.commands.common import *
from stgit import git


help = 'show the commit corresponding to a patch (or the current patch)'
usage = """%prog [options] [<patch1>] [<patch2>] [<patch3>..<patch4>]

Show the commit log and the diff corresponding to the given
patches. The output is similar to that generated by the 'git show'
command."""

options = [make_option('-b', '--branch',
                       help = 'use BRANCH instead of the default one'),
           make_option('-a', '--applied',
                       help = 'show the applied patches',
                       action = 'store_true'),
           make_option('-u', '--unapplied',
                       help = 'show the unapplied patches',
                       action = 'store_true'),
           make_option('-O', '--diff-opts',
                       help = 'options to pass to git-diff')]


def func(parser, options, args):
    """Show commit log and diff
    """
    applied = crt_series.get_applied()
    unapplied = crt_series.get_unapplied()

    if options.applied:
        patches = applied
    elif options.unapplied:
        patches = unapplied
    elif len(args) == 0:
        patches = ['HEAD']
    else:
        if len(args) == 1 and args[0].find('..') == -1 \
               and not crt_series.patch_exists(args[0]):
            # it might be just a commit id
            patches = args
        else:
            patches = parse_patches(args, applied + unapplied +\
                                crt_series.get_hidden(), len(applied))

    if options.diff_opts:
        diff_flags = options.diff_opts.split()
    else:
        diff_flags = []

    commit_ids = [git_id(patch) for patch in patches]
    commit_str = '\n'.join([git.pretty_commit(commit_id, diff_flags=diff_flags)
                            for commit_id in commit_ids])
    if commit_str:
        pager(commit_str)
