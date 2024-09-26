import setuptools
from setuptools import setup
from setuptools.command.sdist import sdist
import subprocess
import sys
import os

data_files = [
    ('/etc/dbus-1/system.d', ['autorun/ancs4linux-advertising.conf']),
    ('/usr/lib/systemd/system', ['autorun/ancs4linux-advertising.service']),
    ('/etc/dbus-1/system.d', ['autorun/ancs4linux-observer.conf']),
    ('/usr/lib/systemd/system', ['autorun/ancs4linux-observer.service']),
    ('/usr/lib/systemd/user', ['autorun/ancs4linux-desktop-integration.service']),
]


setup(name='ancs4linux',
      version='0.0.1',
      description='Python module for system storage configuration',
      author='Toxin', author_email='itstoxinx@gmail.com',
      url='https://github.com/toxin-x/ancs4linux',
      data_files=data_files,
      packages=['ancs4linux']
     )