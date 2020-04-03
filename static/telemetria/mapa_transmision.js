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


$(document).ready(function() {


    // crear la capa base del mapa
    var mymap = L.map('mapid').setView([-0.25, -78.43], 9);
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
		    maxZoom: 18,
		    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
			    '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			    'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		    id: 'mapbox.streets'
	}).addTo(mymap);

	// añadir el ambito del FONAG
	var nexrad = L.tileLayer.wms("http://3.13.203.7/geoserver/geonode/wms", {
        layers: 'geonode:ambito_fonag_2019',
        format: 'image/png',
        transparent: true,
        //attribution: "Weather data © 2012 IEM Nexrad"
    }).addTo(mymap);


    var datos_json = $.ajax({
        type: 'POST',
        url: '/ajax/telemetria/mapa_alarma_transmision',
        data: {
            'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val(),
        },
        async: false,
        dataType: 'json',
        done: function(results) {},
        fail: function( jqXHR, textStatus, errorThrown ) {
            console.log( 'Could not get posts, server response: ' + textStatus + ': ' + errorThrown );
        }
    }).responseJSON;

    var geojsonFeature = datos_json.estaciones;
    var limites = datos_json.limites;

    generar_informacion(geojsonFeature, limites);


    /*$.each(geojsonFeature.features, function(i, item) {
        //console.log(item.properties.codigo);
        var num_normal = 0;
        var num_expectante = 0;
        var num_fallo = 0;
        var objHTML = '';
        if (item.properties.estado==="NORMAL"){
            num_normal ++;
            objHTML = set_info_estacion(item);

            $("#div_lista_success").append(objHTML);
        }
        else if (item.properties.estado==="EXPECTANTE"){

            num_expectante ++;
            objHTML = set_info_estacion(item);
            $("#div_lista_warning").append(objHTML);

        }
        else if (item.properties.estado==="FALLO"){
            num_fallo ++;
            objHTML = set_info_estacion(item);
            $("#div_lista_danger").append(objHTML);

        }

        if (num_normal == 0){
            $("#div_lista_success").html('Sin estaciones por el momento');
        }
        if (num_expectante == 0){
            console.log("expectante");
            $("#div_lista_warning").html('Sin estaciones por el momento');
        }
        if (num_fallo == 0){
            $("#div_lista_danger").html('Sin estaciones por el momento');
        }


        $("#span_success").html(num_normal);
        $("#span_warning").html(num_expectante);
        //$("#span_danger").html(num_fallo);


    });
    // Mensajes de explicación de las alertas
     var msg_success = "Transmisión continua < ";
     msg_success += parseFloat(limites.lim1) + " hora(s).</small>";
     var msg_warning = "Transmisión intermitente.";
     var msg_danger = "Estaciones sin transmisión en las últimas ";
     msg_danger += parseFloat(limites.lim2) + " horas. ";
     msg_danger += '<button class="btn btn-primary btn-sm" type="button" data-toggle="collapse" data-target="#collapseExample" aria-expanded="false" aria-controls="collapseExample">'
     msg_danger += 'Ver</button>'

    $("#div_msg_success").html(msg_success);
    $("#div_msg_warning").html(msg_warning);
    $("#div_msg_danger").html(msg_danger);

    */



    //generar los iconos por estacion
    var success_icon = L.icon({
		iconUrl: '/static/leaflet/images/icon-success.png',
		iconSize: [24, 24],
		iconAnchor: [8, 16],
		popupAnchor: [0, -28]
	});

	var warning_icon = L.icon({
		iconUrl: '/static/leaflet/images/icon-warning.png',
		iconSize: [24, 24],
		iconAnchor: [8, 16],
		popupAnchor: [0, -28]
	});

	var danger_icon = L.icon({
		iconUrl: '/static/leaflet/images/icon-danger.png',
		iconSize: [24, 24],
		iconAnchor: [8, 16],
		popupAnchor: [0, -28]

	});


	// Dar estilo a la capa json por el estado de transmisión de la estacion
	function pointToLayer(feature, latlng){
	    switch(feature.properties.estado){
            case "NORMAL":
            return L.marker(latlng, {icon: success_icon});
            break;
            case "EXPECTANTE":
            return L.marker(latlng, {icon: warning_icon});
            break
            case "FALLO":
            return L.marker(latlng, {icon: danger_icon});
            break
        }

	}


    //cargar la capa de estaciones al mapa
    L.geoJSON(geojsonFeature, {
        pointToLayer: pointToLayer,
        onEachFeature: onEachFeature,
    }).bindPopup(set_content_popup).addTo(mymap);


    // Agregar funcionalidades a los eventos del mapa
    function onEachFeature(feature, layer) {
        layer.on({
            mouseover: openPopup,
            mouseout: closePopup,
            click: zoomToFeature
        });
    }
    //Abrir Popup cuando posa el mouse sobre el marker
    function openPopup(e) {
        var layer = e.target;
        layer.bindPopup(set_content_popup).openPopup();
    }
    //Cerrar Popup cuando quitar el mouse del marker
    function closePopup(e) {
        var layer = e.target;
        layer.closePopup();
    }
    //acercar el mapa al marker
    function zoomToFeature(e) {
        console.log(e.target.getLatLng());
        var corner1 = e.target.getLatLng();
        var corner2 = e.target.getLatLng();
        bounds = L.latLngBounds(corner1, corner2);

		mymap.fitBounds(bounds);
	}

    //leyenda del mapa
    var legend = L.control({position: 'bottomright'});
    legend.onAdd = function (map) {
        var div =  L.DomUtil.create('div', 'legend');
        div.innerHTML = '<img src="/static/leaflet/images/icon-success.png" height="16px" width="16px" alt="NORMAL"> NORMAL<br>';
        div.innerHTML += '<img src="/static/leaflet/images/icon-warning.png" height="16px" width="16px" alt="EXPECTANTE"> EXPECTANTE<br>';
        div.innerHTML += '<img src="/static/leaflet/images/icon-danger.png" height="16px" width="16px" alt="FALLO"> FALLO<br>';
        return div
    };
    //Agregar la leyenda al mapa
    legend.addTo(mymap);


    var info = L.control({position: 'topright'});

    info.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
        this._div.innerHTML += '<button id ="btn_reset_zoom">Reset</button>';
        return this._div;
    };
    info.addTo(mymap);

    $("#btn_reset_zoom").click(function(){
        console.log("llego");
        mymap.setView([-0.25, -78.43], 9);
    });


    // Insertar información en el popup
    function set_content_popup(layer){
        var feature = layer.feature;

        var objHTML='<p><b>Codigo:</b>'+feature.properties.codigo+'<br>';
        objHTML+='<b>Nombre:</b> '+feature.properties.nombre+'<br>';
        objHTML+='<b>Última Fecha:</b> '+feature.properties.fecha_estado_actual+'<br></p>';

        return objHTML;
    }

    function set_info_estacion(feature){

        var objHTML='<li><small><b>Codigo:</b>'+feature.properties.codigo+' ';
        //objHTML+='<b>Nombre:</b> '+feature.properties.nombre+'-';
        objHTML+='<b>Última Fecha Transmisión:</b> '+feature.properties.fecha_estado_actual.replace('T',' ')+'<br></small></li>';

        return objHTML;

    }

    function generar_informacion(estaciones, limites){
        var num_normal = 0;
        var num_expectante = 0;
        var num_fallo = 0;
        $("#div_lista_success").html('<ul>');
        $("#div_lista_warning").html('<ul>');
        $("#div_lista_danger").html('<ul>');
        $.each(estaciones.features, function(i, item) {
            //console.log(item.properties.codigo);
            var objHTML = '';
            if (item.properties.estado==="NORMAL"){
                num_normal ++;
                objHTML = set_info_estacion(item);
                $("#div_lista_success").append(objHTML);
            }
            else if (item.properties.estado==="EXPECTANTE"){
                num_expectante ++;
                objHTML = set_info_estacion(item);
                $("#div_lista_warning").append(objHTML);
            }
            else if (item.properties.estado==="FALLO"){
                num_fallo ++;
                objHTML = set_info_estacion(item);
                $("#div_lista_danger").append(objHTML);
            }
        });

        $("#div_lista_success").append('</ul>');
        $("#div_lista_warning").append('</ul>');
        $("#div_lista_danger").append('</ul>');

        if (num_normal == 0){
            $("#div_lista_success").html('Sin estaciones por el momento');
        }
        if (num_expectante == 0){
            $("#div_lista_warning").html('Sin estaciones por el momento');
        }
        if (num_fallo == 0){
            $("#div_lista_danger").html('Sin estaciones por el momento');
        }

        console.log(num_fallo);
        // Mensajes de explicación de las alertas
        /*var msg_success = "Transmisión continua < ";
        msg_success += parseFloat(limites.lim1) + " hora(s).</small>";
        var msg_warning = "Transmisión intermitente.";
        var msg_danger = "Estaciones sin transmisión en las últimas ";
        msg_danger += parseFloat(limites.lim2) + " horas. ";
        //msg_danger += get_button('danger',num_fallo);*/
        set_mensaje_transmision('success',limites);
        set_mensaje_transmision('warning',limites);
        set_mensaje_transmision('danger',limites);
        set_button('success',num_normal);
        set_button('warning',num_expectante);
        set_button('danger',num_fallo);

        //$("#div_msg_success").html(msg_success);
        //$("#div_msg_warning").html(msg_warning);
        //$("#div_msg_danger").html(msg_danger);


    }

    //insertar mensaje html

    function set_mensaje_transmision(type,limites){
        var mensaje = '';
        var $div_mensaje = $("#div_msg_"+type);
        if (type === 'success'){
            mensaje = "Estaciones con transmisión continua < " + parseFloat(limites.lim1) + " hora(s).";
        }
        else if (type === 'warning'){
            mensaje = "Estaciones con transmisión intermitente.";
        }
        else if (type === 'danger'){
            mensaje = "Estaciones sin transmisión en las últimas " + parseFloat(limites.lim2) + " horas. ";
        }
        $div_mensaje.html(mensaje);
    }
    //insertar button HTML
    function set_button (type,numero){
        var btn_html = '<button type="button" class="btn btn-' + type +' " data-toggle="collapse" ';
        btn_html += 'data-target="#div_'+type+'" aria-expanded="false" aria-controls="div_'+type+'">Ver ';
        btn_html += '<span class="badge badge-light">'+numero+'</span></button>'
        var $div = $('#div_btn_'+type);
        $div.html(btn_html);

        //return btn_html;
    }



});