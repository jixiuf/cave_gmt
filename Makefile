# -*- coding:utf-8 -*-
.PHONY: build-dep

ROOT_DIR=$(shell pwd)

build-dep:
	virtualenv virtual
	./virtual/bin/pip install tornado
	./virtual/bin/pip install DBUtils
	./virtual/bin/pip install chardet
	./virtual/bin/pip install qiniu
	./virtual/bin/pip install redis
	./virtual/bin/pip install Tornado-MySQL
# cd tornado-mysql
# ../virtual/bin/python setup.py install
	cd src/tea;sh buildtea.sh