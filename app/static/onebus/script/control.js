
$("#frmSearch").submit(function( event ){
    event.preventDefault();
    clearMap();
    
//    $("#divSearch").animate({ top: "5%" }, 800);
//    $("#background").slideUp("normal", function() { $(this).remove(); } );
//    $("#logo").slideUp("normal", function() { $(this).remove(); } );
//    $("#intro").slideUp("normal", function() { $(this).remove(); } );
//    $("#txtSearch").blur()
//    disable_inputs();

    var currentdate = new Date();
    var datetime =  currentdate.getFullYear() + "-"
                  + currentdate.getMonth() + "-"
                  + currentdate.getDate() + "|"
                  + currentdate.getHours() + ":"
                  + currentdate.getMinutes() + ":"
                  + currentdate.getSeconds()

    var $btn = $('#btnSubmit').button('loading')



//    $("#loading_hold").animate({ top: "0" }, 800);
    $.ajax({
        type: "POST",
        url: "/onebus/api",
        data: JSON.stringify({search_text: $("#txtSearch").val(),
                                home_gps: home_gps,
                                current_time: datetime}),
        success: function(response){ refreshMap(response); $btn.button('reset');},
        contentType: "application/json",
        dataType:'json'})

});

