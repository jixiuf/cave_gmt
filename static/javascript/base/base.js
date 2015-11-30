serverChoise = {
    'useLikeThis': function() {
       var  useStr = "var platformData = {% raw result %},\n" +
                     "    serverWrapEl = $('.op-server-wrap');\n" +

                     "**append to page\n" +
                     "serverChoise.serverDomAdd(platformData, serverWrapEl, showTest = false);\n" +

                     "**get list\n" +
                     "list = serverChoise.servers(channelEl);\n" +

                     "**check server\n" +
                     "if(!serverChoise.hasServer(list)) {\n" +
                     "    return false;\n" +
                     "}"
        return useStr;
    },

    'serverDomAdd': function(platformData, serverWrapEl, showTest) {
        var htmlStr = '';
        for(var platformIndex in platformData) {
            var platformStr = '',
                platformName = '';
            //不显示停服中服务器
            if(!showTest) {
                if(platformIndex > 100) {
                    continue;
                }
            }
            for(var serverIndex in platformData[platformIndex]) {
                var serverInfo = platformData[platformIndex][serverIndex];
                if(serverInfo['platform_name'] != '') {
                    platformName = serverInfo['platform_name'];
                }
                platformStr += '<li class="ui-server-item">' +
                                 serverInfo['server_name'] +
                                 '<input class="op-server-select" type="checkbox" data-server="' + serverIndex + '">' +
                              '</li>'
            }
            htmlStr += '<li class="ui-channel-item clearfix op-channel-item" data-channel="' + platformIndex + '">' +
                           '<div class="ui-channel-name">' +
                               platformName + '<input type="checkbox" class="op-select-all">' +
                           '</div>' +
                           '<div class="ui-server-field">' +
                               '<ul class="ui-server-list clearfix">' +
                                   platformStr +
                               '</ul>' +
                           '</div>' +
                       '</li>'
        }
        serverWrapEl.append(htmlStr);
        serverWrapEl.delegate('.op-select-all', 'click', function(e) {
            var targetEl = $(e.currentTarget);
            if(targetEl.is(':checked')) {
                targetEl.parent().parent().find('.op-server-select').each(function() {
                    this.checked = true;
                });
            } else {
                targetEl.parent().parent().find('.op-server-select').removeAttr('checked');
            }
        });
    },

    'servers': function(channelEl, allServer) {
        list = {};
        for(var i = 0, ilen = channelEl.length; i < ilen; i++) {
            var channel = channelEl.eq(i).data('channel'),
                serverEl = channelEl.eq(i).find('.op-server-select');
            if(allServer) {
                serverList = {}
            } else {
                serverList = [];
            }
            for(var j = 0, jlen = serverEl.length; j < jlen; j++) {
                var serverId = $(serverEl[j]).data('server');
                if(allServer) {
                    var checked = '0';
                    if(serverEl[j].checked) {
                        checked = '1';
                    }
                    serverList[serverId + ''] = checked;
                } else {
                    if(serverEl[j].checked) {
                        serverList.push(serverId);
                    }
                }
            }

            if(allServer) {
                list[channel + ''] = serverList;
            } else {
                if(serverList.length) {
                    list[channel + ''] = serverList;
                }
            }
        }
        return list;
    },

    'hasServer': function(list, allServer) {
        var checked = false;
        if(allServer) {
            for(var i in list) {
                for(var j in list[i]) {
                    if(list[i][j] == '1') {
                        checked = true;
                    }
                }
            }
        } else {
            var keys = [];
            for(var i in list) {
                keys.push(i);
            }

            if(keys.length) {
                checked = true;
            }
        }
        return checked;
    }
};

