#!/bin/python3

from subprocess import Popen, check_output
from os.path import exists
from copy import deepcopy

import time
import sys
import os

yes = True  # there's absolutely
no  = False # no need to do this.

home = os.getenv("HOME")
dirs = []
sys.stdout.write("\x1b[0;1;93m")

if not exists("/var/lib/yellowpkg/installed"):
    if os.getuid() == 0:
        os.system("\
mkdir -p /var/lib/yellowpkg\
echo > /var/lib/yellowpkg/installed;\
chmod -R 1777 /var/lib/yellowpkg;\
")
    else:
        sys.stderr.write("\x1b[0;1;31mYellowpkg depends on a file called /var/lib/yellowpkg/installed,\
with special permissions. Please run yellowpkg once as root to create this file.\x1b[0m")
        sys.exit(1)

# /**********************************
# *   PARSING PACKAGE DIRECTORIES   *
# **********************************/

# XDG_DATA_DIRS is the place for /usr/share-related shit, but it usually
# doesn't exist on a minimal GNU/Linux install, so you can't consider it
# portable.

for dire in ('/usr/share/yellowpkg/pkgs', "/var/lib/yellowpkg/pkgs", home+'/.local/share/yellowpkg/pkgs'):
    if exists(dire) and dire not in dirs:
        dirs = [dire]+dirs

if exists("/etc/yellowpkg.conf"):
    f = open("/etc/yellowpkg.conf")
    c = f.read()
    f.close()
    r = no
    for line in c.splitlines():
        if line.strip().startswith("#"):
            continue # comment, like this one, except they need to be on their
                     # own line, like this one.

        if line.strip().lower() == "[dirs]":
            r = yes
        elif line.strip().startswith('['):
            r = no
        else:
            dire = line.replace("$HOME", home)
            if exists(dire) and dire not in dirs:
                dirs = [dire]+dirs

if exists(home+"/.config/yellowpkg.conf"):
    f = open(home+"/.config/yellowpkg.conf")
    c = f.read()
    f.close()
    r = no
    for line in c.splitlines():
        if line.strip().startswith("#"):
            continue

        if line.strip().lower() == "[dirs]":
            r = yes
        elif line.strip().startswith('['):
            r = no
        else:
            dire = line.replace("$HOME", home)
            if exists(dire) and dire not in dirs:
                dirs = [dire]+dirs

# /***********************************
# *         ARGUMENT PARSING         *
# ***********************************/

args = deepcopy(sys.argv)
del args[0]
packages = []
flags = []
options = {}
action = "help"
ha = no
i = 0

while i < len(args):
    arg = args[i]
    if arg.startswith('-'): # Some sort of option
        if arg.startswith('--'): # Long option
            if '=' in arg:
                v = no
                k = ""
                c = ""
                for l in arg[2:]:
                    if v:
                        c += l
                    else:
                        if l == '=':
                            v = yes
                        else:
                            k += l
                options[k] = c
            else:
                arg = arg[2:] # remove the --
                if arg not in flags:
                    flags += [arg]
        else:
            for l in arg[1:]:
                flags += l
    elif not ha:
        ha = yes
        action = arg
    else:
        packages += [arg]
    i += 1

actions = ['help', 'install', 'info']
vflags = ['verbose', 'v', 'ignore-depends', 'help', 'h', 'version', 'force']
voptions = []
odoc = {}
adoc = {
    "help": "Prints help for the selected action.",
    "install": "Install a package.",
    "info": "Show details about a package."
}
fdoc = {
    "verbose": "Print extra detail about what the program is doing.",
    "v": "Same as --verbose.",
    "ignore-depends": "Ignore all dependencies. THIS IS A BAD IDEA. DO \x1b[4mNOT\x1b[24m USE IT UNLESS YOU NEED TO.",
    "help": "Print this help text and exit.",
    "h": "Same as --help",
    "version": "Print the program version and exit.",
    "force": "Force-clean the install directory for the packages. This should only be used if a package failed to compile \
or install properly, and ypkg won't continue until you remove the source directory. \
Please don't go randomly using this flag, because ypkg is still under development and \
if two processes try to install the same package at almost the same time it can lead \
to unintended side-effects."    
}

def padright(s, w):
    if len(s) > w:
        return s
    return s + (' ' * (w - len(s)))

#print((packages, flags))

def F_help(stream=sys.stdout):
    n = sys.argv[0] # The name of the executable
    stream.write("""\
Usage:
    %s [OPTION…] ACTION [PACKAGE…]
    
Allowed options:
""" % (n))
    for opt in voptions:
        stream.write(padright("    --"+opt+'=VALUE ', 21) + odoc[opt] + "\n")
    for fla in vflags:
        if len(fla) == 1:
            m = "    -"
        else:
            m = "    --"
        stream.write(padright(m+fla, 21) + fdoc[fla] + "\n")
    stream.write("""
Known actions:
""")
    for act in actions:
        stream.write(padright("    "+act+": ", 21) + adoc[act] + "\n")
    stream.write("\x1b[0m")

