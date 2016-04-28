
var map;
var infowindow;
var markers = [];
var shape;
var home;
var home_gps;
var bounds;
var current_marker;

var set_center = 0;

function initMap(){
    var mapDiv = document.getElementById('map');

    map = new google.maps.Map(mapDiv, {
        zoom: 13,
        streetViewControl: false,
        mapTypeControl: false,
    });

    map.setMapTypeId(google.maps.MapTypeId.TERRAIN);

    var geo_options = {
        enableHighAccuracy: true,
        maximumAge        : 30000,
        timeout           : 1000
    };

    if (navigator.geolocation) {
        navigator.geolocation.watchPosition(location_success, location_error, geo_options);

    } else {
        home_gps = {lat: 51.0486151, lng:-114.0708459}

    }

    infowindow = new google.maps.InfoWindow({
        content: '',
        maxWidth: 200
        });

     google.maps.event.addListener(
        map,
        'click',
        function(){
                infowindow.close();
        }
    );

        // setup map
    shape = new google.maps.Polyline({
        geodesic: true,
        strokeColor: '#0000FF ',
        strokeOpacity: 0.5,
        strokeWeight: 6
    });
    shape.setMap(map);

}


function location_success(position) {
    home_gps = {lat: position.coords.latitude, lng: position.coords.longitude};
    if(set_center==0){
        map.setCenter(home_gps);
        add_marker(home_gps, true);
        set_center=1;
    }

    if(home){
        home.position = new google.maps.LatLng({lat: position.coords.latitude, lng: position.coords.longitude}); // update home position
    }

}

function location_error() {
    home_gps = {lat: 51.0486151, lng:-114.0708459}
    // don't add my position label in this case
}

function refreshMap(data) {

    // define map elements
    destinations = data['results']

    // handles now result
    if(Object.keys(destinations).length == 0){
        $('#noResultContent').empty();

        if(data['routes'].length == 0){
            $('#noResultContent').after("<p>Looks like there is no accessible bus around you in our database. We apologize. Please leave us a feedback and we can make improvements.</p>");
        } else {
            $('#noResultContent').after("<p>It looks like there is nothing around accessible by OneBus. Try to search a more generalized key word. Bus routes around you are: " + data['routes'] + "</p>");
        }

        $('#modelNoResult').modal('show');
    }
    // add result markers
    bounds = new google.maps.LatLngBounds();
    bounds.extend(home.position);

    for( var key in destinations ){
        add_marker(destinations[key], false);
    }

    map.fitBounds(bounds);
}

function add_marker_to_bounds(marker){
    if(bounds){
        bounds.extend(marker.position);
    }
}

function add_marker(target, is_home) {

    var lat_lng = {lat: target.lat, lng: target.lng};
    if(is_home){

        var marker = new google.maps.Marker({
        position: lat_lng,
        labelContent: 'H',
        map: map,
        animation: google.maps.Animation.DROP,
        title: 'Home',
        description: 'My Location',
        path: target.path
        });

        marker.setIcon("onebus\\images\\home.png");

        google.maps.event.addListener(
            marker,
            'click',
            function(){
                infowindow.close();
                infowindow.setContent(marker.description);
                infowindow.open(map, marker);
            }
        );
        home = marker;

    } else {

        var marker = new google.maps.Marker({
        index: markers.length,
        position: lat_lng,
        map: map,
        animation: google.maps.Animation.DROP,
        title: target.dest_name,
        address: target.address,
        image_url: target.image_url,
        yelp_url: target.yelp_url,
        review_count: target.review_count,
        ratings_img: target.ratings_img,
        path: target.path,
        start_stop: target.start_stop,
        start_stop_time: target.start_stop_time,
        start_stop_name: target.start_stop_name,
        end_stop: target.end_stop,
        end_stop_time: target.end_stop_time,
        end_stop_name: target.end_stop_name,
        trip_id: target.trip_id,
        trip_headsign: target.trip_headsign,
        route_id: target.route_id,
        city_code: target.city_code,
        shape: ""
        });

        marker.setIcon("onebus\\images\\pin.png");

        google.maps.event.addListener(
            marker,
            'click',
            function(){
                current_marker = marker;
                infowindow.close();
                clear_polyline();
                infowindow.setContent(make_infobox(marker));
                infowindow.open(map, marker);
                highlight_item(marker);
                get_trip_shape(marker);
//                fit_map(marker);
            }
        );
        markers.push(marker);
        add_marker_to_bounds(marker);
        populate_table(marker);
    }

}

function make_infobox(marker){
    retVal = "<b><font size=\"3\">";
    retVal += marker.title +"</font></b><br>" ;
    retVal += "<img src=\"" + marker.ratings_img + "\"><br>";
    retVal += "<b>Bus No.: " + marker.route_id + " " + marker.trip_headsign + "</b><br>";
    retVal += "<b>" + convert_timeint_to_time(marker.start_stop_time) + "</b> from " + marker.start_stop_name + "<br>";
    retVal += "<b>" + convert_timeint_to_time(marker.end_stop_time) + "</b> arrive at " + marker.end_stop_name;
    return retVal;
}

function convert_timeint_to_time(time_int_string){
    var number = parseInt(time_int_string);
    var hour = Math.floor(number/3600);
    var minute = Math.floor((number % 3600) / 60);

    var a_pm = "AM";
    if(hour >= 12){
        a_pm = "PM";

        if(hour > 12){
            hour -= 12;
        }
    }

    return FormatNumberLength(hour, 2) + ":" + FormatNumberLength(minute, 2) + " " + a_pm
}

function FormatNumberLength(num, length) {
    var r = "" + num;
    while (r.length < length) {
        r = "0" + r;
    }
    return r;
}


function get_trip_shape(marker){
    // if shape is requested, just request
    if(marker.shape!=""){
        add_shape(marker.shape);
        return
    }

    $.ajax({
    type: "POST",
    url: "/onebus/api/route",
    data: JSON.stringify({trip_id: marker.trip_id,
                            start_stop: marker.start_stop,
                            end_stop: marker.end_stop,
                            city_code: marker.city_code
                            }),
    success: function(response){ marker.shape = plot_shape(response); },
    contentType: "application/json",
    dataType:'json'})

}

function fit_map(marker){
    bounds = new google.maps.LatLngBounds();
    bounds.extend(home.position);
    bounds.extend(marker.position);
    map.fitBounds(bounds);
}

function plot_shape(data, marker){
    if(data["success"] == "0"){
        return ""
    }

    var encoded_shape = data["results"];
    add_shape(encoded_shape);

    return encoded_shape
}

function add_shape(encoded_shape){
    var decoded_path = google.maps.geometry.encoding.decodePath(encoded_shape)
    shape.setPath(decoded_path);
}

// Sets the map on all markers in the array.
function setMapOnAll(map) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

function clear_polyline(){
  shape.setPath([]);
}

// Deletes all markers and bus routes in the array by removing references to them.
function clearMap() {
  setMapOnAll(null);
  clear_polyline();
  markers = [];
}


