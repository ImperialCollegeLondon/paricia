function generate_traces_dispersion(data, source_type, color){
    var result = [];
    var columns = Object.keys(data);
    columns = columns.filter((e) => e !== "time");
    for (const c of columns) {
      result.push(
        {
          x: data.time,
          y: data[c],
          mode: 'markers',
          name: c,
          showlegend: false,
          marker: {
            color: color,
            size: 2
          },
          type: 'scattergl',
          legendgroup: source_type
        }
      );

    }

    // Legend
    result.push(
        {
          x: [null],
          y: [null],
          mode: 'markers',
          name: source_type,
          showlegend: true,
          marker: {
            color: color,
          },
          type: 'scattergl',
          legendgroup: source_type
        }
    );
    return result;
}

function generate_traces_bars(data, source_type, color){
    var result = [];
    var columns = Object.keys(data);
    columns = columns.filter((e) => e !== "time");

    for (const c of columns) {
      result.push(
        {
          x: data.time,
          y: data[c],
          mode: 'lines',
          name: c + ' - ' + source_type,
          marker: {
            color: color,
            size: 2
          },
          showlegend: true,
          type: 'scattergl',
        }
      );
    }

    return result;
}


function bar_plot(series, append_to, variable){
    var data_array = [];

    let measurement = generate_traces_bars(series.measurement, "Measurement", 'rgb(0, 0, 255)');
    data_array.push(...measurement);
    let validated = generate_traces_bars(series.validated, "Validated", 'rgb(0, 255, 0)');
    data_array.push(...validated);
    let selected = generate_traces_bars(series.selected, "Selected", 'rgb(0, 0, 0)');
    data_array.push(...selected);

    var layout = {
        title: variable.var_nombre,
        showlegend: true,
    };

    const miDiv = document.querySelector("#" + append_to);
    miDiv.style.height = "450px";
    miDiv.style.width = "850px";
    Plotly.newPlot(append_to, data_array, layout, {renderer: 'webgl'});
}

function dispersion_plot(series, append_to, variable){
    var data_array = [];

    let measurement = generate_traces_dispersion(series.measurement, "Measurement", 'rgb(0, 0, 255)');
    data_array.push(...measurement);
    let validated = generate_traces_dispersion(series.validated, "Validated", 'rgb(0, 255, 0)');
    data_array.push(...validated);
    let selected = generate_traces_dispersion(series.selected, "Selected", 'rgb(0, 0, 0)');
    data_array.push(...selected);

    var layout = {
        title: variable.var_nombre,
        showlegend: true,
    };

    const miDiv = document.querySelector("#" + append_to);
    miDiv.style.height = "450px";
    miDiv.style.width = "850px";
    Plotly.newPlot(append_to, data_array, layout, {renderer: 'webgl'});
}


var dateFormat = "yy-mm-dd";

tr_ini = '<tr>';
tr_fin = '</tr>';
var json_data = {};
var data_date = [];
var data_value = [];
var data_maximum = [];
var data_minimum = [];
//var num_dias = 0;
var num_datos = 0;

var indicators_subhourly = {
    num_time: 0,
    num_value: 0,
    num_maximum: 0,
    num_minimum:0,
    num_stddev: 0,
    // TODO check if renaming num_data is needed
    num_data:0
}

var indicators_daily = {
    num_date: 0,
    num_percentage: 0,
    num_value: 0,
    num_maximum: 0,
    num_minimum: 0,
    num_days: 0
}

var num_date = 0;


$(document).ready(function() {

    $("#btn_detail_new").attr("disabled", true);

    $("#btn_submit").click(daily_query_submit);

    $("#btn_periodos_validacion").click(function(){
        $("#btn_periodos_validacion").attr("disabled", true);
    });


    // consultar los limites de la variable
    $("#id_variable").change(function () {
        var variable_id = $(this).val();
        var url = '/variable/variable/' + variable_id.toString() + '/?format=json';
        const url_total = window.location.origin + url;

        fetch(url_total)
          .then(response => response.json())
          .then(data => {
            $("#id_minimum").val(data.minimum);
            $("#id_maximum").val(data.maximum);
          })
          .catch(error => {
            console.error(error);
            alert(error);
          });
    });

    /*Filtros de la tablas*/
    $("#chk_porcentaje").change(filtrar_diario);
    $("#chk_fecha").change(filtrar_diario);
    $("#chk_numero").change(filtrar_diario);

    $("#chk_detail_time").change(filter_detail_table);
    $("#chk_detail_value").change(filter_detail_table);
    $("#chk_detail_stddev").change(filter_detail_table);
    $("#chk_detail_selected").change(filter_detail_table);
    $("#chk_detail_value_difference").change(filter_detail_table);

    var $table = $('#table_daily');

    /*Control de los botones*/
    var $btn_daily_select = $('#btn_daily_select');
    var $btn_daily_unselect = $('#btn_daily_unselect');
    var $btn_daily_unvalidate = $('#btn_daily_unvalidate');
    var $btn_daily_history = $('#btn_daily_history');
    var $btn_daily_delete = $('#btn_daily_delete');
    var $btn_daily_show = $('#btn_daily_show');
    var $btn_daily_send = $('#btn_daily_send');

//    var $btn_nuevo_promedio = $('#btn_nuevo_promedio');
//    var $btn_nuevo_acumulado = $('#btn_nuevo_acumulado');
//    var $btn_modificar_promedio = $('#btn_modificar_promedio');
//    var $btn_modificar_acumulado = $('#btn_modificar_acumulado');
//    var $btn_modificar_agua = $('#btn_modificar_agua');
//    var $btn_graficar = $('#btn_grafico');


    ///fondo blnco para la tabal diaria
    //$table.css("background-color","white");
//    var $btn_delete_valor = $("#btn_delete_valor");
    
    
    var $btn_detail_select = $('#btn_detail_select');
    var $btn_detail_unselect = $('#btn_detail_unselect');    
    var $btn_detail_new = $("#btn_detail_new");
    var $btn_detail_plot = $('#btn_detail_plot');
    var $btn_detail_delete = $('#btn_detail_delete');
    var $btn_detail_undo = $('#btn_detail_undo');
    var $btn_detail_save = $('#btn_detail_save');




//
//    
//    var $btn_nuevo_promedio = $('#btn_nuevo_promedio');
//    var $btn_nuevo_acumulado = $('#btn_nuevo_acumulado');
//    var $btn_modificar_promedio = $('#btn_modificar_promedio');
//    var $btn_modificar_acumulado = $('#btn_modificar_acumulado');
//    var $btn_modificar_agua = $('#btn_modificar_agua');
//    var $btn_graficar = $('#btn_grafico');
    var $btn_detail_new_averaged = $('#btn_detail_new_averaged');
    var $btn_detail_new_cumulative = $('#btn_detail_new_cumulative');
    var $btn_detail_modify_averaged = $('#btn_detail_modify_averaged');
    var $btn_detail_modify_cumulative = $('#btn_detail_modify_cumulative');
    var $btn_detail_modify_waterlevel = $('#btn_detail_modify_waterlevel');
//
//    var $btn_history = $('#btn_history');
//    var $btn_unvalidate = $('#btn_unvalidate');
//    var $table = $('#table_daily');
//    ///fondo blnco para la tabal diaria
//    //$table.css("background-color","white");
//    var $btn_delete_valor = $("#btn_delete_valor");
//    var $btn_detail_new = $("#btn_detail_new");

//    $btn_send.click(guardar_validados);
//    $btn_show.click(mostrar);
//    $btn_delete.click(eliminar);
//    $btn_select.click(marcar);
//    $btn_unselect.click(desmarcar);
//    $btn_nuevo_promedio.click(nuevo_registro);
//    $btn_nuevo_acumulado.click(nuevo_registro);
//    $btn_modificar_acumulado.click(modificar);
//    $btn_modificar_promedio.click(modificar);
//    $btn_modificar_agua.click(modificar);
//    $btn_guardar.click(guardar_crudos);
//    $btn_graficar.click(graficar);
//    $btn_detail_plot.click(graficar);
//    $btn_history.click(periodos_validacion);
//    $btn_delete_valor.click(eliminar_crudo);
//    $btn_unvalidate.click(desvalidar_datos);


    $btn_daily_select.click(marcar);
    $btn_daily_unselect.click(desmarcar);
    $btn_daily_unvalidate.click(desvalidar_datos);
    $btn_daily_history.click(periodos_validacion);
    $btn_daily_delete.click(eliminar);
    $btn_daily_show.click(mostrar);
    $btn_daily_send.click(save_daily);


//    $btn_guardar.click(guardar_crudos);
//    $btn_graficar.click(graficar);
//    $btn_detail_plot.click(graficar);
//    $btn_delete_valor.click(eliminar_crudo);


    $btn_detail_select.click(marcar);
    $btn_detail_unselect.click(desmarcar);
    $btn_detail_new.click(open_form_new);
    $btn_detail_delete.click(eliminar);
    $btn_detail_undo.click(mostrar);
    $btn_detail_save.click(save_detail);

//    $btn_nuevo_promedio.click(nuevo_registro);
//    $btn_nuevo_acumulado.click(nuevo_registro);
//    $btn_modificar_acumulado.click(modificar);
//    $btn_modificar_promedio.click(modificar);
//    $btn_modificar_agua.click(modificar);
    $btn_detail_new_averaged.click(new_register);
    $btn_detail_new_cumulative.click(new_register);
    $btn_detail_modify_cumulative.click(detail_modify);
    $btn_detail_modify_averaged.click(detail_modify);
    $btn_detail_modify_waterlevel.click(detail_modify);


    var dateFormat = "yy-mm-dd";
    $( "#id_start_date" ).datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat:"yy-mm-dd",
        yearRange: '2000:'+(new Date).getFullYear()
    });
    $( "#id_start_date" ).on( "change", function() {
        $( "#id_end_date" ).datepicker( "option", "minDate", getDate( this ) );
    });
    $( "#id_end_date" ).datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat:"yy-mm-dd",
        yearRange: '2000:'+(new Date).getFullYear()
    });
    $( "#id_end_date" ).on( "change", function() {
        $( "#id_start_time" ).datepicker( "option", "maxDate", getDate( this ) );
    });

    function getDate( element ) {
        var date;
        try {
            date = $.datepicker.parseDate( dateFormat, element.value );
        } catch( error ) {
            date = null;
        }
        return date;
    }


});