print("""\
               #            
 m   m  mmmm   #   m   mmmm 
 "m m"  #" "#  # m"   #" "# 
  #m#   #   #  #"#    #   # 
  "#    ##m#"  #  "m  "#m"# 
  m"    #              m  # 
 ""     "               ""
Version 0.1 for Yellow-PRE1
""")

if action not in actions:
    sys.stderr.write("\x1b[1;31mError: unknown action %s.\n" % action)
    F_help(sys.stderr)
    sys.exit(1)
for flg in flags:
    if flg not in vflags:
        if len(flg) == 1:
            m = '-'
        else:
            m = '--'
        sys.stderr.write("\x1b[1;31mError: unknown option %s. Run %s --help for a list of options.\x1b[0m\n" % (m+flg, sys.argv[0]))
        sys.exit(1)
    if flg in ['h', 'help']:
        F_help()
        sys.exit(0)
    if flg in ['version']:
        print("""\x1b[93m\
               #            
 m   m  mmmm   #   m   mmmm 
 "m m"  #" "#  # m"   #" "# 
  #m#   #   #  #"#    #   # 
  "#    ##m#"  #  "m  "#m"# 
  m"    #              m  # 
 ""     "               ""
Version 0.1 for Yellow-PRE1

Copyright 2021 linux_kettle.
This program is free software, you are
free to modify and/or distribute it
under the GNU General Public License,
version 3 or later.

You should have recieved a copy of the
GPL with this program. If not, you can
get it at https://gnu.org/licenses/.
\x1b[0m""")
        sys.exit(0)
    if flg in ['ignore-depends']:
        sys.stderr.write("\x1b[1;31m\
Warning: It is absolutely \x1b[4mNOT\x1b[24m reccommended to use --ignore-depends.\n\
This is because when a package depends on another, it's usually for\n\
a very good reason and the package won't compile without it.\x1b[1;93m\n")
        
if action == 'help':
    if len(packages):
        for action in packages:
            if action in actions:
                sys.stdout.write(padright("\x1b[1;93m%s" % sys.argv[0] + " " + action + " ", 25) + adoc[action] + "\n")
            else:
                sys.stderr.write("\x1b[1;31mError: unknown action %s.\x1b[93m\n" % action)
    else:
        F_help()
        sys.exit(0)

# /***********************************
# *       DEPENDENCY RESOLVING       *
# ***********************************/

def gfc(pkg):
    if len(pkg) < 5:
        print("Warning: All package names should be at least 5 characters.")
        return pkg[0]   # We're on thin ice here, ignore the 'lib' part no matter what.
    if pkg[0:3] == "lib":
        return pkg[0:4] # It isn't a problem now, but as Debian apt has shown,
    else:               # there are a lot of packages starting with 'lib', so
        return pkg[0]   # we need to group those separately.

if not len(packages):
    print("Warning: no packages provided. Exiting...")
    sys.exit(0)

print()
print("\x1b[32m=> Resolving dependencies... \x1b[93m")
pm = {}

def Tstr(t):
    if len(t):
        o = str(t[0])
        if len(t) > 1:
            for i in t[1:]:
                o += ", " + str(i)
        return str(o)
    return "(Empty list)"

def build(pkg, callerstack=()):
    global pm
    if pkg in [""]:
        return

    try:
        __ = pm[pkg]
    except KeyError:
        pm[pkg] = {
            "Name": pkg,
            "Description": "No description was provided",
            "Architecture": "any",
            "Version": "1.0",
            "Depends": [],
            "Url": "http://doesnt.exist/the_package_you_are_installing_has_no_url",
            "Install": "yellowinstall\n"
        }
    else:
        return
    
    for d in dirs:
        if exists(d + "/" + gfc(pkg) + "/" + pkg):
            f = open(d + "/" + gfc(pkg) + "/" + pkg)
            c = f.read()
            f.close()
            section = "[Meta]"
            for line in c.splitlines():
                line = line.strip()
                if line == "" and section != "[Description]":
                    continue
                if line.startswith("#") or line.startswith(";"):
                    continue
                if line.startswith("[") and line.endswith("]"):
                    section = line
                    continue
                
                if section == "[Meta]":
                    k = ""
                    v = ""
                    s = no
                    for c in line:
                        if c == "=":
                            s = yes
                            continue
                        
                        if s:
                            v += c
                        else:
                            k += c
                    pm[pkg][k] = v
                elif section == "[Description]":
                    if pm[pkg]['Description'] == "No description was provided":
                        pm[pkg]['Description'] = line
                    else:
                        pm[pkg]['Description'] += "\n" + line
                elif section == "[Depends]":
                    if 'ignore-depends' not in flags:
                        packages.append(line)
                        pm[pkg]["Depends"].append(line)
                        build(line, callerstack + (pkg,))
                elif section == "[Install]":
                    if pm[pkg]['Install'] == "yellowinstall\n":
                        pm[pkg]['Install'] = line + "\n"
                    else:
                        pm[pkg]['Install'] += line + "\n"
                else:
                    print("Ignoring unknown section %s in file %s." % (section, d + "/" + gfc(pkg) + "/" + pkg))
            break
    else:
        sys.stderr.write("\x1b[1;31mError: couldn't find package %s.\x1b[0m\n" % pkg)
        if len(callerstack):
            sys.stderr.write("(Depended on by these packages: %s)\n" % Tstr(callerstack))
        sys.exit(2)

