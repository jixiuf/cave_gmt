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
	elif [ -d "cave/config/" ];then \
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -locale=zh -confdir=cave/config/;\
	elif [ -d "../cave/config/" ];then \
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -locale=zh -confdir=../cave/config/;\
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
	elif [ -d "cave/config/" ];then \
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -locale=zh -confdir=cave/config/;\
	elif [ -d "../cave/config/" ];then \
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -locale=zh -confdir=../cave/config/;\
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
		sudo yum install python-virtualenv ;\
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
package:
	@rm -rf /tmp/cave_gmt
	@mkdir -p /tmp/cave_gmt
	@cp -rf . /tmp/cave_gmt
	@rm -rf /tmp/cave_gmt/.git
	@rm -rf /tmp/cave_gmt/data/*
	@rm -rf /tmp/cave_gmt.tgz
	@cd /tmp;tar -czf /tmp/cave_gmt.tgz cave_gmt
	if [ -d ~/www.najaplus.com/template_static  ]; then\
		mv /tmp/cave_gmt.tgz ~/www.najaplus.com/template_static;\
		echo "~/www.najaplus.com/template_static/cave_gmt.tgz";\
		echo "http://www.najaplus.com/cave_gmt.tgz";\
	fi
	@echo "/tmp/cave_gmt.tgz"
