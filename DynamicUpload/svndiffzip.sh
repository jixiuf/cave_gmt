#!/bin/sh
# 将两个版本之间变化的文件导出成一个zip
#用法举例比如 ./svndiffzip.sh 1005 1139 svn://svn.najaplus.com/game1/dev/Data dest.zip [svnusername,svnpassword]
# ./svndiffzip.sh 11124 11127 svn://svn.najaplus.com/game2/dev/client/cocos2d-x-2.2.6/projects/client/Resources d.zip
 # ./svndiffzip.sh 1005 1139 svn://svn.najaplus.com/game1/dev/Data dest.zip svnuser svnpass
 # ./svndiffzip.sh 1005 1139 svn://svn.najaplus.com/game1/dev/Data dest.zip
# 其中svnusername svnpassword 可省略,省略则用系统缓存的
# 需要用到的命令 ，确保svn  zip 以安装
from=$1
to=$2
svnpath=$3
saveZipFileTo=$4
innner_version=$5
show_version=$6
if [ -z $7 ];then
    svnuser=""
 else
    svnuser="--username $7"
fi
if [ -z $8 ];then
    svnpass=""
 else
    svnpass="--password $8"
fi

# svnurl=`svn info --no-newline --show-item url $svnpath`
# if [ $? -ne 0 ];then
#     # 任何一个svn相关的命令执行失败，则退出整个脚本，退出状态为1即，exit 1
#     exit 1
# fi
svn_diff_status=`svn $svnuser $svnpass --non-interactive --no-auth-cache diff -r $from:$to  --no-diff-deleted --summarize $svnpath |grep -v "^D">change_file_list.txt`
if [ $? -ne 0 ];then
    rm -rf change_file_list.txt
    # 任何一个svn相关的命令执行失败，则退出整个脚本，退出状态为1即，exit 1
    exit 2
fi
changed_file=`cat change_file_list.txt|awk -F" " '{print $2}'`
rm -rf change_file_list.txt

rm  -rf dest
mkdir -p dest
for url in $changed_file ; do
    # 最后的sed 是为了去除目录最前面的/，以免变成绝对路径
    if [ -z `svn $svnuser $svnpass --non-interactive --no-auth-cache ls $url --depth empty` ]; then
        echo "$url is directory and is ignored for export"
        continue ;
    fi
    relativePath=`echo $url|sed "s|$svnpath||g"|sed 's|^/||g'`
    relativeDir=`echo $relativePath|sed 's|/|\\\\|g'`
    svn $svnuser $svnpass --no-auth-cache --non-interactive export --force -r $to $url dest/$relativeDir
    if [ $? -ne 0 ];then
        # 任何一个svn相关的命令执行失败，则退出整个脚本，退出状态为1即，exit 1
        exit 3
    fi

done
svn $svnuser $svnpass --no-auth-cache --non-interactive export --force -r $to $svnpath/config.json dest/config.json
if [ -n "$innner_version" ] && [ "default" != "$innner_version" ]; then
    echo "change innner_version to $innner_version of $resourceDirDest/config.json"
    sed -i  .bak "s|\"innner_version\": *\".*\"|\"innner_version\": \"$innner_version\"|g"  dest/config.json
fi
if [ -n "$show_version" ] && [ "default" != "$show_version" ]; then
    echo "change show_version to $show_version of $resourceDirDest/config.json"
    sed -i  .bak  "s|\"show_version\": *\".*\"|\"show_version\": \"$show_version\"|g" dest/config.json
fi
rm -f dest/config.json.bak
head dest/config.json

rm -rf dest.zip

# 加密lua

rm -rf destTmp
mkdir -p destTmp
python ./cocos2d-console/console/cocos2d.py luacompile -s dest/ -d destTmp --disable-compile -e true -k cb4166-a92250-e3a55d-c0549d-3ea2365c -b WANNA_DECRYPTION_??
cp -rf destTmp/* dest

cd dest/ ;zip ../dest.zip *;cd ..
rm -rf ./dest
if [ ! -z $saveZipFileTo ]; then
    mv dest.zip $saveZipFileTo
fi
