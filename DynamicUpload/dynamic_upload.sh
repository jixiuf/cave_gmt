#!/bin/bash
# 需要用到的命令 ，确保svn  zip,curl,python 以安装
#用法举例比如 ./dynamic_upload.sh gamename 版本号  svnVersionFrom svnVersionTo svn_resource_url gmt_notify_url show_version channel1 channel2 ....channelN
#用法举例比如 ./dynamic_upload.sh goldflower 1100083  1005 1139 svn://svn.najaplus.com/game1/dev/Data http://dev.najaplus.com:8000 v1.2.3 6 7
# ./dynamic_upload.sh cave 1001005  10174 10888 svn://svn.najaplus.com/game2/dev/client/cocos2d-x-2.2.6/projects/client/Resources http://cavegmt.zh.najaplus.com  v1.2.3 10
dir=`pwd`
cd `dirname $0`
# qiniu accesskey secretkey
qiniu_bucket=najaplus
qiniu_accesskey=AYwnALpeN5pT5c--NG2sjbnUNP1ey9px4SZAFD-3
qiniu_secretkey=jLLvul-joXk6ALMCNkJVnxexsi7yMa7U--dJjwnU
qiniu_base_url=http://qiniu.najaplus.com/

gamename=$1
version=$2
from=$3
to=$4
svnpath=$5
gmt_url=$6
show_version=$7

channel_begin_param=7           # 加参数时要改此值

svnUser=version
svnPassword=u3gZa2fWKM

gmt_notify_url="$gmt_url""/api/game/dynamic"
gmt_update_version_url="$gmt_url""/game/server_version_update"
# 压缩zip包
./svndiffzip.sh $from $to $svnpath dest.zip $version $show_version $svnUser $svnPassword
filesize=`wc -c <dest.zip|xargs` # use xargs to trim space

# 把上层目录加入到path下
export PATH=$PATH:`pwd`
if [ `uname -s` = "Darwin" ] ; then
    qshell=qshell_darwin_amd64;
 else
    qshell=qshell_linux_amd64;
fi
chmod 755 qshell*

qiniu_filename="$gamename""_""$version""_""$from""_""$to"".zip"


$qshell account $qiniu_accesskey $qiniu_secretkey
qiniu_upload_result=`$qshell fput $qiniu_bucket $qiniu_filename dest.zip true`
echo $qiniu_upload_result
# 上传返回的字符串中如果含有success则认为成功
if [ `echo $qiniu_upload_result | grep -c "success" ` -eq 0 ]; then
    # 如果上传失败
    echo "qiniu upload fail";
   exit 1
fi


# prefetch指令根据七牛的公开API prefetch 更新七牛空间中的某个文件。配置
# 了镜像存储的空间，在一个文件首次回源源站拉取资源后，就不再回源了。如果
# 源站更新了一个文件，那么这个文件不会自动被同步更新到七牛空间，这个时候
# 需要使用prefetch去主动拉取一次这个文件的新内容回来覆盖七牛空间中的旧文
# 件。
# 1. 每天文件刷新限额500个，文件预取限额100个；
# 2. 每次提交文件刷新最多20个，文件预取最多20个；

# qiniu_prefetch_result=`$qshell prefetch $qiniu_bucket $qiniu_filename`
# echo $qiniu_prefetch_result
# # 上传返回的字符串中如果含有success则认为成功
# if [ `echo $qiniu_prefetch_result | grep -c "success" ` -eq 0 ]; then
#     # 如果上传失败
#     echo "qiniu prefetch $qiniu_filename fail";
#    exit 1
# fi


# 遍历渠道号
args_idx=0
for channel in $@
do
    if [ $args_idx -ge $channel_begin_param ] ; then
        # 从第6个参数开始 以后的参数都是渠道号
        qiniu_file_url="$qiniu_base_url""$qiniu_filename"
        echo "<a href='$qiniu_file_url'>$qiniu_file_url</a>"
        # quoted_qiniu_file_url=`python -c "import sys, urllib as ul;print ul.quote_plus(\"$qiniu_file_url\")"`
        gmt_notify_url_with_param="$gmt_notify_url""?user=najaplus&password=qHcdGfE6TH&fucker=najaplus&channel=""$channel""&version=""$version""&url=""$qiniu_file_url""&size=""$filesize""&svnVersion=""$to"
        echo $gmt_notify_url_with_param
        curl $gmt_notify_url_with_param
        echo ""

    fi
    let ++args_idx
done

# echo "到gmt后台去完成最后一步，刷新版本 $gmt_update_version_url"
# if [ `uname -s` = "Darwin" ] ; then
#     open $gmt_update_version_url
# fi

rm dest.zip
cd $dir                         # 回到执行此脚本时所在的目录
