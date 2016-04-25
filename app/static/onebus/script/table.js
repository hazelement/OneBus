
var current_selection;

function populate_table(marker){

    var added_line = '<a href="#" class="list-group-item" id=' + marker.index.toString() + '>';
    added_line += '<h4 class="list-group-item-heading"> <b>' + marker.title + "</b> <img align='right' src=\"" + marker.ratings_img + "\">" + '</h4>';
    added_line += '<p class="list-group-item-text">'
    added_line += "Number of Reviews: " + marker.review_count.toString() + "<br>";
    added_line += marker.address
    added_line += '</p></a>';
    $('#poi-list').append(added_line);

}

function highlight_item(marker){
    if(current_selection){
        current_selection.classList.remove('active');
    }
    current_selection = $('#' + marker.index.toString())[0];
    current_selection.classList.add('active');
}

$('#poi-list').on('click', '.list-group-item', function(e) {
    var index = parseInt(e.currentTarget.id);

    google.maps.event.trigger(markers[index], 'click');
});