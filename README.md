# FMods

The framework for functional testing of microservices

Functional сapabilities:
1. Build a container from git repository
2. Create, start and stop containers
3. Send and receive messages from Kafka, RabbitMQ
4. Write and read data from mySQL, MariaDB, PostgreSQL
5. Write and read data from FTP, MinIO

## Install

```
pip3 install git+https://github.com/Lunkov/fmods.git
```

## Upgrade

```
pip3 install --upgrade git+https://github.com/Lunkov/fmods.git
```

# How it works 

## Settings of modules

The main module is FMods. Its constructor has three parameters: path to settings, path to template folder and verbose.

```
# New object of settings of modules
fm = FMods("mods/", "tmp/", True)

# Read settings
fm.scan()
```


## FTP

### Settings


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
    create_folders:
      - folder-test/folder-test1
      - folder-test/folder-test2
      - folder-test1

```

### Testing

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

## Minio

### Settings

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
    create_folders:
      - "bucket-test:folder000"
      - "bucket-test2:folder1/folder1"
```

### Testing
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


## MySQL

### Settings

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


migrate:
  command: "--path=/migrations/ --database=\"mysql://root:pwd@tcp(mysql-test:3306)/test-db\" up"
  path: migrations
  timeout_before_migrate: 10
```

### Testing
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

## PostgreSQL

### Settings

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

### Testing
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


# Additional information

## Testing

### Prepare
```
sudo apt install python3-pytest
```

### Run tests
```
sudo pytest-3 -s
```

## Builds

### Build documentation

```
pydoc-markdown --render-toc --py3 --verbose > fmods.md
```

## Test coverage

```
---------- coverage: platform linux, python 3.8.10-final-0 -----------
Name                        Stmts   Miss  Cover
-----------------------------------------------
src/docker.py                 260     64    75%
src/fmod.py                    26      1    96%
src/fmod_db.py                 37      6    84%
src/fmods.py                  157     20    87%
src/ftp.py                    246     31    87%
src/git.py                     17      1    94%
src/http.py                    64     28    56%
src/httpserver.py              58     12    79%
src/kafka.py                  171     74    57%
src/lfs.py                     30     17    43%
src/migrate.py                 82     23    72%
src/minio.py                  123     24    80%
src/mysql.py                   47      3    94%
src/postgre.py                 44      3    93%
src/rabbitmq.py               152     42    72%
src/test/docker_test.py        77      6    92%
src/test/fmods_test.py         14      1    93%
src/test/ftp_test.py           43      1    98%
src/test/git_test.py           14      1    93%
src/test/http_test.py          23      1    96%
src/test/kafka_test.py         34      8    76%
src/test/minio_test.py         41      1    98%
src/test/mysql_test.py         45      1    98%
src/test/postgre_test.py       42      1    98%
src/test/rabbitmq_test.py      42      1    98%
-----------------------------------------------
TOTAL                        1889    371    80%
```