//consultar el historial de validacion
function periodos_validacion(event){
    debugger;
    fecha_inicio = $("input[name='inicio']").val();
    fecha_fin = $("input[name='fin']").val();
    if (fecha_inicio == '' && fecha_fin == '')
        {
            token = $("input[name='csrfmiddlewaretoken']").val();
            station_id = $("#id_station").val();
            variable_id = $("#id_variable").val();
        
            $.ajax({
                url: '/val2/',
                data: $("#form_validation").serialize(),
                type:'POST',
                beforeSend: function () {
                    activar_espera("historial");
                    $("#div_modal_historial").modal("show");
                },
                success: function (data) {
                    $("#div_historial").html(data)
                    desactivar_espera("historial");
                },
                error: function () {
        
                    show_message("historial");
        
                }
            });
        }
        else {
            token = $("input[name='csrfmiddlewaretoken']").val();
            station_id = $("#id_station").val();
            variable_id = $("#id_variable").val();
        
            $.ajax({
                url: '/val2/periodos_validacion/',
                data: $("#form_validation").serialize(),
                type:'POST',
                beforeSend: function () {
                    activar_espera("historial");
                    $("#div_modal_historial").modal("show");
                },
                success: function (data) {
                    $("#div_historial").html(data)
                    desactivar_espera("historial");
                },
                error: function () {
        
                    show_message("historial");
        
                }
            });
        }
   

}

// pasar los datos crudos a validados

function save_daily(event){
//    debugger;
    var $table_daily = $('#table_daily');
    var $table_detail = $('#table_detail');
    token = $("input[name='csrfmiddlewaretoken']").val();
    station_id = $("#id_station").val();
    variable_id = $("#id_variable").val();
    maximum = $("#id_maximum").val();
    minimum = $("#id_minimum").val();
    start_date = $("input[name='start_date']").val();
    end_date = $("input[name='end_date']").val();

    changes = JSON.stringify($table_daily.bootstrapTable('getData',{unfiltered:true, includeHiddenRows: true}));

    $.ajax({
        url: '/validated/daily_save/',
        data: {
            'csrfmiddlewaretoken': token,
            'station_id': station_id,
            'variable_id': variable_id,
            'start_date': start_date,
            'end_date': end_date,
            'maximum': maximum,
            'minimum': minimum,
            'changes': changes
        },
        type:'POST',
        beforeSend: function () {
            $table_daily.bootstrapTable('showLoading');
            $table_detail.bootstrapTable('showLoading');
        },
        success: function (data) {
            if (data.result == true){
                $("#div_body_message").html('Data saved correctly to Validated!')
                $("#div_validation_message").modal("show");
                $("#div_information").hide();
                clean_filters('daily');
                clean_filters('detail');
                $table_detail.bootstrapTable('removeAll');
                $table_daily.bootstrapTable('removeAll');
            }
            else{
                $("#div_body_message").html('There was a problem with the validation please contact the administrator')
                $("#div_validation_message").modal("show");
            }
            $table_daily.bootstrapTable('hideLoading');
            $table_detail.bootstrapTable('hideLoading');
        },
        error: function () {
            $("#div_body_message").html('There was a problem with the validation please contact the administrator')
            $("#div_validation_message").modal("show");
            $table_daily.bootstrapTable('hideLoading');
        }
    });

}

//eliminar datos validados de la base de datos