serverChoiseSingle = {
    'useLikeThis': function() {
        var  useStr = "serverChoiseSingle.allBinding(platformEl, serverEl);\n" +
                      "serverChoiseSingle.platformBinding(platformEl);\n" +
                      "serverChoiseSingle.search(searchEl, callback);";
        return useStr;
    },

    'allBinding': function(platformEl, serverEl, showTest) {
        this.action = 'allBinding';
        if(showTest) this.showTest = showTest;
        this.platformEl = platformEl;
        this.serverEl = serverEl;
        this.serverInfo(this.addAll);
    },

    'platformBinding': function(platformEl, showTest) {
        this.action = 'platformBinding';
        if(showTest) this.showTest = showTest;
        this.platformEl = platformEl;
        this.serverInfo(this.addPlatform);
    },

    'addAll': function(data, self) {
        self.addPlatformDom(data);
        self.addServerDom(data);
    },

    'addPlatform': function(data, self) {
        self.addPlatformDom(data);
    },

    'serverInfo': function(callback) {
        var self = this;
        $.ajax({
            url: '/api/server/info',
            type: 'post',
            data: {},
            callback: callback
        })
        .done(function(data) {
            data = JSON.parse(data);
            this.callback(data, self);
        });
    },

    'addPlatformDom': function(data) {
        var platformName,
            platformStr = '';
        for(var platformIndex in data) {
            if(!this.showTest) {
                if(platformIndex > 100) {
                    continue;
                }
            }
            platformName = data[platformIndex][Object.keys(data[platformIndex])[0]]['platform_name'];
            platformStr += '<option value="' + platformIndex + '">' + platformName + '</option>';
        }
        this.platformEl.append(platformStr);
    },

    'addServerDom': function(data) {
        var self = this,
            serverName;
        this.platformEl.on('change', function() {
            var platformId = platformEl.val(),
                serverStr = '<option value="0">请选择服务器</option>';
            if(platformId != '0') {
                for(var serverIndex in data[platformId]) {
                    serverName = data[platformId][serverIndex]['server_name'];
                    serverStr += '<option value="' + serverIndex + '">' + serverName + '</option>';
                }
            }
            serverEl.html(serverStr);
        });
    },

    'search': function(searchEl, callback) {
        this.callback = callback;
        var self = this;
        searchEl.on('click', function() {
            var platform,
                server;
            if(self.action == 'allBinding') {
                platform = self.platformEl.val();
                server = self.serverEl.val();
                if(platform != 0 && server != 0) {
                    self.callback(platform, server);
                }
            }
            if(self.action == 'platformBinding') {
                platform = self.platformEl.val();
                if(platform != 0) {
                    self.callback(platform);
                }
            }
        });
    }
};

anyTime = {
    'timeDouble': function(startEl, endEl, dataRule) {
        var oneSecond = 1000,
            oneDay = 24*60*60*1000,
            rangeDemoFormat = "%Y-%m-%d";
        if(dataRule) {
            rangeDemoFormat = dataRule;
        }
        rangeDemoConv = new AnyTime.Converter({format:rangeDemoFormat});
        //$("#rangeDemoToday").click(function(e) {
        //    startEl.val(rangeDemoConv.format(new Date())).change();
        //});
        //$("#rangeDemoClear").click(function(e) {
        //    startEl.val("").change();
        //});
        startEl.AnyTime_picker({format:rangeDemoFormat});
        startEl.change(function(e) {
            try {
                var fromDay = rangeDemoConv.parse(startEl.val()).getTime(),
                    dayLater = new Date(fromDay+oneDay);
                if(dataRule) {
                    dayLater = new Date(fromDay+oneSecond);
                }
                //dayLater.setHours(0,0,0,0);
                //var ninetyDaysLater = new Date(fromDay+(90*oneDay));
                //ninetyDaysLater.setHours(23,59,59,999);
                endEl
                    .AnyTime_noPicker()
                    .removeAttr("disabled")
                    .val(rangeDemoConv.format(dayLater))
                    .AnyTime_picker({
                        earliest: dayLater,
                        format: rangeDemoFormat
                        //latest: ninetyDaysLater
                    });
            } catch(e) {
                endEl.val("").attr("disabled","disabled");
            }
        });
    }
},

uploadQiniu = {
    'upload': function(file, uploadedCbk, uploadingCbk, useFileName, insertOnly) {
        this.url = 'http://up.qiniu.com/';
        this.file = file;
        this.uploadedCbk = uploadedCbk;
        this.uploadingCbk = uploadingCbk;
        this.useFileName = useFileName;
        this.insertOnly = true;
        if(!insertOnly) {
            this.insertOnly = false;
        }
        this.getUptoken();
    },

    'onprogress': function(evt) {
        if (evt.lengthComputable) {
            var percent = Math.round(evt.loaded * 100 / evt.total);
            self.uploadingCbk(percent, self.uploadQiniu.file.name);
        }
    },

    'xhrFun': function() {
        var xhr = $.ajaxSettings.xhr(),
            onprogress = self.uploadQiniu.onprogress;
        if(onprogress && xhr.upload) {
            xhr.upload.addEventListener('progress', onprogress, false);
        }
        return xhr;
    },

    'getUptoken': function() {
        var self = this,
            data = {};
        if(ajaxing) return false;
        ajaxing = true;
        data['insert'] = this.insertOnly;
        if(this.useFileName) {
            data['file_name'] = this.file.name;
        }
        $.ajax({
            url: '/api/qiniu/uptoken',
            type: 'post',
            data: data
        })
        .done(function(data) {
            self.fetch(self, JSON.parse(data).uptoken)
        });
    },

    'fetch': function(self, uptoken) {
        var data = new FormData();
        data.append("token", uptoken);
        data.append("file", self.file);
        if(self.useFileName) {
            data.append("key", self.file.name);
        }
        $.ajax({
            url: self.url,
            type: 'post',
            processData: false,
            contentType: false,
            data: data,
            statusCode: {
                614: function() {
                    alert(self.file.name + ' already exists!');
                }
            },
            xhr: self.xhrFun
        })
        .done(function(data) {
            var info = data.url;
            ajaxing = false;
            self.uploadedCbk(self.file, info)
        });
    }
}

