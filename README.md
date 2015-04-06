A repo that contains python files for managing a cluster of machines.

To view which machines are available to use, see the issues page (or the repo's [waffle board](https://waffle.io/JasYoung314/CardiffMathsClusterAdmin))

The sysadmin.py file uses [docopt](http://docopt.org/) and should be run with the two following patterns:

```python
    python sysadmin.py [options] <machines>...
    python sysadmin.py [options]
```

The arguments are a list of machines that all the options should be run on.
The names of these machines should be the name specified in .ssh/config file.
For example, if I wanted to run `[options]` on a machine `Foo`, the command would be:

```python
    python sysadmin.py [options] Foo
```

And Foo has already been entered in to the `.ssh/config` file like so:

```
host Foo
    hostname 192.168.0.1
    user Bar
```

If no machine is entered, the script will automatically look for the file `sysadmin.yml` in the same directory. See the existing yaml database for an example.

