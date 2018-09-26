import hashlib
import os
import file_core
import hashlib

#########
#PRIVATE#
#########

def sha1(path):
    with open(path, "rb") as f:
        file_hash = hashlib.sha1(f.read())
    return file_hash.hexdigest()


class Reference(object):
    def __init__(self, string=""):
        self.string = string

    def pharse_file(self, path):
        with open("./gits/refs/{}".format(path)) as f:
            raw = f.read()

        pharsed_lines = sorted([i for i in raw.split("\r\n")])

        return pharsed_lines

    def add_line(self, line):
        if self.string == "":
            self.string += line
        else:
            self.string += "\r\n" + line

        return True

    def index_ref(self):
        filename = hashlib.sha1(self.string).hexdigest()
        # In case same ref already exists
        if os.path.exists("./gits/refs/{}".format(filename)):
            return filename

        ref_file = open("./gits/refs/{}".format(filename), "w")
        ref_file.write(self.string)
        ref_file.close()

        return filename

    def create_all(self, path):
        pharsed_lines = self.pharse_file(path)
        for i in pharsed_lines:
            if i[0] == "F":
                file_core.create_from_index(*i.split("|")[1:])
            else:
                self.create_all(i)

        return True

    def get_files(self, ref):
        pharsed_lines = self.pharse_file(ref)
        res = []
        for i in pharsed_lines:
            if i[0] == "F":
                res.append(i)
            else:
                self.get_files(i)

        return res


my_ref = Reference()


########
#PUBLIC#
########


def create_all_func(path):
    my_ref.create_all(path)

def get_files_ref(ref):
    if ref == '':
        return []
    return my_ref.get_files(ref)

def create_ref(files):
    string = "F|{}|{}".format(files[0], sha1(files[0]))
    for f in files[1:]:
        string += "\r\nF|{}|{}".format(f, sha1(f))

    new_ref = Reference(string)

    return new_ref.index_ref()

