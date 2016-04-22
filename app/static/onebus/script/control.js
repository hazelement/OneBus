
$("#frmSearch").submit(function( event ){
    event.preventDefault();
    if($("#txtSearch").val()==""){
        return;
    }
    clearMap();


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
        contentType: "application/json",
        dataType:'json'})

});


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

//    var $btn = $('#btnSubmit').button('loading')
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


$( document ).ready(function() {
        if (document.cookie.indexOf('visited=true') == -1) {
            var fifteenDays = 1000*60*60*24*15;
            var expires = new Date((new Date()).valueOf() + fifteenDays);
            document.cookie = "visited=true;expires=" + expires.toUTCString();
            $('#modelWelcome').modal("show");
        }
});

