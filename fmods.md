# Table of Contents

* [fmods](#fmods)
  * [FMods](#fmods.FMods)
    * [\_\_init\_\_](#fmods.FMods.__init__)
    * [scan](#fmods.FMods.scan)
    * [print\_list](#fmods.FMods.print_list)
    * [get\_mods\_count](#fmods.FMods.get_mods_count)
    * [get\_mod\_config](#fmods.FMods.get_mod_config)
    * [get\_tmp\_folder](#fmods.FMods.get_tmp_folder)
    * [git\_clone](#fmods.FMods.git_clone)
    * [docker\_build](#fmods.FMods.docker_build)
    * [docker\_remove](#fmods.FMods.docker_remove)
    * [docker\_run](#fmods.FMods.docker_run)
    * [get\_connect\_to\_postresql](#fmods.FMods.get_connect_to_postresql)
    * [setUp](#fmods.FMods.setUp)
    * [tearDown](#fmods.FMods.tearDown)
* [fmods\_test](#fmods_test)

<a name="fmods"></a>
# fmods

Class for work with testing Modules

<a name="fmods.FMods"></a>
## FMods Objects

```python
class FMods(object)
```

Class for load and build environment modules for functional tests

<a name="fmods.FMods.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(path_modules, path_tmp, verbose)
```

Initialising object
Parameters
----------
path_modules : str
    path to modules settings
path_tmp : str
    path to temporary files
verbose : bool
    verbose output

<a name="fmods.FMods.scan"></a>
#### scan

```python
 | scan()
```

Scan subfolders for modules settings (path_modules)

<a name="fmods.FMods.print_list"></a>
#### print\_list

```python
 | print_list()
```

Output the list of modules

<a name="fmods.FMods.get_mods_count"></a>
#### get\_mods\_count

```python
 | get_mods_count()
```

Count of modules

<a name="fmods.FMods.get_mod_config"></a>
#### get\_mod\_config

```python
 | get_mod_config(module_name)
```

Get configuration of module
Parameters
----------
module_name : str
    name of module

<a name="fmods.FMods.get_tmp_folder"></a>
#### get\_tmp\_folder

```python
 | get_tmp_folder(module_name)
```

Get temporary path for module
Parameters
----------
module_name : str
    name of the module

Returns
-------
path:
    temporary path for the module

<a name="fmods.FMods.git_clone"></a>
#### git\_clone

```python
 | git_clone(module_name, config)
```

Clone git repository of module
Parameters
----------
module_name : str
    name of module
config : dictionary
    configuration of module

<a name="fmods.FMods.docker_build"></a>
#### docker\_build

```python
 | docker_build(module_name, config)
```

Build docker container of module
Parameters
----------
module_name : str
    name of module
config : dictionary
    configuration of module

<a name="fmods.FMods.docker_remove"></a>
#### docker\_remove

```python
 | docker_remove(container_name)
```

Remove docker container of module
Parameters
----------
module_name : str
    name of module
config : dictionary
    configuration of module

<a name="fmods.FMods.docker_run"></a>
#### docker\_run

```python
 | docker_run(module_name, config)
```

Run docker container of module
Parameters
----------
module_name : str
    name of module
config : dictionary
    configuration of module

<a name="fmods.FMods.get_connect_to_postresql"></a>
#### get\_connect\_to\_postresql

```python
 | get_connect_to_postresql(module_name)
```

Connect to postgresql database
Attributes
----------
module_name : str
    name of module

<a name="fmods.FMods.setUp"></a>
#### setUp

```python
 | setUp()
```

setUp for UTests

<a name="fmods.FMods.tearDown"></a>
#### tearDown

```python
 | tearDown()
```

tearDown for UTests

<a name="fmods_test"></a>
# fmods\_test

