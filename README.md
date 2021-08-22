# pyFuncTest

The framework for functional testing of microservices

Functional сapabilities:
1. Build a container from git repository
2. Create, start and stop containers
3. Send and receive messages from Kafka, RabbitMQ
4. Write and read data from mySQL, MariaDB, PostgreSQL
5. Write and read files from FTP, MinIO

Additional:
1. You can create folders before running tests for FTP, MinIO
2. You can migrate structure and data before running tests for databases
3. You can replace configuration and other files inside container before work
4. You can run docker services in a specific sequence before running tests

# Table of Contents

* [Install](#install)
* [How it works ](#itworks)
  * [Settings of modules](#settings)
  * [Docker](#docker)
    * [Build container](#docker-build)
    * [Start container](#docker-start)
    * [Start compose](#docker-start-compose)
  * [FTP](#ftp)
    * [Settings](#ftp-settings)
    * [Testing](#ftp-testing)
  * [Minio](#minio)
    * [Settings](#minio-settings)
    * [Testing](#minio-testing)
  * [MySQL](#mysql)
    * [Settings](#mysql-settings)
    * [Testing](#mysql-testing)
  * [PostgreSQL](#mysql)
    * [Settings](#postgresql-settings)
    * [Testing](#postgresql-testing)
  * [RabbitMQ](#rabbitmq)
    * [Settings](#rabbitmq-settings)
    * [Testing](#rabbitmq-testing)
  * [Kafka](#kafka)
    * [Settings](#kafka-settings)
    * [Testing](#kafka-testing)

## Install<a name="install"></a>

```
pip3 install pyfunctest
```

Upgrade

```
pip3 install --upgrade pyfunctest
```

# How it works<a name="itworks"></a>

## Settings of modules<a name="settings"></a>

The main module is FMods. Its constructor has three parameters: path to settings, path to template folder and verbose.
The example of structure settings: https://github.com/Lunkov/pyfunctest/tree/master/data/mods

The example commands for tests

```
import unittest

class TestServices(unittest.TestCase):

  def setUp(self):
    # New object of settings of modules
    self.fm = FMods("mods/", "tmp/", True)

    # Read settings
    self.fm.scan()

    # Run all containers
    self.fm.startAll()

  def testReceiveMessage(self):
    # New object of RabbitMQ Client
    rabbitmq = self.fm.newRabbitMQ('rabbitmq')

    # Create routes
    queue = 'log3'
    exchange = 'log3'
    routing_key = ''
    exchange_type = 'fanout'	
    self.assertTrue(rabbitmq.createRoute(exchange, exchange_type, routing_key, queue))

    # Send message
    self.assertTrue(rabbitmq.send(exchange, routing_key, 'message 1'))    

    # New object of PostgreSQL Client
    pg = self.fm.newPostgre('pg')

    # Check structure of database
    self.assertEqual(pg.getTableList(), [('public', 'messages')])

    # Get and check data from table
    self.assertEqual(pg.getData('select * from public.messages'), [(1, 'message 1')])

  
  def tearDown(self):
    # Stop all containers
    self.fm.stopAll()

if __name__ == '__main__':
  unittest.main()
```


## Docker<a name="docker"></a>

### Build container<a name="docker-build"></a>

Example file .yaml
```
name: srv-report
actions:
  - build

git:
  src: "https://github.com/Lunkov/srv-report.git"
  branch: master

docker:
  name: srv-report-test
  src: srv-report-test

  dockerfile: Dockerfile
  buildpath: .
```

Commands for tests
```
# New object of settings of modules
fm = FMods("mods/", "tmp/", True)

# Read settings
fm.scan()

# Get module
srvDocker = fm.newDocker('srv-report')

# Container must have status: not found
self.assertTrue(srvDocker.statusWaiting('not found'))

# Build container
self.assertTrue(srvDocker.build())

# Run container
self.assertTrue(srvDocker.run())

```

### Start container<a name="docker-start"></a>

Example file .yaml
```
name: nginx
order: 10
actions:
  - run

docker:
  name: nginx-test
  src: nginx
  ports:
    - "3010:81"

  env:
    - NGINX_PORT: 81
  
  volumes:
    - "data/mods/nginx/html/:/usr/share/nginx/html:ro"
    - "data/mods/nginx/test.conf:/etc/nginx/conf.d/default.conf"
```

Commands for tests
```
# New object of settings of modules
fm = FMods("mods/", "tmp/", True)

# Read settings
fm.scan()

# Get module
srvNginx = fm.newDocker('nginx')

# Run container
self.assertTrue(srvNginx.run())

# Container must have status: running
self.assertEqual(srvNginx.status(), 'running')

```

### Start compose<a name="docker-start-compose"></a>

Example file .yaml
```
name: kafka
order: 1
actions:
  - run
  - init

docker:
  name: kafka_kafka-test_1
  compose: docker-compose.yml

  network: test-net

  init:
    create_channels:
      - channel-test
      - channel1-test
      - channel2-test

kafka:
  url_inside: "localhost:9092"
  url_outside: "localhost:9094"
  id_group: main
```

Commands for tests
```
# New object of settings of modules
fm = FMods("mods/", "tmp/", True)

# Read settings
fm.scan()

# Get module
srvDocker = fm.newDocker('kafka') # Docker Compose

# Run container
self.assertTrue(srvDocker.startCompose())

# Container must have status: running
self.assertEqual(srvDocker.status(), 'running')

# Stop container
self.assertTrue(srvDocker.stopCompose())

```


## FTP<a name="ftp"></a>

### Settings<a name="ftp-settings"></a>


Example file .yaml
```
name: ftp
order: 5
actions:
  - run

docker:
  name: ftp-test
  src: teezily/ftpd
  ports:
    - "3021:21"
    - "35000-35004:35000-35004"

  patch:
    - start-ftp: /
  env:
    - FTP_USER: user
    - FTP_PASSWORD: pwd
    - PASV_MIN_PORT: 35000
    - PASV_MAX_PORT: 35004

ftp:
  user: user
  password: pwd
  port: 3021
  init:
    # You can create folders before running tests
    create_folders:
      - folder-test/folder-test1
      - folder-test/folder-test2
      - folder-test1

```

### Testing<a name="ftp-testing"></a>

```
# New object of FTP Client
ftp = fm.newFTP('ftp')

# Check structure of folder
self.assertEqual(ftp.getDirList(), ['incoming'])

# Upload file
self.assertTrue(ftp.uploadFile('folder-test', 'test.txt', 'data/files/test.txt'))

# Compare local and remote files 
self.assertTrue(ftp.compareFiles('folder-test', 'test.txt', 'data/files/test.txt'))
```

## Minio<a name="minio"></a>

### Settings<a name="minio-settings"></a>

Example file .yaml
```
name: minio
order: 6
actions:
  - run
  - init

docker:
  name: minio-test
  src: minio/minio
  ports:
    - "3010:9000"

  run_command: "server /data"


s3:
  access_key: minioadmin
  secret_key: minioadmin
  port: 3010
  init:
    # You can create folders before running tests
    create_folders:
      - "bucket-test:folder000"
      - "bucket-test2:folder1/folder1"
```

### Testing<a name="minio-testing"></a>
```
# New object of Minio Client
minio = fm.newMinIO('minio')

# Check structure of basket
self.assertEqual(minio.getBasketsList(), ['bucket-test'])

# Upload file
self.assertTrue(minio.uploadFile('bucket-test', 'test.txt', 'data/files/test.txt'))

# Compare local and remote files 
self.assertTrue(minio.compareFiles('bucket-test', 'test.txt', 'data/files/test.txt'))
```


## MySQL<a name="mysql"></a>

### Settings<a name="mysql-settings"></a>

Example file .yaml
```
name: mysql
order: 2
actions:
  - run
  - migrate

docker:
  name: mysql-test
  src: mariadb

  ports:
    - "17436:3306"

  # You can replace configuration file inside container before work
  patch: 
    - 50-server.cnf: /etc/mysql/mariadb.conf.d/

  env:
    - MYSQL_ROOT_PASSWORD: pwd
    - MYSQL_USER: user
    - MYSQL_PASSWORD: pwd
    - MYSQL_DATABASE: test-db
    - ALLOW_EMPTY_PASSWORD: yes

db:
  name: test-db
  user: root
  password: pwd
  port: 17436

# You can migrate your data before tests
migrate:
  command: "--path=/migrations/ --database=\"mysql://root:pwd@tcp(mysql-test:3306)/test-db\" up"
  path: migrations
  timeout_before_migrate: 10
```

### Testing<a name="mysql-testing"></a>

Commands for tests
```
# New object of mySQL Client
msql = fm.newMySQL('mysql')

# Check structure of database
self.assertEqual(msql.getTableList(), ['article', 'article2', 'article3'])

# Create table
self.assertTrue(msql.loadSQL('data/mysql/create_tables.sql'))

# Insert Data
self.assertTrue(msql.loadSQL('data/mysql/insert.sql'))

# Get and check data from table
self.assertEqual(msql.getData('select * from article'), ((1, 'article 1', 'description'),))

```

## PostgreSQL<a name="postgresql"></a>

### Settings<a name="postgresql-settings"></a>

Example file .yaml
```
name: pg
actions:
  - run
  - migrate

docker:

  name: pg-test
  src: postgres:alpine
  ports:
    - "17432:5432"
  env:
    - POSTGRES_PASSWORD: pwd
    - POSTGRES_USER: user
    - POSTGRES_DB: test-db

db:
  name: test-db
  user: user
  password: pwd
  port: 17432

migrate:
  command: --path=/migrations/ --database="postgres://user:pwd@pg-test:5432/test-db?sslmode=disable" up
  path: migrate
  timeout_before_migrate: 5
```

### Testing<a name="postgresql-testing"></a>
```
# New object of PostgreSQL Client
pg = fm.newPostgre('pg')

# Check structure of database
self.assertEqual(pg.getTableList(), [('public', 'article'), ('public', 'article2'), ('public', 'article3')])

# Create table
self.assertTrue(pg.loadSQL('data/postgre/create_table.sql'))

# Insert Data
self.assertTrue(pg.loadSQL('data/postgre/insert.sql'))

# Get and check data from table
self.assertEqual(pg.getData('select * from public.article'), [(1, 'article 1', 'description', None)])

```

## RabbitMQ<a name="rabbitmq"></a>

### Settings<a name="rabbitmq-settings"></a>

Example file .yaml
```
name: rabbitmq
actions:
  - run
  - init

docker:
  name: rabbitmq-test
  src: rabbitmq:management-alpine
  ports:
    - "5672:5672"
    - "15672:15672"
  env:
    - RABBITMQ_DEFAULT_USER: user
    - RABBITMQ_DEFAULT_PASS: pwd
    - RABBITMQ_DEFAULT_VHOST: /


rabbitmq:
  url: "amqp://user:pwd@localhost:5672/"
  user: user
  password: pwd
  init:
    # You can create channels before running tests
    create_channels:
      - "log3:fanout::log3"
      - "log1:fanout::log1"
```

### Testing<a name="rabbitmq-testing"></a>
```
# New object of RabbitMQ Client
rabbitmq = fm.newRabbitMQ('rabbitmq')

# Create routes
self.assertTrue(rabbitmq.createRoute(exchange, exchange_type, routing_key, queue))

# Send message
self.assertTrue(rabbitmq.send(exchange, routing_key, 'message 1'))

# Recieve message
msg, ok = rabbitmq.receive(queue)
self.assertTrue(ok)
self.assertEqual(msg, 'message 1')

# Send file
self.assertTrue(rabbitmq.sendFile(exchange, routing_key, 'data/files/test.txt'))

# Recieve and compare file
self.assertTrue(rabbitmq.receiveAndCompareFile(queue, 'data/files/test.txt'))
```

## Kafka<a name="kafka"></a>

### Settings<a name="kafka-settings"></a>

Example file .yaml
```
name: kafka
order: 1
actions:
  - run
  - init

docker:
  name: kafka_kafka-test_1
  compose: docker-compose.yml

  network: test-net

  init:
    # You can create channels before running tests
    create_channels:
      - channel-test
      - channel1-test
      - channel2-test

kafka:
  url_inside: "localhost:9092"
  url_outside: "localhost:9094"
  id_group: main
```

### Testing<a name="kafka-testing"></a>
```
# New object of Kafka Client
kafka = fm.newKafka('kafka')

# Send message
self.assertTrue(kafka.send(channel, 'message 1'))

# Recieve message
msg, ok = kafka.receive(channel)
self.assertTrue(ok)
self.assertEqual(msg, 'message 1')

# Send file
self.assertTrue(kafka.sendFile(channel, 'data/files/test.txt'))

# Recieve and compare file
self.assertTrue(kafka.receiveAndCompareFile(channel, 'data/files/test.txt'))
```

