import sys
import branch
import tree
import core_functions
import file_core
import os
import glob

def get_cur_branch():
    """
    Get the current branch
    :return: string
    """
    with open("./gits/HEAD.txt", "rb") as f:
        return f.read()


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


def init():
    """
    Initials the gits folder in master branch
    """
    if is_repo():
        print "Alredy a Gits repository"
        return

    os.mkdir("gits")
    os.mkdir("gits/branches")
    os.mkdir("gits/refs")
    os.mkdir("gits/index")
    with open("gits/HEAD.txt", "wb") as f:
        f.write("master")


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


def main():
    if len(sys.argv) == 1:
        print "Gits by Nadav"
        exit()

    if sys.argv[1] == "init":
        init()
        print "Done"

    if not os.path.isdir("gits"):
        print "Not a Gits repository"
        exit()

    cur_branch = get_cur_branch()
    cur_commit = get_cur_commit(cur_branch)

    if sys.argv[1] == "status":
        core_functions.status(cur_branch, cur_commit)

    if sys.argv[1] == "add":
        add_file(sys.argv[2])

    if sys.argv[1] == "commit":
        core_functions.commit(cur_branch, sys.argv[2])

    if sys.argv[1] == "log":
        log = branch.get_log(cur_branch)
        print log
        if log == ['']:
            print "There are no commits yes!"
            exit()
        print "\r\nLog of branch {}\r\n".format(cur_branch)
        for line in log:
            print "\t" + "  ".join(line.split("|")[::-1])
        exit()

    if sys.argv[1] == "checkout":
        if len(sys.argv) == 3:
            move_branch(sys.argv[2])
        elif len(sys.argv) == 4 and sys.argv[2] == "-b":
            branch.create_new_branch(cur_branch, sys.argv[3])
            move_branch(sys.argv[3])
        else:
            raise Exception()

    if sys.argv[1] == "branch":
        branches = glob.glob("gits/branches/*")
        print "Branches:"
        for i in branches:
            print "\t" + os.path.basename(i)

if __name__ == '__main__':
    main()
