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
    var eml = this.parentNode.children[1]
    console.log("yes"+id)
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id//prod_id=id goes to url pluscart
        },
        success: function(data){//if success then success function is called
            console.log(data)
            console.log("success")
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount

        }
            
    })
})

$('.minus-cart').click(function () {
    console.log("minus-clicked")
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[1]
    console.log("yes"+id)
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id//prod_id=id goes to url minuscart
        },
        success: function(data){//if success then success function is called
            console.log(data)
            console.log("success")
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount

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

        }
            
    })
})

//Wishlist
$(".add-wishlist").on('click',function(){
    var pid = $(this).attr('data-product');
    var vm = $(this);
    // console.log("product_id"+pid);
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

                // console.log($(".reviews").prepend(_html))//for showing at top same like stack
                $(".reviewsed").prepend(_html);//prepend data
                $("#ProductReview").modal('hide');//hide modal
                $(".nodata").hide()//hide pclass nodata after review is added

                //avg rating
                console.log(res.avg_reviews.avg_rating)
                $(".avgrating").text(res.avg_reviews.avg_rating.toFixed(1))//tofixed shows 1 number after decimal like 1.2

            }
        }
    });
    e.preventDefault();//helps to prevent the page from reloading
});