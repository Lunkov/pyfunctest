# Table of Contents

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
* [fmod](#fmod)
  * [FMod](#fmod.FMod)
    * [\_\_init\_\_](#fmod.FMod.__init__)
    * [isDocker](#fmod.FMod.isDocker)
* [minio](#minio)
  * [MinIO](#minio.MinIO)
    * [\_\_init\_\_](#minio.MinIO.__init__)
* [\_\_init\_\_](#__init__)
* [mysql](#mysql)
  * [MySQL](#mysql.MySQL)
    * [\_\_init\_\_](#mysql.MySQL.__init__)
* [git](#git)
  * [GIT](#git.GIT)
    * [\_\_init\_\_](#git.GIT.__init__)
    * [clone](#git.GIT.clone)
* [httpserver](#httpserver)
  * [HTTPSrv](#httpserver.HTTPSrv)
    * [\_\_init\_\_](#httpserver.HTTPSrv.__init__)
* [migrate](#migrate)
  * [Migrate](#migrate.Migrate)
    * [\_\_init\_\_](#migrate.Migrate.__init__)
    * [isMigrate](#migrate.Migrate.isMigrate)
    * [run](#migrate.Migrate.run)
* [fmod\_db](#fmod_db)
  * [FModDB](#fmod_db.FModDB)
    * [\_\_init\_\_](#fmod_db.FModDB.__init__)
* [postgre](#postgre)
  * [Postgre](#postgre.Postgre)
    * [\_\_init\_\_](#postgre.Postgre.__init__)
* [http](#http)
  * [HTTP](#http.HTTP)
    * [\_\_init\_\_](#http.HTTP.__init__)
* [lfs](#lfs)
  * [LFS](#lfs.LFS)
    * [rm](#lfs.LFS.rm)
* [rabbitmq](#rabbitmq)
  * [RabbitMQ](#rabbitmq.RabbitMQ)
    * [\_\_init\_\_](#rabbitmq.RabbitMQ.__init__)
    * [getConnect](#rabbitmq.RabbitMQ.getConnect)
* [kafka](#kafka)
  * [Kafka](#kafka.Kafka)
    * [\_\_init\_\_](#kafka.Kafka.__init__)
    * [getConnect](#kafka.Kafka.getConnect)
* [ftp](#ftp)
  * [FTP](#ftp.FTP)
    * [getConnect](#ftp.FTP.getConnect)
* [docker](#docker)
  * [Docker](#docker.Docker)
    * [\_\_init\_\_](#docker.Docker.__init__)
    * [build](#docker.Docker.build)
    * [status](#docker.Docker.status)
    * [start](#docker.Docker.start)
    * [restart](#docker.Docker.restart)
    * [stop](#docker.Docker.stop)
    * [remove](#docker.Docker.remove)
    * [logs](#docker.Docker.logs)
    * [run](#docker.Docker.run)
    * [statusWaiting](#docker.Docker.statusWaiting)
    * [copy](#docker.Docker.copy)
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
* [src.fmod](#src.fmod)
  * [FMod](#src.fmod.FMod)
    * [\_\_init\_\_](#src.fmod.FMod.__init__)
    * [isDocker](#src.fmod.FMod.isDocker)
* [src.test](#src.test)
* [src.test.mysql\_test](#src.test.mysql_test)
* [src.test.docker\_test](#src.test.docker_test)
* [src.test.kafka\_test](#src.test.kafka_test)
* [src.test.http\_test](#src.test.http_test)
* [src.test.minio\_test](#src.test.minio_test)
* [src.test.fmods\_test](#src.test.fmods_test)
* [src.test.rabbitmq\_test](#src.test.rabbitmq_test)
* [src.test.git\_test](#src.test.git_test)
* [src.test.postgre\_test](#src.test.postgre_test)
* [src.test.ftp\_test](#src.test.ftp_test)
* [src.minio](#src.minio)
  * [MinIO](#src.minio.MinIO)
    * [\_\_init\_\_](#src.minio.MinIO.__init__)
* [src.mysql](#src.mysql)
  * [MySQL](#src.mysql.MySQL)
    * [\_\_init\_\_](#src.mysql.MySQL.__init__)
* [src.git](#src.git)
  * [GIT](#src.git.GIT)
    * [\_\_init\_\_](#src.git.GIT.__init__)
    * [clone](#src.git.GIT.clone)
* [src.httpserver](#src.httpserver)
  * [HTTPSrv](#src.httpserver.HTTPSrv)
    * [\_\_init\_\_](#src.httpserver.HTTPSrv.__init__)
* [src.migrate](#src.migrate)
  * [Migrate](#src.migrate.Migrate)
    * [\_\_init\_\_](#src.migrate.Migrate.__init__)
    * [isMigrate](#src.migrate.Migrate.isMigrate)
    * [run](#src.migrate.Migrate.run)
* [src.fmod\_db](#src.fmod_db)
  * [FModDB](#src.fmod_db.FModDB)
    * [\_\_init\_\_](#src.fmod_db.FModDB.__init__)
* [src.postgre](#src.postgre)
  * [Postgre](#src.postgre.Postgre)
    * [\_\_init\_\_](#src.postgre.Postgre.__init__)
* [src.http](#src.http)
  * [HTTP](#src.http.HTTP)
    * [\_\_init\_\_](#src.http.HTTP.__init__)
* [src.lfs](#src.lfs)
  * [LFS](#src.lfs.LFS)
    * [rm](#src.lfs.LFS.rm)
* [src.rabbitmq](#src.rabbitmq)
  * [RabbitMQ](#src.rabbitmq.RabbitMQ)
    * [\_\_init\_\_](#src.rabbitmq.RabbitMQ.__init__)
    * [getConnect](#src.rabbitmq.RabbitMQ.getConnect)
* [src.kafka](#src.kafka)
  * [Kafka](#src.kafka.Kafka)
    * [\_\_init\_\_](#src.kafka.Kafka.__init__)
    * [getConnect](#src.kafka.Kafka.getConnect)
* [src.ftp](#src.ftp)
  * [FTP](#src.ftp.FTP)
    * [getConnect](#src.ftp.FTP.getConnect)
* [src.docker](#src.docker)
  * [Docker](#src.docker.Docker)
    * [\_\_init\_\_](#src.docker.Docker.__init__)
    * [build](#src.docker.Docker.build)
    * [status](#src.docker.Docker.status)
    * [start](#src.docker.Docker.start)
    * [restart](#src.docker.Docker.restart)
    * [stop](#src.docker.Docker.stop)
    * [remove](#src.docker.Docker.remove)
    * [logs](#src.docker.Docker.logs)
    * [run](#src.docker.Docker.run)
    * [statusWaiting](#src.docker.Docker.statusWaiting)
    * [copy](#src.docker.Docker.copy)

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
 | __init__(pathModules, pathTmp='', verbose=True)
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

<a name="fmod"></a>
# fmod

Class for work with testing Modules

<a name="fmod.FMod"></a>
## FMod Objects

```python
class FMod()
```

Class for environment module for functional tests

<a name="fmod.FMod.__init__"></a>
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

<a name="fmod.FMod.isDocker"></a>
#### isDocker

```python
 | isDocker()
```

Get parameters of module for docker
Returns
-------
ok
    success

<a name="minio"></a>
# minio

Class for work with testing Modules

<a name="minio.MinIO"></a>
## MinIO Objects

```python
class MinIO(FMod)
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

<a name="__init__"></a>
# \_\_init\_\_

<a name="mysql"></a>
# mysql

Class for work with testing Modules

<a name="mysql.MySQL"></a>
## MySQL Objects

```python
class MySQL(FModDB)
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

<a name="git"></a>
# git

Class for work with testing Modules

<a name="git.GIT"></a>
## GIT Objects

```python
class GIT(FMod)
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

<a name="httpserver"></a>
# httpserver

Class for work with testing Modules

<a name="httpserver.HTTPSrv"></a>
## HTTPSrv Objects

```python
class HTTPSrv(FMod)
```

Class for work with HTTP (server)

<a name="httpserver.HTTPSrv.__init__"></a>
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

<a name="migrate"></a>
# migrate

Class for work with testing Modules

<a name="migrate.Migrate"></a>
## Migrate Objects

```python
class Migrate(FMod)
```

Class for load and build environment modules for functional tests

<a name="migrate.Migrate.__init__"></a>
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

<a name="migrate.Migrate.isMigrate"></a>
#### isMigrate

```python
 | isMigrate()
```

Get parameters of module for Migrate
Returns
-------
ok
    success

<a name="migrate.Migrate.run"></a>
#### run

```python
 | run()
```

Migrate for Database container

<a name="fmod_db"></a>
# fmod\_db

Class for work with testing Modules

<a name="fmod_db.FModDB"></a>
## FModDB Objects

```python
class FModDB(FMod)
```

Class for environment module for functional tests

<a name="fmod_db.FModDB.__init__"></a>
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

<a name="postgre"></a>
# postgre

Class for work with testing Modules

<a name="postgre.Postgre"></a>
## Postgre Objects

```python
class Postgre(FModDB)
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

<a name="http"></a>
# http

Class for work with testing Modules

<a name="http.HTTP"></a>
## HTTP Objects

```python
class HTTP(FMod)
```

Class for work with HTTP (client)

<a name="http.HTTP.__init__"></a>
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

<a name="lfs"></a>
# lfs

Class for work with testing Modules

<a name="lfs.LFS"></a>
## LFS Objects

```python
class LFS(object)
```

Class for load and build environment modules for functional tests

<a name="lfs.LFS.rm"></a>
#### rm

```python
 | @staticmethod
 | rm(pathName)
```

remove folders

<a name="rabbitmq"></a>
# rabbitmq

Class for work with testing Modules

<a name="rabbitmq.RabbitMQ"></a>
## RabbitMQ Objects

```python
class RabbitMQ(FMod)
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
 | getConnect()
```

Connect to rabbitMQ

<a name="kafka"></a>
# kafka

Class for work with testing Modules

<a name="kafka.Kafka"></a>
## Kafka Objects

```python
class Kafka(FMod)
```

Class for work with Kafka

<a name="kafka.Kafka.__init__"></a>
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

<a name="kafka.Kafka.getConnect"></a>
#### getConnect

```python
 | getConnect()
```

Connect to rabbitMQ

<a name="ftp"></a>
# ftp

Class for work with testing Modules

<a name="ftp.FTP"></a>
## FTP Objects

```python
class FTP(FMod)
```

Class for work with FTP

<a name="ftp.FTP.getConnect"></a>
#### getConnect

```python
 | getConnect()
```

Connect to FTP

<a name="docker"></a>
# docker

Class for work with testing Modules

<a name="docker.Docker"></a>
## Docker Objects

```python
class Docker(FMod)
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

<a name="docker.Docker.build"></a>
#### build

```python
 | build(rm=True)
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

<a name="docker.Docker.restart"></a>
#### restart

```python
 | restart()
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
 | run(rm=True)
```

Run docker container of module

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

<a name="docker.Docker.copy"></a>
#### copy

```python
 | copy(src, dstDir)
```

src shall be an absolute path

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
 | __init__(pathModules, pathTmp='', verbose=True)
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

<a name="src.fmod"></a>
# src.fmod

Class for work with testing Modules

<a name="src.fmod.FMod"></a>
## FMod Objects

```python
class FMod()
```

Class for environment module for functional tests

<a name="src.fmod.FMod.__init__"></a>
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

<a name="src.fmod.FMod.isDocker"></a>
#### isDocker

```python
 | isDocker()
```

Get parameters of module for docker
Returns
-------
ok
    success

<a name="src.test"></a>
# src.test

<a name="src.test.mysql_test"></a>
# src.test.mysql\_test

<a name="src.test.docker_test"></a>
# src.test.docker\_test

<a name="src.test.kafka_test"></a>
# src.test.kafka\_test

<a name="src.test.http_test"></a>
# src.test.http\_test

<a name="src.test.minio_test"></a>
# src.test.minio\_test

<a name="src.test.fmods_test"></a>
# src.test.fmods\_test

<a name="src.test.rabbitmq_test"></a>
# src.test.rabbitmq\_test

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
class MinIO(FMod)
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

<a name="src.mysql"></a>
# src.mysql

Class for work with testing Modules

<a name="src.mysql.MySQL"></a>
## MySQL Objects

```python
class MySQL(FModDB)
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

<a name="src.git"></a>
# src.git

Class for work with testing Modules

<a name="src.git.GIT"></a>
## GIT Objects

```python
class GIT(FMod)
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

<a name="src.httpserver"></a>
# src.httpserver

Class for work with testing Modules

<a name="src.httpserver.HTTPSrv"></a>
## HTTPSrv Objects

```python
class HTTPSrv(FMod)
```

Class for work with HTTP (server)

<a name="src.httpserver.HTTPSrv.__init__"></a>
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

<a name="src.migrate"></a>
# src.migrate

Class for work with testing Modules

<a name="src.migrate.Migrate"></a>
## Migrate Objects

```python
class Migrate(FMod)
```

Class for load and build environment modules for functional tests

<a name="src.migrate.Migrate.__init__"></a>
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

<a name="src.migrate.Migrate.isMigrate"></a>
#### isMigrate

```python
 | isMigrate()
```

Get parameters of module for Migrate
Returns
-------
ok
    success

<a name="src.migrate.Migrate.run"></a>
#### run

```python
 | run()
```

Migrate for Database container

<a name="src.fmod_db"></a>
# src.fmod\_db

Class for work with testing Modules

<a name="src.fmod_db.FModDB"></a>
## FModDB Objects

```python
class FModDB(FMod)
```

Class for environment module for functional tests

<a name="src.fmod_db.FModDB.__init__"></a>
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

<a name="src.postgre"></a>
# src.postgre

Class for work with testing Modules

<a name="src.postgre.Postgre"></a>
## Postgre Objects

```python
class Postgre(FModDB)
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

<a name="src.http"></a>
# src.http

Class for work with testing Modules

<a name="src.http.HTTP"></a>
## HTTP Objects

```python
class HTTP(FMod)
```

Class for work with HTTP (client)

<a name="src.http.HTTP.__init__"></a>
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

<a name="src.lfs"></a>
# src.lfs

Class for work with testing Modules

<a name="src.lfs.LFS"></a>
## LFS Objects

```python
class LFS(object)
```

Class for load and build environment modules for functional tests

<a name="src.lfs.LFS.rm"></a>
#### rm

```python
 | @staticmethod
 | rm(pathName)
```

remove folders

<a name="src.rabbitmq"></a>
# src.rabbitmq

Class for work with testing Modules

<a name="src.rabbitmq.RabbitMQ"></a>
## RabbitMQ Objects

```python
class RabbitMQ(FMod)
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
 | getConnect()
```

Connect to rabbitMQ

<a name="src.kafka"></a>
# src.kafka

Class for work with testing Modules

<a name="src.kafka.Kafka"></a>
## Kafka Objects

```python
class Kafka(FMod)
```

Class for work with Kafka

<a name="src.kafka.Kafka.__init__"></a>
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

<a name="src.kafka.Kafka.getConnect"></a>
#### getConnect

```python
 | getConnect()
```

Connect to rabbitMQ

<a name="src.ftp"></a>
# src.ftp

Class for work with testing Modules

<a name="src.ftp.FTP"></a>
## FTP Objects

```python
class FTP(FMod)
```

Class for work with FTP

<a name="src.ftp.FTP.getConnect"></a>
#### getConnect

```python
 | getConnect()
```

Connect to FTP

<a name="src.docker"></a>
# src.docker

Class for work with testing Modules

<a name="src.docker.Docker"></a>
## Docker Objects

```python
class Docker(FMod)
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

<a name="src.docker.Docker.build"></a>
#### build

```python
 | build(rm=True)
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

<a name="src.docker.Docker.restart"></a>
#### restart

```python
 | restart()
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
 | run(rm=True)
```

Run docker container of module

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

<a name="src.docker.Docker.copy"></a>
#### copy

```python
 | copy(src, dstDir)
```

src shall be an absolute path

