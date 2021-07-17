# FMods

## API
[Link to API](fmods.md)

## Install

```
pip3 install git+https://github.com/Lunkov/fmods.git
```

## Upgrade

```
pip3 install --upgrade git+https://github.com/Lunkov/fmods.git
```

## Tests

Prepare
```
sudo apt install python3-pytest
```

Run tests
```
sudo pytest-3 -s
```

## Builds

### Build documentation

```
pydoc-markdown --render-toc --py3 --verbose > fmods.md
```

## Examples

### Settings of modules

```
# New object of settings of modules
fm = FMods("mods/", "tmp/", True)

# Read settings
fm.scan()
```


### FTP

#### Settings

Example file .env
```
NAME=ftp
TYPE=docker
ORDER=5

CONTAINER_NAME=ftp-test

CONTAINER_SRC=teezily/ftpd

CONTAINER_PORTS=3021:21,35000-35004:35000-35004

FTP_USER=user
FTP_PASSWORD=pwd
FTP_PORT=3021

CONTAINER_ENV_FTP_USER=user
CONTAINER_ENV_FTP_PASSWORD=pwd
CONTAINER_ENV_PASV_MIN_PORT=35000
CONTAINER_ENV_PASV_MAX_PORT=35004
```

#### Testing

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

### Minio

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

# Test coverage

```
----------- coverage: platform linux, python 3.8.5-final-0 -----------
Name                        Stmts   Miss  Cover
-----------------------------------------------
src/docker.py                 257     55    79%
src/fmods.py                  143     13    91%
src/ftp.py                    255     27    89%
src/git.py                     17      0   100%
src/http.py                    66     26    61%
src/httpserver.py              60     11    82%
src/kafka.py                  173     38    78%
src/lfs.py                     30     17    43%
src/migrate.py                 78     21    73%
src/minio.py                  127     22    83%
src/mysql.py                   83      8    90%
src/postgre.py                 79     11    86%
src/rabbitmq.py               150     40    73%
-----------------------------------------------
TOTAL                        1893    309    84%
```
