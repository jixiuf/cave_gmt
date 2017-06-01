#!/bin/sh
# 将两个版本之间变化的文件导出成一个zip
#用法举例比如 ./svndiffzip.sh 1005 1139 svn://svn.najaplus.com/game1/dev/Data dest.zip [svnusername,svnpassword]
 # ./svndiffzip.sh 1005 1139 svn://svn.najaplus.com/game1/dev/Data dest.zip svnuser svnpass
 # ./svndiffzip.sh 1005 1139 svn://svn.najaplus.com/game1/dev/Data dest.zip
# 其中svnusername svnpassword 可省略,省略则用系统缓存的
# 需要用到的命令 ，确保svn  zip 以安装
from=$1
to=$2
svnpath=$3
saveZipFileTo=$4
if [ -z $5 ];then
    svnuser=""
 else
    svnuser="--username $5"
fi
if [ -z $6 ];then
    svnpass=""
 else
    svnpass="--password $6"
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
