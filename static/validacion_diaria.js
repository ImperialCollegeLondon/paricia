
tr_ini = '<tr>';
tr_fin = '</tr>';
var datos_json = {};
var data_fecha = [];
var data_valor = [];
var data_maximo = [];
var data_minimo = [];




$(document).ready(function() {

    $("#btn_buscar").click(function(){
        var $table = $('#table_diario');
        $.ajax({
            url: $("#form_validacion").attr('action'),
            data: $("#form_validacion").serialize(),
            type:'POST',
            beforeSend: function () {
                //$("#div_grafico").hide();
                activar_espera("#div_loading", "#div_informacion", "#div_error");

                $table.bootstrapTable('showLoading');

            },
            success: function (data) {
                $("#btn_buscar").attr("disabled", false);

                var_id = data.variable[0]['var_id'];
                variable = data.variable[0];
                estacion = data.estacion[0];

                datos_json = data.datos
                rows=''

                data_fecha = [];
                data_valor = [];
                data_maximo = [];
                data_minimo = [];

                for (var i in datos_json) {

                    data_fecha.push(new Date(datos_json[i]['dia']));
                    data_valor.push(datos_json[i]['valor']);
                    if (var_id !== 1) {
                        data_maximo.push(datos_json[i]['maximo']);
                        data_minimo.push(datos_json[i]['minimo']);

                    }
                }

                $table.bootstrapTable('destroy');
                var columns = get_colums_diario(var_id);
                $table.bootstrapTable({columns:columns, data: datos_json })

                graficar(data.variable[0], data.estacion[0] );

                desactivar_espera("#div_loading", "#div_informacion", "#div_error")
                //$("#div_grafico").show();
                $table.bootstrapTable('hideLoading');

            },
            error: function () {
                //$("#div_grafico").hide();
                mostrar_error("#div_loading", "#div_informacion", "#div_error")

            }
        });
    });


    $(".link-validacion").click(function(e){

    });

});

// generar la tabla de datos de validacion
function detalle_crudos(e, value, row){

    var $table = $('#table_validado');
    var estacion_id = $("#id_estacion").val();
    var variable_id = $("#id_variable").val();
    console.log(estacion_id)
    enlace = '/validacion/lista/' + estacion_id + '/' + variable_id + '/' + row.dia;
    console.log("llego", row.dia);
    //enlace = $(this).attr('href')
    $.ajax({
        url: enlace,
        type:'GET',
        beforeSend: function () {
        },
        success: function (data) {
            datos_json = data;
            $table.bootstrapTable('destroy');
            var columns = get_column_validado(var_id);
            $table.bootstrapTable({columns:columns, data: datos_json})



        },
        error: function () {

            console.log("llego")

        }
    });

};


function get_colums_diario(var_id){
    var columns = [];
    if (var_id === 1) {
        columns = [
            {
                field:'dia',
                title:'Fecha'
            },
            {
                field:'porcentaje',
                title:'Porcentaje',
                cellStyle: style_porcentaje
            },
            {
                field:'valor',
                title:'Valor'
            },
            {
                field: 'accion',
                title: 'Acción',
                formatter: operate_table_diario,
                events: {
                   'click .search': detalle_crudos,

                }
            }

        ]
    }
    else{
        columns = [
            {
                field:'state',
                checkbox:true
            },
            {
                field:'dia',
                title:'Fecha'
            },
            {
                field:'porcentaje',
                title:'Porcentaje',
                cellStyle: style_porcentaje
            },
            {
                field:'valor',
                title:'Valor',
                cellStyle: style_valor,
                formatter: format_valor
            },
            {
                field:'maximo',
                title:'Máximo'
            },
            {
                field:'minimo',
                title:'Mínimo'
            },
            {
                field:'valor_error',
                title:'# Valores Sospechosos',
                visible:false
            },
            {
                field:'maximo_error',
                title:'# Valores máximos Sospechosos',
                visible:false
            },
            {
                field:'minimo_error',
                title:'# Valores mínimos Sospechosos',
                visible:false
            },
            {
                field: 'accion',
                title: 'Acción',
                formatter: operate_table_diario,
                events: {
                   'click .search': detalle_crudos,

                }
            }

        ]
    }
    return columns

}




function get_column_validado(){
    var columns = [
        {
            field:'fecha',
            title:'Fecha'
        },
        {
            field:'valor_seleccionado',
            title:'Validacion'
        },
        {
            field:'valor',
            title:'Valor'
        },
        {
            field:'',
            title:'Valores Atípicos'
        },
        {
            field:'comentario',
            title:'Comentario'
        },


    ]


    return columns
}


function operate_table_diario(value, row, index) {
    return [
      '<a class="search" href="javascript:void(0)" title="Buscar">',
      '<i class="fa fa-search"></i>',
      '</a>  ',
    ].join('')
}


function style_porcentaje(value, row, index) {
    if (row.porcentaje<70) {
      return {
        classes: 'error'
      }
    }
    else{
        return {
            classes: 'normal'
        }
    }

}

function style_valor(value, row, index){
    var clase = ''
    if (row.valor_numero>0)
        clase = 'error';
    else
        clase = 'normal';
    return { classes: clase}
}


function format_valor(value, row){
    var span = '<span class="badge badge-light">num</span>';
    var content = ''
    if (row.valor_numero>0){
        span = span.replace('num',row.valor_numero.toString())
        content = value + ' ' + span;
    }
    else{
        content = value
    }
    return content

}


function get_thead_val(){
    var row = ''
    var th_fecha = ''
    var th_porcentaje = ''
    var th_valor = ''

    th_fecha = '<th scope="col" class="col-3">Fecha</th>';
    th_validado = '<th scope="col" class="col-2">Validación</th>';
    th_valor = '<th scope="col" class="col-2">Valor</th>';
    th_stddev = '<th scope="col" class="col-2">Valores atípicos</th>';
    th_comentario = '<th scope="col" class="col-3">Comentario</th>';
    row += '<tr>'
    row += th_fecha + th_validado + th_valor + th_stddev + th_comentario;
    row += '</tr>'


    return row
}

function graficar(variable, estacion){
    var_id = variable['var_id'];
    var_nombre = variable['var_nombre']
    est_nombre = estacion['est_nombre']
    if (var_id === 1){
        var trace1 = {
            x: data_fecha,
            y: data_valor,
            name: 'Valor',
            type: 'bar'
        };

        var data = [trace1];
    }
    else{
        var trace1 = {
            x: data_fecha,
            y: data_valor,
            name: 'Valor',
            type: 'scatter'
        };
        var trace2 = {
            x: data_fecha,
            y: data_maximo,
            name: 'Maximo',
            type: 'scatter'
        };
        var trace3 = {
            x: data_fecha,
            y: data_minimo,
            name: 'Minimo',
            type: 'scatter'
        };


        var data = [trace1, trace2, trace3];
        //var data = [trace1, trace2, trace3];
        //var data = [trace1, trace2, trace3, limite_min];
    }

    var layout = {
        title: var_nombre + ' - '+ est_nombre,
        //showlegend: false
    };
    Plotly.newPlot('div_grafico', data, layout, {scrollZoom: true});

};