for pkg in packages:
    build(pkg)

def MTstr(t):
    T = list(t)
    for i in range(0, len(T)):
        T[i] = "%s(%s)" % (T[i], pm[T[i]]["Name"])
    return Tstr(T)

if action != "install":
    if action == "info":
        print()
        for pkg in packages:
            print("\x1b[36m=== %s ===\x1b[0;1m" % pkg)
            m = pm[pkg]
            for i in m:
                if i not in ["Depends", "Description", "Install"]:
                    print("- "+padright(i + ": ", 20) + str(m[i]))
                else:
                    continue
            if len(m["Depends"]):
                print("- Needs these other packages: " + Tstr(m['Depends']))
            print("\x1b[0;1;94m")
            print(m["Description"])
            print("\x1b[93m")
    sys.exit(0)

# /**********************************
# *   CHECKING OTHER REQUIREMENTS   *
# **********************************/
print("\x1b[32m=> The following packages will be installed: \x1b[93m\n")

if 'verbose' in flags or 'v' in flags:
    for pkg in packages:
        print("\x1b[36m=== %s ===\x1b[0;1m" % pkg)
        m = pm[pkg]
        for i in m:
            if i not in ["Depends", "Description", "Install"]:
                print("- "+padright(i + ": ", 20) + str(m[i]))
            else:
                continue
        if len(m["Depends"]):
            print("- Needs these other packages: " + Tstr(m['Depends']))
        print("\x1b[0;1;94m")
        print(m["Description"])
        print("\x1b[93m")
else:
    print(MTstr(packages))
    print()

i = input("Is this OK? [Y/n]: ")
if i.lower().startswith("y") or i == "":
    pass
else:
    print("Cancelled operation.")
    sys.exit(2)

u = (check_output(["uname", "-m"])).decode('utf-8').strip()

arches = (u, "any")
if u in ['x86_64', 'amd64']:
    # Goodness knows what people will put for architecture!
    arches = ('x86_64', 'x64', 'amd64', 'i386', 'i686', 'i?86', 'any')
elif u == ['x86'] or (u.startswith('i') and u.endswith('86')):
    arches = ('x86', 'i386', 'i686', 'i?86', 'any')

print("\n\x1b[32m=> Checking package requirements... \x1b[93m")

for pkg in pm:
    a = pm[pkg]["Architecture"].split(",")
    for A in a:
        if A in arches: # Acceptable architecture
            pm[pkg]["ma"] = A
            break
    else: # No matching architectures
        sys.stderr.write("\n\x1b[31mError: package %s doesn't work on any of these architectures: %s\x1b[0m\n" % (
            pkg, Tstr(arches)
        ))
        sys.exit(3)

print("\x1b[92m   All requirements are satisfied.\n\x1b[32m=> Downloading packages... \x1b[93m")

subprocesses = []
tmp = "/tmp/ypkg_" + str(os.getuid())
os.system('mkdir -p '+tmp)

def rms(s):
    if s.endswith("/"):
        return s[:-1]
    return s

# /**********************************
# *        DOWNLOADING FILES        *
# **********************************/

for pkg in pm: # How many times must I type this?
    # Doing my best to avoid accidental shell injection.
    url = pm[pkg]["Url"].replace("$a", pm[pkg]["ma"]).replace("$v", pm[pkg]["Version"]).replace("'", '_')
    print("Downloading %s..." % pkg)
    filename = os.path.basename(rms(url))
    pm[pkg]["sf"] = tmp + "/" + filename
    # Without the -q, wget fills the terminal with strange shit.
    subprocesses.append([Popen(['wget', url, '-qO', tmp + "/" + filename]), pkg])

