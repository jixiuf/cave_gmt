var goodsAddEl = $('#op-award-goods-add'),
    awardlistEl = $('#op-award-content-list'),
    awardtypeEl = $('#op-award-goods-type'),
    awardnumEl = $('#op-award-goods-num'),
    awardgoodsIdEl = $('#op-award-goods-id'),
    awardgoodsIdNameEl = $('#op-award-goods_id_name'),
    awardgoodsParam1El = $('#op-award-goods-param1'),
    awardgoodsParam2El = $('#op-award-goods-param2'),
    awardIdData,
    getAwardSubIdFun,
    getAwardDataFun;


goodsAddEl.on('click', function() {
    var typeName = '',
        typeId = '',
        goodsId = '',
        count = '',
        htmlStr = '';

    tokens=awardtypeEl.val().split(":");
    typeId = tokens[0];
    /*             hasId  = tokens[1]; */
    goodsId = awardgoodsIdEl.val();
    goodsParam1=awardgoodsParam1El.val();
    goodsParam2=awardgoodsParam2El.val();
    goodsIdName=awardgoodsIdNameEl.val();
    count = awardnumEl.val();
    if(isNaN(goodsId)){
        alert("物品id格式不对 不是数字");
        return false;
    }
    if(isNaN(count)){
        alert("数量格式不对 不是数字");
        return false;
    }
    if(typeId != '0' && count != ''&&count!='0') {
        typeName = awardtypeEl.find("option:selected").text();
        if(goodsId==""){
            htmlStr += '<li class="ui-award-item clearfix op-goods-item" data-id="' + typeId + '"'+' data-goods-desc="'+ typeName + 'x' + count+ '"'+' data-goodsid="0" data-count="' + count + '">' +
                '<span>' + typeName + 'x' + count + '</span>' +
                '<button class="btn btn-default ui-item-delete op-award-delete">删除</button>' +
                '</li>';
        }else{
            htmlStr += '<li class="ui-award-item clearfix op-goods-item" data-id="' + typeId + '"'+
                ' data-goods-desc="[' + typeName+" "+goodsIdName+"("+goodsId +")"  +":"+ goodsParam1 +":"+ goodsParam2+ ']x' + count
                +'" data-goodsid="' + goodsId + '" data-count="' + count +'" data-goods-param1="'+goodsParam1 +'" data-goods-param2="' +goodsParam2 + '">' +
                '<span>[' + typeName +":"+goodsIdName+'('+goodsId+')'  +":"+ goodsParam1 +":"+ goodsParam2+  ']x' + count +'</span>' +
                '<button class="btn btn-default ui-item-delete op-award-delete">删除</button>' +
                '</li>';
        }
        awardlistEl.append(htmlStr);
        // awardtypeEl.children().eq(0).attr('selected', 'true');
        awardgoodsIdEl.val('');
        awardgoodsParam1El.val('');
        awardgoodsParam2El.val('');
        awardnumEl.val('');
        // awardgoodsIdEl.addClass('hide');
        // awardgoodsParam1El.addClass('hide');
        // awardgoodsParam2El.addClass('hide');
    } else {
        return false;
    }
});

awardlistEl.delegate('.op-award-delete', 'click', function(e) {
    $(e.currentTarget).parent().remove();
    return false;
});

getAwardSubIdFun = function(type) {
    var url='/award/sub_id_list';
    var infoType = type;

    ajaxing = true;
    $.ajax({
        url: url,
        type: 'post',
        infoType: infoType,
        data:{"id":type}
    })
        .done(function(data) {
            if(data['action'] == 'success') {
                ajaxing = false;
                awardIdData=JSON.parse(data['result']);
                awardgoodsIdEl.autocomplete({source: awardIdData, minLength:0,
                                        select: function( event, ui ) {awardgoodsIdNameEl.val(ui.item.label);}});
                awardgoodsIdEl.autocomplete( "search", awardgoodsIdEl.val());
            }
        });
}


awardtypeEl.on('change', function(e) {
    var val = e.currentTarget.value;
    awardgoodsIdEl.val('');
    if(val.indexOf(":true")!= -1 ) {
        awardgoodsIdEl.removeClass('hide');
        awardgoodsParam1El.removeClass('hide');
        awardgoodsParam2El.removeClass('hide');
    } else {
        awardgoodsIdEl.addClass('hide');
        awardgoodsParam1El.addClass('hide');
        awardgoodsParam2El.addClass('hide');

    }
});

awardgoodsIdEl.on('click', function() {
    var type = awardtypeEl.val(),
        data;
    tokens=type.split(":");
    type=tokens[0];
    hasId=tokens[1];
    if(ajaxing) return false;
    if(hasId=="true") {
        getAwardSubIdFun(type);
    } else {
        return false;
    }
});

getAwardDataFun=function() {
    var data = {},
        awardStr = "",
        awardsDesc = "",
        goods = $('.op-goods-item'),
        id,count;
    goods = $('.op-goods-item');
    if(goods.length == 0) {
        data['awards'] = awardStr;
        return data;
    }
    data["award_list"]=[];
    for(var i = 0, len = goods.length; i < len; i++ ) {
        var info = {};
        id = goods.eq(i).data('id');
        goodsId = goods.eq(i).data('goodsid');
        count = goods.eq(i).data('count');
        param1 = goods.eq(i).data('goods-param1');
        param2 = goods.eq(i).data('goods-param2');
        awardStr=awardStr+ id+":"+goodsId+":"+count;
        awardsDesc+=goods.eq(i).data('goods-desc');
        awardJson={}
        awardJson["award_type"]=id;
        awardJson["award_id"]=goodsId;
        awardJson["award_count"]=count;
        awardJson["award_param_list"]=[];
        if (param1!=''&&param1!=undefined) {
            if(!isNaN(param1)){
                param1=param1.toString();
            }
            awardJson["award_param_list"].push(param1);
            awardStr=awardStr+ ":"+param1;
        }
        if (param2!=''&&param2!=undefined) {
            if(!isNaN(param2)){
                param2=param2.toString();
            }
            awardStr=awardStr+ ":"+param2;
            awardJson["award_param_list"].push(param2);
        }
        if (i!=len-1) {
            awardStr=awardStr+"|";
            awardsDesc+="|";
        }
        data["award_list"].push(awardJson);
    }
    data["award_list"]=JSON.stringify(data["award_list"]);
    data['awards'] = awardStr;
    data['awardsDesc'] = awardsDesc;
    return data
}

getAwardIdFun = function() {
    var url='/award/id_list';

    ajaxing = true;
    $.ajax({
        url: url,
        type: 'post',
        data:{}
    })
        .done(function(data) {
            if(data['action'] == 'success') {
                ajaxing = false;
                awardIdData=JSON.parse(data['result']);
                for(var key in awardIdData){
                    htmlStr ="<option value='"+key+":"+awardIdData[key]["has_id"]+"'>"+awardIdData[key]["name"]+"</option>"
                    awardtypeEl.append(htmlStr);
                }
            }
        });
}
// demo
// submitEl.on('click', function(){
//     ajaxing = true;
//     $.ajax({
//         url: '/present_award/add',
//         type: 'post',
//         data: getAwardDataFun()
//     })
//         .done(function(data) {
//             ajaxing = false;
//             location.href = '/present_award/list'
//         });
//     return false;
// });

