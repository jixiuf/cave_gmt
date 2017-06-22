#!/bin/sh
# 将两个版本之间变化的文件导出成一个zip
#用法举例比如 ./svndiffzip.sh 1005 1139 svn://svn.najaplus.com/game1/dev/Data dest.zip [svnusername,svnpassword]
# ./svndiffzip.sh 11664 11667 svn://svn.najaplus.com/game2/dev/client/cocos2d-x-2.2.6/projects/client/Resources dest.zip 100301111 v.1.3.7 version u3gZa2fWKM
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
    relativePath=`echo $url|sed "s|$svnpath||g"|sed 's|^/||g'` # lua/Core/Engine/CocosEasy.lua
    relativeDir=`echo $relativePath|sed 's|/|\\\\|g'` # "lua\Core\Engine\CocosEasy.lua" this is a file name  not dir
    svn $svnuser $svnpass --no-auth-cache --non-interactive export --force -r $to $url dest/$relativeDir
    if [ $? -ne 0 ];then
        # 任何一个svn相关的命令执行失败，则退出整个脚本，退出状态为1即，exit 1
        exit 3
    fi

    # 处理特殊类型的 *.ExportJson 文件 ，因为此文件内会引用别的文件，当此文件变更时，需要同时把它引用的文件打包进来，故
    #此得把它引用的文件找出来
    ext="${url##*.}"             # 取后缀art_highrt\ui\ui_battle_profile.json -> json
    filenamePrefix="${relativePath%/*}" # 去掉最后一个/ 及后面的内容 art_highrt/ui/ui_battle_profile.json -> art_highrt/ui
    filenamePrefix="$filenamePrefix/"  # art_highrt/ui-->art_highrt/ui/
    svnPrefix="${url%/*}" #svn://svn.najaplus.com/game2/dev/client/cocos2d-x-2.2.6/projects/client/Resources/art_high/art/model/trap/a.file--> svn://svn.najaplus.com/game2/dev/client/cocos2d-x-2.2.6/projects/client/Resources/art_high/art/model/trap
    if [ "ExportJson" = "$ext" ]; then
        relatedFiles=`python get_exportjson_related_files.py dest/$relativeDir`
        for relatedFile in $relatedFiles; do # a.plist
            relatedFileDir=`echo $filenamePrefix$relatedFile|sed 's|/|\\\\|g'` # "lua\Core\Engine\CocosEasy.lua" this is a file name  not dir
            relativeFileSvnUrl="${svnPrefix}/$relatedFile"
            svn $svnuser $svnpass --no-auth-cache --non-interactive export --force -r $to $relativeFileSvnUrl dest/$relatedFileDir
            if [ $? -ne 0 ];then
                # 任何一个svn相关的命令执行失败，则退出整个脚本，退出状态为1即，exit 1
                exit 3
            fi
        done
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
