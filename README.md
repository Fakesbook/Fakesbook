Fakesbook
=================
A teaching platform designed to enable visualization of social networking graphs and data privacy.


![Creative Commons Attribution-ShareAlike 4.0 International License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png "CC BY")
This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License (CC BY)](https://creativecommons.org/licenses/by/4.0/).

Getting started
------
Go to the github [releases page](https://github.com/Fakesbook/Fakesbook/releases) and download the latest release for your platform

Launch the application and have fun playing with the tool!

Contributing
-----
If you encounter a problem while using Fakesbook, then please file an issue on [github](https://github.com/Fakesbook/Fakesbook/issues).

We would love any contributions that you want to make to the project!
If you have something that you want to add then you should fork the project, make a branch on your fork with the changes and then make a pull request here.

## Developing with Fakesbook

### Requirements
#### Note: Fakesbook has only been tested on MacOS and the most recent releases of Ubuntu.

* Python3
* Git
* Virtualenv

First make sure that you have python3 installed either by downloading it from the [python site](https://www.python.org/downloads/), or by installing via the terminal.

##### MacOS:
via [Homebrew](https://brew.sh/)
```bash
$ brew install python
```

##### Ubuntu
```bash
$ sudo apt-get install python3
```

Then install [virtualenv](https://virtualenv.pypa.io/en/stable/) via pip.

```bash
$ pip install virtualenv
```

### Setup

Clone this repository to your desired location and navigate to the repository in a terminal application.

Then setup a virtual environment to contain all of the dependencies for the platform.
```bash
$ virtualenv -p$(which python3) venv
```

Next activate the virtual environment and install the requirements.
```bash
$ source venv/bin/activate # or activate.csh, activate.fish depending on shell
$ pip install -r requirements.txt
```
Use `deactivate` to exit the virtualenv.

Running the app
---------------

Before running the app you need to reactivate the virtual env.
```bash
$ source venv/bin/activate
```

Now you can start a test environment on `localhost:8081` by running:
```bash
$ python privacy_app.py
```

Or you can start the gui application by running:
```bash
$ python fakesbook.py
```

When you are done running the application use `$ deactivate` to exit the virtualenv.

To build an application bundle you can run:
```bash
$ ./pyinstaller.sh
```
The application should be placed at `dist/fakesbook`

-----------
The example profile pictures are in the public domain and can be found at [pexels.com](https://www.pexels.com/).
