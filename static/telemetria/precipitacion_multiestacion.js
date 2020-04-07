//var graf_width = 950;
var graf_height = 470;
var graf_margin_right = 15;
var graf_margin_top = 90;
var graf_margin_bottom = 120;
var graf_margin_left = 55;
//var legends = {};


function cargar_datos(data){
    //$(".bloque-grafico").empty();
    var ngraf = 0;
    grafico_serie_barras(data, ngraf);

}


function grafico_serie_barras(data, ngraf){

    width_graph = $("#div_grafico").width();

    var trace = {
        name: 'Precip.',
        x: data.estacion,
        y: data.valor,
        type: 'bar',
        //marker: {color: 'rgb(32, 32, 90)',},
    };


    var layout = {
        title: 'Precipitación acumulada (mm)',
        width: width_graph,
        height: graf_height,
        margin: {
            r: graf_margin_right,
            t: graf_margin_top,
            b: graf_margin_bottom,
            l: graf_margin_left,
            pad: 0
        },
        yaxis: {
            rangemode: 'nonnegative',
            autorange: true
        },
        xaxis: {
            tickangle: -68,
        },
    };

    //var graf_id = 'graf' + ngraf;
    //$(".bloque-grafico").append("<div id='" + graf_id + "' style='display:inline-block' ></div>");
    //Plotly.newPlot(graf_id, [trace], layout, {showSendToCloud: false,});
    Plotly.newPlot('div_informacion', [trace], layout, {showSendToCloud: false,});

}



function enviar_consulta(){
    $.ajax({
        url: "/telemetria/multiestacion_precipitacion/",
        data: $("#form_telemetria").serialize(),
        type:'POST',
        beforeSend: function () {
            activar_espera();
        },
        success: function (data) {
            desactivar_espera();
            cargar_datos(data);
        },
        error: function () {
            mostrar_mensaje();
        }
    });
};


$(document).ready(function() {

    $( ":checkbox" ).prop('checked', true);

    $("#visualizar").click(function(){
        //$(".bloque-grafico").empty();
        enviar_consulta();

    });

    $("#select_estacion").change(function(){
        if ($(this).val() === 'all') {
            $( ":checkbox" ).prop('checked', true);
        }
        else{
            $( ":checkbox" ).prop('checked', false);
        }
    });

    $("#id_inicio").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "yy-mm-dd",
        showButtonPanel: true,
        yearRange: '2000:'+(new Date).getFullYear()
    });

    $("#id_inicio").datepicker().focus(function () {
        $("#ui-datepicker-div").position({ my: "center top", at: "center bottom", of: $("#id_inicio")});
    });


    $("#id_fin").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "yy-mm-dd",
        showButtonPanel: true,
        yearRange: '2000:'+(new Date).getFullYear()
    });

    $("#id_fin").datepicker().focus(function () {
        $("#ui-datepicker-div").position({ my: "center top", at: "center bottom", of: $("#id_fin")});
    });

    $("#id_fin").datepicker().datepicker("setDate", new Date());

    $( "#id_fin" ).change(function() {
        //$(".bloque-grafico").empty();
    });

    $( "#id_inicio" ).change(function() {
        //$(".bloque-grafico").empty();
    });

});