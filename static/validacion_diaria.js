
tr_ini = '<tr>';
tr_fin = '</tr>';
var datos_json = {};
var data_fecha = [];
var data_valor = [];
var data_maximo = [];
var data_minimo = [];

var var_maximo = [];
var var_minimo = [];


$(document).ready(function() {

    $("#btn_buscar").click(function(){
        $.ajax({
            url: $("#form_validacion").attr('action'),
            data: $("#form_validacion").serialize(),
            type:'POST',
            beforeSend: function () {
                $("#div_grafico").hide();
                activar_espera("#div_loading", "#div_informacion", "#div_error")
            },
            success: function (data) {
                $("#btn_buscar").attr("disabled", false);

                var_id = data.variable[0]['var_id'];
                variable = data.variable[0];

                //datos_json = jQuery.parseJSON(data.datos)
                datos_json = data.datos
                rows=''

                data_fecha = [];
                data_valor = [];
                data_maximo = [];
                data_minimo = [];

                var_maximo = [];
                var_minimo = [];

                for (var i in datos_json) {
                    rows += '<tr>';
                    col_fecha = get_col(var_id, "fecha", datos_json[i]['dia'], "");
                    data_fecha.push(new Date(datos_json[i]['dia']))
                    data_valor.push(datos_json[i]['valor'])
                    rows += col_fecha;
                    rows += get_col(var_id, "porcentaje", datos_json[i]['porcentaje'], datos_json[i]['class_porcentaje']);
                    rows += get_col(var_id, "valor", datos_json[i]['valor'], datos_json[i]['class_valor']);
                    if (var_id !== 1) {
                        data_maximo.push(datos_json[i]['maximo']);
                        data_minimo.push(datos_json[i]['minimo']);
                        var_maximo.push(variable['var_maximo']);
                        var_minimo.push(variable['var_minimo']);
                        rows += get_col(var_id, "maximo", datos_json[i]['maximo'], datos_json[i]['class_maximo']);
                        rows += get_col(var_id, "minimo", datos_json[i]['minimo'], datos_json[i]['class_minimo']);
                    }
                    else{
                        var_maximo.push(60);
                    }
                    //rows += get_col(var_id, "valor", datos_json[i]['valor'], datos_json[i]['class_valor']);
                    rows += get_col(var_id, "link", datos_json[i]['valor'], datos_json[i]['class_valor']);
                    rows += '</tr>';

                }
                thead = get_thead(var_id);
                $("#tabla_diario > thead").html(thead);
                $("#tabla_diario > tbody").html(rows);
                graficar(data.variable[0], data.estacion[0] );

                desactivar_espera("#div_loading", "#div_informacion", "#div_error")
                $("#div_grafico").show();

            },
            error: function () {
                $("#div_grafico").hide();
                mostrar_error("#div_loading", "#div_informacion", "#div_error")

            }
        });
    });
});


function get_col(var_id, tipo, valor, clase) {

    var col = ''
    if (tipo === 'fecha'){
        //fecha = new Date(valor)
        //fecha = fecha.getDate() + "/" + fecha.getMonth() + "/" + fecha.getFullYear()
        if (var_id === 1){
            col = '<th scope="row" class="col-3">'+valor+'</th>'
        }
        else{
            col = '<th scope="row" class="col-2">'+valor+'</th>'
        }
    }
    else if (tipo === 'link'){
        if (var_id === 1 ){
            col = '<td class="col-3">'
            col += '<a class="link-validacion" href="#">'
            //col += '<span class="fas fa-search" aria-hidden="true"></span>'
            //col += '<span class="" aria-hidden="true"></span>'
            col += 'Revisar'
            col += '</a></td>'
            //col += '</td>'
        }
        else{
            col = '<td class="col-2">'
            col += '<a class="link-validacion" href="#">'
            //col += '<span class="fas fa-search" aria-hidden="true"></span>'
            //col += '<span class="" aria-hidden="true"></span>'
            col += 'Revisar'
            col += '</a></td>'
            //col += '</td>'
        }
    }
    else{
        if(var_id == 1){
            col= '<td class="col-3 valor '+clase+'">'+valor+'</td>'
        }
        else{
            col = '<td class="col-2 '+clase+'">'+valor+'</td>'

        }
    }
    return col

};

function get_thead(var_id){
    var row = ''
    var th_fecha = ''
    var th_porcentaje = ''
    var th_valor = ''

    if (var_id === 1) {
        th_fecha = '<th scope="col" class="col-3">Fecha</th>';
        th_porcentaje = '<th scope="col" class="col-3">Porcentaje</th>';
        th_valor = '<th scope="col" class="col-3">Valor</th>';
        th_accion = '<th scope="col" class="col-3">Acción</th>';
        row += '<tr>'
        row += th_fecha + th_porcentaje + th_valor + th_accion;
        row += '</tr>'
    }
    else{
        th_fecha = '<th scope="col" class="col-2">Fecha</th>';
        th_porcentaje = '<th scope="col" class="col-2">Porcentaje</th>';
        th_valor = '<th scope="col" class="col-2">Valor</th>';
        th_maximo = '<th scope="col" class="col-2">Máximo</th>';
        th_minimo = '<th scope="col" class="col-2">Mínimo</th>';
        th_accion = '<th scope="col" class="col-2">&nbsp;</th>';
        row += '<tr>'
        row += th_fecha + th_porcentaje + th_valor + th_maximo +  th_minimo + th_accion
        row += '</tr>'

    }
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

        var limite = {
            x: data_fecha,
            y: var_maximo,
            name: 'Límite',
            type: 'lines'
        };

        var data = [trace1, limite];
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

        var limite_max = {
            x: data_fecha,
            y: var_maximo,
            name: 'Límite Máximo',
            type: 'lines'
        };

        var limite_min = {
            x: data_fecha,
            y: var_minimo,
            name: 'Límite Mínimo',
            type: 'lines'
        };

        var data = [trace1, trace2, trace3, limite_max, limite_min];
        //var data = [trace1, trace2, trace3];
        //var data = [trace1, trace2, trace3, limite_min];
    }

    var layout = {
        title: var_nombre + ' - '+ est_nombre,
        //showlegend: false
    };
    Plotly.newPlot('div_grafico', data, layout, {scrollZoom: true});

};