uploadToQiniu = {
    'run': function(upUrl, uploadEl, optionEl, action, perEl) {
        this.url = 'http://up.qiniu.com/';
        this.uploadEl = uploadEl;
        this.action = action;
        if(perEl) this.perEl = perEl;
        if(action == 'image') {
            this.imgEl = optionEl;
            this.imgChangeBinding();
        }
        if(action == 'zip'){
            this.optionEl = optionEl;
            this.zipChangeBinding();
        }
    },

    'onprogress': function(evt) {
        if (evt.lengthComputable) {
            var percent = Math.round(evt.loaded * 100 / evt.total);
            if(self.uploadToQiniu.perEl) {
                self.uploadToQiniu.perEl.html('上传进度:' + percent + '%');
            }
        }
    },

    'xhrFun': function() {
        var xhr = $.ajaxSettings.xhr(),
            onprogress = self.uploadToQiniu.onprogress;
        if(onprogress && xhr.upload) {
            xhr.upload.addEventListener('progress', onprogress, false);
        }
        return xhr;
    },

    'beforeSend': function(xhr) {
        var fun = function() {
                console.log(xhr);
                setTimeout(fun,2000);
            }

        fun();
    },

    'uploadFile': function(self, uptoken) {
        var data = new FormData();
        data.append("token", uptoken);
        data.append("file", self.file);
        if(self.action == 'zip') {
            data.append("key", self.file.name);
        }
        self.uploadEl.attr('disabled', 'true');
        $.ajax({
            url: self.url,
            type: 'post',
            processData: false,
            contentType: false,
            data: data,
            xhr: self.xhrFun
//          beforeSend: self.beforeSend
        })
        .done(function(data) {
            var info = upUrl + data.key;
            if(self.action == 'image') {
                self.imgEl.attr('src', info);
            }
            if(self.action == 'zip') {
                self.optionEl.data('url', info);
            }
            ajaxing = false;
            self.uploadEl.removeAttr('disabled');
        });
        return false;
    },

    'getUptoken': function(callback) {
        var self = this;
        if(ajaxing) return false;
        ajaxing = true;
        $.ajax({
            url: '/api/qiniu/uptoken',
            type: 'post'
        })
        .done(function(data) {
            callback(self, JSON.parse(data).uptoken);
        });
    },

    'imgChangeBinding': function() {
        var self = this;
        this.uploadEl.on('change', function(e) {
            var fileEl = $(e.currentTarget),
                file = e.currentTarget.files[0],
                reader = new FileReader();
            self.file = file;
            reader.onload = function(event) {
                var dataUri = event.target.result,
                    img = new Image();
                img.src = dataUri;
                if(img.width == 550 && img.height == 210) {
                    self.getUptoken(self.uploadFile);
                } else {
                    alert('图片尺寸错误');
                    fileEl.val('');
                }
            };
            reader.readAsDataURL(file);
        });
    },

    'zipChangeBinding': function() {
        var self = this;
        this.uploadEl.on('change', function(e) {
            var fileEl = $(e.currentTarget),
                file = e.currentTarget.files[0];
            self.file = file;
            if(file.name.split('.')[1] == "zip") {
                self.getUptoken(self.uploadFile);
            } else {
                alert('只允许上传zip包');
                fileEl.val('');
            }
        });
    }
},

parseDate = function (input) {
    var parts = input.match(/(\d+)/g);
    return new Date(parts[0], parts[1]-1, parts[2], parts[3], parts[4], parts[5]);
},

defaultChannelName = {
    '6': 'app store',
    '7': 'iphonecake',
},

defaultRewardName = {
    '1': '金币',
    '2': '友情点',
    '3': 'FP',
    '4': 'Exp',
    '5': '钻石',
    '6': '道具',
    '7': '装备',
    '8': '卡片',
    '9': 'RMB',
    '10': '体力',
    '11': '卡片栏',
    '12': '装备栏',
    '13': '掉落组',
    '14': '荣誉',
    '16': '碎片',
    '17': '竞技场积分，功勋'
},

getJsonLength = function(jsonData){
    var jsonLength = 0;
    for(var item in jsonData){
        jsonLength++;
    }
    return jsonLength;
}
