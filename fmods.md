# Table of Contents

* [fmods](#fmods)
  * [FMods](#fmods.FMods)
    * [\_\_init\_\_](#fmods.FMods.__init__)
    * [scan](#fmods.FMods.scan)
    * [printList](#fmods.FMods.printList)
    * [count](#fmods.FMods.count)
    * [getConfig](#fmods.FMods.getConfig)
    * [getTmpFolder](#fmods.FMods.getTmpFolder)
    * [gitClone](#fmods.FMods.gitClone)
    * [getDocker](#fmods.FMods.getDocker)
    * [dockerBuild](#fmods.FMods.dockerBuild)
    * [dockerStatus](#fmods.FMods.dockerStatus)
    * [dockerStart](#fmods.FMods.dockerStart)
    * [dockerStop](#fmods.FMods.dockerStop)
    * [dockerRemove](#fmods.FMods.dockerRemove)
    * [dockerLogs](#fmods.FMods.dockerLogs)
    * [dockerRun](#fmods.FMods.dockerRun)
    * [dockerStatusWaiting](#fmods.FMods.dockerStatusWaiting)
    * [getConnectToPostreSQL](#fmods.FMods.getConnectToPostreSQL)
    * [startAll](#fmods.FMods.startAll)
    * [stopAll](#fmods.FMods.stopAll)
* [\_\_init\_\_](#__init__)
* [src](#src)
* [src.fmods](#src.fmods)
  * [FMods](#src.fmods.FMods)
    * [\_\_init\_\_](#src.fmods.FMods.__init__)
    * [scan](#src.fmods.FMods.scan)
    * [printList](#src.fmods.FMods.printList)
    * [count](#src.fmods.FMods.count)
    * [getConfig](#src.fmods.FMods.getConfig)
    * [getTmpFolder](#src.fmods.FMods.getTmpFolder)
    * [gitClone](#src.fmods.FMods.gitClone)
    * [getDocker](#src.fmods.FMods.getDocker)
    * [dockerBuild](#src.fmods.FMods.dockerBuild)
    * [dockerStatus](#src.fmods.FMods.dockerStatus)
    * [dockerStart](#src.fmods.FMods.dockerStart)
    * [dockerStop](#src.fmods.FMods.dockerStop)
    * [dockerRemove](#src.fmods.FMods.dockerRemove)
    * [dockerLogs](#src.fmods.FMods.dockerLogs)
    * [dockerRun](#src.fmods.FMods.dockerRun)
    * [dockerStatusWaiting](#src.fmods.FMods.dockerStatusWaiting)
    * [getConnectToPostreSQL](#src.fmods.FMods.getConnectToPostreSQL)
    * [startAll](#src.fmods.FMods.startAll)
    * [stopAll](#src.fmods.FMods.stopAll)
* [src.test](#src.test)
* [src.test.fmods\_test](#src.test.fmods_test)

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
 | __init__(pathModules, pathTmp, verbose)
```

Initialising object
Parameters
----------
pathModules : str
    path to modules settings
pathTmp : str
    path to temporary files
verbose : bool
    verbose output

<a name="fmods.FMods.scan"></a>
#### scan

```python
 | scan()
```

Scan subfolders for modules settings (path_modules)

<a name="fmods.FMods.printList"></a>
#### printList

```python
 | printList()
```

Output the list of modules

<a name="fmods.FMods.count"></a>
#### count

```python
 | count()
```

Count of modules

<a name="fmods.FMods.getConfig"></a>
#### getConfig

```python
 | getConfig(moduleName)
```

Get configuration of module
Parameters
----------
moduleName : str
    name of module

<a name="fmods.FMods.getTmpFolder"></a>
#### getTmpFolder

```python
 | getTmpFolder(moduleName)
```

Get temporary path for module
Parameters
----------
moduleName : str
    name of the module

Returns
-------
path:
    temporary path for the module

<a name="fmods.FMods.gitClone"></a>
#### gitClone

```python
 | gitClone(moduleName)
```

Clone git repository of module
Parameters
----------
moduleName : str
    name of module
config : dictionary
    configuration of module

<a name="fmods.FMods.getDocker"></a>
#### getDocker

```python
 | getDocker(moduleName)
```

Get parameters of module for docker
Parameters
----------
moduleName : str
    name of module
Returns
-------
containerName
    a name of docker container
config
    a dictionary of strings
ok
    success

<a name="fmods.FMods.dockerBuild"></a>
#### dockerBuild

```python
 | dockerBuild(moduleName)
```

Build docker container of module
Parameters
----------
moduleName : str
    name of module
config : dictionary
    configuration of module

<a name="fmods.FMods.dockerStatus"></a>
#### dockerStatus

```python
 | dockerStatus(moduleName)
```

Status docker container of module
Parameters
----------
moduleName : str
    name of module

<a name="fmods.FMods.dockerStart"></a>
#### dockerStart

```python
 | dockerStart(moduleName)
```

Start docker container of module
Parameters
----------
moduleName : str
    name of module

<a name="fmods.FMods.dockerStop"></a>
#### dockerStop

```python
 | dockerStop(moduleName)
```

Stop docker container of module
Parameters
----------
moduleName : str
    name of module

<a name="fmods.FMods.dockerRemove"></a>
#### dockerRemove

```python
 | dockerRemove(moduleName)
```

Remove docker container of module
Parameters
----------
moduleName : str
    name of module

<a name="fmods.FMods.dockerLogs"></a>
#### dockerLogs

```python
 | dockerLogs(moduleName)
```

Output logs of docker container of module
Parameters
----------
moduleName : str
    name of module

<a name="fmods.FMods.dockerRun"></a>
#### dockerRun

```python
 | dockerRun(moduleName)
```

Run docker container of module
Parameters
----------
moduleName : str
    name of module

<a name="fmods.FMods.dockerStatusWaiting"></a>
#### dockerStatusWaiting

```python
 | dockerStatusWaiting(moduleName, status, timeout=120)
```

Waiting docker container status
Parameters
----------
moduleName : str
    name of module
status : str
    status
timeout : int
    timeout in seconds

<a name="fmods.FMods.getConnectToPostreSQL"></a>
#### getConnectToPostreSQL

```python
 | getConnectToPostreSQL(moduleName)
```

Connect to postgresql database
Attributes
----------
moduleName : str
    name of module

<a name="fmods.FMods.startAll"></a>
#### startAll

```python
 | startAll()
```

setUp for UTests

<a name="fmods.FMods.stopAll"></a>
#### stopAll

```python
 | stopAll()
```

tearDown for UTests

<a name="__init__"></a>
# \_\_init\_\_

<a name="src"></a>
# src

<a name="src.fmods"></a>
# src.fmods

Class for work with testing Modules

<a name="src.fmods.FMods"></a>
## FMods Objects

```python
class FMods(object)
```

Class for load and build environment modules for functional tests

<a name="src.fmods.FMods.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(pathModules, pathTmp, verbose)
```

Initialising object
Parameters
----------
pathModules : str
    path to modules settings
pathTmp : str
    path to temporary files
verbose : bool
    verbose output

<a name="src.fmods.FMods.scan"></a>
#### scan

```python
 | scan()
```

Scan subfolders for modules settings (path_modules)

<a name="src.fmods.FMods.printList"></a>
#### printList

```python
 | printList()
```

Output the list of modules

<a name="src.fmods.FMods.count"></a>
#### count

```python
 | count()
```

Count of modules

<a name="src.fmods.FMods.getConfig"></a>
#### getConfig

```python
 | getConfig(moduleName)
```

Get configuration of module
Parameters
----------
moduleName : str
    name of module

<a name="src.fmods.FMods.getTmpFolder"></a>
#### getTmpFolder

```python
 | getTmpFolder(moduleName)
```

Get temporary path for module
Parameters
----------
moduleName : str
    name of the module

Returns
-------
path:
    temporary path for the module

<a name="src.fmods.FMods.gitClone"></a>
#### gitClone

```python
 | gitClone(moduleName)
```

Clone git repository of module
Parameters
----------
moduleName : str
    name of module
config : dictionary
    configuration of module

<a name="src.fmods.FMods.getDocker"></a>
#### getDocker

```python
 | getDocker(moduleName)
```

Get parameters of module for docker
Parameters
----------
moduleName : str
    name of module
Returns
-------
containerName
    a name of docker container
config
    a dictionary of strings
ok
    success

<a name="src.fmods.FMods.dockerBuild"></a>
#### dockerBuild

```python
 | dockerBuild(moduleName)
```

Build docker container of module
Parameters
----------
moduleName : str
    name of module
config : dictionary
    configuration of module

<a name="src.fmods.FMods.dockerStatus"></a>
#### dockerStatus

```python
 | dockerStatus(moduleName)
```

Status docker container of module
Parameters
----------
moduleName : str
    name of module

<a name="src.fmods.FMods.dockerStart"></a>
#### dockerStart

```python
 | dockerStart(moduleName)
```

Start docker container of module
Parameters
----------
moduleName : str
    name of module

<a name="src.fmods.FMods.dockerStop"></a>
#### dockerStop

```python
 | dockerStop(moduleName)
```

Stop docker container of module
Parameters
----------
moduleName : str
    name of module

<a name="src.fmods.FMods.dockerRemove"></a>
#### dockerRemove

```python
 | dockerRemove(moduleName)
```

Remove docker container of module
Parameters
----------
moduleName : str
    name of module

<a name="src.fmods.FMods.dockerLogs"></a>
#### dockerLogs

```python
 | dockerLogs(moduleName)
```

Output logs of docker container of module
Parameters
----------
moduleName : str
    name of module

<a name="src.fmods.FMods.dockerRun"></a>
#### dockerRun

```python
 | dockerRun(moduleName)
```

Run docker container of module
Parameters
----------
moduleName : str
    name of module

<a name="src.fmods.FMods.dockerStatusWaiting"></a>
#### dockerStatusWaiting

```python
 | dockerStatusWaiting(moduleName, status, timeout=120)
```

Waiting docker container status
Parameters
----------
moduleName : str
    name of module
status : str
    status
timeout : int
    timeout in seconds

<a name="src.fmods.FMods.getConnectToPostreSQL"></a>
#### getConnectToPostreSQL

```python
 | getConnectToPostreSQL(moduleName)
```

Connect to postgresql database
Attributes
----------
moduleName : str
    name of module

<a name="src.fmods.FMods.startAll"></a>
#### startAll

```python
 | startAll()
```

setUp for UTests

<a name="src.fmods.FMods.stopAll"></a>
#### stopAll

```python
 | stopAll()
```

tearDown for UTests

<a name="src.test"></a>
# src.test

<a name="src.test.fmods_test"></a>
# src.test.fmods\_test

