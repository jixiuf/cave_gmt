# -*- coding:utf-8 -*-
.PHONY: build-dep
.PHONY: test

ROOT_DIR=$(shell pwd)

run:
	./virtual/bin/python src/main.py
test:
# ./virtual/bin/python src/db/databasetemplate/sum_test.py
# ./virtual/bin/python src/db/databasetemplate/conn_test.py
	./virtual/bin/python src/test_ping.py
build-dep:
	@if [ !  -f ./virtual/bin/pip  ]; then  \
		virtualenv virtual; \
	fi
	./virtual/bin/pip install tornado
	./virtual/bin/pip install chardet
	./virtual/bin/pip install qiniu
	./virtual/bin/pip install redis
	./virtual/bin/pip install tornado-mysql
	cd src/tea;sh buildtea.sh