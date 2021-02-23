"use strict";

window.onload = function () {
    console.log('DOM ready');
    $('.basket_record').on('change', "input[type='number']", function (event) {
        let qty = event.target.value;
        let BasketItemPK = event.target.name;
        console.log(productPk, qty);
        $.ajax({
            url: "/basket/edit/" + t_href.name + "/" + t_href.value + "/",

            success: function (data) {
                $('.basket_list').html(data.result);
            },
        });
    });
}
