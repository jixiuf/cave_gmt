# -*- coding:utf-8 -*-
.PHONY: build-dep
.PHONY: test

ROOT_DIR=$(shell pwd)

run:
	./virtual/bin/python src/main.py
run-stage:
	./virtual/bin/python src/main.py -host=0.0.0.0
run-pro:
	./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -locale=zh
run-pro-en:
	./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -locale=en

test:
	cd src;../virtual/bin/python -m runtests
build-dep:
	@if [ !  -f ./virtual/bin/pip  ]; then  \
		virtualenv virtual; \
	fi
	./virtual/bin/pip install tornado
	./virtual/bin/pip install chardet
	./virtual/bin/pip install qiniu
	./virtual/bin/pip install redis
	./virtual/bin/pip install simplejson
	./virtual/bin/pip install python-etcd
	./virtual/bin/pip install tornado-mysql
	cd src/tea;sh buildtea.sh
clean:
	find . -name "*.pyc" -exec rm {} \;
