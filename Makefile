# -*- coding:utf-8 -*-
.PHONY: build-dep
.PHONY: test

ROOT_DIR=$(shell pwd)

run-pro:
	@if [ -d "~/.cave/" ];then \
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -etcd=127.0.0.1:2379 -locale=zh -confdir=~/.cave/;\
	elif [ -d "/data/cave/config/" ];then \
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -etcd=127.0.0.1:2379 -locale=zh -confdir=/data/cave/config/;\
	elif [ -d "./config/" ]; then\
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -etcd=127.0.0.1:2379 -locale=zh -confdir=./config/;\
	elif [ -d "../config/" ];then \
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -etcd=127.0.0.1:2379 -locale=zh -confdir=../config/;\
	elif [ -d "cave/config/" ];then \
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -etcd=127.0.0.1:2379 -locale=zh -confdir=cave/config/;\
	elif [ -d "../cave/config/" ];then \
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -etcd=127.0.0.1:2379 -locale=zh -confdir=../cave/config/;\
	else \
		echo "no confdir,please give -confdir like";\
		echo "./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -etcd=127.0.0.1:2379 -locale=zh -confdir=../config/";\
	fi

run-stage:
	./virtual/bin/python src/main.py -mode=stage
run:
	./virtual/bin/python src/main.py
run-pro-en:
	@if [ -d "~/.cave/" ];then \
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -etcd=127.0.0.1:2379 -locale=en -confdir=~/.cave/;\
	elif [ -d "/data/cave/config/" ];then \
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -etcd=127.0.0.1:2379 -locale=en -confdir=/data/cave/config/;\
	elif [ -d "./config/" ]; then\
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -etcd=127.0.0.1:2379 -locale=en -confdir=./config/;\
	elif [ -d "../config/" ];then \
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -etcd=127.0.0.1:2379 -locale=en -confdir=../config/;\
	elif [ -d "cave/config/" ];then \
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -etcd=127.0.0.1:2379 -locale=zh -confdir=cave/config/;\
	elif [ -d "../cave/config/" ];then \
		./virtual/bin/python src/main.py -host=0.0.0.0 -mode=pro -etcd=127.0.0.1:2379 -locale=zh -confdir=../cave/config/;\
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
		if [ `uname -s` = "Darwin" ] ; then \
				sudo easy_install pip;\
				sudo pip install virtualenv;\
		else \
			sudo yum install python-virtualenv ;\
		fi;\
		virtualenv virtual; \
	fi
	./virtual/bin/pip install tornado==4.4
	./virtual/bin/pip install chardet
	./virtual/bin/pip install qiniu
	./virtual/bin/pip install redis
	./virtual/bin/pip install simplejson
	./virtual/bin/pip install python-etcd
	./virtual/bin/pip install tornado-mysql
	cd src/tea;sh buildtea.sh

clean:
	find . -name "*.pyc" -exec rm {} \;
package-full:
	@rm -rf /tmp/cave_gmt
	@mkdir -p /tmp/cave_gmt
	@cp -rf . /tmp/cave_gmt
	@rm -rf /tmp/cave_gmt/.git
	@rm -rf /tmp/cave_gmt/data/*
	@rm -rf /tmp/cave_gmt/DynamicUpload/destTmp
	@rm -rf /tmp/cave_gmt.tgz
	@cd /tmp;tar -czf /tmp/cave_gmt.tgz cave_gmt
	if [ -d ~/www.najaplus.com/template_static  ]; then\
		mv /tmp/cave_gmt.tgz ~/www.najaplus.com/template_static;\
		echo "~/www.najaplus.com/template_static/cave_gmt.tgz";\
		echo "`md5sum ~/www.najaplus.com/template_static/cave_gmt.tgz`";\
		echo "http://www.najaplus.com/cave_gmt.tgz";\
	fi
	@echo "/tmp/cave_gmt.tgz"
package:
	@rm -rf /tmp/cave_gmt
	@mkdir -p /tmp/cave_gmt
	@cp -rf . /tmp/cave_gmt
	@rm -rf /tmp/cave_gmt/.git
	@rm -rf /tmp/cave_gmt/data/*
	@rm -rf /tmp/cave_gmt/virtual/
	@rm -rf /tmp/cave_gmt/DynamicUpload/destTmp
	@rm -rf /tmp/cave_gmt.tgz
	@cd /tmp;tar -czf /tmp/cave_gmt.tgz cave_gmt
	if [ -d ~/www.najaplus.com/template_static  ]; then\
		mv /tmp/cave_gmt.tgz ~/www.najaplus.com/template_static;\
		echo "~/www.najaplus.com/template_static/cave_gmt.tgz";\
		echo "`md5sum ~/www.najaplus.com/template_static/cave_gmt.tgz`";\
		echo "http://www.najaplus.com/cave_gmt.tgz";\
	fi
	@echo "/tmp/cave_gmt.tgz"

update:
	rm -rf /tmp/tmp_cave_gmt
	mkdir /tmp/tmp_cave_gmt
	curl -L http://www.najaplus.com/cave_gmt.tgz >/tmp/tmp_cave_gmt/cave_gmt.tgz
	tar -xf /tmp/tmp_cave_gmt/cave_gmt.tgz -C /tmp/tmp_cave_gmt/
	mkdir -p /data/cave_gmt/{DynamicUpload,virtual,src,template,static}
	cp -rf /tmp/tmp_cave_gmt/cave_gmt/DynamicUpload/* /data/cave_gmt/DynamicUpload/
	cp -rf /tmp/tmp_cave_gmt/cave_gmt/static/* /data/cave_gmt/static/
	cp -rf /tmp/tmp_cave_gmt/cave_gmt/template/* /data/cave_gmt/template/
	cp -rf /tmp/tmp_cave_gmt/cave_gmt/src/* /data/cave_gmt/src/
	cp -rf /tmp/tmp_cave_gmt/cave_gmt/Makefile /data/cave_gmt/
	@if [ -d /tmp/tmp_cave_gmt/cave_gmt/virtual/ ]; then  \
		cp -rf /tmp/tmp_cave_gmt/cave_gmt/virtual/* /data/cave_gmt/virtual/;\
	fi

