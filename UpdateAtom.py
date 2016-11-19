#!/usr/bin/env python3
import os
import shutil
import sys
import zipfile
import urllib.request
import json

'''
The MIT License (MIT)

Copyright (c) 2015 pseudoj

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, tmerge, publish, distribute, sublicense, and/or sell
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
'''

# Configuration
ATOM_PATH = r"."  # Pre-existing directory where Atom is installed to
DOWNLOAD_PATH = r""  # Leave blank to use working directory
FILE_NAME = "atom-windows.zip"  # Name to save the zip as


def verify_configuration():
    if len(ATOM_PATH.strip()) == 0 or not os.path.exists(ATOM_PATH):
        print("\nNo valid Atom installation path specified. Terminating!")
        sys.exit(1)
    elif len(DOWNLOAD_PATH.strip()) == 0 or not os.path.exists(DOWNLOAD_PATH):
        option = input("\nNo valid download path specified. "
                       "Your options are:"
                       "\n\tY: Use the current working directory "
                       "(" + os.getcwd() + ")"
                       "\n\tN: Terminate the script"
                       "\nSelect an option [y/N]")
        if len(option.strip()) != 0 and "y" in option.strip().lower()[0]:
            print("Using current working directory " + os.getcwd() + ".")
        else:
            sys.exit(1)
    elif len(FILE_NAME.strip()) == 0:
        print("\nNo valid file name specified for downloading the zip. "
              "Terminating!")
        sys.exit(1)


def get_download_path():
    if len(DOWNLOAD_PATH.strip()) == 0 or not os.path.exists(DOWNLOAD_PATH):
        file_path = os.getcwd()
    else:
        file_path = DOWNLOAD_PATH
    return file_path


def get_latest_version():
    request = urllib.request.urlopen('https://api.github.com/'
                                     'repos/atom/atom/releases')
    data = json.loads(request.readall().decode('utf-8'))
    return data[0]['name']


def download(version):
    file_path = get_download_path()
    print("Downloading " + FILE_NAME + " to " + file_path + "...")
    urllib.request.urlretrieve('https://github.com/atom/atom/' +
                               'releases/download/v' + version +
                               '/atom-windows.zip',
                               os.path.join(file_path, FILE_NAME))


def unzip():
    print("Extracting Atom archive...")
    with zipfile.ZipFile(os.path.join(get_download_path(),
                                      FILE_NAME), 'r') as atom_zip:
        atom_zip.extractall()


def install():
    print("Installing Atom to specified path...")
    files = os.path.join(get_download_path(), "Atom")
    for item in os.listdir(files):
        source = os.path.join(files, item)
        destination = os.path.join(ATOM_PATH, item)
        if os.path.isdir(source):
            if os.path.exists(destination):
                shutil.rmtree(destination)
            shutil.copytree(source, destination)
        else:
            if os.path.exists(destination):
                os.remove(destination)
            shutil.copy(source, destination)


def clean():
    print("Cleaning up files...")
    try:
        os.remove(os.path.join(get_download_path(), FILE_NAME))
        shutil.rmtree(os.path.join(get_download_path(), "Atom"))
    except OSError:
        pass

# Run
print("Your installation of Atom will now be updated."
      "\nEnsure that your configuration is valid "
      "and correct before proceeding."
      "\nBy proceeding, you agree to the terms of the license.")
confirm = input("Proceed? [Y/n]")
if (len(confirm.strip()) != 0 and 'n' in confirm.strip().lower()[0]):
        sys.exit(0)
else:
    version = get_latest_version()
    agree = input("\nDo you want to download and install version"
                  "{} of Atom? [Y/n]".format(version))
    if len(agree.strip()) != 0 and 'n' in agree.strip().lower()[0]:
        sys.exit(0)
    else:
        verify_configuration()
        download(version)
        unzip()
        # install()
        clean()
        print("Done.")
        input("Press ENTER to terminate.")