function eliminar_validados(event){
    debugger;
    var $table = $('#table_daily');
    var $table_detail = $('#table_detail');
    //$table.css("background-color","white");
    token = $("input[name='csrfmiddlewaretoken']").val();
    station_id = $("#id_station").val();
    variable_id = $("#id_variable").val();
    //comentario_general = $("textarea[name='comentario_general']").val();
    changes = JSON.stringify($table.bootstrapTable('getData',{unfiltered:true, includeHiddenRows: true}));


    $.ajax({
        url: '/val2/eliminarvalidados/',
        data: {
            'csrfmiddlewaretoken': token,
            'station_id': station_id,
            'variable_id': variable_id,
            'changes': changes
        },
        type:'POST',
        beforeSend: function () {
            //$table.bootstrapTable('showLoading');

        },
        success: function (data) {
            if (data.result == true){
                //$("#div_body_mensaje").html('Datos Guardados')
                //$("#div_mensaje_validacion").modal("show");

                clean_filters('daily');
                clean_filters('detail');
                //$table_detail.bootstrapTable('removeAll');
                //$table.bootstrapTable('removeAll');
                daily_query_submit();


            }
            else{
                $("#div_body_message").html('There was a problem with the validation please contact the administrator')
                $("#div_validation_message").modal("show");

            }
            $table.bootstrapTable('hideLoading');
            $table_detail.bootstrapTable('hideLoading');


        },
        error: function () {
            $("#div_body_message").html('There was a problem with the validation please contact the administrator')
            $("#div_validation_message").modal("show");
            $table.bootstrapTable('hideLoading');
        }
    });

}

// guardar los cambios en los datos crudos
function save_detail(event){
    debugger;
//    cambios = JSON.stringify($table.bootstrapTable('getData',{unfiltered:true}));
//    //detalle_crudos();
    document.getElementById("tab3-tab").style.display = "none";
    var $table = $('#table_detail');
    token = $("input[name='csrfmiddlewaretoken']").val();
    station_id = $("#id_station").val();
    variable_id = $("#id_variable").val();
    start_date = $("input[name='start_date']").val();
    end_date = $("input[name='end_date']").val();
    data = JSON.stringify($table.bootstrapTable('getData',{unfiltered:true}));

    $.ajax({
        url: '/validated/detail_save/',
        data: {
            'csrfmiddlewaretoken': token,
            'station_id': station_id,
            'variable_id': variable_id,
            'start_date': start_date,
            'end_date': end_date,
            'data': data
        },
        type:'POST',
        beforeSend: function () {
            $table.bootstrapTable('showLoading');
        },
        success: function (response) {
            console.log(typeof response.resultado)
            if (response.resultado == true){
                $("#div_body_message").html('Data saved successfully')
                $("#div_validation_message").modal("show");
                detail_details();
                modify_row();
                clean_filters('detail');
            }
            else{
                $("#div_body_message").html('There was a problem with the validation please contact the administrator')
                $("#div_validation_message").modal("show");
                $table.bootstrapTable('hideLoading');
            }
        },
        error: function () {
            $("#div_body_message").html('There was a problem with the validation please contact the administrator')
            $("#div_validation_message").modal("show");
            $table.bootstrapTable('hideLoading');
        }
    });


}

// Consultar la serie de datos diarios desde el servidor de base de datos
function daily_query_submit(){
//    debugger;
    var $table_daily = $('#table_daily');
    var var_id = $("#id_variable").val();
    var flag_error = false;
    var message = '';
    $("#orig_variable_id").val(var_id);
    $("#div_information").html('')
//    $("#resize_plot").hide();
    clean_filters('daily');
    clean_filters('detail');
    //$("#table_crudo").bootstrapTable('removeAll');
//    debugger;
    start_date = document.querySelector('input[name="start_date"]').value;
    end_date = document.querySelector('input[name="end_date"]').value;
    if( start_date == '' || end_date == '')
    {
        $("#div_message_dates").show("slow");
        $("#div_c").html("");
    }
    else {
        $("#div_message_dates").hide();
        $("#div_c").html("");
        $.ajax({
            url: $("#form_validation").attr('action'),
            data: $("#form_validation").serialize(),
            type:'POST',
            beforeSend: function () {
                $table_daily.bootstrapTable('showLoading');
            },
            success: function (data) {
                $("#btn_submit").attr("disabled", false);
                for (var key in data){
                    if (key == 'error'){
                        flag_error = true;
                        message = data.error;
                    }
                }
                if (flag_error == true){
                    $table_daily.bootstrapTable('hideLoading');
//                    $("#resize_plot").hide();
                    $("#div_body_message").html(message)
                    $("#div_validation_message").modal("show");
                    return;
                }


                if (data.data.length < 1){
                    $("#div_information").show("slow");
                    $("#div_information").html('<div><h1 style="background-color : red">No hay datos</h1></div>');
                    return;
                }

                $("#div_c").html(data.curva);

                if (data.variable.is_cumulative){
                    bar_plot(data.series, "div_information", data.variable);
                }else{
                    dispersion_plot(data.series, "div_information", data.variable);
                }

//                enable_new();
                var_id = data.variable.id;
                variable = data.variable;
                station = data.station;
//                        json_data = data.datos;
                json_data = data.data
                //num_dias = data.indicadores[0]['num_dias'];
                $table_daily.bootstrapTable('destroy');
//                for (const index in data.indicators){
//                    debugger;
//                    indicators_daily[index]= data.indicators[index];
//                }
//                debugger;
                indicators_daily = data.indicators;
//                        debugger;
//                var columns = get_columns_daily(var_id, data.indicators);
                var columns = get_columns_daily(var_id, data.value_columns);
                $table_daily.bootstrapTable({
                    columns:columns,
                    data: json_data,
                    height: 420,
                    showFooter: true,
                    uniqueId: 'id',
                    rowStyle: style_row
                });

                $table_daily.bootstrapTable('hideLoading');
                $("#table_detail").bootstrapTable('removeAll');

    
            },
            error: function () {
//                debugger;
                $table_daily.bootstrapTable('hideLoading');
                $("#div_body_message").html('Ocurrio un problema con la validación por favor contacte con el administrador')
                $("#div_validation_message").modal("show");
                //mostrar_mensaje()
    
            }
        });
    
    }

    var tab1 = document.getElementById("tab1-tab");
    tab1.click();
}


function getTab(evt, tabName) {
    var i, tabpane;
    tabpane = document.getElementsByClassName("tab-pane");
    for (i = 0; i < tabpane.length; i++) {
        tabpane[i].style.display = "none";
        tabpane[i].classList.remove("show");
    }

    var e = document.getElementById(tabName);
    e.classList.add("show");
    e.style.display = "";
}