while len(subprocesses): # Wait until all download jobs are finished.
    i = 0
    while i < len(subprocesses):
        p = subprocesses[i][0]
        if p.poll() is not None: # The subprocess has finished
            if p.poll() == 0:
                print("Downloaded %s." % subprocesses[i][1])
                del subprocesses[i]
            else:
                sys.stderr.write("Error: failed to retrieve file %s.")
                sys.exit(4)
        else: # Process is still going
            i += 1

print("\x1b[92m   Packages have been downloaded.\n\x1b[32m=> Extracting packages... \x1b[93m")

i = 0
while i < len(packages): # Quite a lot, by the looks of it :~)
    pkg = packages[i]
    sf = pm[pkg]["sf"]
    d = tmp + "/" + pkg
    if exists(d):
        if 'force' in flags:
            os.system("rm -rf '"+d+"'")
        else:
            sys.stderr.write("\x1b[93mSkipping extract and install of already extracted package %s. \
Re-run this command with --force to remove the directory and re-install the package.\n" % pkg)
            del pm[pkg]
            del packages[i]
            continue
    if 'verbose' in flags or 'v' in flags:
        print("Extracting %s to %s..." % (sf, d))
    Popen(['mkdir', '-p', d]).communicate();
    if sf.endswith(".zip"):
        if os.system("cd '" + d + "'; unzip -qq '"+sf+"'") != 0:
            sys.stderr.write("\x1b[31mError: Couldn't extract %s. Cancelling.\x1b[0m\n" % sf)
            sys.exit(5)
    elif sf.endswith(".tgz") or sf.endswith(".tar.gz") or sf.endswith(".tar.bz2") or sf.endswith(".tar.xz"):
        # Tarball, the tar command will handle the compression
        if os.system("cd '" + d + "'; tar -xf '"+sf+"'") != 0:
            sys.stderr.write("\x1b[31mError: Couldn't extract %s. Cancelling.\x1b[0m\n" % sf)
            sys.exit(5)
    else:
        sys.stderr.write("\x1b[31mError: Couldn't determine the file format of %s. \
(it has to be .tgz, .tar.gz, .tar.xz, .tar.bz2 or .zip, and .zip files \
depend on the program unzip). Cancelling.\x1b[0m\n" % sf)
        sys.exit(5)
    i += 1

print("\x1b[92m   Packages have been extracted.\n\x1b[32m=> Installing packages... \x1b[93m")

# /**********************************
# *       INSTALLING PACKAGES       *
# **********************************/

isps = {}

# That's a sweet reverse for right there:
i = len(packages)

while i > 0:
    i -= 1
    pkg = packages[i]
    for dependency in pm[pkg]["Depends"]:
        while isps[dependency].poll() is None:
            # The package hasn't finished installing yet
            time.sleep(0.5)
        if isps[dependency].poll():
            sys.stderr.write("\x1b[31mError: package %s failed to install. Cancelling.\x1b[0m\n" % dependency)
            sys.exit(6)
        else:
            print("\x1b[92m   Finished installing %s.\x1b[93m" % dependency)
            os.system("echo '%s' >> /var/lib/yellowpkg/installed" % dependency + "/" + pm[dependency]["Version"])
            del isps[dependency]
    print("\x1b[32m > Installing %s... \x1b[93m" % pkg)
    d = tmp + "/" + pkg
    _i = open(d + "/.YPKG_INSTALL", 'w')
    _i.write(pm[pkg]["Install"])
    _i.close()
    isps[pkg] = Popen(['sh', '-c', "cd '" + d + "'; . ./.YPKG_INSTALL"])

while len(isps):
    i = 0
    while i < len(isps):
        p = isps[list(isps)[i]]
        if p.poll() is not None:
            if p.poll() == 0:
                print("\x1b[92m   Finished installing %s.\x1b[93m" % list(isps)[i])
                os.system("echo '%s' >> /var/lib/yellowpkg/installed" % list(isps)[i] + "/" + pm[list(isps)[i]]["Version"])
                del isps[list(isps)[i]]
            else:
                sys.stderr.write("\x1b[31mError: package %s failed to install. Cancelling.\x1b[0m\n" % list(isps)[i])
                sys.exit(6)
        else:
            time.sleep(0.5)
            i += 1

print("\x1b[92m   All packages are now happily on your computer.\n\x1b[32m=> Cleaning up... \x1b[93m")
os.system("rm -rf " + tmp)

print("""\x1b[32m\
                      m
 m   m   mmm   m   m  #
 "m m"  "   #  "m m"  #
  #m#   m\"""#   #m#  "
  "#    "mm"#   "#    #
  m"            m"     
 ""            ""      
All packages have successfully been installed.\x1b[0m""")

