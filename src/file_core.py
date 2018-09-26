import hashlib
import os


#########
#PRIVATE#
#########

def sha1(path):
    """
    Gets sha1 of a file
    """
    with open(path, "rb") as f:
        file_hash = hashlib.sha1(f.read())
    return file_hash.hexdigest()


class File(object):
    def __init__(self):
        pass

    def is_indexed(self, path):
        """
        Checks if already stored in the indexer
        :param path: the sha1 of the file is the filename in the gits index
        :return boolean:
        """
        return os.path.exists("./gits/index/{}".format(path))

    def index_file(self, path):
        """
        Stored file's data in the index directory
        :param path: path to the file in the repo
        """
        if self.is_indexed(sha1(path)):
            return False

        with open(path, "rb") as input_file, open("./gits/index/{}".format(sha1(path)), "w") as output_file:
            output_file.write(input_file.read())

        return True

    def create_from_index(self, path, sha):
        """
        The inverse of index- creates the file in the repo
        :param path: path to the file in the repo
        :param sha: the sha1 of the file's data
        """
        if not self.is_indexed(sha):
            raise Exception("File is not indexed")
        if os.path.dirname(path) != ".":
            os.makedirs(os.path.dirname(path))
        with open("./gits/index/{}".format(sha), "rb") as input_file, open(path, "w") as output_file:
            output_file.write(input_file.read())

        return True


my_file = File()


########
#PUBLIC#
########

def index_file(path):
    return my_file.index_file(path)


def create_from_index(path, sha):
    return my_file.create_from_index(path, sha)
