var goodsAddEl = $('#op-award-goods-add'),
    listEl = $('#op-award-content-list'),
    typeEl = $('#op-award-goods-type'),
    numEl = $('#op-award-goods-num'),
    goodsIdEl = $('#op-award-goods-id'),
    goodsIdNameEl = $('#op-award-goods_id_name'),
    goodsParam1El = $('#op-award-goods-param1'),
    goodsParam2El = $('#op-award-goods-param2'),
    idData,
    getAwardSubIdFun,
    getAwardDataFun;


goodsAddEl.on('click', function() {
    var typeName = '',
        typeId = '',
        goodsId = '',
        count = '',
        htmlStr = '';

    tokens=typeEl.val().split(":");
    typeId = tokens[0];
    /*             hasId  = tokens[1]; */
    goodsId = goodsIdEl.val();
    goodsParam1=goodsParam1El.val();
    goodsParam2=goodsParam2El.val();
    goodsIdName=goodsIdNameEl.val();
    count = numEl.val();
    if(isNaN(goodsId)){
        alert("物品id格式不对 不是数字");
        return false;
    }
    if(isNaN(count)){
        alert("数量格式不对 不是数字");
        return false;
    }
    if(typeId != '0' && count != ''&&count!='0') {
        typeName = typeEl.find("option:selected").text();
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
        listEl.append(htmlStr);
        // typeEl.children().eq(0).attr('selected', 'true');
        goodsIdEl.val('');
        goodsParam1El.val('');
        goodsParam2El.val('');
        numEl.val('');
        // goodsIdEl.addClass('hide');
        // goodsParam1El.addClass('hide');
        // goodsParam2El.addClass('hide');
    } else {
        return false;
    }
});

listEl.delegate('.op-award-delete', 'click', function(e) {
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
                idData=JSON.parse(data['result']);
                goodsIdEl.autocomplete({source: idData, minLength:0,
                                        select: function( event, ui ) {goodsIdNameEl.val(ui.item.label);}});
                goodsIdEl.autocomplete( "search", goodsIdEl.val());
            }
        });
}


typeEl.on('change', function(e) {
    var val = e.currentTarget.value;
    goodsIdEl.val('');
    if(val.indexOf(":true")!= -1 ) {
        goodsIdEl.removeClass('hide');
        goodsParam1El.removeClass('hide');
        goodsParam2El.removeClass('hide');
    } else {
        goodsIdEl.addClass('hide');
        goodsParam1El.addClass('hide');
        goodsParam2El.addClass('hide');

    }
});

goodsIdEl.on('click', function() {
    var type = typeEl.val(),
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
            awardJson["award_param_list"].push(param1);
            awardStr=awardStr+ ":"+param1;
        }
        if (param2!=''&&param2!=undefined) {
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
                idData=JSON.parse(data['result']);
                for(var key in idData){
                    htmlStr ="<option value='"+key+":"+idData[key]["has_id"]+"'>"+idData[key]["name"]+"</option>"
                    typeEl.append(htmlStr);
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

