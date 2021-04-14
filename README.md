# ypkg
A simple, mostly stable package manager for *nix

Most package managers have vast, complicated databases that know exactly why every file on your computer is there, and are populated with thousands of packages you're unlikely to ever need.

ypkg doesn't aim to be one of those package managers. ypkg's job is merely to provide a simple way to add and remove software from your Unix-like computer.

ypkg could be used for many different reasons, but mine is for a lightweight minimal Linux distribution that isn't big enough to need all of those luxuries.

## What it *can* do

ypkg has the basic ability to install packages from small metadata files in `/var/lib/yellowpkg/pkgs`, and it keeps track of dependencies and I will add versioning support. ypkg has a simple colourful command-line interface, for those people who miss the beauty of a X or Wayland desktop, and don't miss the fact that their OS only takes up 4 GB of disk space.

ypkg can give you information about a package and all of the packages it depends on, and usually compiles its packages from source.

The help text looks like this:

```
               #            
 m   m  mmmm   #   m   mmmm 
 "m m"  #" "#  # m"   #" "# 
  #m#   #   #  #"#    #   # 
  "#    ##m#"  #  "m  "#m"# 
  m"    #              m  # 
 ""     "               ""
Version 0.1 for Yellow-PRE1

Usage:
    /usr/bin/ypkg [OPTION…] ACTION [PACKAGE…]
    
Allowed options:
    --verbose        Print extra detail about what the program is doing.
    -v               Same as --verbose.
    --ignore-depends Ignore all dependencies. THIS IS A BAD IDEA. DO NOT USE IT UNLESS YOU NEED TO.
    --help           Print this help text and exit.
    -h               Same as --help
    --version        Print the program version and exit.
    --force          Force-clean the install directory for the packages. This should only be used if a package failed to compile or install properly, and ypkg won't continue until you remove the source directory. Please don't go randomly using this flag, because ypkg is still under development and if two processes try to install the same package at almost the same time it can lead to unintended side-effects.

Known actions:
    help:            Prints help for the selected action.
    install:         Install a package.
    info:            Show details about a package.
```

## You will need

You will need an up-to-date Python interpreter (I recommend 3.9 or later), along with these packages pre-installed:

- GNU Coreutils (or another package that provides those commands)
- You'll need GCC, Binutils, Glibc etc to compile most of the packages (consider those as runtime dependencies)

- wget (absolutely essential for downloading files)

- tar (if you want to be able to use tar packages, note that xz, gz and bz2 support need to be compiled into tar for ypkg to work with them)
- gz (same thing)
- xz (for xzipped tars)
- bzip2 (for bzipped tars)
- unzip (optional, few people zip their source code)

## How to install it

Extract this tarball to somewhere on your computer, and run the `install.sh` script as root, or open it in a text editor if you're sceptical about anything. Then, to test it out, install GNU Hello with this command:

```sh
ypkg install hello
```

as root.