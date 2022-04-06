/*  ---------------------------------------------------
    Template Name: Fashi
    Description: Fashi eCommerce HTML Template
    Author: Colorlib
    Author URI: https://colorlib.com/
    Version: 1.0
    Created: Colorlib
---------------------------------------------------------  */

'use strict';
// function clearform(){
//     document.getElementById('form').reset();
//     console.log("yessasdf");
// }
(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(200).fadeOut("slow");
        $(".ajaxloading").hide();
    });

    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });

    /*------------------
		Navigation
	--------------------*/
    $(".mobile-menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });
   

})(jQuery);

$('.plus-cart').click(function () {
    console.log("plus-clicked")
    var id = $(this).attr("pid").toString();
    var emls = this.parentNode.children[1]
    var eml = this.parentNode.children[2]
    console.log("yes"+id)
    console.log("yeseml "+eml)
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id//prod_id=id goes to url pluscart
        },
        success: function(data){//if success then success function is called
            console.log(data)
            if(data.quantity<=data.pquantity){
                console.log("success")
                emls.innerText = data.quantity
                document.getElementById("amount").innerText = data.amount
                document.getElementById("totalamount").innerText = data.totalamount
                
            }
            else{
                alertify.error("product will be out of stock if quantity will be more than "+ data.pquantity)
                // $(".plus-cart").hide()
                // emls.hide()
                eml.addClass('disabled').removeClass('plus-cart')          
            }
        }      
    })
})

$('.minus-cart').click(function () {
    console.log("minus-clicked")
    var id = $(this).attr("pid").toString();
    var emls = this.parentNode.children[1]
    var eml = this.parentNode.children[2]
    console.log("yes"+id)
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id//prod_id=id goes to url minuscart
        },
        success: function(data){//if success then success function is called
            console.log(data)
            if(data.quantity>=0){
                console.log("success")
                emls.innerText = data.quantity
                document.getElementById("amount").innerText = data.amount
                document.getElementById("totalamount").innerText = data.totalamount
            }
            // else{
            //     alertify.error("product quantity can't be zero")
            // }

        }
            
    })
})

$('.remove-cart').click(function () {
    console.log("remove-clicked")
    var id = $(this).attr("pid").toString();
    var eml = this
    console.log("yes"+id)//prints product id
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id//prod_id=id goes to url removecart
        },
        success: function(data){//if success then success function is called
            console.log(data)
            console.log("success")
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
            eml.parentNode.parentNode.parentNode.remove()
            console.log('badgecount'+data.cartcount)
            document.getElementById("badge").innerText = data.cartcount      
        }
            
    })
})

//increment btn in product detail
$('.increment-btn').click(function (e) {
    e.preventDefault();
    var proquan =  $(this).attr("pid").toString();
    var inc_value = $(this).closest('.row').find('.qty-input').val();
    var value = parseInt(inc_value,10);
    value = isNaN(value) ? 0 : value;
    console.log("goodebst "+proquan)
    if(value < proquan)
    {
        value++;
        $(this).closest('.row').find('.qty-input').val(value);
    }
    else{
        $(this).removeClass('qtybtn');
        $(this).addClass('newhover');
    }
});
//decrement btn in product detail
$('.decrement-btn').click(function (e) {
    e.preventDefault();

    var inc_value = $(this).closest('.row').find('.qty-input').val();
    var value = parseInt(inc_value,10);
    value = isNaN(value) ? 0 : value;
    if(value > 1)
    {
        value--;
        $(this).closest('.row').find('.qty-input').val(value);
    }
});

//Wishlist
$(".add-wishlist").on('click',function(){
    alertify.success("Product has been moved to Wishlist");
    var pid = $(this).attr('data-product');
    var vm = $(this);
    console.log("product_id"+pid);
    //Ajax
    $.ajax({
        url:"/add-wishlist",
        data:{
            product:pid//product=pid goes to url add-wishlist
        },
     //we receive datatype as json
        success:function(res){
            if(res.bool==true){
                vm.addClass('disabled').removeClass('add-wishlist');
            }
            console.log("wowow"+res.wlistcount)
            document.getElementById("wlistbadge").innerText = res.wlistcount
        }
    });
    //EndAjax

});

//wishlist removeitem
$('.remove-item').click(function () {
    console.log("remove-clicked")
    var id = $(this).attr("pid").toString();
    var eml = this
    console.log("yes"+id)//prints product id
    $.ajax({
        type: "GET",
        url: "/removeitem",
        data: {
            prod_id: id//prod_id=id goes to url removeitem and it is sent to remove_item in views.py
        },
        success: function(data){//if success then success function is called
            console.log("success")
            eml.parentNode.parentNode.remove()
            document.getElementById("wlistbadge").innerText = data.wlistcount

        }
            
    })
})

