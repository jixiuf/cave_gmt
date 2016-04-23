var goodsAddEl = $('#op-award-goods-add'),
    listEl = $('#op-award-content-list'),
    typeEl = $('#op-award-goods-type'),
    numEl = $('#op-award-goods-num'),
    goodsIdEl = $('#op-award-goods-id'),
    goodsIdNameEl = $('#op-award-goods_id_name'),
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
            htmlStr += '<li class="ui-award-item clearfix op-goods-item" data-id="' + typeId + '" data-goodsid="' + goodsId + '" data-count="' + count + '">' +
                '<span>' + typeName + 'x' + count + '</span>' +
                '<button class="btn btn-default ui-item-delete op-award-delete">删除</button>' +
                '</li>';
        }else{
            htmlStr += '<li class="ui-award-item clearfix op-goods-item" data-id="' + typeId + '" data-goodsid="' + goodsId + '" data-count="' + count + '">' +
                '<span>[' + typeName +" "+goodsIdName+ ']x' + count + '</span>' +
                '<button class="btn btn-default ui-item-delete op-award-delete">删除</button>' +
                '</li>';
        }
        listEl.append(htmlStr);
        typeEl.children().eq(0).attr('selected', 'true');
        goodsIdEl.val('');
        goodsIdEl.addClass('hide');
        numEl.val('');
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
    } else {
        goodsIdEl.addClass('hide');
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
        award_awards = "",
        goods = $('.op-goods-item'),
        id,count;
    goods = $('.op-goods-item');
    if(goods.length == 0) {
        alert("未添加任何奖品");
        return data;
    }
    for(var i = 0, len = goods.length; i < len; i++ ) {
        var info = {};
        id = goods.eq(i).data('id');
        goodsId = goods.eq(i).data('goodsid');
        if (goodsId=="") {
            goodsId='0';
        }
        count = goods.eq(i).data('count');
        award_awards=award_awards+ id+":"+goodsId+":"+count;
        if (i!=len-1) {
            award_awards=award_awards+"|"
        }
    }
    data['awards'] = award_awards;
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

