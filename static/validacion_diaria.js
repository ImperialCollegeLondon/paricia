
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
                activar_espera("#div_loading", "#div_grafico", "#div_error");
                $table.bootstrapTable('showLoading');
            },
            success: function (data) {
                $("#btn_buscar").attr("disabled", false);
                var_id = data.variable[0]['var_id'];
                variable = data.variable[0];
                estacion = data.estacion[0];
                datos_json = data.datos
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
                $table.bootstrapTable({columns:columns, data: datos_json})

                graficar(data.variable[0], data.estacion[0] );

                desactivar_espera("#div_loading", "#div_grafico", "#div_error")
                //$("#div_grafico").show();
                $table.bootstrapTable('hideLoading');

            },
            error: function () {
                //$("#div_grafico").hide();
                mostrar_error("#div_loading", "#div_grafico", "#div_error")

            }
        });
    });


    var $button = $('#btn_enviar');
    var $btn_mostrar = $('#btn_mostrar');
    var $btn_mostrar_crudo = $('#btn_mostrar_crudo');

    var $btn_eliminar = $('#btn_eliminar');
    var $btn_eliminar_crudo = $('#btn_eliminar_crudo');

    var $btn_seleccionar = $('#btn_seleccionar');
    var $btn_seleccionar_crudo = $('#btn_seleccionar_crudo');

    var $btn_desmarcar = $('#btn_desmarcar');
    var $btn_desmarcar_crudo = $('#btn_desmarcar_crudo');

    var $btn_modificar_promedio = $('#btn_modificar_promedio');
    var $btn_modificar_acumulado = $('#btn_modificar_acumulado');

    var $table = $('#table_diario');

    $button.click(function () {
        alert(JSON.stringify($table.bootstrapTable('getData')));
    });


    $btn_mostrar.click(mostrar);
    $btn_mostrar_crudo.click(mostrar);

    $btn_eliminar.click(eliminar);
    $btn_eliminar_crudo.click(eliminar);

    $btn_seleccionar.click(marcar);
    $btn_desmarcar.click(desmarcar);

    $btn_seleccionar_crudo.click(marcar);
    $btn_desmarcar_crudo.click(desmarcar);

    /*
    $btn_modificar_promedio.click(function () {
        var inputs = $("#form_promedio").serializeArray();
        var $modal = $('#modal_promedio');
        modificar(inputs, $modal);
    });

    $btn_modificar_acumulado.click(function () {
        var inputs = $("#form_acumulado").serializeArray();
        var $modal = $('#modal_acumulado');
        modificar(inputs, $modal);
    });
    */
    $btn_modificar_acumulado.click(modificar);
    $btn_modificar_promedio.click(modificar);

});

//Mostrar filas ocultas en la tabla
function mostrar(event){
    var name = event.target.name;
    if (name === 'crudo')
        $table = $("#table_crudo");
    else
        $table = $("#table_diario");

    setTimeout(function(){
        $table.bootstrapTable('showLoading');
        setTimeout(function(){
            //index comienza en 0
            //obtener los ids de todas las filas ocultas
            var ids = $.map($table.bootstrapTable('getHiddenRows'), function (row) {
                return row.id
            });
            //recorrer los ids y actualizar la columna estado
            ids.map(function(id){
                $table.bootstrapTable('updateByUniqueId', {
                    id: id,
                    row: {estado: true}
                }).bootstrapTable('uncheck', id-1)
            });

            //mostrar todas las columnas ocultas
            $table.bootstrapTable('getHiddenRows', true);
            setTimeout(function(){
                $table.bootstrapTable('hideLoading');

            },0 | Math.random() * 100);
        },0 | Math.random() * 100);
    },0 | Math.random() * 100);


}

//Quitar filas de la tabla
function eliminar(event){
    $(this).attr('disabled',true);
    var name = event.target.name;
    if (name === 'crudo')
        $table = $("#table_crudo");
    else
        $table = $("#table_diario");

    setTimeout(function(){
        $table.bootstrapTable('showLoading');
        console.log("show");
        setTimeout(function(){
            //actualizar_estado($table);
            console.log("funcion");
            var ids = $.map($table.bootstrapTable('getSelections'), function (row) {
                return row.id
            });
            ids.map(function(id){
                $table.bootstrapTable('updateByUniqueId', {
                    id: id,
                    row: {estado: false}
                }).bootstrapTable('hideRow',{
                    uniqueId:id
                })

            });
            setTimeout(function(){
                console.log("hide");
                $table.bootstrapTable('hideLoading');
            },0 | Math.random() * 100);
        },0 | Math.random() * 100);
    },0 | Math.random() * 100);

    $(this).attr("disabled", false);
}


