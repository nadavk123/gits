import os


#########
#PRIVATE#
#########

class Branch(object):
    def __init__(self):
        pass

    def create_new(self, name, ref, description=""):
        with open("./gits/branches/{}".format(name), "wb") as f:
            f.write("{0}|{1}".format(ref, description))

    def log(self, name):
        if not os.path.exists("./gits/branches/{}".format(name)):
            return []
        with open("./gits/branches/{}".format(name), "rb") as f:
            return f.read().split("\r\n")

    def update_ref(self, name, ref, description):
        if not os.path.exists("./gits/branches/{}".format(name)):
            self.create_new(name, ref, description)
            return

        with open("./gits/branches/{}".format(name), "ab") as f:
            f.write("\r\n{0}|{1}".format(ref, description))


my_branch = Branch()

########
#PUBLIC#
########

def get_log(name):

    return my_branch.log(name)



def update(name, ref, description):
    my_branch.update_ref(name, ref, description)

    return True


def create_new_branch(from_name, to_name):
    last_commit = my_branch.log(from_name)[-1]
    my_branch.create_new(to_name, *last_commit.split("|"))

    return True
