
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

//    $("#loading_hold").animate({ top: "0" }, 800);
    $.ajax({
        type: "POST",
        url: "/api",
        data: JSON.stringify({search_text: $("#txtSearch").val(),
                                home_gps: home_gps,
                                current_time: datetime}),
        success: function(data){ refreshMap(data); enable_inputs();},
        contentType: "application/json",
        dataType:'json'})

});

