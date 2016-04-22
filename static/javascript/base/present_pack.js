var goodsAddEl = $('#op-pack-goods-add'),
    listEl = $('#op-pack-content-list'),
    typeEl = $('#op-pack-goods-type'),
    numEl = $('#op-pack-goods-num'),
    goodsIdEl = $('#op-pack-goods-id'),
    goodsIdNameEl = $('#op-pack-goods_id_name'),
    idData,
    getIdFun,
    getPackDataFun;


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
            htmlStr += '<li class="ui-pack-item clearfix op-goods-item" data-id="' + typeId + '" data-goodsid="' + goodsId + '" data-count="' + count + '">' +
                '<span>' + typeName + 'x' + count + '</span>' +
                '<button class="btn btn-default ui-item-delete op-pack-award-delete">删除</button>' +
                '</li>';
        }else{
            htmlStr += '<li class="ui-pack-item clearfix op-goods-item" data-id="' + typeId + '" data-goodsid="' + goodsId + '" data-count="' + count + '">' +
                '<span>[' + typeName +" "+goodsIdName+ ']x' + count + '</span>' +
                '<button class="btn btn-default ui-item-delete op-pack-award-delete">删除</button>' +
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

listEl.delegate('.op-pack-award-delete', 'click', function(e) {
    $(e.currentTarget).parent().remove();
    return false;
});

getIdFun = function(type) {
    var url='/present_pack/id_list';
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
        getIdFun(type);
    } else {
        return false;
    }
});

getPackDataFun=function() {
    var data = {},
        pack_awards = "",
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
        pack_awards=pack_awards+ id+":"+goodsId+":"+count;
        if (i!=len-1) {
            pack_awards=pack_awards+"|"
        }
    }
    data['pack_awards'] = pack_awards;
    return data
}
// demo
// submitEl.on('click', function(){
//     ajaxing = true;
//     $.ajax({
//         url: '/present_pack/add',
//         type: 'post',
//         data: getPackDataFun()
//     })
//         .done(function(data) {
//             ajaxing = false;
//             location.href = '/present_pack/list'
//         });
//     return false;
// });
