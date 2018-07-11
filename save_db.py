import tarfile
import pathlib
from sys import argv

USAGE = "Usage: python3 save_db.py <database directory> <save filename>"

def save_db(savedir, savename):
    tf = tarfile.open(name=savename, mode='w:gz')

    tf.add(savedir, arcname=".")

    tf.close()

if __name__ == '__main__':
    if len(argv) == 3:
        savedir = argv[1]
        savename = argv[2].split(".")[0] + ".tar.gz"
        if not pathlib.Path(savedir).is_dir() or (pathlib.Path(savename).is_file() and not ('y' in input("This will overwrite the file at {}. Continue? [y/n] ".format(savename)))):
            print(USAGE)
            exit(1)

        save_db(savedir, savename)