// Cambiar valores modificados en la tabla
function modificar(event){
    var name = event.target.name;
    var $form = $("#form_"+name);
    var inputs =$form.serializeArray();
    var $modal = $("#modal_"+name);
    var data = {};
    var table = $table = $("#table_crudo");
    $.each(inputs, function(i, field){
        data[field.name] = field.value;
    });
    id = data['id'];
    delete data['id'];
    $table.bootstrapTable('updateByUniqueId',{
        id: id,
        row: data
    });
    $modal.modal('hide');

}
//Marcar filas por rango de ids
function marcar(event){
    var name = event.target.name;
    var cadena = '';
    var $table = '';

    if (name === 'crudo'){
        $table = $("#table_crudo");
        cadena = $("#txt_seleccionar_crudo").val().toString();
    }
    else{
        cadena = $("#txt_seleccionar").val().toString();
        $table = $("#table_diario");
    }
    $table.bootstrapTable('showLoading');
    var arr_id = cadena.split(',');
    var arr_range = cadena.split('-');
    var ids = []

    if (arr_id.length>1){
        ids = arr_id.map(function(id){
            return parseInt(id)
        });
    }
    if (arr_range.length>0){
        var inicio = parseInt(arr_range[0]);
        var fin = parseInt(arr_range[1]);

        for (var id = inicio; id <= fin; id++){
            ids.push(id);
        }
    }

    $table.bootstrapTable('checkBy', {field: 'id', values: ids})
    $table.bootstrapTable('hideLoading');
}

// Desmarcar filas seleccionadas
function desmarcar(event){
    var $table = '';
    if (event.target.name==='crudo')
        $table = $("#table_crudo");
    else
        $table = $("#table_diario");


    $table.bootstrapTable('showLoading');
    var ids = $.map($table.bootstrapTable('getSelections'), function (row) {
        return row.id
    });
    $table.bootstrapTable('uncheckBy', {field: 'id', values: ids});
    $table.bootstrapTable('hideLoading');

}



// generar la tabla de datos de validacion
function detalle_crudos(e, value, row){

    var $table = $('#table_crudo');
    var estacion_id = $("#id_estacion").val();
    var variable_id = $("#id_variable").val();
    enlace = '/validacion/lista/' + estacion_id + '/' + variable_id + '/' + row.dia;
    $.ajax({
        url: enlace,
        type:'GET',
        beforeSend: function () {
            $table.bootstrapTable('showLoading');
        },
        success: function (data) {
            datos_json = data;
            $table.bootstrapTable('destroy');
            var columns = get_column_validado(variable_id);
            $table.bootstrapTable({columns:columns, data: datos_json})
            $table.bootstrapTable('hideLoading');
        },
        error: function () {
            console.log("llego")
        }
    });

};

//funcion para modificar una fila

//funcion para eliminar una fila de la tabla diario
function eliminar_diario(e, value, row, index){
    var $table = $('#table_diario');
    $table.bootstrapTable('updateRow', {
        index: index,
        row: {
            estado: false
        }
    });
    $table.bootstrapTable('hideRow', {
        index: index
    })
}
//funcion para eliminar una fila de la tabla crudos
function eliminar_crudo(e, value, row, index){
    var $table = $('#table_crudo');
    $table.bootstrapTable('updateRow', {
        index: index,
        row: {
            estado: false
        }
    });
    $table.bootstrapTable('hideRow', {
        index: index
    })
}

//funcion para abrir un formulario de edicion
function abrir_formulario(e, value, row, index){
    var variable_id = $("#id_variable").val();


    if (variable_id === '1'){
        var $form_modal = $('#modal_acumulado');
        var inputs = $("#form_acumulado").serializeArray();

    }
    else{
        var $form_modal = $('#modal_promedio');
        var inputs = $("#form_promedio").serializeArray();
    }

    $.each(inputs, function(i, field){
        $('input[name="'+field.name+'"]').val(row[field.name])
    });
    $form_modal.modal("show");
}

//Generar las columnas de la tabla de datos diarios
function get_colums_diario(var_id){
    var columns = [];

    var state = {
        field:'state',
        checkbox:true
    };

    var id = {
        field:'id',
        title:'Id'
    };

    var fecha = {
        field:'dia',
        title:'Fecha'

    };
    var porcentaje = {
        field:'porcentaje',
        title:'Porcentaje',
        cellStyle: style_porcentaje,
        footerFormatter: promedio
    };

    var accion = {
        field: 'accion',
        title: 'Acción',
        formatter: operate_table_diario,
        events: {
           'click .search': detalle_crudos,
           'click .delete': eliminar_diario,
           //'click .update': abrir_formulario

        }
    };

    columns.push(state);
    columns.push(id);
    columns.push(fecha);
    columns.push(porcentaje);


    if (var_id !== 1) {
        var valor = {
            field:'valor',
            title:'Valor',
            cellStyle: style_valor,
            formatter: format_valor,
            footerFormatter: promedio
        };
        var maximo = {
            field:'maximo',
            title:'Máximo',
            cellStyle: style_valor,
            formatter: format_valor,
            footerFormatter: promedio
        };

        var minimo= {
            field:'minimo',
            title:'Mínimo',
            cellStyle: style_valor,
            formatter: format_valor,
            footerFormatter: promedio
        }
        columns.push(valor);
        columns.push(maximo);
        columns.push(minimo);
    }
    else{
        var valor = {
            field:'valor',
            title:'Valor',
            cellStyle: style_valor,
            formatter: format_valor,
            footerFormatter: suma
        };
        columns.push(valor);
    }

    columns.push(accion);

    return columns

}



