var mymap = mymap = L.map('map').setView([40.730610, -73.935242], 11);
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
        '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="http://mapbox.com">Mapbox</a>',
    id: 'mapbox.streets'
}).addTo(mymap);

function heatMapColorforValue(value) {

    var colorscale = [[0, '#EDE7F6'],
    [0.11, '#D1C4E9'],
    [0.22, '#B39DDB'],
    [0.33, '#9575CD'],
    [0.44, '#7E57C2'],
    [0.55, '#673AB7'],
    [0.66, '#5E35B1'],
    [0.77, '#512DA8'],
    [0.88, '#4527A0'],
    [1, '#311B92']];
    for (var i = 0; i < colorscale.length; i++) {
        if (value <= colorscale[i][0]) {
            return colorscale[i][1];
        }
    }
}

function findMax(data) {
    var arr = Object.keys(data).map(function (key) { return data[key]; });
    return Math.max.apply(null, arr);
}

function printMap(taxi_courses, geometries) {
    var max_number_of_courses = findMax(taxi_courses);
    for (var key in geometries) {
        number_of_courses = taxi_courses[key];
        if (!number_of_courses) {
            number_of_courses = 0;
        }
        color = heatMapColorforValue(number_of_courses / max_number_of_courses)
        var geometry = L.geoJSON(JSON.parse(geometries[key].geometry), {
            style: {
                color: color,
                weight: 1,
                opacity: 0.5,
                fillOpacity: 0.5,
                fillColor: color
            }
        });
        geometry.addTo(mymap);
    }
}