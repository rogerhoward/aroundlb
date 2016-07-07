
console.log('map init start');
L.mapbox.accessToken = 'pk.eyJ1Ijoicm9nZXJob3dhcmQiLCJhIjoiY2lrOXlnZHFvMGc5ZnY0a3ViMHkyYTE0dyJ9.CWAOOChPtxviw8fVB0R1mQ';
var map = L.mapbox.map('map','mapbox.comic')
    .setView([33.793418, -118.153740], 13)
    .on('ready', function() {
        new L.Control.MiniMap(L.mapbox.tileLayer('mapbox.streets'))
            .addTo(map);
});

var lastData;

L.control.fullscreen().addTo(map);
console.log('map init end');


$( document ).ready(function() {

    console.log('ready');

    $.getJSON( "/core/panos", function( data ) {
      $.each( data, function( index, value ) {
        console.log(value);
        lastData = value;
        itemHandler(value);
      });
    });

});



function itemHandler(data) {
    var thisMarker = L.mapbox.featureLayer().addTo(map);
    // console.log(data);
    thisMarkerGeoJSON = {
        // this feature is in the GeoJSON format: see geojson.org
        // for the full specification
        type: 'Feature',
        geometry: {
            type: 'Point',
            // coordinates here are in longitude, latitude order because
            // x, y is the standard for GeoJSON and many formats
            coordinates: [
              data.longitude,
              data.latitude
            ]
        },
        properties: {
            title: data.title,
            description: data.description,
            'marker-size': 'large',
            'marker-color': '#770000',
            'marker-symbol': 'danger'
        }
    };

    console.log(thisMarkerGeoJSON);
    thisMarker.setGeoJSON(thisMarkerGeoJSON);

    thisMarker.on('mouseover', function(e) {
        e.layer.openPopup();
    });

    thisMarker.on('mouseout', function(e) {
        e.layer.closePopup();
    });

}