//generar las columnas para la tabla de datos crudos
function get_column_validado(var_id){
    var columns = [];
    var state = {
        field:'state',
        checkbox:true
    };

    var id = {
        field:'id',
        title:'Id'
    };

    var fecha = {
        field:'fecha',
        title:'Fecha'
    };

    var valor_atipico = {
        field:'',
        title:'Valores Atípicos',
        cellStyle: style_stddev
    };

    var comentario = {
        field:'comentario',
        title:'Comentario'
    };

    var accion = {
        field: 'accion',
        title: 'Acción',
        formatter: operate_table_crudo,
        events: {
           'click .delete': eliminar_crudo,
           'click .update': abrir_formulario

        }
    };

    columns.push(state);
    columns.push(id);
    columns.push(fecha);
    if (var_id!=='1'){
        var valor = {
            field:'valor',
            title:'Valor',
            cellStyle: style_error_crudo,
            footerFormatter: promedio
        };

        var maximo = {
            field:'maximo',
            title:'Máximo',
            cellStyle: style_error_crudo,
            footerFormatter: promedio
        };
        var minimo = {
            field:'minimo',
            title:'Mínimo',
            cellStyle: style_error_crudo,
            footerFormatter: promedio
        };
        columns.push(valor);

        columns.push(maximo);
        columns.push(minimo);

    }
    else{
        var valor = {
            field:'valor',
            title:'Valor',
            cellStyle: style_error_crudo,
            footerFormatter: suma
        };
        columns.push(valor);
    }
    columns.push(valor_atipico);
    columns.push(comentario);
    columns.push(accion);
    return columns
}


function operate_table_diario(value, row, index) {
    return [
      '<a class="search" href="javascript:void(0)" title="Detalle">',
      '<i class="fa fa-search"></i>',
      '</a>  ',
      '<a class="delete" href="javascript:void(0)" title="Eliminar">',
      '<i class="fa fa-trash"></i>',
      '</a>  ',
    ].join('')
}

function operate_table_crudo(value, row, index) {
    return [
      '<a class="delete" href="javascript:void(0)" title="Eliminar">',
      '<i class="fa fa-trash"></i>',
      '</a>  ',
      '<a class="update" href="javascript:void(0)" title="Modificar">',
      '<i class="fa fa-edit"></i>',
      '</a>  ',
    ].join('')
}

// Formato para el porcentaje de datos diarios
function style_porcentaje(value, row, index) {
    var clase = ''
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

//Formato para el valor, maximo, minimo.
function style_valor(value, row, index, field){
    var clase = ''
    field_numero = field+'_numero';
    if (row[field_numero]>0)
        clase = 'error';
    else
        clase = 'normal';
    return { classes: clase}
}
// Función para mostrar error
function style_error_crudo(value, row, index, field){
    var clase = ''
    field_error = field+'_error'
    if (row[field_error] === true)
        clase = 'error';
    else
        clase = 'normal';
    return { classes: clase}
}
//función para darle estilo a la desviación estandar
function style_stddev(value, row, index){
    var clase = ''
    if (row.stddev_error === true)
        clase = 'error';
    else
        clase = '';
    return { classes: clase}
}
//función para darle formato a la fecha
function style_fecha(value, row, index){
    var clase = ''
    if (row.estado === true)
        clase = 'normal';
    else
        clase = 'error';
    return { classes: clase}

}

// Poner el numero de errores en el día
function format_valor(value, row, index, field){
    var span = '<span class="badge badge-light">num</span>';
    var content = ''
    var field_numero = field + '_numero'
    if (row[field_numero]>0 ){
        span = span.replace('num',row[field_numero].toString());
        content = value + ' ' + span;
    }
    else{
        //span = span.replace('num',0);
        content = value;
    }
    return content
}

// Obtener el promedio de los datos
function promedio(data){
    var field = this.field;
    var promedio = 0;
    var suma = data.reduce(function (sum, i) {
        if (i['estado'])
            return sum + parseFloat(i[field])
        else
            return sum
    }, 0);
    var num_datos = data.reduce(function (sum, i) {
        if (i['estado'])
            return sum + 1
        else
            return sum
    }, 0);

    if (isNaN(suma))
        promedio = '-';
    else
        promedio = (suma / num_datos).toFixed(2);
    return promedio;
}
//obtener la suma de los datos
function suma(data){
    var field = this.field;
    var suma = data.reduce(function (sum, i) {
        if (i['estado']){
            return sum + parseFloat(i[field])
        }
        else{
            return sum
        }

    }, 0);
    return suma.toFixed(2);
}


function graficar(variable, estacion){
    var_id = variable['var_id'];
    var_nombre = variable['var_nombre'];
    est_nombre = estacion['est_nombre'];

    var width_graph = $(".container").width();

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
        width: width_graph,
        //showlegend: false
    };
    Plotly.newPlot('div_grafico', data, layout);

};