$("#addForm").submit(function(e){
    $.ajax({
        data:$(this).serialize(),//pass all the data into form
        method:$(this).attr('method'),//same like above in minuscart where the type is post in form method = post in productdetail.html
        url:$(this).attr('action'),//sends it to the respective url defined in form action in productsdetails.html
        dataType:'json',
        success:function(res){
            if(res.boolean==true){
                $(".ajaxRes").html('Data has been added');
                $("#reset").trigger('click');
                $(".reviewBtn").hide();//hidebutton

                //create data for review
                var _html='<ul class="reviews">';
                _html+='<li>'; 
                _html+='<div class="review-heading">';
                _html+='<h5 class="name">'+res.data.user+'</h5>'; //concatinating the javascript
                _html+='<div class="review-rating">'; 
                for(var i=1;i<=res.data.review_rating; i++){
                    _html+= '<i class="fa fa-star"></i>';
                }
                _html+='</div>'; 
                _html+='</div>'; 
                _html+='<div class="review-body">'; 
                _html+='<p>'+res.data.review_text+'</p>'; 
                _html+='</div>'; 
                _html+='</hr>'; 
                _html+='</li>'; 
                _html+='</ul>'; 
                _html+='<hr>';

                // console.log($(".reviews").prepend(_html))//for showing at top same like stack
                $(".reviewsed").prepend(_html);//prepend data
                $("#ProductReview").modal('hide');//hide modal
                $(".nodata").hide()//hide pclass nodata after review is added
                console.log(res.counter)
                document.getElementById("reviewcount").innerText = res.counter
                // $(".reviewcount").innerText = res.counter

                //avg rating
                console.log(res.avg_reviews.avg_rating)
                $(".avgrating").text(res.avg_reviews.avg_rating.toFixed(1))//tofixed shows 1 number after decimal like 1.2

            }
        }
    });
    e.preventDefault();//helps to prevent the page from reloading
});

$("#loadmore").on('click',function(){
    var currentproducts = $(".productbox").length;//this currentproducts means how many products are shown in productlist html
    var limit=$(this).attr('data-limit');//this is the number of products we want to show in a row
    var total = $(this).attr('data-total');//this total means the total products we have in database
    var catid = $(this).attr('catid');
    console.log("hahha"+currentproducts,limit,total,catid)
    var url = "/load-more-data/"+ catid;
    console.log("url"+ url)
    //start ajax
    $.ajax({
        url: url,
        data: {//this data is sent to the server
            limit: limit,
            curproducts: currentproducts
        },
        dataType:'json',
        beforeSend:function(){//data fetch hune agadi chalne code when users click on load more button
            $("#loadmore").attr('disabled',true);
            $(".load-more-icon").addClass('fa-spin');
        },
        success:function(res){//catches the data which is given by views.py
            console.log("success")
            $("#productlists").append(res.datas);
            $("#loadmore").attr('disabled',false);
            $(".load-more-icon").removeClass('fa-spin');

            var curtotalproducts = $(".productbox").length;
            if(curtotalproducts==total){
                $("#loadmore").remove();
            }
        }
            
    })
    //end ajax
})

// for filtering price of product list
$(".form-check-input").on('click',function(){
    console.log("clicked baby");
    var catid = $(this).attr('catid');
    var url = "/filter-data/"+ catid;
    var filterObj = {};
    $(".form-check-input").each(function(index,ele){//looping for each iteration
        var filterval = $(this).val();//value dinxa form-check-input ko
        var filterkey = $(this).attr('data-filter');//data-filter attribute ma lekheko key dinxa i.e.brand which is defined under .form-check-input class
        // console.log(filterval,filterkey);
        filterObj[filterkey]=Array.from(document.querySelectorAll('input[data-filter='+filterkey+']:checked')).map(function(el){//filterobj vane array ma click gareko filter ko id pass garauna hamile esto use gareko
            return el.value;
       });
    });
    console.log(filterObj)

    $.ajax({
        url:url,
        data:filterObj,
        dataType:'json',
        beforeSend:function(){//It will show things until we get the response from server
            $(".ajaxloading").show();
        },
        success:function(res){
            console.log("success");
            $("#productlists").html(res.data);
            $(".ajaxloading").hide();
        }

    });
});


// Filter Product According to the price
$("#maxPrice").on('blur',function(){
    var _min=$(this).attr('min');
    var _max=$(this).attr('max');
    var _value=$(this).val();
    console.log(_value,_min,_max);
    if(_value < parseInt(_min) || _value > parseInt(_max)){
        alert('Values should be '+_min+'-'+_max);
        $(this).val(_min);
        $(this).focus();
        $("#rangeInput").val(_min);
        return false;
    }
});