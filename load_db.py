import tarfile
import pathlib
from sys import argv
from shutil import rmtree

USAGE = "Usage: python3 load_db.py <database tarfile> <directory to extract to>"

def load_db(loaddir, loadname):
    if not tarfile.is_tarfile(loaddir):
        print("Save file is not tar file, please try again.")
        print(USAGE)
        return

    if pathlib.Path(loadname).is_dir():
        rmtree(loadname)

    tf = tarfile.open(name=loaddir, mode='r:gz')

    tf.extractall("./" + loadname)

    tf.close()

if __name__ == '__main__':
    if len(argv) == 3:
        loaddir = argv[1].split(".")[0] + ".tar.gz"
        loadname = argv[2]
        if not pathlib.Path(loaddir).is_file() or (pathlib.Path(loadname).is_dir() and not ('y' in input("This will overwrite the current database at {}. Continue? [y/n] ".format(loadname)))):
            print(USAGE)
            exit(1)

        load_db(loaddir, loadname)
