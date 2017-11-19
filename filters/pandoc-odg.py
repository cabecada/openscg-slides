#! /usr/bin/env python
"""
Pandoc filter to convert odg files to pdf.

Based on Jerome Robert's pandoc-svg.py as suggested at:
https://github.com/jgm/pandoc/issues/265#issuecomment-27317316
"""

__author__ = "Jan Wieck"

import mimetypes
import subprocess
import os
import sys
from pandocfilters import toJSONFilter, Str, Para, Image

fmt_to_option = {
    "latex": ("--export-pdf","pdf"),
    "beamer": ("--export-pdf","pdf"),
}

def odg_to_any(key, value, fmt, meta):
    if key == 'Image':
       if len(value) == 2:
           # before pandoc 1.16
           alt, [src, title] = value
           attrs = None
       else:
           attrs, alt, [src, title] = value
       mimet,_ = mimetypes.guess_type(src)
       option = fmt_to_option.get(fmt)
       if mimet == 'application/vnd.oasis.opendocument.graphics' and option:
           noext_name,_ = os.path.splitext(src)
           base_name = os.path.basename(src)
           dir_name = os.path.dirname(src)
           eps_name = noext_name + "." + option[1]
           try:
               mtime = os.path.getmtime(eps_name)
           except OSError:
               mtime = -1
           if mtime < os.path.getmtime(src):
	       cwd = os.getcwd()
               os.chdir(dir_name)
               cmd_line = ['soffice', '--headless',
                           '--convert-to', option[1] + ':draw_' + option[1] + '_Export',
                           '-env:UserInstallation=file://' + os.environ['HOME'] + '/.soffice-batch',
                           base_name]
               sys.stderr.write("Running %s\n" % " ".join(cmd_line))
               subprocess.call(cmd_line, stdout=sys.stderr.fileno())
	       os.chdir(cwd)
           if attrs:
               return Image(attrs, alt, [eps_name, title])
           else:
               return Image(alt, [eps_name, title])

if __name__ == "__main__":
  toJSONFilter(odg_to_any)
