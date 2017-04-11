# -*- coding:utf-8 -*-
.PHONY: build-dep
.PHONY: test

ROOT_DIR=$(shell pwd)

run-pro:
	@if [ -d "~/.cave/" ];then \
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -locale=zh -confdir=~/.cave/;\
	elif [ -d "/data/cave/config/" ];then \
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -locale=zh -confdir=/data/cave/config/;\
	elif [ -d "./config/" ]; then\
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -locale=zh -confdir=./config/;\
	elif [ -d "../config/" ];then \
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -locale=zh -confdir=../config/;\
	else \
		echo "no confdir,please give -confdir like";\
		echo "./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -locale=zh -confdir=../config/";\
	fi

run:
	./virtual/bin/python src/main.py
run-pro-en:
	@if [ -d "~/.cave/" ];then \
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -locale=en -confdir=~/.cave/;\
	elif [ -d "/data/cave/config/" ];then \
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -locale=en -confdir=/data/cave/config/;\
	elif [ -d "./config/" ]; then\
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -locale=en -confdir=./config/;\
	elif [ -d "../config/" ];then \
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -locale=en -confdir=../config/;\
	else \
		echo "no confdir,please give -confdir like";\
		echo "./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -locale=en -confdir=../config/";\
	fi

test:
	cd src;../virtual/bin/python -m runtests
build-dep:
	@if [ `uname -s` = "Darwin" ] ; then \
		if [ -z `which svn` ]; then \
			brew install svn; \
		fi ; \
	else \
		sudo yum install svn zip;\
	fi

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
