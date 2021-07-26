
$(document).ready(function() {

   

    // crear la capa base del mapa
    var mymap = L.map('mapid').setView([-10, -75], 4);
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
            '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox/streets-v11',
	}).addTo(mymap);
    // añadir el ambito del FONAG
	/*var nexrad = L.tileLayer.wms("http://3.13.203.7/geoserver/geonode/wms", {
        layers: 'geonode:ambito_fonag_2019',
        format: 'image/png',
        transparent: true,
        //attribution: "Weather data © 2012 IEM Nexrad"
    }).addTo(mymap);*/
    //consultar la capa de estaciones del FONAG en JSON
    geojsonFeature = $.ajax({
        type: 'GET',
        url: '/estacion/getjson',
        async: false,
        dataType: 'json',
        done: function(results) {},
        fail: function( jqXHR, textStatus, errorThrown ) {
            console.log( 'Could not get posts, server response: ' + textStatus + ': ' + errorThrown );
        }
    }).responseJSON;

    //generar los iconos por estacion
    var hidro_icon = L.icon({
		iconUrl: '/static/leaflet/images/ico-hidro.png',
		iconSize: [16, 16],
		iconAnchor: [8, 16],
		popupAnchor: [0, -28]
	});

	var pluvio_icon = L.icon({
		iconUrl: '/static/leaflet/images/ico-pluvio.png',
		iconSize: [16, 16],
		iconAnchor: [8, 16],
		popupAnchor: [0, -28]
	});

	var meteo_icon = L.icon({
		iconUrl: '/static/leaflet/images/ico-meteo.png',
		iconSize: [16, 16],
		iconAnchor: [8, 16],
		popupAnchor: [0, -28]
	});
    //cargar la capa de estaciones al mapa
    L.geoJSON(geojsonFeature, {

        pointToLayer: function (feature, latlng) {

            switch(feature.properties.tipo){
                case "Climatológica":
                return L.marker(latlng, {icon: meteo_icon});
                break;
                case "Pluviométrica":
                return L.marker(latlng, {icon: pluvio_icon});
                break
                case "Hidrométrica":
                return L.marker(latlng, {icon: hidro_icon});
                break
            }
            //return L.marker(latlng, {icon: hidro_icon});
        },

        //onEachFeature: onEachFeature,

    }).bindPopup(function (layer) {
        objHTML=get_content_estacion(layer.feature)
        return objHTML;
    }).addTo(mymap);

    //leyenda del mapa

    var legend = L.control({position: 'bottomright'});
    legend.onAdd = function (map) {

        var div =  L.DomUtil.create('div', 'legend');
        div.innerHTML = '<img src="/static/leaflet/images/ico-meteo.png" height="16px" width="16px" alt="Meteorologica"> Climatológica<br>';
        div.innerHTML += '<img src="/static/leaflet/images/ico-pluvio.png" height="16px" width="16px" alt="Pluviometrica"> Pluviométrica<br>';
        div.innerHTML += '<img src="/static/leaflet/images/ico-hidro.png" height="16px" width="16px" alt="Hidrologica"> Hidrológica<br>';
        return div

    };

    legend.addTo(mymap);
    // llamar las estaciones por tipo de transmisión
    $("#id_transmision").change(function () {
        var transmision = $(this).val();

        $("#id_estacion").find('option').remove().end()
        $("#id_estacion").append('<option value="">---------</option>');
        $("#id_variable").find('option').remove().end()
        $("#id_variable").append('<option value="">---------</option>');
        $.ajax({
            url: '/estaciones/tipo',
            data: {
                'transmision': transmision
            },
            dataType: 'json',
            success: function (data) {
            //datos=JSON.parse(data)

                $.each(data, function(index, value) {
                    $("#id_estacion").append('<option value="' + index + '">' + value + '</option>');
                });
            }
        });
        
    });

    // Funcionalidad del click en la tabla
    $(document).on("click", "#data_reporte tr", function() {
        var codigo = $(this).children("td").html();
        codigo = codigo.split(" - ")
        set_zoom_estacion(codigo[0], geojsonFeature,mymap);
    });


    // llamar las variables por estaciones
    $("#id_estacion").change(function () {
        var codigo = $('#id_estacion option:selected').text();
        /*var estacion = $(this).val();
        var codigo = $('#id_estacion option:selected').text();
        $("#id_variable").find('option').remove().end()
        $("#id_variable").append('<option value="">---------</option>');
        $.ajax({
            url: '/anuarios/variables/'+estacion,
            dataType: 'json',
            success: function (data) {

                $.each(data, function(index, value) {
                    $("#id_variable").append('<option value="' + index + '">' + value + '</option>');
                });
            }
        });*/
        set_zoom_estacion(codigo, geojsonFeature,mymap);
    });



    //cambiar el zoom del mapa a una estacion
    function set_zoom_estacion(codigo, capa_estaciones,mapa){
        console.log(codigo);
        var popup = L.popup();
        var contentHTML="";
        var latlng = L.latLng(-10, -75.5);
        var latlng_popup = L.latLng(-10, -75.5);
        $.each(capa_estaciones.features, function(i, item) {
            //console.log(item.properties.codigo);
            if (item.properties.codigo==codigo){
                latlng.lat=item.properties.latitud-(-0.016);
                latlng.lng=item.properties.longitud;
                contentHTML=get_content_estacion(item)
                latlng_popup.lat=item.properties.latitud-(-0.004)
                latlng_popup.lng=item.properties.longitud
            }
        });
        popup
            .setLatLng(latlng_popup)
            .setContent(contentHTML)
            .openOn(mapa);
        mapa.flyTo(latlng,10)
        return latlng

    }

    function get_content_estacion(feature){
        objHTML='<p><b>Codigo:</b>'+feature.properties.codigo+'<br>'
        objHTML+='<b>Nombre:</b> '+feature.properties.nombre+'<br>'
        objHTML+='<b>Tipo:</b> '+feature.properties.tipo+'<br>'
        objHTML+='<b>Latitud:</b> '+feature.properties.latitud+'<br>'
        objHTML+='<b>Longitud:</b> '+feature.properties.longitud+'</p>'
        return objHTML;
    }
    // enfocar la estacion cuando se recarga la pagina
    var codigo = $('#id_estacion option:selected').text();
    if (codigo!="---------"){
        //set_zoom_estacion(codigo, geojsonFeature,mymap);
    }

});
