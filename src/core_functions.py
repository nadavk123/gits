import os
import hashlib
import glob
import tree
import file_core
import branch
import shutil


#########
# PRIVATE#
#########

def sha1(path):
    with open(path, "rb") as f:
        file_hash = hashlib.sha1(f.read())
    return file_hash.hexdigest()


def get_added_files():
    if not os.path.exists("gits/add.txt"):
        return {}
    with open("gits/add.txt", "rb") as f:
        return {i: sha1(i) for i in f.read().split("\r\n") if os.path.exists(i)}


def get_added_removed():
    if not os.path.exists("gits/add.txt"):
        return {}
    with open("gits/add.txt", "rb") as f:
        return {i for i in f.read().split("\r\n") if not os.path.exists(i)}

def reset_add():
    os.remove("gits/add.txt")


def recursive_glob(lst=[], cur="."):
    new = ["{}".format(i) for i in glob.glob("{}/*".format(cur))]
    try:
        new.remove(".\\gits")
    except:
        pass

    lst += new
    for name in new:
        if os.path.isdir(name):
            lst.remove(name)
            recursive_glob(lst, name)

    return lst


########
# PUBLIC#
########

def status(name, ref):
    lst1 = recursive_glob()
    lst2 = tree.get_files_ref(ref)
    new = []
    moved = []
    renamed = []
    copied = []
    untracked = []
    removed = []
    added_deleted = []
    modified = []
    added_modified = []
    dict1 = {i: sha1(i) for i in lst1}
    dict1_keys = dict1.keys()
    dict1_values = dict1.values()
    dict2 = {i.split("|")[1]: i.split("|")[2] for i in lst2}
    dict22 = {i.split("|")[2]: i.split("|")[1] for i in lst2}
    dict2_keys = dict2.keys()
    dict2_values = dict2.values()
    dict3 = get_added_files()
    for i in dict1_keys:
        if i not in dict2_keys:
            untracked.append(i)
            continue
        if i in dict2_keys:
            if dict1[i] != dict2[i]:
                modified.append(i)

    for i in dict2_keys:
        if i not in dict1_keys:
            removed.append(i)

    for i in dict3.items():
        if i[0] in untracked:
            untracked.remove(i[0])
        if i[0] in removed:
            removed.remove(i[0])
            added_deleted.append(i[0])
            continue
        if i[0] in modified:
            modified.remove(i[0])
            added_modified.append(i[0])
            continue
        if i[1] in dict2.values():
            if not dict22[i[1]] in removed:
                copied.append(i[0])
            elif os.path.dirname(r"{}".format(os.path.realpath(i[0]))) == os.path.dirname(
                    r"{}".format(os.path.realpath(dict22[i[1]]))):
                renamed.append(i[0])
                removed.remove(dict22[i[1]])
            else:
                moved.append(i[0])
                removed.remove(dict22[i[1]])

        else:
            new.append(i[0])

    for i in get_added_removed():
        added_deleted.append(i)
        removed.remove(i)

    print "On branch {}\r\n".format(name)
    # In current commit
    if len(added_modified) > 0:
        print "\r\nadded modified:\r\n\t{}".format("\r\n\t".join(added_modified))
    if len(new) > 0:
        print "\r\nnew:\r\n\t{}".format("\r\n\t".join(new))
    if len(renamed) > 0:
        print "\r\nrenamed:\r\n\t{}".format("\r\n\t".join(renamed))
    if len(moved) > 0:
        print "\r\nmoved:\r\n\t{}".format("\r\n\t".join(moved))
    if len(added_deleted) > 0:
        print "\r\nadded deleted:\r\n\t{}".format("\r\n\t".join(added_deleted))

    # Out of current commit
    if len(modified) > 0:
        print "\r\nmodified:\r\n\t{}".format("\r\n\t".join(modified))
    if len(removed) > 0:
        print "\r\ndeleted:\r\n\t{}".format("\r\n\t".join(removed))
    if len(untracked) > 0:
        print "\r\nuntracked:\r\n\t{}".format("\r\n\t".join(untracked))


def commit(branch_name, description):
    files = recursive_glob()
    for i in files:
        file_core.index_file(i)

    new_ref = tree.create_ref(files)

    branch.update(branch_name, new_ref, description)
    reset_add()
    return True


def reset_repo():
    files_to_delete = glob.glob("*")
    files_to_delete.remove("gits")
    for file in files_to_delete:
        try:
            os.remove(file)
        except:
            shutil.rmtree(file)
