function consulta_mapa(){
    $.ajax({
        url: "/ajax/telemetria/mapa_alarma_transmision",
        data: {
            'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val(),
        },
        type:'POST',
        beforeSend: function () {
            $("#div_error").hide();
            $("#div_loading").show();
        },
        success: function (data) {
            $("#div_loading").hide();
            $("#div_error").hide();
            cargar_datos(data);
        },
        error: function () {
            $("#div_loading").hide();
            $("#div_error").show();
        }
    });
};


function cargar_datos(e){

    $("table#NORMAL > tbody").empty();
    $("table#EXPECTANTE > tbody").empty();
    $("table#FALLO > tbody").empty();
    $("#div-mapa").empty();

    var punto = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": []
                    },
                    "properties": {
                        "estado": "",
                        "description": "",
                    },
                };
    var puntos = [];



    for (const idx in e.estaciones){
        $('#'+ e.estaciones[idx].estado +' > tbody:last-child').append('<tr><td>'+e.estaciones[idx].codigo+'</td></tr>');
        //////////
        _punto = JSON.parse(JSON.stringify(punto));
        _punto.geometry.coordinates = [e.estaciones[idx].longitud, e.estaciones[idx].latitud];
        _punto.properties.estado = e.estaciones[idx].estado;
        var fecha_estado_actual = e.estaciones[idx].fecha_estado_actual;
        fecha_estado_actual = fecha_estado_actual.replace('T',' ');
        fecha_estado_actual = fecha_estado_actual.slice(0, -4);
        _punto.properties.description = e.estaciones[idx].codigo + "<br>" + fecha_estado_actual;
        puntos.push(_punto);
    };

    $("table#NORMAL > thead > tr > th ").html("NORMAL<br><small>Transmisión continua < " + parseFloat(e.limites.lim1) + " hora(s).</small>");
    $("table#EXPECTANTE > thead > tr > th ").html("EXPECTANTE<br><small>Transmisión intermitente.");
    $("table#FALLO > thead > tr > th ").html("FALLO<br><small>Sin transmisión en las últimas " + parseFloat(e.limites.lim2) + " horas.</small>");




    mapboxgl.accessToken = 'pk.eyJ1IjoicGFibG8tdWlvMjAyMCIsImEiOiJjazU5cG1ncDIwcnd4M2xvMXNkaHlhNDEyIn0.hNSx3eMIBzAVuoftwdvQPg';
    var map = new mapboxgl.Map({
        container: 'map',
        zoom: 9,
        center: [-78.38, -0.28],
        style: 'mapbox://styles/mapbox/outdoors-v11'
        //style: 'mapbox://styles/mapbox/satellite-v9'
    });

    map.on('style.load', function (e) {
        map.addSource('markers', {
            "type": "geojson",
            "data": {
                "type": "FeatureCollection",
                "features": puntos
            }
        });

        map.addLayer({
            "id": "normal",
            "source": "markers",
            "type": "circle",
            "paint": {
                "circle-radius": 12,
                "circle-color": "#007c00",
                "circle-opacity": 0.6,
                "circle-stroke-width": 0,
            },
            "filter": ["==", "estado", "NORMAL"],
        });

        map.addLayer({
            "id": "expectante",
            "source": "markers",
            "type": "circle",
            "paint": {
                "circle-radius": 12,
                "circle-color": "#7c7c00",
                "circle-opacity": 0.6,
                "circle-stroke-width": 0,
            },
            "filter": ["==", "estado", "EXPECTANTE"],
        });

        map.addLayer({
            "id": "fallo",
            "source": "markers",
            "type": "circle",
            "paint": {
                "circle-radius": 12,
                "circle-color": "#7c0000",
                "circle-opacity": 0.6,
                "circle-stroke-width": 0,
            },
            "filter": ["==", "estado", "FALLO"],
        });
    });


    map.on('mousemove', 'normal', (e) => {
        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = e.features[0].properties.description;
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) { coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;}
        new mapboxgl.Popup().setLngLat(coordinates).setHTML(description).addTo(map);
    });

    map.on('mouseleave', 'normal',  function() {$(".mapboxgl-popup").remove();});

    map.on('mousemove', 'expectante', (e) => {
        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = e.features[0].properties.description;
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) { coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;}
        new mapboxgl.Popup().setLngLat(coordinates).setHTML(description).addTo(map);
    });

    map.on('mouseleave', 'expectante',  function() {$(".mapboxgl-popup").remove();});

    map.on('mousemove', 'fallo', (e) => {
        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = e.features[0].properties.description;
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) { coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;}
        new mapboxgl.Popup().setLngLat(coordinates).setHTML(description).addTo(map);
    });

    map.on('mouseleave', 'fallo',  function() {$(".mapboxgl-popup").remove();});

};





$(document).ready(function() {
    consulta_mapa();
    setInterval(consulta_mapa, 1800000);

});