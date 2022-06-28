$(document).ready(function(){
    let form = $('#form_buy_product');
    console.log(form);

    function basketUpdating(product_id, am = 1, is_delete) {
        let data = {};
        data.product_id = product_id;
        data.am = am;

        let csrf_token = $('#form_buy_product [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;

        if (is_delete) {
            data["is_delete"] = true;
        }

        let url = form.attr("action");
        console.log(data);
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                console.log("success");
                console.log(data.products_total_amount);
                if (data.products_total_amount || data.products_total_amount == 0) {
                    $('#basket_total_amount').text("("+data.products_total_amount+")");
                    console.log(data.products);
                    $('.basket-items ul').html("");
                    $.each(data.products, function(key, value) {
                        $('.basket-items ul').append('<li>'+value.product_name+', ' + value.quantity + ' ед. ' + 'по ' +
                        value.item_price + 'BYN  ' + '<a class="delete-item" href="" data-product_id="'+value.id+'">X</a>' + '</li>');
                    })
                }

            },
            error: function() {
            console.log("error");
            }
       })
    }


    form.on('submit', function(e){
        e.preventDefault();
        let am = $('#amount').val();
        console.log(am);
        let submit_button = $('#submit_btn');
        let product_id = submit_button.data("product_id");
        let product_name = submit_button.data("product_name");
        let product_price = submit_button.data("price");
        console.log(product_id);
        console.log(product_name);

        basketUpdating(product_id, am, is_delete=false)


    });

    $('.basket-container').on('click', function(e){
        $(".basket-items").removeClass("d-none");
    });

    $('.basket-container').mouseover(function(){
        $('.basket-items').removeClass('d-none');
    });

    $('.basket-container').mouseout(function(){
        $('.basket-items').addClass('d-none');
    });

    $(document).on('click', '.delete-item', function(e){
        e.preventDefault();
        product_id = $(this).data("product_id");
        am = 0;
        basketUpdating(product_id, am, is_delete=true)
    })


    function calculatingBasketCost() {
        let order_total_cost = 0;
        $('.total-product-in-basket-cost').each(function() {
            order_total_cost = order_total_cost + parseFloat($(this).text());
        });
        $('.order_total_cost').text(order_total_cost.toFixed(2));
    };

    $(document).on('change', ".product-in-basket-am", function() {
        let current_amount = $(this).val();
        let current_tr = $(this).closest('tr');
        let current_price = parseFloat(current_tr.find('.product-price').text()).toFixed(2);
        let total_cost = parseFloat(current_amount*current_price).toFixed(2);
        current_tr.find('.total-product-in-basket-cost').text(total_cost);
        calculatingBasketCost();
    })

    calculatingBasketCost();

});