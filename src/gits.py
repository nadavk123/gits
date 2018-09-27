import sys
import branch
import tree
import core_functions
import file_core
import os
import glob

BAD_CHARACTERS = r"-/\!@#$%^&*(){}[]`~';|-=_+,.?><" + '"'


def get_cur_branch():
    """
    Get the current branch
    :return: string
    """
    with open("./gits/HEAD.txt", "rb") as f:
        return f.read()


def get_branches():
    branches = [os.path.basename(path) for path in glob.glob("gits/branches/*")]
    return branches


def move_branch(to):
    """
    Switch branches
    :param to: name of destination branch
    """
    with open("./gits/HEAD.txt", "wb") as f:
        f.write(to)
    core_functions.reset_repo()
    tree.create_all_func(get_cur_commit(to))


def get_cur_commit(name):
    """
    get the file name of the current commite ref
    :param name: branch's name
    :return: commit's ref
    """
    log = branch.get_log(name)
    if log == []:
        return ''
    else:
        return log[-1].split("|")[0]


def get_branch_commit():
    cur_branch = get_cur_branch()
    return cur_branch, get_cur_commit(cur_branch)


def is_repo():
    """
    Checks if its a gits repository
    :return:
    """
    return os.path.isdir("gits")


def add_file(filename):
    """
    Git add
    """
    if not os.path.exists("gits/add.txt"):
        with open("gits/add.txt", "wb") as f:
            f.write(filename)
        return
    with open("gits/add.txt", "ab") as f:
        f.write("\r\n{}".format(filename))


def handle_init(param):
    """
    Initials the gits folder in master branch
    """
    if is_repo():
        print "\nAlredy a Gits repository"
        return

    dirs_to_create = ["gits", "gits/branches", "gits/refs", "gits/index"]

    for dir in dirs_to_create:
        os.mkdir(dir)
    with open("gits/HEAD.txt", "wb") as f:
        f.write("master")
    print "\nRepository created successfully."


def handle_status(param):
    core_functions.status(*get_branch_commit())


def handle_add(param):
    for filename in param:
        if os.path.exists(filename):
            add_file(filename)
        else:
            print "file: {} does not exists"


def handle_commit(param):
    core_functions.commit(get_cur_branch(), param[0])


def handle_log(param):
    cur_branch = get_cur_branch()
    log = branch.get_log(cur_branch)

    print log
    if log == ['']:
        print "There are no commits yes!"
        exit()
    print "\r\nLog of branch {}\r\n".format(cur_branch)
    for line in log:
        print "\t" + "  ".join(line.split("|")[::-1])
    exit()


def handle_checkout(param):
    if len(param) > 2 or len(param) == 0:
        print "Wrong number of parameters.\n"

    repo_branches = get_branches()
    if len(param) == 1:
        if param[0] in repo_branches:
            move_branch(param[0])
        else:
            print "{} is not a Branch.".format(param[0])
            print "Use -b to create new branch.\n"

    if len(param) == 2 and param[0] == "-b":
        branch.create_new_branch(get_cur_branch(), param[0])
        move_branch(param[0])




def handle_branch(param):
    print "\nBranches: \n"
    for branch in get_branches():
        print "\t{}".format(branch)


def handle_input():
    parameters = sys.argv[1:]
    handle_dict = {"init": handle_init, "status": handle_status, "add": handle_add,
                   "commit": handle_commit, "log": handle_log, "checkout": handle_checkout,
                   "branch": handle_branch}
    if len(parameters) == 0:
        print "\nGits by Nadav\n"
        print "Available Commands:\r\n"
        for i in handle_dict.keys():
            print "\t{}".format(i)

    elif parameters[0] == "init":
        handle_init(parameters)

    elif not is_repo() and parameters[0] != "init":
        print "Not a Gits repository"
    else:
        cur_branch = get_cur_branch()
        cur_commit = get_cur_commit(cur_branch)

        handle_dict[parameters[0]](parameters[1:])


def main():
    handle_input()


if __name__ == '__main__':
    main()
