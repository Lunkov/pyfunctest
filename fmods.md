# Table of Contents

* [pylint-recursive](#pylint-recursive)
  * [check](#pylint-recursive.check)
* [fmods](#fmods)
  * [FMods](#fmods.FMods)
    * [\_\_init\_\_](#fmods.FMods.__init__)
    * [scan](#fmods.FMods.scan)
    * [printList](#fmods.FMods.printList)
    * [count](#fmods.FMods.count)
    * [getConfig](#fmods.FMods.getConfig)
    * [getTmpFolder](#fmods.FMods.getTmpFolder)
    * [startAll](#fmods.FMods.startAll)
    * [stopAll](#fmods.FMods.stopAll)
* [minio](#minio)
  * [MinIO](#minio.MinIO)
    * [\_\_init\_\_](#minio.MinIO.__init__)
    * [getConnect](#minio.MinIO.getConnect)
* [\_\_init\_\_](#__init__)
* [mysql](#mysql)
  * [MySQL](#mysql.MySQL)
    * [\_\_init\_\_](#mysql.MySQL.__init__)
    * [getConnect](#mysql.MySQL.getConnect)
* [git](#git)
  * [GIT](#git.GIT)
    * [\_\_init\_\_](#git.GIT.__init__)
    * [clone](#git.GIT.clone)
* [postgre](#postgre)
  * [Postgre](#postgre.Postgre)
    * [\_\_init\_\_](#postgre.Postgre.__init__)
    * [getConnect](#postgre.Postgre.getConnect)
* [rabbitmq](#rabbitmq)
  * [RabbitMQ](#rabbitmq.RabbitMQ)
    * [\_\_init\_\_](#rabbitmq.RabbitMQ.__init__)
    * [getConnect](#rabbitmq.RabbitMQ.getConnect)
* [ftp](#ftp)
  * [FTP](#ftp.FTP)
    * [\_\_init\_\_](#ftp.FTP.__init__)
    * [getConnect](#ftp.FTP.getConnect)
* [docker](#docker)
  * [Docker](#docker.Docker)
    * [\_\_init\_\_](#docker.Docker.__init__)
    * [isDocker](#docker.Docker.isDocker)
    * [build](#docker.Docker.build)
    * [status](#docker.Docker.status)
    * [start](#docker.Docker.start)
    * [stop](#docker.Docker.stop)
    * [remove](#docker.Docker.remove)
    * [logs](#docker.Docker.logs)
    * [run](#docker.Docker.run)
    * [statusWaiting](#docker.Docker.statusWaiting)
* [src](#src)
* [src.fmods](#src.fmods)
  * [FMods](#src.fmods.FMods)
    * [\_\_init\_\_](#src.fmods.FMods.__init__)
    * [scan](#src.fmods.FMods.scan)
    * [printList](#src.fmods.FMods.printList)
    * [count](#src.fmods.FMods.count)
    * [getConfig](#src.fmods.FMods.getConfig)
    * [getTmpFolder](#src.fmods.FMods.getTmpFolder)
    * [startAll](#src.fmods.FMods.startAll)
    * [stopAll](#src.fmods.FMods.stopAll)
* [src.test](#src.test)
* [src.test.mysql\_test](#src.test.mysql_test)
* [src.test.docker\_test](#src.test.docker_test)
* [src.test.minio\_test](#src.test.minio_test)
* [src.test.fmods\_test](#src.test.fmods_test)
* [src.test.git\_test](#src.test.git_test)
* [src.test.postgre\_test](#src.test.postgre_test)
* [src.test.ftp\_test](#src.test.ftp_test)
* [src.minio](#src.minio)
  * [MinIO](#src.minio.MinIO)
    * [\_\_init\_\_](#src.minio.MinIO.__init__)
    * [getConnect](#src.minio.MinIO.getConnect)
* [src.mysql](#src.mysql)
  * [MySQL](#src.mysql.MySQL)
    * [\_\_init\_\_](#src.mysql.MySQL.__init__)
    * [getConnect](#src.mysql.MySQL.getConnect)
* [src.git](#src.git)
  * [GIT](#src.git.GIT)
    * [\_\_init\_\_](#src.git.GIT.__init__)
    * [clone](#src.git.GIT.clone)
* [src.postgre](#src.postgre)
  * [Postgre](#src.postgre.Postgre)
    * [\_\_init\_\_](#src.postgre.Postgre.__init__)
    * [getConnect](#src.postgre.Postgre.getConnect)
* [src.rabbitmq](#src.rabbitmq)
  * [RabbitMQ](#src.rabbitmq.RabbitMQ)
    * [\_\_init\_\_](#src.rabbitmq.RabbitMQ.__init__)
    * [getConnect](#src.rabbitmq.RabbitMQ.getConnect)
* [src.ftp](#src.ftp)
  * [FTP](#src.ftp.FTP)
    * [\_\_init\_\_](#src.ftp.FTP.__init__)
    * [getConnect](#src.ftp.FTP.getConnect)
* [src.docker](#src.docker)
  * [Docker](#src.docker.Docker)
    * [\_\_init\_\_](#src.docker.Docker.__init__)
    * [isDocker](#src.docker.Docker.isDocker)
    * [build](#src.docker.Docker.build)
    * [status](#src.docker.Docker.status)
    * [start](#src.docker.Docker.start)
    * [stop](#src.docker.Docker.stop)
    * [remove](#src.docker.Docker.remove)
    * [logs](#src.docker.Docker.logs)
    * [run](#src.docker.Docker.run)
    * [statusWaiting](#src.docker.Docker.statusWaiting)

<a name="pylint-recursive"></a>
# pylint-recursive

Module that runs pylint on all python scripts found in a directory tree..

<a name="pylint-recursive.check"></a>
#### check

```python
check(cfgDir, module)
```

apply pylint to the file specified if it is a *.py file

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

<a name="minio"></a>
# minio

Class for work with testing Modules

<a name="minio.MinIO"></a>
## MinIO Objects

```python
class MinIO(object)
```

Class for work with Minio

<a name="minio.MinIO.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(config, pathTmp, verbose)
```

Initialising object
Parameters
----------
config : dict
    config of module
pathTmp : str
    path to temporary files
verbose : bool
    verbose output

<a name="minio.MinIO.getConnect"></a>
#### getConnect

```python
 | getConnect(moduleName)
```

Connect to postgresql database
Attributes
----------
moduleName : str
    name of module

<a name="__init__"></a>
# \_\_init\_\_

<a name="mysql"></a>
# mysql

Class for work with testing Modules

<a name="mysql.MySQL"></a>
## MySQL Objects

```python
class MySQL(object)
```

Class for work with DB

<a name="mysql.MySQL.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(config, pathTmp, verbose)
```

Initialising object
Parameters
----------
config : dict
    config of module
pathTmp : str
    path to temporary files
verbose : bool
    verbose output

<a name="mysql.MySQL.getConnect"></a>
#### getConnect

```python
 | getConnect(moduleName)
```

Connect to postgresql database
Attributes
----------
moduleName : str
    name of module

<a name="git"></a>
# git

Class for work with testing Modules

<a name="git.GIT"></a>
## GIT Objects

```python
class GIT(object)
```

Class for load and build environment modules for functional tests

<a name="git.GIT.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(config, pathTmp, verbose)
```

Initialising object
Parameters
----------
config : dict
    config of module
pathTmp : str
    path to temporary files
verbose : bool
    verbose output

<a name="git.GIT.clone"></a>
#### clone

```python
 | clone()
```

Clone git repository

<a name="postgre"></a>
# postgre

Class for work with testing Modules

<a name="postgre.Postgre"></a>
## Postgre Objects

```python
class Postgre(object)
```

Class for work with DB

<a name="postgre.Postgre.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(config, pathTmp, verbose)
```

Initialising object
Parameters
----------
config : dict
    config of module
pathTmp : str
    path to temporary files
verbose : bool
    verbose output

<a name="postgre.Postgre.getConnect"></a>
#### getConnect

```python
 | getConnect(moduleName)
```

Connect to postgresql database
Attributes
----------
moduleName : str
    name of module

<a name="rabbitmq"></a>
# rabbitmq

Class for work with testing Modules

<a name="rabbitmq.RabbitMQ"></a>
## RabbitMQ Objects

```python
class RabbitMQ()
```

Class for work with RabbitMQ

<a name="rabbitmq.RabbitMQ.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(config, pathTmp, verbose)
```

Initialising object
Parameters
----------
config : dict
    config of module
pathTmp : str
    path to temporary files
verbose : bool
    verbose output

<a name="rabbitmq.RabbitMQ.getConnect"></a>
#### getConnect

```python
 | getConnect(moduleName)
```

Connect to postgresql database
Attributes
----------
moduleName : str
    name of module

<a name="ftp"></a>
# ftp

Class for work with testing Modules

<a name="ftp.FTP"></a>
## FTP Objects

```python
class FTP()
```

Class for work with FTP

<a name="ftp.FTP.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(config, pathTmp, verbose)
```

Initialising object
Parameters
----------
config : dict
    config of module
pathTmp : str
    path to temporary files
verbose : bool
    verbose output

<a name="ftp.FTP.getConnect"></a>
#### getConnect

```python
 | getConnect(moduleName)
```

Connect to postgresql database
Attributes
----------
moduleName : str
    name of module

<a name="docker"></a>
# docker

Class for work with testing Modules

<a name="docker.Docker"></a>
## Docker Objects

```python
class Docker(object)
```

Class for load and build environment modules for functional tests

<a name="docker.Docker.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(config, pathTmp, verbose)
```

Initialising object
Parameters
----------
config : dict
    config of module
pathTmp : str
    path to temporary files
verbose : bool
    verbose output

<a name="docker.Docker.isDocker"></a>
#### isDocker

```python
 | isDocker()
```

Get parameters of module for docker
Returns
-------
ok
    success

<a name="docker.Docker.build"></a>
#### build

```python
 | build()
```

Build docker container of module
Parameters
----------
moduleName : str
    name of module
config : dictionary
    configuration of module

<a name="docker.Docker.status"></a>
#### status

```python
 | status()
```

Status docker container of module

<a name="docker.Docker.start"></a>
#### start

```python
 | start()
```

Start docker container of module

<a name="docker.Docker.stop"></a>
#### stop

```python
 | stop()
```

Stop docker container of module
Parameters
----------
moduleName : str
    name of module

<a name="docker.Docker.remove"></a>
#### remove

```python
 | remove()
```

Remove docker container of module

<a name="docker.Docker.logs"></a>
#### logs

```python
 | logs()
```

Output logs of docker container of module

<a name="docker.Docker.run"></a>
#### run

```python
 | run()
```

Run docker container of module
Parameters
----------
moduleName : str
    name of module

<a name="docker.Docker.statusWaiting"></a>
#### statusWaiting

```python
 | statusWaiting(status, timeout=120)
```

Waiting docker container status
Parameters
----------
status : str
    status
timeout : int
    timeout in seconds

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

<a name="src.test.mysql_test"></a>
# src.test.mysql\_test

<a name="src.test.docker_test"></a>
# src.test.docker\_test

<a name="src.test.minio_test"></a>
# src.test.minio\_test

<a name="src.test.fmods_test"></a>
# src.test.fmods\_test

<a name="src.test.git_test"></a>
# src.test.git\_test

<a name="src.test.postgre_test"></a>
# src.test.postgre\_test

<a name="src.test.ftp_test"></a>
# src.test.ftp\_test

<a name="src.minio"></a>
# src.minio

Class for work with testing Modules

<a name="src.minio.MinIO"></a>
## MinIO Objects

```python
class MinIO(object)
```

Class for work with Minio

<a name="src.minio.MinIO.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(config, pathTmp, verbose)
```

Initialising object
Parameters
----------
config : dict
    config of module
pathTmp : str
    path to temporary files
verbose : bool
    verbose output

<a name="src.minio.MinIO.getConnect"></a>
#### getConnect

```python
 | getConnect(moduleName)
```

Connect to postgresql database
Attributes
----------
moduleName : str
    name of module

<a name="src.mysql"></a>
# src.mysql

Class for work with testing Modules

<a name="src.mysql.MySQL"></a>
## MySQL Objects

```python
class MySQL(object)
```

Class for work with DB

<a name="src.mysql.MySQL.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(config, pathTmp, verbose)
```

Initialising object
Parameters
----------
config : dict
    config of module
pathTmp : str
    path to temporary files
verbose : bool
    verbose output

<a name="src.mysql.MySQL.getConnect"></a>
#### getConnect

```python
 | getConnect(moduleName)
```

Connect to postgresql database
Attributes
----------
moduleName : str
    name of module

<a name="src.git"></a>
# src.git

Class for work with testing Modules

<a name="src.git.GIT"></a>
## GIT Objects

```python
class GIT(object)
```

Class for load and build environment modules for functional tests

<a name="src.git.GIT.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(config, pathTmp, verbose)
```

Initialising object
Parameters
----------
config : dict
    config of module
pathTmp : str
    path to temporary files
verbose : bool
    verbose output

<a name="src.git.GIT.clone"></a>
#### clone

```python
 | clone()
```

Clone git repository

<a name="src.postgre"></a>
# src.postgre

Class for work with testing Modules

<a name="src.postgre.Postgre"></a>
## Postgre Objects

```python
class Postgre(object)
```

Class for work with DB

<a name="src.postgre.Postgre.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(config, pathTmp, verbose)
```

Initialising object
Parameters
----------
config : dict
    config of module
pathTmp : str
    path to temporary files
verbose : bool
    verbose output

<a name="src.postgre.Postgre.getConnect"></a>
#### getConnect

```python
 | getConnect(moduleName)
```

Connect to postgresql database
Attributes
----------
moduleName : str
    name of module

<a name="src.rabbitmq"></a>
# src.rabbitmq

Class for work with testing Modules

<a name="src.rabbitmq.RabbitMQ"></a>
## RabbitMQ Objects

```python
class RabbitMQ()
```

Class for work with RabbitMQ

<a name="src.rabbitmq.RabbitMQ.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(config, pathTmp, verbose)
```

Initialising object
Parameters
----------
config : dict
    config of module
pathTmp : str
    path to temporary files
verbose : bool
    verbose output

<a name="src.rabbitmq.RabbitMQ.getConnect"></a>
#### getConnect

```python
 | getConnect(moduleName)
```

Connect to postgresql database
Attributes
----------
moduleName : str
    name of module

<a name="src.ftp"></a>
# src.ftp

Class for work with testing Modules

<a name="src.ftp.FTP"></a>
## FTP Objects

```python
class FTP()
```

Class for work with FTP

<a name="src.ftp.FTP.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(config, pathTmp, verbose)
```

Initialising object
Parameters
----------
config : dict
    config of module
pathTmp : str
    path to temporary files
verbose : bool
    verbose output

<a name="src.ftp.FTP.getConnect"></a>
#### getConnect

```python
 | getConnect(moduleName)
```

Connect to postgresql database
Attributes
----------
moduleName : str
    name of module

<a name="src.docker"></a>
# src.docker

Class for work with testing Modules

<a name="src.docker.Docker"></a>
## Docker Objects

```python
class Docker(object)
```

Class for load and build environment modules for functional tests

<a name="src.docker.Docker.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(config, pathTmp, verbose)
```

Initialising object
Parameters
----------
config : dict
    config of module
pathTmp : str
    path to temporary files
verbose : bool
    verbose output

<a name="src.docker.Docker.isDocker"></a>
#### isDocker

```python
 | isDocker()
```

Get parameters of module for docker
Returns
-------
ok
    success

<a name="src.docker.Docker.build"></a>
#### build

```python
 | build()
```

Build docker container of module
Parameters
----------
moduleName : str
    name of module
config : dictionary
    configuration of module

<a name="src.docker.Docker.status"></a>
#### status

```python
 | status()
```

Status docker container of module

<a name="src.docker.Docker.start"></a>
#### start

```python
 | start()
```

Start docker container of module

<a name="src.docker.Docker.stop"></a>
#### stop

```python
 | stop()
```

Stop docker container of module
Parameters
----------
moduleName : str
    name of module

<a name="src.docker.Docker.remove"></a>
#### remove

```python
 | remove()
```

Remove docker container of module

<a name="src.docker.Docker.logs"></a>
#### logs

```python
 | logs()
```

Output logs of docker container of module

<a name="src.docker.Docker.run"></a>
#### run

```python
 | run()
```

Run docker container of module
Parameters
----------
moduleName : str
    name of module

<a name="src.docker.Docker.statusWaiting"></a>
#### statusWaiting

```python
 | statusWaiting(status, timeout=120)
```

Waiting docker container status
Parameters
----------
status : str
    status
timeout : int
    timeout in seconds

