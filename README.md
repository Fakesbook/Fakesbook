Fakesbook
=================
A teaching platform designed to enable visualization of social networking graphs and data privacy.


![Creative Commons Attribution-ShareAlike 4.0 International License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png "CC BY")
This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License (CC BY)](https://creativecommons.org/licenses/by/4.0/).

Setup and Installation
-----

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
$ virtualenv -p$(which python3) venv # only do this once
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
$ make test
```

Or you can start a production environement on `localhost:8080` by running:
```bash
make run
```

When you are done running either environment use `$ deactivate` to exit the virtualenv.

Using other Utilities
-----------

**Reseting a user password**
```bash
$ python reset_password.py app.db # or wherever the app database is
```

**Save a database**
```bash
$ python save_db.py path/to/database/directory <name of save file>
```

**Load a database**
```bash
$ python load_db.py <name of save file> path/to/database/directory
```

**Generate a database**
```bash
$ python populate_db.py <name of database file> <name of admin user> # the admin user's name will be used as the password
```

-----------
The example profile pictures are in the public domain and can be found at [pexels.com](https://www.pexels.com/).
