
var current_selection;
var current_selection_small;

function populate_table(marker){

    var added_line = '<button href="#" class="list-group-item" id=' + marker.index.toString() + '>';
    added_line += '<h4 class="list-group-item-heading"> <b>' + marker.title + "</b> <img align='right' src=\"" + marker.ratings_img + "\">" + '</h4>';
    added_line += '<p class="list-group-item-text">'
    added_line += "Number of Reviews: " + marker.review_count.toString() + "<br>";
    added_line += marker.address
    added_line += "<div align='right'><a href=\"" + marker.yelp_url + "\" target=\"_blank\">" + "<img src=\"onebus\\images\\yelp_review_btn_light.png\"></a><br>";
    added_line += '</div></p></button>';

    $('#poi-list').append(added_line);

    var added_line = '<button href="#" class="list-group-item" id=' + marker.index.toString() + '_sm>';
    added_line += '<h4 class="list-group-item-heading"> <b>' + marker.title + "</b> <img align='right' src=\"" + marker.ratings_img + "\">" + '</h4>';
    added_line += '<p class="list-group-item-text">'
    added_line += "Number of Reviews: " + marker.review_count.toString() + "<br>";
    added_line += marker.address
    added_line += "<div align='right'><a href=\"" + marker.yelp_url + "\" target=\"_blank\">" + "<img src=\"onebus\\images\\yelp_review_btn_light.png\"></a><br>";
    added_line += '</div></p></button>';

    $('#poi-list-small').append(added_line);

}

function highlight_item(marker){
    if(current_selection){
        current_selection.classList.remove('active');
    }

    var scroll_speed = 300;


    current_selection = $('#' + marker.index.toString())[0];
    current_selection.classList.add('active');
//    current_selection.focus()
    var offset = -$("#poi-list").height()/3;
    $("#poi-list").scrollTo(current_selection, scroll_speed, {offset: offset});


    if(current_selection_small){
        current_selection_small.classList.remove('active');
    }

    current_selection_small = $('#' + marker.index.toString() + '_sm')[0];
    current_selection_small.classList.add('active');
//    current_selection_small.focus()
    $("#poi-list-small").scrollTo(current_selection_small, scroll_speed);
}

$('#poi-list').on('click', '.list-group-item', function(e) {
    var index = parseInt(e.currentTarget.id);
    google.maps.event.trigger(markers[index], 'click');
});

$('#poi-list-small').on('click', '.list-group-item', function(e) {
    var index = parseInt(e.currentTarget.id);
    google.maps.event.trigger(markers[index], 'click');
});

$('#poi-list-small').on('shown.bs.collapse', function() {
    if(current_marker){
        highlight_item(current_marker);
    }
}).on('show.bs.collapse', function() {
});