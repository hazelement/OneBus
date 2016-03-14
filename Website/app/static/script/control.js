
$("#frmSearch").submit(function( event ){
    event.preventDefault();
    clearMap();
    
    $("#divSearch").animate({ top: "5%" }, 800);
    $("#background").slideUp("normal", function() { $(this).remove(); } );
    $("#logo").slideUp("normal", function() { $(this).remove(); } );
    $("#intro").slideUp("normal", function() { $(this).remove(); } );
    disable_inputs();

//    $("#loading_hold").animate({ top: "0" }, 800);
    $.ajax({
        type: "POST",
        url: "/api",
        data: JSON.stringify({search_text: $("#txtSearch").val(), home_gps: home_gps, search_option: $('input[name=rbEngines]:checked').val()}),
        success: function(data){ refreshMap(data); enable_inputs();},
        contentType: "application/json",
        dataType:'json'})

});



function disable_inputs(){
    var radios = document.getElementsByName('rbEngines');
    for (var i = 0; i< radios.length;  i++){
        radios[i].disabled = true;
    };

    var input_field = document.getElementsByName('txtSearch');
    input_field.readOnly = true;

    document.getElementById("loading_hold").style.zIndex = "5";
    $("#loading_hold").animate({ opacity: "0.8" }, 200);

}

function enable_inputs(){

    var radios = document.getElementsByName('rbEngines');
    for (var i = 0; i< radios.length;  i++){
        radios[i].disabled = false;
    };

    var input_field = document.getElementsByName('txtSearch');
    input_field.readOnly = false;

    $("#loading_hold").animate({ opacity: "0" }, 200);
    document.getElementById("loading_hold").style.zIndex = "1";
}