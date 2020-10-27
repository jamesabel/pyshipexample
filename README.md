
# pyship

pyship's major features

* freeze practically any Python application
* creates an installer
* automatic application updating in the background (no user intervention)
* OS native application (e.g. .exe for Windows)
* run on OS startup option 

# Learn how to use pyship by example
 
Use this `pyshipexample` program to learn how to use pyship. This example already has all the files necessary to create a 
stand-alone application. The directions below show you how to use pyship from scratch. 

## 1) Create your Python application

Create a your Python program as "run the module as an application" (e.g. you can run your application as `python -m <module>`). 
Note that there is nothing about this step that is particularly special about pyship.  See 
[execute as main module](https://docs.python.org/3/using/cmdline.html#cmdoption-m) for details.

* Unless your application is extremely simple, your application should be organized in a separate directory (since it's a package) 
and contain an `__init__.py` and `__main__.py` files.

pyshipexample's directory structure:

```
pyshipexample
    __init__.py        # required for a package
    __main__.py        # this file will be "run" from the "python -m pyshipexample" command
    __version__.py     # contains __version__ string
    main.py            # in this example, the actual application code is in main.py
```

When this is complete, you can run your application `python -m pyshipexample`. See `pyshipexample.bat` for an example.
 
## 2) Package your application up as a distribution

Package your application up as a distribution using whatever tool you like (e.g. `flit`, `setup.py`, etc.). The result should be a 
distribution (e.g. a wheel), typically in the `dist` directory.  This part is also general and not specific to PyShip.

The pyshipexample distribution was created with flit, therefore `pyproject.toml` has several sections and key/value pairs already filled in.

## 3) Fill in pyproject.toml with your project name and pyship specific directives

This is the first part that is pyship specific.

If you're using flit, a `pyproject.toml` file will already exist.  If not, create a `pyproject.toml`.  In any case, add the lines below 
for pyship.

pyproject.toml:
```
[project]
name = "pyshipexample"

[tool.pyship]
is_gui = true
```

## 4) Run pyship

Obviously this is pyship specific.  Run:

```
python -m pyship
```

This creates all the artifacts necessary for you to ship your app, including creating an installer in the `installers` directory.

```
installers
    pyshipexample_installer_win64.exe
```

If you're using AWS, the installer (e.g. `pyshipexample_installer_win64.exe`) and the `clip` file will be uploaded to S3. You can 
merely point your users to the installer in S3 and they can download the installer from there (either make the bucket
public or manage permissions via AWS's IAM). The `clip` file is used for updating (more on this later).

Once the installer is run, an executable will be placed in the application location for the particular OS.  Example:

`C:\Program Files (x86)\abel\pyshipexample\pyshipexample\pyshipexample.exe`

## 5) Updating

If desired, your application can self-update.

< fill this in once updating is added to the example app >

# pyship Architecture Basics

You don't need to know this to use pyship, but in case you're curious or you need to debug, here is a basic description of the
pyship architecture.

## Packaged "main module" application

pyship achieves modularity and simplicity by using Python's existing "main module" and packaging features.  Once your application 
adheres to these conventions and capabilities, using pyship is relatively simple and straight-forward. You'll present your application
to pyship as a "main module" (run-able via the python -m switch) in a standard distribution (e.g. a wheel).

## The Complete Location Independent Python (clip)

One of the most important artifacts created with pyship is the Complete Location Independent Python (clip).  The clip directory
contains a complete Python environment (full interpreter, all required packages, and the application) in an independent and 
relocatable directory.  This directory is versioned, so it's name is `<application name>_<version string>` .  
For example: `pyshipexample_0.0.1` .  This directory is also zipped up into a `.clip` file and uploaded AWS S3, and can be used 
for application updating.

## Launcher

pyship creates a "launcher", which is an executable of the form `<project_name>.exe` .  This program source is actually
in Python and uses `pyinstaller` to create this frozen binary (and associated files).  It's main job is to find the 
greatest clip (by version) and execute it.  It also facilitates updating by re-running an application if the application 
requests it.  If an application wants to self-update, it uses pyshipupdate and downloads a new clip (e.g. from AWS S3) and 
exits with a restart request.  Upon restart the application will be updated since the most recent clip will be used. 

See pyship's launcher sub-module for the source.
