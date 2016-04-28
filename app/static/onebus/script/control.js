
$("#frmSearch").submit(function( event ){
    event.preventDefault();
    if($("#txtSearch").val()==""){
        return;
    }
    clearMap();
    $("#poi-list").empty();
    $("#poi-list-small").empty();


    var currentdate = new Date();
    var datetime =  currentdate.getFullYear() + "-"
                  + currentdate.getMonth() + "-"
                  + currentdate.getDate() + "|"
                  + currentdate.getHours() + ":"
                  + currentdate.getMinutes() + ":"
                  + currentdate.getSeconds()

    var $btn = $('#btnSubmit').button('loading')

    $.ajax({
        type: "POST",
        url: "/onebus/api",
        data: JSON.stringify({search_text: $("#txtSearch").val(),
                                home_gps: home_gps,
                                current_time: datetime}),
        success: function(response){ refreshMap(response); $btn.button('reset');},
        error: function(response){ ajax_fail(response); $btn.button('reset');},
        timeout: 10000,
        contentType: "application/json",
        dataType:'json'})

});

function ajax_fail(response){
    $('#modelAjaxFail').modal("show");
}

//sumbit feedback
$("#frmFeedback").submit(function( event ){
    event.preventDefault();

    if($("#onebuscomment").val()==""){
        $('#submitsuccess').removeClass('label-success').addClass('label-warning');
        $('#submitsuccess').text("Please enter your comment below.");
        return;
    }

    var name = "anonymous";
    var email = "anonymous";
    var phone = "anonymous";
    var message = $("#onebuscomment").val();

    var $btn = $('#onebusReview');
    $btn.button('loading');

    $.ajax({
        url: "/email/contact_me",
        type: "POST",
        data: JSON.stringify({
            name: name,
            phone: phone,
            email: email,
            message: message
        }),
        cache: false,
        success: function() {
            // Enable button & show success message
            $btn.button('reset');
            //clear all fields
            $('#onebuscomment').val('');
            $('#submitsuccess').removeClass('label-warning').addClass('label-success');
            $('#submitsuccess').text("Thank you!");
        },
        error: function() {
            // Fail message

            //clear all fields
            $btn.button('reset');
            $('#submitsuccess').removeClass('label-success').addClass('label-warning');
            $('#submitsuccess').text("Sorry looks like our email server is down!");
        },
        contentType: "application/json",
        dataType:'json'
    })
});

$( "#feedbackClose" ).click(function() {
  $('#submitsuccess').text('');
  $('#onebuscomment').val('');
});


//welcome screen for first time visitor
$( document ).ready(function() {
        if (document.cookie.indexOf('visited=true') == -1) {
            var fifteenDays = 1000*60*60*24*15;
            var expires = new Date((new Date()).valueOf() + fifteenDays);
            document.cookie = "visited=true;expires=" + expires.toUTCString();
            $('#modelWelcome').modal("show");
        }
});

// toggle show list button
$("#btnToggleList").click(function () {
  $(this).text(function(i, text){

      return ($('#poi-list-small').hasClass('in')) ? "Show List" : "Hide List";

//      return text === "Hide List" ? "Show List" : "Hide List";
  })
});