// actualizar una fila de la tabla de datos diarios
function modify_row(){
    debugger;
    var $table = $('#table_detail');
    var $table_daily = $('#table_daily');

    var id_diario = $("#orig_id_diario").val();
    var fecha = $("#orig_fecha_diario").val();
    var var_id = $("#orig_variable_id").val();

    var limite_inferior = $("#id_limite_inferior").val();
    var limite_superior = $("#id_limite_superior").val();

    var datos_crudos = $table.bootstrapTable('getData', {unfiltered:true});

    var suma_valor = 0;
    var suma_maximo = 0;
    var suma_minimo = 0;

    var suma_nivel = 0;
    var suma_caudal = 0;

    var avg_valor = 0;
    var avg_maximo = 0;
    var avg_minimo = 0;

    var avg_nivel = 0;
    var avg_caudal = 0;

    var num_valor = 0;
    var num_maximo = 0;
    var num_minimo = 0;

    var num_nivel = 0;
    var num_caudal = 0;

    var num_date = 0;

    var sum_datos = 0;

    $.each(datos_crudos, function(i, item) {
        if (item.estado){

            if (var_id == 10 || var_id == 11){
                if (typeof(parseFloat(item.nivel)) == "number"){
                    suma_nivel = suma_nivel + parseFloat(item.nivel);

                    if ((parseFloat(item.nivel)<limite_inferior) || (parseFloat(item.nivel)>limite_superior))
                        num_nivel += 1;
                }

                if (typeof(parseFloat(item.caudal)) == "number"){
                    suma_caudal = suma_caudal + parseFloat(item.caudal);
                }

            }
            else{
                if (typeof(parseFloat(item.valor)) == "number"){
                    suma_valor = suma_valor + parseFloat(item.valor);

                    if ((parseFloat(item.valor)<limite_inferior) || (parseFloat(item.valor)>limite_superior))
                        num_valor += 1;
                }
            }



            if (var_id != 1 && var_id != 10 && var_id != 11){
                if (typeof(parseFloat(item.maximo)) == "number"){
                    suma_maximo = suma_maximo + parseFloat(item.maximo);
                    if ((parseFloat(item.maximo)<limite_inferior) || (parseFloat(item.maximo)>limite_superior))
                        num_maximo += 1;
                }
                if (typeof(parseFloat(item.minimo)) == "number"){
                    suma_minimo = suma_minimo + parseFloat(item.minimo);
                    if ((parseFloat(item.minimo)<limite_inferior) || (parseFloat(item.minimo)>limite_superior))
                        num_minimo += 1;
                }
            }

            if (item.seleccionado == false || item.estado == false)
                num_date += 1;

            sum_datos += 1;

        }
    });


    if (isNaN(suma_valor))
        avg_valor = null;
    else
        avg_valor = (suma_valor / sum_datos).toFixed(2);

    if (isNaN(suma_maximo))
        avg_maximo = null;
    else
        avg_maximo = (Math.max.apply(Math, datos_crudos.map(function(o) {
                    return o.maximo;
                }))).toFixed(2);

    if (isNaN(suma_minimo))
        avg_minimo = null;
    else
        avg_minimo = (Math.min.apply(Math, datos_crudos.map(function(o) {
                    return o.minimo;
                }))).toFixed(2);

    if (isNaN(suma_nivel))
        avg_nivel = null;
    else
        avg_nivel = (avg_nivel / sum_datos).toFixed(2);


    if (isNaN(suma_caudal))
        avg_caudal = null;
    else
        avg_caudal = (avg_caudal / sum_datos).toFixed(2);

    var porcentaje = (sum_datos * 100 / indicators_subhourly['num_data']).toFixed(2);

    var porcentaje_error = false

    if (var_id == 1){
        porcentaje_error = porcentaje < 80 || porcentaje > 100 ? true : false
    }
    else{
        porcentaje_error = porcentaje < 70 || porcentaje > 100 ? true : false
    }





    if (var_id != 1){
        $table_daily.bootstrapTable('updateByUniqueId', {
            id: id_diario,
            row: {valor: avg_valor, maximo: avg_maximo, minimo: avg_minimo, validado: true,
                valor_numero: num_valor, maximo_numero: num_maximo, minimo_numero: num_minimo,
                porcentaje: porcentaje, porcentaje_error: porcentaje_error, fecha_numero: num_date,
                valor_error: num_valor > 0 ? true : false,
                maximo_error: num_maximo > 0 ? true: false,
                minimo_error: num_minimo > 0 ? true: false
            }
        });

    }
    else if (var_id == 10 || var_id == 11){
        $table_daily.bootstrapTable('updateByUniqueId', {
            id: id_diario,
            row: {nivel: avg_nivel, caudal: avg_caudal, validado: true,
                nivel_numero: num_nivel,
                porcentaje: porcentaje, porcentaje_error: porcentaje_error, fecha_numero: num_date,
                nivel_error: num_nivel > 0 ? true : false
            }
        });
    }
    else {
        $table_daily.bootstrapTable('updateByUniqueId', {
            id: id_diario,
            row: {valor: suma_valor.toFixed(2), validado: true, valor_numero: num_valor, porcentaje: porcentaje,
                porcentaje_error: porcentaje_error, fecha_numero: num_date,
                valor_error: num_valor > 0 ? true : false
            }
        });
    }


}



