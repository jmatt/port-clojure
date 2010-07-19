#!/usr/bin/python

"""Update macport's sources.conf and create symlinks to this git repository.

Usage: python port-clojure-conf.py [options]

Options:
  -s, --sources-file       Full path to the sources.conf file
  -l, --local-dir          Directory to install local Portsfile Repositories
  -c, --copy               Copy Portsfiles instead of symlinking
  -d, --debug              Print debug information

Notes:
sudo may be required to edit the sources.conf file.

If you already have a local ports directory then you simply need to move or symlink the clojure-devel and clojure-contrib-devel directories to your local ports directory.

Further information:
http://guide.macports.org/#development.local-repositories
http://github.com/jmatt/port-clojure
"""

__author__  = "J. Matt Peterson (jmatt@jmatt.org)"
__version__ = "0.2"
__date__    = "$Date: 2010/07/17 19:11:11 $"
__license__ = "EPL"

import sys
import shutil
import os
import getopt

def update_sources_file(sources_file, local_dir, debug):
    if debug:
        print("update_sources_file.")
    new_local_dir = """file://""" + local_dir
    if debug:
        print("  adding this local directory to MacPort's sources.conf " + new_local_dir)
    try:
        sources_file_backup = sources_file + "~"
        shutil.move(sources_file, sources_file_backup)
        new_sources = open(sources_file, "w")
        old_sources = open(sources_file_backup, "r")
        i = 0
        add_once = True
        for line in old_sources:
            if add_once and (line.strip().startswith("rsync:") or line.strip().startswith("file:")):
                if debug:
                    print("  inserting local directory at line number " + str(i))
                    print("  current line = " + line)
                new_line = new_local_dir + "\n"
                if line != new_line: # do not add it, if it already exists.
                    new_sources.write(new_line)
                    if debug:
                        print("  duplicate local directory at line number " + str(i))
                new_sources.write(line)
                add_once = False
            else:
                new_sources.write(line)
            i = i + 1
    except:
        try:
            old_sources.close()
            shutil.move(sources_file_backup, sources_file)
        except:
            pass #sometimes variables are not defined yet.
        print("Problem updating sources file! You may need to use sudo.")
        return False
    finally:
        try:
            old_sources.close()
            new_sources.close()
        except:
            pass #sometimes there could be an error because variables aren't defined yet.
    return True

def make_directories(local_dir, debug=False):
    if debug:
        print("make_directories.")
    complete_local_dir = os.path.join(local_dir, "lang")
    os.system("mkdir -p " + complete_local_dir)
    if debug:
        print("  directory created " + os.path.join(local_dir, "lang"))
    return True

def copy_portindex(local_dir, debug=False):
    if debug:
        print("copy_portindex.")
    source_portindex = os.path.abspath("ports/PortIndex")
    source_portindex_quick = os.path.abspath("ports/PortIndex.quick")
    shutil.copy(source_portindex, local_dir)
    shutil.copy(source_portindex_quick, local_dir)
    return True

def link_directories(local_dir, debug=False):
    make_directories(local_dir, debug)
    copy_portindex(local_dir, debug)
    if debug:
        print("link_directories.")
    source_clojure_devel = os.path.abspath("ports/lang/clojure-devel")
    source_clojure_contrib_devel = os.path.abspath("ports/lang/clojure-contrib-devel")
    dest_clojure_devel = os.path.abspath(os.path.join(local_dir, "lang/clojure-devel"))
    dest_clojure_contrib_devel = os.path.abspath(os.path.join(local_dir, "lang/clojure-contrib-devel"))
    if debug:
        print("  clojure-devel path <-- " + source_clojure_devel)
        print("  clojure-devel path --> " + dest_clojure_devel)
        print("  clojure-contrib-devel path <-- " + source_clojure_contrib_devel)
        print("  clojure-contrib-devel path --> " + dest_clojure_contrib_devel)
    if not os.path.exists(dest_clojure_devel):
        os.symlink(source_clojure_devel, dest_clojure_devel)
    elif debug:
        print("  destination clojure-devel path already exists.")
    if not os.path.exists(dest_clojure_contrib_devel):
        os.symlink(source_clojure_contrib_devel, dest_clojure_contrib_devel)
    elif debug:
        print("  destination clojure-contrib-devel path already exists.")
    return True

def copy_directories(local_dir, debug=False):
    make_directories(local_dir, debug)
    copy_portindex(local_dir, debug)
    if debug:
        print("copy_directories.")
    source_clojure_devel = os.path.abspath("ports/lang/clojure-devel")
    source_clojure_contrib_devel = os.path.abspath("ports/lang/clojure-contrib-devel")
    dest_clojure_devel = os.path.abspath(os.path.join(local_dir, "lang/clojure-devel"))
    dest_clojure_contrib_devel = os.path.abspath(os.path.join(local_dir, "lang/clojure-contrib-devel"))
    if debug:
        print("  clojure-devel path <-- " + source_clojure_devel)
        print("  clojure-devel path --> " + dest_clojure_devel)
        print("  clojure-contrib-devel path <-- " + source_clojure_contrib_devel)
        print("  clojure-contrib-devel path --> " + dest_clojure_contrib_devel)
    if not os.path.exists(dest_clojure_devel):
        shutil.copytree(source_clojure_devel, dest_clojure_devel)
    elif debug:
        print("  destination clojure-devel path already exists.")
    if not os.path.exists(dest_clojure_contrib_devel):
        shutil.copytree(source_clojure_contrib_devel, dest_clojure_contrib_devel)
    elif debug:
        print("  destination clojure-devel path already exists.")
    return True

def usage():
    print __doc__

def main(argv):
    debug_option = False
    copy_option = False
    homedir = os.path.expanduser('~')
    sources_file = "/opt/local/etc/macports/sources.conf"
    local_dir = os.path.join(homedir, 'ports')
    try:
        opts, args = getopt.getopt(argv, "hdcs:l:", ["help", "debug", "copy", "sources-file", "local-dir"])
    except getopt.GetoptError:
        usage()
        sys.exit(1)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-d", "--debug"):
            debug_option = True
            print("Printing debug information!")
        elif opt in ("-c", "--copy"):
            copy_option = True
        elif opt in ("-s", "--sources-file"):
            sources_file = str(arg)
        elif opt in ("-l", "--local-dir"):
            local_dir = str(arg)
    result_update_sources_file = update_sources_file(sources_file, local_dir, debug_option)
    if copy_option:
        result_copy_directories = copy_directories(local_dir, debug_option)
        if result_copy_directories and result_update_sources_file:
            print "Completed Successfully!"
    else:
        result_link_directories = link_directories(local_dir, debug_option)
        if result_link_directories and result_update_sources_file:
            print "Completed Successfully!"

if __name__ == "__main__":
    main(sys.argv[1:])
    sys.exit()
