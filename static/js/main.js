var Price = function(){
    var numSeats = $('#seats').val();
    if (numSeats === undefined)
        numSeats = 1;
    var price = 10; 
    var totalPrice = price * numSeats;
    var strprice = 'Price:&nbsp;&nbsp;('+ price.toString()+ 'x'+ numSeats +') = '+totalPrice.toString() + '$';
    $("#price").empty();
    $("#price").append(strprice);
}  

$(function(){
    Price();
})