//Deshacer los cambios realizados en la tabla crudos/diarios
function mostrar(event){
    debugger;
    var name = event.currentTarget.name;
    if (name === 'crudo')
        $table = $("#table_detail");
    else
        $table = $("#table_daily");

    setTimeout(function(){
        $table.bootstrapTable('showLoading');
        setTimeout(function(){
            //index comienza en 0
            //obtener los ids de todas las filas ocultas
            var ids = $.map($table.bootstrapTable('getData',{unfiltered:true, includeHiddenRows: true}), function (row) {
                if (row.estado == false){
                    return row.id
                }
            });

            //recorrer los ids y actualizar la columna estado
            ids.map(function(id){
                $table.bootstrapTable('updateByUniqueId', {
                    id: id,
                    row: {estado: true}
                })
            });

            $table.bootstrapTable('uncheckBy', {field: 'id', values: ids});

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
    debugger;
    $(this).attr('disabled',true);
    var name = event.currentTarget.name;
    console.log(name)
    if (name === 'crudo')
        $table = $("#table_detail");
    else
        $table = $("#table_daily");

    setTimeout(function(){
        $table.bootstrapTable('showLoading');
        setTimeout(function(){

            var ids = $.map($table.bootstrapTable('getSelections'), function (row) {
                return row.id
            });
            ids.map(function(id){
                $table.bootstrapTable('updateByUniqueId', {
                    id: id,
                    row: {estado: false}
                })/*.bootstrapTable('hideRow',{
                    uniqueId:id
                })*/

            });

            $table.bootstrapTable('uncheckBy', {field: 'id', values: ids})

            setTimeout(function(){
                //$table.bootstrapTable('uncheckAll');
                $table.bootstrapTable('hideLoading');

            },0 | Math.random() * 100);
        },0 | Math.random() * 100);
    },0 | Math.random() * 100);

    $(this).attr("disabled", false);
}

// desvalidar datos
// desvalidar datos
function desvalidar_datos(event){
    debugger;
    $(this).attr('disabled',true);
    var name = event.currentTarget.name;
    console.log(name)
    if (name === 'crudo')
        $table = $("#table_detail");
    else
        $table = $("#table_daily");

    setTimeout(function(){
        $table.bootstrapTable('showLoading');
        setTimeout(function(){

            var ids = $.map($table.bootstrapTable('getSelections'), function (row) {
                return row.id
            });
            ids.map(function(id){
                $table.bootstrapTable('updateByUniqueId', {
                    id: id,
                    row: {validado: false}
                })/*.bootstrapTable('hideRow',{
                    uniqueId:id
                })*/

            });

            $table.bootstrapTable('uncheckBy', {field: 'id', values: ids})


            setTimeout(function(){
                //$table.bootstrapTable('uncheckAll');
                eliminar_validados();

                //$table.bootstrapTable('hideLoading');

            },0 | Math.random() * 100);
        },0 | Math.random() * 100);
    },0 | Math.random() * 100);

    $(this).attr("disabled", false);
}


//Crear un nuevo registro en la tabla de crudos
function new_register(event){
    debugger;
    var limite_inferior = $("#id_limite_inferior").val();
    var limite_superior = $("#id_limite_superior").val();
    var variable_id = $("#id_variable").val();

    var name = event.currentTarget.name;

    var $form = $("#form_nuevo_"+name);
    var $form_name = "#form_nuevo_"+name;
    $($form_name+',input[name="fecha"]').attr('disabled',false);

    var inputs =$form.serializeArray();
    var $modal = $("#modal_nuevo_"+name);
    var data = {};
    var table = $table = $("#table_detail");

    $.each(inputs, function(i, field){
        data[field.name] = field.value;
    });

    var num_datos = $table.bootstrapTable('getData').length
    data['id']= num_datos + 1;
    console.log(data['fecha']);
    data['fecha'] = data['fecha']+"T"+data['hora']+":00";
    delete data['hora'];
    data['validado'] = false;
    data['seleccionado'] = true;
    data['estado'] = true;
    data['maximo']=limite_superior;
    data['minimo']=limite_inferior;
    data['fecha_error'] = '1';
    data['stddev_error'] = false;
    //data['varcon_error'] = false;
    index = data['fila'];
    delete data['fila'];

    if (variable_id == 1){
        data['valor_error'] = get_value_error(data['valor']);
    }
    else{
        data['nivel_error'] = get_value_error(data['nivel']);
    }
    console.log($table);
    console.log(data);
    datos = $table.bootstrapTable('getData')
    var fila = get_existe_en_tabla(data['fecha'],datos);
    if (fila.length == 0) {
        $table.bootstrapTable('insertRow', {
            index: index,
            row: data
        });

        $modal.modal('hide');
    }
    else{


    }

}

function get_existe_en_tabla(fecha, datos){
    debugger;
    var existe = false;
    return datos.filter(
        function(datos){
            //if(datos.fecha == fecha)
                //existe = true
            return datos.fecha == fecha
        }
    )


}


// Cambiar valores modificados en la tabla crudos
function detail_modify(event){
//    debugger;
    $('input[name="detail_time"]').attr('disabled',false);
    var variable_id = parseInt($("#id_variable").val());
    var name = event.currentTarget.name;
    var $form = $("#form_"+name);
    var inputs =$form.serializeArray();
    var $modal = $("#modal_"+name);
    var data = {};
    var table = $table = $("#table_detail");
//    $.each(inputs, function(i, field){
//        data[field.name] = field.value;
//    });

    $.each(inputs, function(i, field){
        if (field.name.includes('detail_')) {
            var _field = field.name.split("_")[1];
            data[_field] = field.value;
        }
    });

    id = data['id'];
    delete data['id'];
    data['state'] = true;
    if (variable_id == 10 || variable_id == 11){
        data['waterlevel_error'] = get_value_error(data['waterlevel']);
    }
    else{
        data['value_error'] = get_value_error(data['value']);
    }


    if (variable_id != 1 && variable_id != 10 && variable_id != 11){
        data['maximum_error'] = get_value_error(data['maximum']);
        data['minimum_error'] = get_value_error(data['minimum']);
    }
    data['stddev_error'] = false;
    console.log(data);
    $table.bootstrapTable('updateByUniqueId',{
        id: id,
        row: data
    });
    $modal.modal('hide');
}

//Marcar filas por rango de ids en la tabla tabla crudos/diarios
function marcar(event){
    debugger;
    var name = event.currentTarget.name;
    var cadena = '';
    var $table = '';

    if (name === 'crudo'){
        $table = $("#table_detail");
        cadena = $("#txt_selection_crudo").val().toString();
    }
    else{
        cadena = $("#txt_selection").val().toString();
        $table = $("#table_daily");
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

// Desmarcar filas seleccionadas tabla crudos/diarios
function desmarcar(event){
    debugger;
    var $table = '';
    var name = event.currentTarget.name;
    if (name ==='crudo')
        $table = $("#table_detail");
    else
        $table = $("#table_daily");


    $table.bootstrapTable('showLoading');
    var ids = $.map($table.bootstrapTable('getSelections'), function (row) {
        return row.id
    });
    $table.bootstrapTable('uncheckBy', {field: 'id', values: ids});
    $table.bootstrapTable('hideLoading');

}

// generar la tabla de datos de validacion
function detail_details(e, value, row){
//    debugger;
    var $table = $('#table_detail');
    var station_id = $("#id_station").val();
    var variable_id = $("#id_variable").val();

    var id_daily = 0;
    var date = '';

    var state = row || false

    if (state == false ){
        id_daily = $("#orig_id_daily").val();
        date = $("#orig_date_daily").val();
    }
    else{
        id_daily = row.id;
        date = row.date;
        $("#orig_id_daily").val(id_daily);
        $("#orig_date_daily").val(date);
    }

    var var_maximum = $("#id_maximum").val();
    var var_minimum = $("#id_minimum").val();

    url = '/validated/detail_list/' + station_id + '/' + variable_id + '/' + date + '/' + var_minimum + '/' + var_maximum;

    $.ajax({
        url: url,
        type:'GET',
        beforeSend: function () {
            $table.bootstrapTable('showLoading');
        },
        success: function (data) {
            document.getElementById("tab3-tab").style.display = "block";
            document.getElementById("tab3-tab").click();
            json_data = data.series;
            $table.bootstrapTable('destroy');
            for (const index in data.indicators){
                indicators_subhourly[index] = data.indicators[index];
//                $("#span_"+index+"_crudo").text(indicators_subhourly[index]);
                // TODO Verificar
                $("#span_"+index+"_detail").text(indicators_subhourly[index]);
            }


            /* this is an example for new snippet extension make by me xD */
            for (const element of json_data) {
                element["time"] = (element['time']).replace('T',' ');
            }

            var columns = get_columns_detail(variable_id, data.value_columns);
            $table.bootstrapTable({
                columns:columns,
                data: json_data,
                rowStyle: style_row,
                height: 320,
                });
            //$table.bootstrapTable({columns:columns, data: json_data})
            $table.bootstrapTable('hideLoading');
        },
        error: function () {
            $("#div_body_message").html('An issue occurred with the validation. Please contact the administrator.')
            $("#div_validation_message").modal("show");
            $table.bootstrapTable('hideLoading');
        }
    });

};

//funcion para eliminar una fila de la tabla diario
function delete_daily(e, value, row, index){
    debugger;
    var $table = $('#table_daily');
    $table.bootstrapTable('updateRow', {
        index: index,
        row: {
            state: false
        }
    });
//    $table.bootstrapTable('uncheckBy', {field: 'id', values: ids});
//    $table.bootstrapTable('uncheckBy', {field: 'id', values: ids});

    /*$table.bootstrapTable('hideRow', {
        index: index
    })*/
}

//funcion para abrir el formulario de eliminar
function open_form_delete(e, value, row, index){
    debugger;
    var $form_modal = $('#modal_delete');
    var inputs = $("#form_delete").serializeArray();
    $.each(inputs, function(i, field){
        $('input[name="'+field.name+'"]').val(row[field.name]);
    });
    $form_modal.modal("show");
}

//funcion para eliminar una fila de la tabla crudos
function eliminar_crudo(event){
    debugger;
    //console.log("row", row);
    var inputs = $("#form_delete").serializeArray();
    var $form_modal = $('#modal_delete');
    var table = $table = $("#table_detail");
    var data = {};
    $.each(inputs, function(i, field){
        data[field.name] = field.value;
    });

    id = data['id'];
    delete data['id'];
    data['estado'] = false;
    $table.bootstrapTable('updateByUniqueId',{
        id: id,
        row: data
    });
    $form_modal.modal('hide');

    /*setTimeout(function(){
                },0 | Math.random() * 10);*/



}

function open_form_new(event){
    debugger;
    var fecha = $("#orig_fecha_diario").val();
    var variable_id = parseInt($("#id_variable").val());
    if (variable_id === 1){
        var $form_modal = $('#modal_nuevo_acumulado');
        var $form = "#form_nuevo_acumulado";
        var inputs = $("#form_nuevo_acumulado").serializeArray();

    }
    else{
        var $form_modal = $('#modal_nuevo_promedio');
        var $form = "#form_nuevo_promedio";
        var inputs = $("#form_nuevo_promedio").serializeArray();
    }
    $($form+',input[name="fecha"]').val(fecha);
    $($form+',input[name="fecha"]').attr('disabled',true);
    $form_modal.modal("show");
}

//funcion para abrir un formulario de edicion de datos crudos
function open_form(e, value, row, index){
    debugger;
    var variable_id = parseInt( $("#id_variable").val());

    if (variable_id === 1){
        var $form_modal = $('#modal_cumulative');
        var inputs = $("#form_cumulative").serializeArray();

    }
    else if(variable_id == 10 || variable_id == 11){
        var $form_modal = $('#modal_waterlevel');
        var inputs = $("#form_waterlevel").serializeArray();
    }
    else{
        var $form_modal = $('#modal_averaged');
        var inputs = $("#form_averaged").serializeArray();
    }

    $.each(inputs, function(i, field){
        if (field.name.includes('detail_')) {
            var _field = field.name.split("_")[1];
            $('input[name="'+field.name+'"]').val(row[_field]);
        }
    });

    $('input[name="detail_time"]').attr('disabled',true);
    $form_modal.modal("show");
}


//Generar las columnas de la tabla de datos diarios
function get_columns_daily(var_id, value_columns){
    var columns = [];

    var state = {
        field:'state',
        checkbox:true
    };
    columns.push(state);

    var id = {
        field:'id',
        title:'Id',
        cellStyle: style_id
    };
    columns.push(id);

    var date = {
        field:'date',
        title: 'Date',
        cellStyle: style_date,
        formatter: format_value,
        footerFormatter: footer_date,
        //filterControl: 'datepicker'
    };
    columns.push(date);


    var percentage = {
        field:'percentage',
        title:'Percnt.',
        cellStyle: style_percentage,
        footerFormatter: footer_average,
        //filterControl: 'input'
    };
    columns.push(percentage);

    if (value_columns.includes("sum")){
        var sum = {
            field:'sum',
            title:'Sum',
            cellStyle: style_value,
            formatter: format_value,
            footerFormatter: footer_sum
        };
        columns.push(sum);
    }

    if (value_columns.includes("average")){
        var average = {
            field:'average',
            title:'Average',
            cellStyle: style_value,
            formatter: format_value,
            footerFormatter: footer_average
        };
        columns.push(average);
    }

    if (value_columns.includes("maximum")){
        var maximum = {
            field:'maximum',
            title:'Max. of Maxs. ',
            cellStyle: style_value,
            formatter: format_value,
            footerFormatter: footer_average
        };
        columns.push(maximum);
    }

    if (value_columns.includes("minimum")){
        var minimum= {
            field:'minimum',
            title:'Min. of Mins. ',
            cellStyle: style_value,
            formatter: format_value,
            footerFormatter: footer_average
        }
        columns.push(minimum);
    }

    var value_difference = {
        field:'value_difference_error_count',
        title:'Diff. Err',
        cellStyle: style_value_diff,
        formatter: format_value,
        footerFormatter: footer_value_diff
    };
    columns.push(value_difference);

    var action = {
        field: 'action',
        title: 'Action',
        formatter: operate_table_daily,
        events: {
           'click .search': detail_details,
           'click .delete': delete_daily,
           //'click .update': abrir_formulario
        }
    };
    columns.push(action);

    return columns
}

//generar las columnas para la tabla de datos crudos
function get_columns_detail(var_id, value_columns){
    var columns = [];
    var span = '<span id="span_id" class="badge badge-danger">num</span>';

    var is_selected = {
        field:'is_selected',
        checkbox:true,
    };
    columns.push(is_selected);

    var id = {
        field:'id',
        title:'Id',
        cellStyle: style_id,
        footerFormatter: footer_id
    };
    columns.push(id);

    var time = {
        field:'time',
        title:'Time',
        cellStyle: style_date,
        footerFormatter: footer_data_count
    };
    columns.push(time);

    if (value_columns.includes("sum")){
        var sum = {
            field:'sum',
            title:'Sum',
            cellStyle: style_error_detail,
//            formatter: format_value,
            footerFormatter: footer_sum
        };
        columns.push(sum);
    }

    if (value_columns.includes("average")){
        var average = {
            field:'average',
            title:'Average',
            cellStyle: style_error_detail,
//            formatter: format_value,
            footerFormatter: footer_average
        };
        columns.push(average);
    }

    if (value_columns.includes("maximum")){
        var maximum = {
            field:'maximum',
            title:'Maximum',
            cellStyle: style_error_detail,
//            formatter: format_value,
            footerFormatter: footer_average
        };
        columns.push(maximum);
    }

    if (value_columns.includes("minimum")){
        var minimum= {
            field:'minimum',
            title:'Minimum',
            cellStyle: style_error_detail,
//            formatter: format_value,
            footerFormatter: footer_average
        }
        columns.push(minimum);
    }

    var outlier_err = {
        field:'stddev_error',
        title:'Outliers',
        cellStyle: style_stddev_err,
        formatter: format_stddev_err,
        footerFormatter: footer_stddev_err
    };
    columns.push(outlier_err);


    var value_difference = {
        field:'value_difference',
        title:'Value diff.',
        cellStyle: style_detail_value_diff,
        footerFormatter: footer_detail_value_diff
    };
    columns.push(value_difference);

    var value_diff_error = {
        field:'value_difference_error',
        visible: false,
    };
    columns.push(value_diff_error);

    var action = {
        field: 'action',
        title: 'Action',
        formatter: operate_table_detail,
        events: {
           'click .delete_detail': open_form_delete,
           'click .update': open_form

        }
    };
    columns.push(action);

    return columns
}

//Función para generar los iconos de acción de la tabla diario
function operate_table_daily(value, row, index) {
//    debugger;
    return [
      '<a class="search" href="javascript:void(0)" title="Detail">',
      '<i class="fa fa-search"></i>',
      '</a>  ',
      '<a class="delete" href="javascript:void(0)" title="Delete">',
      '<i class="fa fa-trash"></i>',
      '</a>  ',
    ].join('')
}

//Función para generar los iconos de acción de la tabla crudos
function operate_table_detail(value, row, index) {
//    debugger;
    return [
      '<a class="delete_detail" href="javascript:void(0)" title="Delete">',
      '<i class="fa fa-trash"></i>',
      '</a>  ',
      '<a class="update" href="javascript:void(0)" title="Modify">',
      '<i class="fa fa-edit"></i>',
      '</a>  ',
    ].join('')
}





function style_row(row, index){
//    debugger;
    var _class = '';
    if (row.state == false) {
      _class = 'error';
    }
    /*if (row.seleccionado == false){
        clase = 'no-seleccionado'
    }*/
    else
        _class = '';
    return {classes: _class}
}





//Formato para el error de la tabla crudos/diarios
function style_error_detail(value, row, index, field){
//    debugger;
    var clase = ''
    field_error = field+'_error'
    if (row[field_error] === true)
        clase = 'error';
    else
        clase = 'normal';
    return { classes: clase}
}

//Formato para la desviación estandar
function style_stddev_err(value, row, index){
//    debugger;
    var _class = '';
    if (value === true)
        _class = 'error';
    return { classes: _class}
}


function style_detail_value_diff(value, row, index){
//    debugger;
    var _class = ''
    if (row.value_difference_error)
        _class = 'error';
    return { classes: _class}
}


function style_id(value, row, index){
    var _class = '';

    if (row.all_validated == true){
        _class = 'validated';
    }
   // TODO check row.seleccionado translation
    else if (row.seleccionado == false){
        _class = 'error';
    }
    else{
        _class = '';
    }
    return { classes: _class}
}



function style_date(value, row, index){
    var _class = '';
    if (row.date_error > 0)
        _class = 'error';
    else
        _class = '';
    return { classes: _class}
}

function style_percentage(value, row, index) {
    if (row.percentage_error == true) {
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


function style_value(value, row, index, field){
    var _class = '';
    field_value = "suspicious_" + field +"s_count";

    if (row[field_value]>0 )
        _class = 'error';
    else
        _class = 'normal';
    return { classes: _class}
}


function style_value_diff(value, row, index){
    var _class = ''
    if (row.value_difference_error_count >= 1)
        _class = 'error';
    else
        _class = '';
    return { classes: _class}
}

function format_value(value, row, index, field){
    var span = '<span class="badge badge-light">num</span>';
    var content = value;
    var errors_field;
    if (["sum", "average", "value", "maximum", "minimum"].includes(field)){
        errors_field = "suspicious_" + field +"s_count";
    }else if (field == "value_difference_error_count"){
        errors_field = "value_difference_error_count";
        content = "";
    }else{
        errors_field = field +"_error";
    }

    if (row[errors_field]>0 ){
        span = span.replace('num',row[errors_field].toString());
        content = content + ' ' + span;
    }
    return content
}

function format_stddev_err(value, row, index, field){
    if (value){
        return "X";
    }
    return "-";
}






function footer_id(data){
//    debugger;
    var span = '<span class="badge badge-danger">num</span>';
    var num_date = data.reduce(function(num, i){
        // TODO check translation: seleccionado
        if (i['state'] && i['is_selected']==false)
            return num + 1;
        else
            return num;
    }, 0);

    span = span.replace('num',num_date.toString());

    return span;

}


function footer_date(data){
//    debugger;
    var span = '<span class="badge badge-danger">num</span>';
    var var_id = $("#id_variable").val();
    var dates = [];

    $.map(data, function(row){
        dates.push(row.date);
    });

    var sum = dates.unique().length;
    var num_date = data.reduce(function(num, i){
        if (i['date_error']>0)
            return num +1;
        else
            return num;
    }, 0);

    // TODO ask the team for prefferred behaviour
    span = span.replace('num', num_date.toString());

    return sum + ' of ' + indicators_daily['num_days'] + ' days ' + span;
}


// Obtener el promedio de los datos
function footer_average(data){
//    debugger;
    var field = this.field;
    var field_error = '';

    field_error = field + '_error';

    var span = '<span class="badge badge-danger">num</span>';
    var mean = 0;
    var sum = data.reduce(function (sum, i) {
          if (i['state'] && i[field] != null && i[field] != "")
            return sum + parseFloat(i[field])
        else
            return sum;
    }, 0);
    var data_count = data.reduce(function (sum, i) {
        if (i['state'] && i[field] != null && i[field] != "")
            return sum + 1;
        else
            return sum;
    }, 0);

    var num_value = data.reduce (function (num, i){
        if (i[field_error] && i['state'])
            return num + 1;
        else
            return num;
    }, 0);

    span = span.replace('num', num_value);

    if (isNaN(sum))
        mean = '-';
    else
        mean = (sum / data_count).toFixed(2);
    return mean + ' ' + span;
}




//obtener la suma de los datos
function footer_sum(data){
//    debugger;
    var field = this.field;
    var field_error = this.field + '_error';
    var span = '<span class="badge badge-danger">num</span>';
    var sum = data.reduce(function (sum, i) {
        if (i['state'] && i[field] != null && i[field] != "" ){
            return sum + parseFloat(i[field])
        }
        else{
            return sum
        }

    }, 0);
    var num_value = data.reduce (function (sum, i){
        if (i[field_error] && i['state'])
            return sum +1 ;
        else
            return sum;
    }, 0);

    span = span.replace('num', num_value);

    return sum.toFixed(2) + ' ' + span;
}


function footer_value_diff(data){
//    debugger;
    var span = '<span class="badge badge-danger">num</span>';
    var num_vd= data.reduce(function(num, i){
        if (i['value_difference_error_count'] >= 1 )
            return num + 1;
        else
            return num;
    }, 0);

    span = span.replace('num',num_vd);
    return span;
}



//total de datos
function footer_data_count(data){
//    debugger;
    var span = '<span class="badge badge-danger">num</span>';

    var sum = data.reduce(function (sum, i) {
//        debugger;
        if (i['state']){
            return sum + 1
        }
        else{
            return sum
        }

    }, 0);

    var num_date = data.reduce(function(num, i){
//        debugger;
        // TODO check logic
        if ( (i['time_lapse_status']==0) || (i['time_lapse_status']==2) || (i['time_lapse_status']==3))
            return num +1;
        else
            return num;
    }, 0);

    span = span.replace('num',num_date.toString());

    return sum + ' of ' + indicators_subhourly['num_data'] + '. ' + span;
}
// valores atípicos
function footer_stddev_err(data){
//    debugger;
    var span = '<span class="badge badge-danger">num</span>';
    var num_stddev = data.reduce(function(num, i){
        if (i['stddev_error'] && i['state'])
            return num +1;
        else
            return num;
    }, 0);

    span = span.replace('num',num_stddev.toString());

    return span;
}

function footer_detail_value_diff(data){
//    debugger;
    var span = '<span class="badge badge-danger">num</span>';
    var num_vde = data.reduce(function(num, i){
//        if (i['value_difference_error'] && i['is_selected'])
        if (i['value_difference_error'])
            return num + 1;
        else
            return num;
    }, 0);

    span = span.replace('num', num_vde.toString());

    return span;
}




/* Filtro de las Tablas */
function filtrar_diario(){
//    debugger;
    var fecha = $("#chk_fecha").val();
    var porcentaje = $("#chk_porcentaje").val();
    var numero = $("#chk_numero").val();

    var filtro_fecha = get_filtro_fecha(fecha);
    var filtro_porcentaje = get_filtro_porcentaje(porcentaje);
    var filtro_valor = get_filtro_valor(numero);

    var var_id = $("#id_variable").val();

    if (var_id == 10 || var_id == 11){
        $("#table_daily").bootstrapTable('filterBy', {
        fecha_error: filtro_fecha,
        porcentaje_error: filtro_porcentaje,
        nivel_error: filtro_valor,
        //estado:[true]
    });

    }
    else {
        $("#table_daily").bootstrapTable('filterBy', {
        fecha_error: filtro_fecha,
        porcentaje_error: filtro_porcentaje,
        valor_error: filtro_valor,
        //estado:[true]
    });

    }


}

function get_filter_time(time){
//    debugger;
    var filter_time = [];
    if (time == 'error')
        filter_time = ['0','2', '3'];
    else if (time == 'normal')
        filter_time = ['1'];
    else
        filter_time = ['0','1', '2', '3'];

    return filter_time
}

function get_filter_percentage(percentage){
//    debugger;
    var filter_percentage = [];

    if (percentage == 'error')
        filter_percentage = [true];
    else if (percentage == 'normal')
        filter_percentage = [false];
    else
        filter_percentage = [true, false];

    return filter_percentage
}

function get_filter_value(numero){
//    debugger;
    var filter_value = [];

    if (numero == 'error')
        filter_value = [true];
    else if (numero == 'normal')
        filter_value = [false];
    else
        filter_value = [true, false, null];

    return filter_value
}


function get_filter_stddev(filter){
    debugger;
    var filter_value = [];

    if (filter == 'error')
        filter_value = [true];
    else if (filter == 'normal')
        filter_value = [false];
    else
        filter_value = [true, false, null];

    return filter_value
}


function get_filter_state(numero){
//    debugger;
    var filter_value = [];

    if (numero == 'error')
        filter_value = [false];
    else if (numero == 'normal')
        filter_value = [true];
    else
        filter_value = [true, false];

    return filter_value
}


function get_filter_selected(option){
//    debugger;
    var filter_value = [];

    if (option == 'selected')
        filter_value = [true];
    else if (option == 'non-selected')
        filter_value = [false];
    else
        filter_value = [true, false];

    return filter_value
}


function get_filter_value_difference(option){
//    debugger;

    var filter = [];

    if (option == 'error')
        filter = [true];
    else if (option == 'normal')
        filter = [false];
    else
        filter = [true, false, null];

    return filter
}

function filter_detail_table(){
//    debugger;

    var time = $("#chk_detail_time").val();
    var value = $("#chk_detail_value").val();
    var stddev = $("#chk_detail_stddev").val();
    var selected = $("#chk_detail_selected").val();
    var value_difference = $("#chk_detail_value_difference").val();

    var filter_time = get_filter_time(time);
    var filter_value = get_filter_value(value);
    var filter_stddev = get_filter_stddev(stddev);
    var filter_selected = get_filter_selected(selected);
    var filter_value_difference = get_filter_value_difference(value_difference);

    $("#table_detail").bootstrapTable('filterBy',
    {
        stddev_error: filter_stddev,
        is_selected: filter_selected,
        value_difference_error: filter_value_difference,
    });
}


function clean_filters(type){
//    debugger;
    if (type == 'detail'){
        $("#chk_detail_time").prop('selectedIndex',0);
        $("#chk_detail_value").prop('selectedIndex',0);
        $("#chk_detail_stddev").prop('selectedIndex',0);
        $("#chk_detail_selected").prop('selectedIndex',0);
        $("#chk_detail_value_difference").prop('selectedIndex',0);
        $("#txt_detail_selection").val('');
    }
    else{
        // for daily filters
    }
}

function get_value_error(value){
//    debugger;
    var minimum = Number($("#id_minimum").val());
    var maximum = Number($("#id_maximum").val());
    var value_error = false;

    if (Number(value) > maximum || Number(value) < minimum )
    {
        value_error = true;
    }
    return value_error;
}


//function enable_new(){
//    var variable_id = $("#id_variable").val();
//
//    if ( variable_id != "11" || variable_id == "4" || variable_id == "5" )
//        $("#btn_detail_new").attr("disabled", false);
//    else
//        $("#btn_detail_new").attr("disabled", true);
//}

//function activar_espera(type){
////    debugger;
//    var type = type || ''
//    if (type !== '') {
//        var $div_data = $('#div_'+type);
//        var $div_loading = $('#div_loading_'+type);
//        var $div_message = $('#div_message_'+type)
//    }
//    else{
//        var $div_data = $('#div_information');
//        var $div_loading = $('#div_loading');
//        var $div_message = $('#div_error')
//
//    }
//    $div_loading.show();
//    $div_data.hide();
//    $div_message.hide();
//    $("#div_information").hide();
//}

//función para quitar duplicados
Array.prototype.unique=function(a){
  return function(){return this.filter(a)}}(function(a,b,c){return c.indexOf(a,b+1)<0
});

//
//function show_message(type){
////    debugger;
//    /*var message = '<div class="alert alert-danger alert-dismissible" role="alert">';
//    message += 'Ocurrio un problema con el procesamiento de la información, por favor intentelo nuevamente';
//    message += '</div>'*/
//
//    var type = type || ''
//    if (type !== ''){
//        var $div_data = $('#div_'+type);
//        var $div_loading = $('#div_loading_'+type);
//        var $div_message = $('#div_message_'+type)
//    }
//    else{
//        var $div_data = $('#div_information');
//        var $div_loading = $('#div_loading');
//        var $div_message = $('#div_error');
//
//    }
//
//    $div_loading.hide();
//    $div_data.hide();
//    //$div_message.html(message);
//    $div_message.show();
//
//}

//function desactivar_espera(type){
////    debugger;
//    var type = type || ''
//    if (type !== '') {
//        var $div_data = $('#div_'+type);
//        var $div_loading = $('#div_loading_'+type);
//        var $div_message = $('#div_message_'+type);
//        var $resize_plot = $('#resize_plot'+type);
//    }
//    else{
//        var $div_data = $('#div_information');
//        var $div_loading = $('#div_loading');
//        var $div_message = $('#div_error');
//        var $resize_plot = $('#resize_plot');
//
//    }
//    $div_loading.hide();
//    $div_data.show();
//    $div_message.hide();
//    $resize_plot.show();
//    $("#div_information").show();
//}
