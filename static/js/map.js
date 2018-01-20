var directionsDisplay;
var directionsService = new google.maps.DirectionsService();
var map;
var endMarker;

function initialize() {
  directionsDisplay = new google.maps.DirectionsRenderer();
  var paris = new google.maps.LatLng(14.5527608,121.0510892);
  var mapOptions = {
    zoom: 13,
    center: paris
  }
  map = new google.maps.Map(document.getElementById("map"), mapOptions);
  directionsDisplay.setMap(map);
    endMarker = new google.maps.Marker({
    position: map.getCenter(),
    map: map,
    draggable: true,
  });
  dropPin();
  copyMarkerpositionToInput();
  // add an event "onDrag"
  google.maps.event.addListener(endMarker, 'dragend', function() {
    copyMarkerpositionToInput();
  });
}

function dropPin() {
  // if any previous marker exists, let's first remove it from the map
  if (endMarker) {
    endMarker.setMap(null);
  }
  // create the marker
  endMarker = new google.maps.Marker({
    position: map.getCenter(),
    map: map,
    draggable: true,
  });
  copyMarkerpositionToInput();
  // add an event "onDrag"
  google.maps.event.addListener(endMarker, 'dragend', function() {
    copyMarkerpositionToInput();
  });
}

function copyMarkerpositionToInput() {
  // get the position of the marker, and set it as the value of input
  document.getElementById("latitude").value = endMarker.getPosition().lat();
  document.getElementById("longitude").value = endMarker.getPosition().lng();
}

google.maps.event.addDomListener(window, 'load', initialize);