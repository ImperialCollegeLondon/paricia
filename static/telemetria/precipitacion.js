//var graf_width = 1300;
//var graf_height = 700;
var graf_margin_right = 5;
var graf_margin_top = 90;
var graf_margin_bottom = 35;
var graf_margin_left = 35;
var graf_title_size = 14;
var graf = 1;

function cargar_datos(data){
    $("#graf1").empty();

    width_graph = $("#div_graficos").width();
    var layout = {
        title: data.estacion  + '\nPrecipitación acumulada',
        titlefont: {
            size: graf_title_size
        },
        showlegend: true,
        width: width_graph,
        barmode: 'stack',
        height: 250,
        margin: {
            r: graf_margin_right,
            t: graf_margin_top,
            b: graf_margin_bottom,
            l: graf_margin_left,
            pad: 0
        },
    };

    var trace = {
        name: 'Diario [mm]',
        x: data.datos.fecha,
        y: data.datos.valor,
        type: 'bar',
    };
    console.log(data.datos.acumulado)
    data.datos.acumulado[0] = 0;
    var acum_total = {
        name: 'Acum. [mm]',
        x: data.datos.fecha,
        y: data.datos.acumulado,
        type: 'bar',
        /*line: {
            color: 'rgb(219, 64, 82)',
        }*/
    };

    var config = {showSendToCloud: false, responsive: true}

    Plotly.newPlot('graf1', [trace, acum_total], layout, config);

    var vmac = data.datos.valor_mayor_a_cero;
    for (var ix in vmac){
        $('#table_valor > tbody').append("<tr><td>" + vmac[ix][0] + "</td><td>" + vmac[ix][1] + "</td></tr>");
    }


    $("#graf3").empty();

    var layout = {
        title: data.estacion  + '\nPrecipitación mensual',
        titlefont: {
            size: graf_title_size
        },
        showlegend: true,
        width: width_graph,
        height: 250,
        barmode: 'group',
        margin: {
            r: graf_margin_right,
            t: graf_margin_top,
            b: graf_margin_bottom,
            l: graf_margin_left,
            pad: 0
        },
    };

    var historico = {
        name: 'Histórico',
        x: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        y: data.datos.historico,
        type: 'bar',
    };

    var actual = {
        name: data.datos.año_actual,
        x: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        y: data.datos.actual,
        type: 'bar',
    };

    Plotly.newPlot('graf3', [historico, actual], layout, config);
}



function enviar_consulta(){
    $.ajax({
        url: "/ajax/telemetria/precipitacion/consulta/",
        data: $("#form_precipitacion").serialize(),
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
    $("#id_inicio").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "yy-mm-dd",
        showButtonPanel: true,
        yearRange:  ((new Date).getFullYear()-1) + ':'+(new Date).getFullYear()
    });

    $("#id_inicio").datepicker().focus(function () {
        $("#ui-datepicker-div").position({ my: "center top", at: "center bottom", of: $("#id_inicio")});
    });


    $("#id_fin").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "yy-mm-dd",
        showButtonPanel: true,
        yearRange:  ((new Date).getFullYear()-1) + ':'+(new Date).getFullYear()
    });

    $("#id_fin").datepicker().focus(function () {
        $("#ui-datepicker-div").position({ my: "center top", at: "center bottom", of: $("#id_fin")});
    })
    $("#id_fin").datepicker().datepicker("setDate", new Date());

    $("#visualizar").click(function(){
        $("#graf1").empty();
        $("input[name='estacion']").val($('#id_estacion').val() );
        $("input[name='fecha']").val($('#id_fecha').val() );
        enviar_consulta();
    });


});