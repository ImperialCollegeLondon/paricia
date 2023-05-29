function generate_traces(data, source_type, color){
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

function bar_plot(data, append_to, variable){

}

function dispersion_plot(series, append_to, variable){
    var data_array = [];

    let measurement = generate_traces(series.measurement, "Measurement", 'rgb(0, 0, 0)');
    data_array.push(...measurement);
    let validated = generate_traces(series.validated, "Validated", 'rgb(0, 0, 255)');
    data_array.push(...validated);
    let selected = generate_traces(series.selected, "Selected", 'rgb(0, 255, 0)');
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
var data_fecha = [];
var data_valor = [];
var data_maximo = [];
var data_minimo = [];
//var num_dias = 0;
var num_datos = 0;

var indicators_subhourly = {
//    num_fecha: 0,
//    num_valor: 0,
//    num_maximo: 0,
//    num_minimo:0,
//    num_stddev: 0,
//    num_datos:0
    num_time: 0,
    num_value: 0,
    num_maximum: 0,
    num_minimum:0,
    num_stddev: 0,
    // TODO check if renaming num_data is needed
    num_data:0
}

var indicators_daily = {
//    num_fecha: 0,
//    num_porcentaje: 0,
//    num_valor: 0,
//    num_maximo: 0,
//    num_minimo: 0,
//    num_dias: 0
    num_date: 0,
    num_percentage: 0,
    num_value: 0,
    num_maximum: 0,
    num_minimum: 0,
    num_days: 0
}

var num_fecha = 0;


$(document).ready(function() {

    $("#btn_detail_new").attr("disabled", true);

//    $('#div_grafico').on('hidden.bs.collapse', function () {
//        $("#btn_grafico").text("Mostrar Gráfico");
//    });
//    $('#div_grafico').on('show.bs.collapse', function () {
//        $("#btn_grafico").text("Ocultar Gráfico");
//    });

    $("#btn_submit").click(daily_query_submit);

    //consultar los periodos de validacion
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

//    $("#chk_fecha_crudo").change(filtrar_crudo);
//    $("#chk_valor_crudo").change(filtrar_crudo);
//    $("#chk_stddev").change(filtrar_crudo);
//    $("#chk_fila").change(filtrar_crudo);
//    $("#chk_varcon").change(filtrar_crudo);
    $("#chk_detail_time").change(filtrar_crudo);
    $("#chk_detail_value").change(filtrar_crudo);
    $("#chk_detail_stddev").change(filtrar_crudo);
    $("#chk_detail_row").change(filtrar_crudo);
    $("#chk_detail_value_difference").change(filtrar_crudo);

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

//    $btn_nuevo_promedio.click(nuevo_registro);
//    $btn_nuevo_acumulado.click(nuevo_registro);
//    $btn_modificar_acumulado.click(modificar);
//    $btn_modificar_promedio.click(modificar);
//    $btn_modificar_agua.click(modificar);
//    $btn_guardar.click(guardar_crudos);
//    $btn_graficar.click(graficar);
//    $btn_detail_plot.click(graficar);
//    $btn_delete_valor.click(eliminar_crudo);


    $btn_detail_select.click(marcar);
    $btn_detail_unselect.click(desmarcar);
    $btn_detail_new.click(abrir_formulario_nuevo);
    $btn_detail_delete.click(eliminar);
    $btn_detail_undo.click(mostrar);
});

//consultar el historial de validacion
function periodos_validacion(event){
    fecha_inicio = $("input[name='inicio']").val();
    fecha_fin = $("input[name='fin']").val();
    if (fecha_inicio == '' && fecha_fin == '')
        {
            token = $("input[name='csrfmiddlewaretoken']").val();
            estacion_id = $("#id_estacion").val();
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
        
                    mostrar_mensaje("historial");
        
                }
            });
        }
        else {
            token = $("input[name='csrfmiddlewaretoken']").val();
            estacion_id = $("#id_estacion").val();
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
        
                    mostrar_mensaje("historial");
        
                }
            });
        }
   

}

// pasar los datos crudos a validados

function save_daily(event){
    var $table_daily = $('#table_daily');
    var $table_detail = $('#table_detail');
    //$table.css("background-color","white");
    token = $("input[name='csrfmiddlewaretoken']").val();
    station_id = $("#id_station").val();
    variable_id = $("#id_variable").val();
    maximum = $("#id_maximum").val();
    minimum = $("#id_minimum").val();
    start_date = $("input[name='start_date']").val();
    end_date = $("input[name='end_date']").val();

    changes = JSON.stringify($table_daily.bootstrapTable('getData',{unfiltered:true, includeHiddenRows: true}));

    $.ajax({
        url: '/validated/guardarvalidados/',
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
                $("#div_body_mensaje").html('Data saved correctly to Validated!')
                $("#div_mensaje_validacion").modal("show");
                $("#resize_plot").hide();
                $("#div_informacion").hide();
                clean_filters('daily');
                clean_filters('detail');
                $table_detail.bootstrapTable('removeAll');
                $table_daily.bootstrapTable('removeAll');
            }
            else{
                $("#div_body_mensaje").html('Ocurrio un problema con la validación por favor contacte con el administrador')
                $("#div_mensaje_validacion").modal("show");
            }
            $table_daily.bootstrapTable('hideLoading');
            $table_detail.bootstrapTable('hideLoading');
        },
        error: function () {
            $("#div_body_mensaje").html('Ocurrio un problema con la validación por favor contacte con el administrador')
            $("#div_mensaje_validacion").modal("show");
            $table_daily.bootstrapTable('hideLoading');
        }
    });

}

//eliminar datos validados de la base de datos

function eliminar_validados(event){
//    debugger;
    var $table = $('#table_daily');
    var $table_crudo = $('#table_crudo');
    //$table.css("background-color","white");
    token = $("input[name='csrfmiddlewaretoken']").val();
    estacion_id = $("#id_estacion").val();
    variable_id = $("#id_variable").val();
    //comentario_general = $("textarea[name='comentario_general']").val();
    cambios = JSON.stringify($table.bootstrapTable('getData',{unfiltered:true, includeHiddenRows: true}));


    $.ajax({
        url: '/val2/eliminarvalidados/',
        data: {
            'csrfmiddlewaretoken': token,
            'estacion_id': estacion_id,
            'variable_id': variable_id,
            'cambios': cambios
        },
        type:'POST',
        beforeSend: function () {
            //$table.bootstrapTable('showLoading');

        },
        success: function (data) {
            if (data.resultado == true){
                //$("#div_body_mensaje").html('Datos Guardados')
                //$("#div_mensaje_validacion").modal("show");

                clean_filters('daily');
                clean_filters('detail');
                //$table_crudo.bootstrapTable('removeAll');
                //$table.bootstrapTable('removeAll');
                daily_query_submit();


            }
            else{
                $("#div_body_mensaje").html('Ocurrio un problema con la validación por favor contacte con el administrador')
                $("#div_mensaje_validacion").modal("show");

            }
            $table.bootstrapTable('hideLoading');
            $table_crudo.bootstrapTable('hideLoading');


        },
        error: function () {
            $("#div_body_mensaje").html('Ocurrio un problema con la validación por favor contacte con el administrador')
            $("#div_mensaje_validacion").modal("show");
            $table.bootstrapTable('hideLoading');
        }
    });

}

// guardar los cambios en los datos crudos
function guardar_crudos(event){
//    debugger;
//    var $table = $('#table_crudo');
//    //$table.css("background-color","white");
//    token = $("input[name='csrfmiddlewaretoken']").val();
//    estacion_id = $("#id_station").val();
//    variable_id = $("#id_variable").val();
//    fecha_inicio = $("input[name='start_date']").val();
//    fecha_fin = $("input[name='end_date']").val();
//    //comentario_general = $("textarea[name='comentario_general']").val();
//    cambios = JSON.stringify($table.bootstrapTable('getData',{unfiltered:true}));
//    //console.log($table.bootstrapTable('getData',{unfiltered:true, }))
//    //detalle_crudos();
    document.getElementById("tab3-tab").style.display = "none";
    var $table = $('#table_crudo');
    token = $("input[name='csrfmiddlewaretoken']").val();
    station_id = $("#id_station").val();
    variable_id = $("#id_variable").val();
    start_date = $("input[name='start_date']").val();
    end_date = $("input[name='end_date']").val();
    data = JSON.stringify($table.bootstrapTable('getData',{unfiltered:true}));

    $.ajax({
        url: '/validated/guardarcrudos/',
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
                $("#div_body_mensaje").html('Datos Guardados')
                $("#div_mensaje_validacion").modal("show");
                detalle_crudos();
                modificar_fila();
                clean_filters('detail');
            }
            else{
                $("#div_body_mensaje").html('Ocurrio un problema con la validación por favor contacte con el administrador')
                $("#div_mensaje_validacion").modal("show");
                $table.bootstrapTable('hideLoading');
            }
        },
        error: function () {
            $("#div_body_mensaje").html('Ocurrio un problema con la validación por favor contacte con el administrador')
            $("#div_mensaje_validacion").modal("show");
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
    var mensaje = '';
    $("#orig_variable_id").val(var_id);
    $("#div_informacion").html('')
//    $("#resize_plot").hide();
    clean_filters('daily');
    clean_filters('detail');
    //$("#table_crudo").bootstrapTable('removeAll');
    debugger;
    start_date = document.querySelector('input[name="start_date"]').value;
    end_date = document.querySelector('input[name="end_date"]').value;
    if( start_date == '' || end_date == '')
    {
        $("#div_message_fechas").show("slow");
        $("#div_c").html("");
    }
    else {
        $("#div_message_fechas").hide();
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
                        mensaje = data.error;
                    }
                }
                if (flag_error == false){
                    if (data.plot_data.length < 1){
                        $("#div_informacion").show("slow");
                        $("#div_informacion").html('<div><h1 style="background-color : red">No hay datos</h1></div>');
                    }
                    else {
                        $("#div_c").html(data.curva);

                        if (data.variable[0].is_cumulative){
                            bar_plot(data.series, "#div_informacion", data.variable[0]);
                        }else{
                            dispersion_plot(data.series, "div_informacion", data.variable[0]);
                        }


                        enable_new();
                        var_id = data.variable[0]['id'];
                        variable = data.variable[0];
                        station = data.station[0];
//                        json_data = data.datos;
                        json_data = data.data
                        //num_dias = data.indicadores[0]['num_dias'];
                        $table_daily.bootstrapTable('destroy');
                        for (const index in data.indicators[0]){
                            indicators_daily[index]= data.indicators[0][index];
                        }
//                        debugger;
                        var columns = get_columns_daily(var_id, data.indicators[0]);
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
                    }
                    
    
                }
                else{
                    $table_daily.bootstrapTable('hideLoading');
//                    $("#resize_plot").hide();
                    $("#div_body_mensaje").html(mensaje)
                    $("#div_mensaje_validacion").modal("show");
    
                }
    
            },
            error: function () {
//                debugger;
                $table_daily.bootstrapTable('hideLoading');
                $("#div_body_mensaje").html('Ocurrio un problema con la validación por favor contacte con el administrador')
                $("#div_mensaje_validacion").modal("show");
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
function modificar_fila(){
    var $table = $('#table_crudo');
    //$table.css("background-color","white");
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

    var num_fecha = 0;

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
                num_fecha += 1;

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
                porcentaje: porcentaje, porcentaje_error: porcentaje_error, fecha_numero: num_fecha,
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
                porcentaje: porcentaje, porcentaje_error: porcentaje_error, fecha_numero: num_fecha,
                nivel_error: num_nivel > 0 ? true : false
            }
        });
    }
    else {
        $table_daily.bootstrapTable('updateByUniqueId', {
            id: id_diario,
            row: {valor: suma_valor.toFixed(2), validado: true, valor_numero: num_valor, porcentaje: porcentaje,
                porcentaje_error: porcentaje_error, fecha_numero: num_fecha,
                valor_error: num_valor > 0 ? true : false
            }
        });
    }


}



// Graficar los datos crudos o diarios de la estacion
function graficar(event){
    var name = event.currentTarget.name;
    if (name === 'crudo')
        $table = $("#table_crudo");
    else
        $table = $("#table_daily");

    var data_fecha = [];
    var data_valor = [];
    var data_maximo = [];
    var data_minimo = [];
    var data_historica = [];
    var data_error_fecha = [];
    var data_error_valor = [];
    var data_porcentaje_fecha = [];
    var data_porcentaje_error = [];
    var data_direccion =[];
    var data_nivel =[];
    var data_caudal =[];


    var var_id = $("#id_variable").val();
    var var_nombre = $('#id_variable option:selected').text();
    var est_nombre = $('#id_estacion option:selected').text();

    var datos = $table.bootstrapTable('getData',{unfiltered:true});
    var width_graph = $(".container").width();

    var data = [];
    var layout =  {};


    $.each(datos, function(i, item) {
        if (item.estado){
            data_fecha.push(item.fecha);

            if (var_id == 1){
                data_valor.push(item.valor);
                data_historica.push(item.media_historica)
            }
            else if ((var_id == 4) || (var_id == 5)){
                data_valor.push(item.valor);
                data_direccion.push(item.direccion)
            }
            /*else if( var_id == 10 || var_id == 11){
                data_nivel.push(item.nivel);
                data_caudal.push(item.caudal);
            }*/
            else{
                data_valor.push(item.valor);
                data_maximo.push(item.maximo);
                data_minimo.push(item.minimo);
            }

            if(item.fecha_error==2){
                console.log("fecha error")
                data_valor.push(null);
                data_fecha.push(null);
                if (var_id != 1){
                    data_maximo.push(null);
                    data_minimo.push(null);
                }
            }

            if (item.valor_error){
                data_error_fecha.push(item.fecha);
                data_error_valor.push(item.valor)
            }

            if ((name == 'diario') && (item.porcentaje_error)){
                data_porcentaje_fecha.push(item.fecha);
                data_porcentaje_error.push(item.valor);

            }

        }
        else{
            data_fecha.push(null);
            data_valor.push(null);
            if (var_id != 1){
                data_maximo.push(null);
                data_minimo.push(null);
            }
        }
    });

    var error_valor = {
        type: 'scatter',
        x: data_error_fecha,
        y: data_error_valor,
        mode: 'markers',
        name: 'Errores',
        showlegend: true,
        marker: {
            color: '#dc3545',
            line: {width: 3},
            //opacity: 0.5,
            size: 12,
            symbol: 'circle-open'
        }
    }


    var error_porcentaje = {
        type: 'scatter',
        x: data_porcentaje_fecha,
        y: data_porcentaje_error,
        mode: 'markers',
        name: '% bajos',
        showlegend: true,
        marker: {
            color: '#ffc107',
            line: {width: 3},
            //opacity: 0.5,
            size: 12,
            symbol: 'circle-open'
        }
    }

    if (var_id == 1){
        var trace1 = {
            x:data_fecha,
            y:data_valor,
            name: 'Valor',
            type: 'bar'
        };
        var trace2 = {
            x:data_fecha,
            y:data_historica,
            name: 'Media Histórica',
            type: 'bar'
        };
        data = [trace1, trace2, error_valor, error_porcentaje];
    }
    else if ((var_id == 4) || (var_id == 5)){
        var trace1 =  {
            name: "Valores",
            type: "scatterpolargl",
            //type: "barpolar",
            r: data_valor,
            theta: data_direccion,
            thetaunit: 'degrees',
            mode: "markers",
            marker: {
                color: "rgb(217,95,2)",
                size: 10,
                line: {
                  color: "white"
                },
                //opacity: 0.10
            },
            cliponaxis: false
        };
        data = [trace1];



    }
    /*else if (var_id == 10 || var_id == 11){
        console.log(data_nivel, data_caudal);
        var trace_nivel = {
            x:data_fecha,
            y:data_nivel,
            name: 'Nivel de Agua',
            type: 'scatter'
        };
        var trace_caudal = {
            x:data_fecha,
            y:data_caudal,
            name: 'Caudal',
            yaxis: 'y2',
            type: 'scatter'
        };
        data = [trace_nivel, trace_caudal];
    }*/
    else{
        var trace1 = {
            x:data_fecha,
            y:data_valor,
            name: 'Valor',
            type: 'scatter'
        };
        var trace2 = {
            x:data_fecha,
            y:data_maximo,
            name: 'Maximo',
            type: 'scatter'
        };
        var trace3 = {
            x:data_fecha,
            y:data_minimo,
            name: 'Minimo',
            type: 'scatter'
        };
        data = [trace1, trace2, trace3, error_valor];
    }

    if ((var_id == 4) || (var_id == 5)){

        layout = {
            title: var_nombre + ' - '+ est_nombre,
            showlegend: true,
            polar: {
                bgcolor: "rgb(233, 233, 233)",

                angularaxis: {
                    tickwidth: 2,
                    linewidth: 3,
                    direction: 'clockwise',
                },
                radialaxis: {
                    side: "counterclockwise",
                    showline: true,
                    linewidth: 2,
                    tickwidth: 2,
                    gridcolor: "#FFF",
                    gridwidth: 2
                },
            },
            paper_bgcolor: "rgb(255, 255, 255)",
            width: width_graph-40,

        }

    }
    /*else if (var_id == 10 || var_id == 11){
        layout = {
            title: 'Caudal y Nivel' + ' - '+ est_nombre,
            yaxis: {title: 'Nivel de Agua (cm)'},
            yaxis2: {
                title: 'Caudal (l/s)',
                overlaying: 'y',
                side: 'right'
            },
            width: width_graph-40,
            //showlegend: false
        };

    }*/
    else{
        layout = {
            title: var_nombre + ' - '+ est_nombre,
            width: width_graph-40,
            //showlegend: false
        };

    }


    Plotly.newPlot('div_grafico', data, layout);
    // renombrar angular axis
        var angulo_index = 0;
        var angulo_dict = {1:'N', 2:'NE', 3:'E', 4:'SE', 5:'S', 6:'SO', 7:'O', 8:'NO'};
        $("g.polarsublayer").find("g.angularaxistick").each(function(){
            angulo_index++;
            $(this).find("text").html(angulo_dict[angulo_index]);
        });

    $("#div_modal_grafico").modal("show");

}

//Deshacer los cambios realizados en la tabla crudos/diarios
function mostrar(event){

    var name = event.currentTarget.name;
    if (name === 'crudo')
        $table = $("#table_crudo");
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
//    debugger;
    $(this).attr('disabled',true);
    var name = event.currentTarget.name;
    console.log(name)
    if (name === 'crudo')
        $table = $("#table_crudo");
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
function desvalidar_datos(event){
//    debugger;
    $(this).attr('disabled',true);
    var name = event.currentTarget.name;
    console.log(name)
    if (name === 'crudo')
        $table = $("#table_crudo");
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
function nuevo_registro(event){
//    debugger;
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
    var table = $table = $("#table_crudo");

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
        data['valor_error'] = get_valor_error(data['valor']);
    }
    else{
        data['nivel_error'] = get_valor_error(data['nivel']);
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
//    debugger;
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
function modificar(event){
//    debugger;
    $('input[name="fecha"]').attr('disabled',false);
    var variable_id = parseInt($("#id_variable").val());
    var name = event.currentTarget.name;
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
    data['estado'] = true;
    if (variable_id == 10 || variable_id == 11){
        data['nivel_error'] = get_valor_error(data['nivel']);
    }
    else{
        data['valor_error'] = get_valor_error(data['valor']);
    }


    if (variable_id != 1 && variable_id != 10 && variable_id != 11){
        data['maximo_error'] = get_valor_error(data['maximo']);
        data['minimo_error'] = get_valor_error(data['minimo']);
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
//    debugger;
    var name = event.currentTarget.name;
    var cadena = '';
    var $table = '';

    if (name === 'crudo'){
        $table = $("#table_crudo");
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
//    debugger;
    var $table = '';
    var name = event.currentTarget.name;
    if (name ==='crudo')
        $table = $("#table_crudo");
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
function detalle_crudos(e, value, row){
//    debugger;
    var $table = $('#table_crudo');
    var station_id = $("#id_station").val();
    var variable_id = $("#id_variable").val();

    var id_diario = 0;
//    var fecha = '';
    var date = '';

    var estado = row || false

    if (estado == false ){
        id_diario = $("#orig_id_diario").val();
//        fecha = $("#orig_fecha_diario").val();
        date = $("#orig_fecha_diario").val();
    }
    else{
//        id_diario = row.id;
//        fecha = row.fecha;
//        $("#orig_id_diario").val(id_diario);
//        $("#orig_fecha_diario").val(fecha);
        id_diario = row.id;
        date = row.date;
        $("#orig_id_diario").val(id_diario);
        $("#orig_fecha_diario").val(date);
    }

    var var_maximo = $("#id_maximum").val();
    var var_minimo = $("#id_minimum").val();


//    enlace = '/validated/lista/' + station_id + '/' + variable_id + '/' + fecha + '/' + var_minimo + '/' + var_maximo;
    enlace = '/validated/lista/' + station_id + '/' + variable_id + '/' + date + '/' + var_minimo + '/' + var_maximo;

    $.ajax({
        url: enlace,
        type:'GET',
        beforeSend: function () {
            $table.bootstrapTable('showLoading');
        },
        success: function (data) {
            document.getElementById("tab3-tab").style.display = "block";
            document.getElementById("tab3-tab").click();
            json_data = data.series;
            $table.bootstrapTable('destroy');
            for (const index in data.indicators[0]){
                indicators_subhourly[index] = data.indicators[0][index];
                $("#span_"+index+"_crudo").text(indicators_subhourly[index]);
            }


            /* this is an example for new snippet extension make by me xD */
            for (const element of json_data) {
                element["time"] = (element['time']).replace('T',' ');
            }

            var columns = get_column_validado(variable_id, data.indicators[0]);
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
            $("#div_body_mensaje").html('Ocurrio un problema con la validación por favor contacte con el administrador')
            $("#div_mensaje_validacion").modal("show");

            $table.bootstrapTable('hideLoading');
        }
    });

};

//funcion para eliminar una fila de la tabla diario
function eliminar_diario(e, value, row, index){
//    debugger;
    console.log(row);
    var $table = $('#table_daily');
    $table.bootstrapTable('updateRow', {
        index: index,
        row: {
            estado: false
        }
    });
    $table.bootstrapTable('uncheckBy', {field: 'id', values: ids});

    /*$table.bootstrapTable('hideRow', {
        index: index
    })*/
}
//funcion para abrir el formulario de eliminar
function abrir_form_eliminar(e, value, row, index){
//    debugger;
    var $form_modal = $('#modal_eliminar');
    var inputs = $("#form_eliminar").serializeArray();
    $.each(inputs, function(i, field){
        $('input[name="'+field.name+'"]').val(row[field.name]);
    });
    $form_modal.modal("show");
}

//funcion para eliminar una fila de la tabla crudos
function eliminar_crudo(event){
//    debugger;
    //console.log("row", row);
    var inputs = $("#form_eliminar").serializeArray();
    var $form_modal = $('#modal_eliminar');
    var table = $table = $("#table_crudo");
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

function abrir_formulario_nuevo(event){
//    debugger;
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
function abrir_formulario(e, value, row, index){
//    debugger;
    var variable_id = parseInt( $("#id_variable").val());


    if (variable_id === 1){
        var $form_modal = $('#modal_acumulado');
        var inputs = $("#form_acumulado").serializeArray();

    }
    else if(variable_id == 10 || variable_id == 11){
        var $form_modal = $('#modal_agua');

        var inputs = $("#form_agua").serializeArray();
    }
    else{
        var $form_modal = $('#modal_promedio');
        var inputs = $("#form_promedio").serializeArray();
    }

    $.each(inputs, function(i, field){
        $('input[name="'+field.name+'"]').val(row[field.name]);
    });

    $('input[name="fecha"]').attr('disabled',true);
    $form_modal.modal("show");
}


//Generar las columnas de la tabla de datos diarios
function get_columns_daily(var_id){

    var span = '<span class="badge badge-danger">num</span>';

    var columns = [];

    var state = {
        field:'state',
        checkbox:true
    };

    var id = {
        field:'id',
        title:'Id',
        cellStyle: style_id
    };

//    var fecha = {
//        field:'fecha',
//        title: 'Fecha',
//        cellStyle: style_fecha,
//        formatter: format_valor,
//        footerFormatter: total_filas,
//        //filterControl: 'datepicker'
//    };
    var date = {
        field:'date',
        title: 'Date',
        cellStyle: style_date,
        formatter: format_value,
        footerFormatter: total_filas,
        //filterControl: 'datepicker'
    };


//    var porcentaje = {
//        field:'porcentaje',
//        title:'Porcentaje ',
//        cellStyle: style_porcentaje,
//        footerFormatter: footer_promedio,
//        //filterControl: 'input'
//    };
    var percentage = {
        field:'percentage',
        title:'Percnt.',
        cellStyle: style_percentage,
        footerFormatter: footer_promedio,
        //filterControl: 'input'
    };

//    var accion = {
//        field: 'accion',
//        title: 'Acción',
//        formatter: operate_table_daily,
//        events: {
//           'click .search': detalle_crudos,
//           'click .delete': eliminar_diario,
//           //'click .update': abrir_formulario
//
//        }
//    };
    var action = {
        field: 'action',
        title: 'Action',
        formatter: operate_table_daily,
        events: {
           'click .search': detalle_crudos,
           'click .delete': eliminar_diario,
           //'click .update': abrir_formulario

        }
    };

//    var n_valor = {
//        field:'n_valor',
//        title:'Variación Consecutiva',
//        cellStyle: style_var_con,
//        footerFormatter: footer_variaConse_cont
//    };
    var n_value = {
        field:'n_value',
        title:'Diff. Err',
        cellStyle: style_var_con,
        footerFormatter: footer_variaConse_cont
    };

    columns.push(state);
    columns.push(id);
    columns.push(date);
    columns.push(percentage);



    if (var_id == 1) {
        var value = {
            field:'value',
            title:'Value ',
            cellStyle: style_value,
            formatter: format_value,
            footerFormatter: footer_suma
        };
        columns.push(value);
        columns.push(n_value);
    }
    else if ((var_id == 4) || (var_id == 5)){

        var value = {
            field:'value',
            title:'Value ',
            cellStyle: style_value,
            //formatter: format_valor,
            footerFormatter: footer_promedio
        };

        var maximum = {
            field:'maximum',
            title:'Maximum ',
            visible: false,
            cellStyle: style_value,
            //formatter: format_valor,
            footerFormatter: footer_promedio
        };

        var minimum= {
            field:'minimum',
            title:'Minimum ',
            visible: false,
            cellStyle: style_value,
            //formatter: format_valor,
            footerFormatter: footer_promedio
        }
        var direccion = {
            field:'direccion',
            title:'Dirección',
            //cellStyle: style_valor,
            //footerFormatter: footer_promedio
        };
        var punto_cardinal = {
            field:'categoria',
            title:'Punto Cardinal',
            //cellStyle: style_valor,
            formatter: format_punto_cardinal,
            //footerFormatter: footer_promedio
        };
        columns.push(value);
        columns.push(maximum);
        columns.push(minimum);
        columns.push(direccion);
        columns.push(punto_cardinal);

    }

    else{
        var value = {
            field:'avg_value',
            title : 'Avg. Val.',
            cellStyle: style_value,
            formatter: format_value,
            footerFormatter: footer_promedio
        };
        var maximum = {
            field:'max_maximum',
            title:'Max. of Maxs. ',
            cellStyle: style_value,
            formatter: format_value,
            footerFormatter: footer_promedio
        };

        var minimum= {
            field:'min_minimum',
            title:'Min. of Mins.',
            cellStyle: style_value,
            formatter: format_value,
            footerFormatter: footer_promedio
        }
        columns.push(value);
        columns.push(maximum);
        columns.push(minimum);
        columns.push(n_value);
    }

    columns.push(action);

    return columns

}

//generar las columnas para la tabla de datos crudos
function get_column_validado(var_id){
    debugger;
    var columns = [];

    var span = '<span id="span_id" class="badge badge-danger">num</span>';

    var state = {
        field:'state',
        checkbox:true
    };

    var id = {
        field:'id',
        title:'Id',
        cellStyle: style_id,
        footerFormatter: footer_id
    };

//    var fecha = {
//        field:'fecha',
//        title:'Fecha',
//        cellStyle: style_date,
//        footerFormatter: total_datos
//    };
    var time = {
        field:'time',
        title:'Time',
        cellStyle: style_date,
        footerFormatter: total_datos
    };

//    var valor_atipico = {
//        field:'',
//        title:'Valores Atípicos',
//        cellStyle: style_stddev,
//        footerFormatter: footer_stddev
//    };
    var outlier = {
        field:'',
        title:'Outliers',
        cellStyle: style_stddev,
        footerFormatter: footer_stddev
    };

//    var comentario = {
//        field:'comentario',
//        title:'Comentario'
//    };
    var comment = {
        field:'comment',
        title:'Comment'
    };



//    var n_valor = {
//        field:'n_valor',
//        title:'Variación Consecutiva',
//        cellStyle: style_varia_error,
//        footerFormatter: footer_variaConse
//    };
    var n_value = {
        field:'value_difference',
        title:'Value difference',
        cellStyle: style_varia_error,
        footerFormatter: footer_variaConse
    };

    var n_value_error = {
        field:'value_difference_error',
        title:'Val diff err',
        visible: false,
    };

//    var accion = {
//        field: 'accion',
//        title: 'Acción',
//        formatter: operate_table_crudo,
//        events: {
//           'click .delete_crudo': abrir_form_eliminar,
//           'click .update': abrir_formulario
//
//        }
//    };
    var action = {
        field: 'action',
        title: 'Action',
        formatter: operate_table_crudo,
        events: {
           'click .delete_crudo': abrir_form_eliminar,
           'click .update': abrir_formulario

        }
    };

    columns.push(state);
    columns.push(id);
    columns.push(time);
    
    if (var_id =='1'){


//        var valor = {
//            field:'valor',
//            title: 'Valor',
//            cellStyle: style_error_crudo,
//            footerFormatter: footer_suma
//        };
        var value = {
            field:'value',
            title: 'Value',
            cellStyle: style_error_crudo,
            footerFormatter: footer_suma
        };
        columns.push(value);

    }
    else if ( (var_id == '4') || ( var_id == '5') ){
//        var valor = {
//            field:'valor',
//            title:'Valor ',
//            cellStyle: style_valor,
//            //formatter: format_valor,
//            footerFormatter: footer_promedio
//        };
        var value = {
            field:'value',
            title:'Value ',
            cellStyle: style_valor,
            //formatter: format_valor,
            footerFormatter: footer_promedio
        };


//        var maximo = {
//            field:'maximo',
//            title: 'Máximo',
//            visible: false,
//            cellStyle: style_error_crudo,
//            footerFormatter: footer_promedio
//        };
        var maximum = {
            field:'maximum',
            title: 'Maximum',
            visible: false,
            cellStyle: style_error_crudo,
            footerFormatter: footer_promedio
        };

//        var minimo = {
//            field:'minimo',
//            title: 'Mínimo',
//            visible: false,
//            cellStyle: style_error_crudo,
//            footerFormatter: footer_promedio
//        };
        var minimum = {
            field:'minimum',
            title: 'Minimum',
            visible: false,
            cellStyle: style_error_crudo,
            footerFormatter: footer_promedio
        };


        var punto_cardinal = {
            field:'categoria',
            title:'Punto Cardinal ',
            //cellStyle: style_valor,
            formatter: format_punto_cardinal,
            //footerFormatter: footer_promedio
        };

        var direccion = {
            field:'direccion',
            title:'Dirección',
            //cellStyle: style_valor,
            //footerFormatter: footer_promedio
        };
        columns.push(value);
        columns.push(maximum);
        columns.push(minimum);
        columns.push(direccion);
        columns.push(punto_cardinal);
    }
    else{
//        var valor = {
//            field:'valor',
//            title:'Valor',
//            cellStyle: style_error_crudo,
//            footerFormatter: footer_promedio
//        };
        var value = {
            field:'value',
            title:'Value',
            cellStyle: style_error_crudo,
            footerFormatter: footer_promedio
        };

//        var maximo = {
//            field:'maximo',
//            title: 'Máximo',
//            cellStyle: style_error_crudo,
//            footerFormatter: footer_promedio
//        };
        var maximum = {
            field:'maximum',
            title: 'Maximum',
            cellStyle: style_error_crudo,
            footerFormatter: footer_promedio
        };

//        var minimo = {
//            field:'minimo',
//            title: 'Mínimo',
//            cellStyle: style_error_crudo,
//            footerFormatter: footer_promedio
//        };
        var minimum = {
            field:'minimum',
            title: 'Minimum',
            cellStyle: style_error_crudo,
            footerFormatter: footer_promedio
        };
        columns.push(value);
        columns.push(maximum);
        columns.push(minimum);

    }
    columns.push(outlier);
    columns.push(comment);
    columns.push(n_value);
    columns.push(n_value_error);
    columns.push(action);
    return columns
}

//Función para generar los iconos de acción de la tabla diario
function operate_table_daily(value, row, index) {
//    debugger;
    return [
      '<a class="search" href="javascript:void(0)" title="Detalle">',
      '<i class="fa fa-search"></i>',
      '</a>  ',
      '<a class="delete" href="javascript:void(0)" title="Eliminar">',
      '<i class="fa fa-trash"></i>',
      '</a>  ',
    ].join('')
}

//Función para generar los iconos de acción de la tabla crudos
function operate_table_crudo(value, row, index) {
//    debugger;
    return [
      '<a class="delete_crudo" href="javascript:void(0)" title="Eliminar">',
      '<i class="fa fa-trash"></i>',
      '</a>  ',
      '<a class="update" href="javascript:void(0)" title="Modificar">',
      '<i class="fa fa-edit"></i>',
      '</a>  ',
    ].join('')
}
/*Formatos para las tablas crudos/diario*/
// Formato para el porcentaje de datos diarios
//function style_porcentaje(value, row, index) {
////    debugger;
//    var clase = ''
//    if (row.porcentaje_error == true) {
//        return {
//            classes: 'error'
//        }
//    }
//    else{
//        return {
//            classes: 'normal'
//        }
//    }
//
//}

function style_percentage(value, row, index) {
//    debugger;
//    var class = '';
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




//Formato para el valor, maximo, minimo de la tabla crudos/diarios
//function style_fila(row, index){
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


//function style_valor(value, row, index, field){
function style_value(value, row, index, field){

    var _class = '';
    field_numero = "suspicious_" + field.split("_")[1] +"s_count";

    // TODO maybe limite_superior could be removed
    limite_superior = $('#id_limite_superior').val();
    if (row[field_numero]>0 )
        _class = 'error';
    else
        _class = 'normal';
    return { classes: _class}
}


//Formato para el error de la tabla crudos/diarios
function style_error_crudo(value, row, index, field){
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
function style_stddev(value, row, index){
//    debugger;
    var clase = ''
    if (row.stddev_error === true)
        clase = 'error';
    else
        clase = '';
    return { classes: clase}
}
function style_var_con(value, row, index){
//    debugger;
    var clase = ''
    if (row.c_varia_err >= 1)
        clase = 'error';
    else
        clase = '';
    return { classes: clase}
}
//function style_varia_error(value, row, index){
////    debugger;
//    var clase = ''
//    if (row.varia_error === true)
//        clase = 'error';
//    else
//        clase = '';
//    return { classes: clase}
//}
function style_varia_error(value, row, index){
//    debugger;
    var clase = ''
    if (row.value_difference_error === true)
        clase = 'error';
    else
        clase = '';
    return { classes: clase}
}

//Formato para el formato de la fecha
//function style_fecha(value, row, index){
////    debugger;
//    // TODO Verify what fecha_error means
////    var clase = ''
////    if (row.fecha_error == 0 || row.fecha_error == 2 || row.fecha_error == 3 || row.fecha_numero > 0)
////        clase = 'error';
////    else
////        clase = '';
////    return { classes: clase}
//    var clase = ''
//    if (row.fecha_error > 0)
//        clase = 'error';
//    else
//        clase = '';
//    return { classes: clase}
//
//}


function style_date(value, row, index){
//    debugger;
    // TODO Verify what fecha_error means
//    var clase = ''
//    if (row.fecha_error == 0 || row.fecha_error == 2 || row.fecha_error == 3 || row.fecha_numero > 0)
//        clase = 'error';
//    else
//        clase = '';
//    return { classes: clase}
    var _class = '';
    if (row.date_error > 0)
        _class = 'error';
    else
        _class = '';
    return { classes: _class}

}

//Formato para la fila validada
function style_id(value, row, index){
//    debugger;
    var _class = '';
//    if (row.validado == true)
    if (row.all_validated == true)
        _class = 'validado';
    ///else if (row.estado == false)
       // clase = 'error';
   // TODO check row.seleccionado translation
    else if (row.seleccionado == false)
        _class = 'error';
    else
        _class = '';
    return { classes: _class}

}
///*Fomatos de celda para las tablas diario/crudos */
//// Poner el numero de errores en el día
//function format_valor(value, row, index, field){
////    debugger;
//    var span = '<span class="badge badge-light">num</span>';
//    var content = ''
//    var field_numero = field + '_numero'
////    field_numero = "suspicious_" + field +"s_count";
//    if (row[field_numero]>0 ){
//        span = span.replace('num',row[field_numero].toString());
//        content = value + ' ' + span;
//    }
//    else{
//        //span = span.replace('num',0);
//        content = value;
//    }
//    return content
//}

/*Fomatos de celda para las tablas diario/crudos */
// Poner el numero de errores en el día
function format_value(value, row, index, field){
//    debugger;
    var span = '<span class="badge badge-light">num</span>';
    var content = '';
//    var field_numero = field + '_numero'
    var field_numero = "suspicious_" + field.split("_")[1] +"s_count";
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



function format_punto_cardinal(value, row, index, field){
//    debugger;
    puntos_cardinales=['N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO'];

    return puntos_cardinales[parseInt(value-1)]


}

/*Funciones para el footeer de la tabla*/

//function footer_id(data){
////    debugger;
//    var span = '<span class="badge badge-danger">num</span>';
//    var num_fecha = data.reduce(function(num, i){
//        if (i['estado'] && i['seleccionado']==false)
//            return num +1;
//        else
//            return num;
//    }, 0);
//
//    span = span.replace('num',num_fecha.toString());
//
//    return span;
//
//}

function footer_id(data){
//    debugger;
    var span = '<span class="badge badge-danger">num</span>';
    var num_date = data.reduce(function(num, i){
        // TODO check translation: seleccionado
        if (i['state'] && i['seleccionado']==false)
            return num + 1;
        else
            return num;
    }, 0);

    span = span.replace('num',num_date.toString());

    return span;

}



// Obtener el promedio de los datos
function footer_promedio(data){
//    debugger;
    var field = this.field;
    var field_error = '';
    if ( this.field.includes("value") || this.field.includes("maximum") || this.field.includes("minimum")){
        field_error = this.field.split("_")[1] + '_error';
    }else{
        field_error = this.field + '_error';
    }


    var span = '<span class="badge badge-danger">num</span>';

    var promedio = 0;
    var suma = data.reduce(function (sum, i) {
//        if (i['estado'] && i[field] != null)
//           debugger;
          if (i['state'] && i[field] != null)
            return sum + parseFloat(i[field])
        else
            return sum;
    }, 0);
    var num_datos = data.reduce(function (sum, i) {
//        debugger;
//        if (i['estado'] && i[field] != null)
        if (i['state'] && i[field] != null)
            return sum + 1;
        else
            return sum;
    }, 0);

    var num_valor = data.reduce (function (num, i){
        //console.log('field',i[field_error])
//        if (i[field_error] && i['estado'])
//        debugger;
        if (i[field_error] && i['state'])
            return num + 1;
        else
            return num;
    }, 0);

    span = span.replace('num', num_valor);

    if (isNaN(suma))
        promedio = '-';
    else
        promedio = (suma / num_datos).toFixed(2);
    return promedio + ' ' + span;
}
//obtener la suma de los datos
function footer_suma(data){
    debugger;
    var field = this.field;
    var field_error = this.field + '_error';
    var span = '<span class="badge badge-danger">num</span>';
    var suma = data.reduce(function (sum, i) {
        if (i['estado'] && i[field] != null){
            return sum + parseFloat(i[field])
        }
        else{
            return sum
        }

    }, 0);
    var num_valor = data.reduce (function (sum, i){
        if (i[field_error] && i['estado'])
            return sum +1 ;
        else
            return sum;
    }, 0);

    span = span.replace('num', num_valor);

    return suma.toFixed(2) + ' ' + span;
}

//total de dias
function total_filas(data){
    var span = '<span class="badge badge-danger">num</span>';

    var var_id = $("#id_variable").val();
//    var fechas = [];
    var dates = [];
//    /*if ((var_id == 4) || (var_id == 5)) {
//        console.log(data);
//        $.map(data, function(row){
//            fechas.push(row.fecha);
//        });
//        console.log( fechas.unique() );
//    }*/

    $.map(data, function(row){
        dates.push(row.date);
    });

//    /*var suma = data.reduce(function (sum, i) {
//        if (i['estado']){
//            return sum + 1
//        }
//        else{
//            return sum
//        }
//
//    }, 0);*/

//    var suma = fechas.unique().length;
    var suma = dates.unique().length;

//    var num_fecha = data.reduce(function(num, i){
//        if ((i['fecha_error']==0) || (i['fecha_error']==2) || (i['fecha_error']==3))
//            return num +1;
//        else
//            return num;
//    }, 0);

//    debugger;
    var num_fecha = data.reduce(function(num, i){
//        if (i['fecha_error']>0)
        if (i['date_error']>0)
            return num +1;
        else
            return num;
    }, 0);

    // TODO ask the team for prefferred behaviour
//    span = span.replace('num',num_fecha.toString());
    span = span.replace('num', num_fecha.toString());

    return suma + ' of ' + indicators_daily['num_days'] + ' days ' + span;
//    return suma + ' of ' + daily_indicators['num_days'] + ' days ' + span;
}

//total de datos
function total_datos(data){
//    debugger;
    var span = '<span class="badge badge-danger">num</span>';

    var suma = data.reduce(function (sum, i) {
        if (i['estado']){
            return sum + 1
        }
        else{
            return sum
        }

    }, 0);

    var num_fecha = data.reduce(function(num, i){
        if ( (i['fecha_error']==0) || (i['fecha_error']==2) || (i['fecha_error']==3))
            return num +1;
        else
            return num;
    }, 0);

    span = span.replace('num',num_fecha.toString());

    return suma + ' de ' + indicators_subhourly['num_data'] + ' datos ' + span;
}
// valores atípicos
function footer_stddev(data){
//    debugger;
    var span = '<span class="badge badge-danger">num</span>';
    var num_stddev = data.reduce(function(num, i){
        if (i['stddev_error'] && i['estado'])
            return num +1;
        else
            return num;
    }, 0);

    span = span.replace('num',num_stddev.toString());

    return span;
}
//function footer_variaConse(data){
//    debugger;
//    var span = '<span class="badge badge-danger">num</span>';
//    var num_vcr = data.reduce(function(num, i){
//        if (i['stddev_error'] && i['estado'])
//            return num +1;
//        else
//            return num;
//    }, 0);
//
//    if (num_vcr > 1){
//        num_vcr -= 1;
//    }
//    span = span.replace('num',num_vcr.toString());
//
//    return span;
//}
function footer_variaConse(data){
//    debugger;
    var span = '<span class="badge badge-danger">num</span>';
    var num_vcr = data.reduce(function(num, i){
        if (i['value_difference_error'] && i['state'])
            return num +1;
        else
            return num;
    }, 0);

    if (num_vcr > 1){
        num_vcr -= 1;
    }
    span = span.replace('num',num_vcr.toString());

    return span;
}

function footer_variaConse_cont(data){
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


/* Filtro de las Tablas */
function filtrar_diario(){
    debugger;
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

function get_filtro_fecha(fecha){
//    debugger;
    var filtro_fecha = [];
    if (fecha == 'error')
        filtro_fecha = ['0','2', '3'];
    else if (fecha == 'normal')
        filtro_fecha = ['1'];
    else
        filtro_fecha = ['0','1', '2', '3'];

    return filtro_fecha
}

function get_filtro_porcentaje(porcentaje){
//    debugger;
    var filtro_porcentaje = [];

    if (porcentaje == 'error')
        filtro_porcentaje = [true];
    else if (porcentaje == 'normal')
        filtro_porcentaje = [false];
    else
        filtro_porcentaje = [true, false];

    return filtro_porcentaje
}

function get_filtro_valor(numero){
//    debugger;
    var filtro_valor = [];

    if (numero == 'error')
        filtro_valor = [true];
    else if (numero == 'normal')
        filtro_valor = [false];
    else
        filtro_valor = [true, false, null];

    return filtro_valor
}

function get_filtro_stddev(numero){
//    debugger;
    var filtro_valor = [];

    if (numero == 'error')
        filtro_valor = [true];
    else if (numero == 'normal')
        filtro_valor = [false];
    else
        filtro_valor = [true, false, null];

    return filtro_valor
}

function get_filtro_estado(numero){
//    debugger;
    var filtro_valor = [];

    if (numero == 'error')
        filtro_valor = [false];
    else if (numero == 'normal')
        filtro_valor = [true];
    else
        filtro_valor = [true, false];

    return filtro_valor
}
function get_filtro_var_con(numero){
//    debugger;
    console.log("Valorfiltro con ", numero);
    var filtro_valor = [];

    if (numero == 'error')
        filtro_valor = [true];
    else if (numero == 'normal')
        filtro_valor = [false];
    else
        filtro_valor = [true, false, null];

    return filtro_valor
}
function filtrar_crudo(){
    debugger;

    var fecha = $("#chk_fecha_crudo").val();
    var valor = $("#chk_valor_crudo").val();
    var stddev = $("#chk_stddev").val();
    var fila = $("#chk_fila").val();
    var varconfil = $("#chk_varcon").val();

    var filtro_fecha = get_filtro_fecha(fecha);
    var filtro_valor = get_filtro_valor(valor);
    var filtro_stddev = get_filtro_stddev(stddev);
    var filtro_fila = get_filtro_estado(fila);
    var filtro_varcon = get_filtro_var_con(varconfil);
    var variable_id = $("#id_variable").val();

//    if (variable_id == 10 || variable_id == 11){
//        $("#table_crudo").bootstrapTable('filterBy', {
//            fecha_error: filtro_fecha,
//            nivel_error: filtro_valor,
//            stddev_error: filtro_stddev,
//            estado:filtro_fila
//        });
//    }
//    else{

        $("#table_crudo").bootstrapTable('filterBy', {
//            fecha_error: filtro_fecha,
//            valor_error: filtro_valor,
//            stddev_error: filtro_stddev,
            value_difference_error: filtro_varcon,
//            estado:filtro_fila
        });

//    }
}


function clean_filters(tipo){
    if (tipo == 'detail'){
        $("#chk_detail_time").prop('selectedIndex',0);
        $("#chk_detail_value").prop('selectedIndex',0);
        $("#chk_detail_stddev").prop('selectedIndex',0);
        $("#chk_detail_row").prop('selectedIndex',0);
        $("#chk_detail_value_difference").prop('selectedIndex',0);
        $("#txt_detail_selection").val('');

    }
    else{
//        $("#chk_fecha").prop('selectedIndex',0);
//        $("#chk_porcentaje").prop('selectedIndex',0);
//        $("#chk_numero").prop('selectedIndex',0);
//        $("#txt_selection").val('');
    }
}

function get_valor_error(valor){
//    debugger;
    var limite_inferior = Number($("#id_limite_inferior").val());
    var limite_superior = Number($("#id_limite_superior").val());

    var valor_error = false;


    if (Number(valor) > limite_superior || Number(valor) < limite_inferior )
        valor_error = true;
    else
        valor_error = false;

    return valor_error;
}


function enable_new(){
//    debugger;
    var variable_id = $("#id_variable").val();

    //if (variable_id == "1" || variable_id == "10" || variable_id == "11")
    if ( variable_id != "11" || variable_id == "4" || variable_id == "5" )
        $("#btn_detail_new").attr("disabled", false);
    else
        $("#btn_detail_new").attr("disabled", true);


}

function activar_espera(type){
//    debugger;
    var type = type || ''
    if (type !== '') {
        var $div_data = $('#div_'+type);
        var $div_loading = $('#div_loading_'+type);
        var $div_message = $('#div_message_'+type)
    }
    else{
        var $div_data = $('#div_informacion');
        var $div_loading = $('#div_loading');
        var $div_message = $('#div_error')

    }
    $div_loading.show();
    $div_data.hide();
    $div_message.hide();
    $("#div_informacion").hide();
}   

//función para quitar duplicados
Array.prototype.unique=function(a){
  return function(){return this.filter(a)}}(function(a,b,c){return c.indexOf(a,b+1)<0
});


function mostrar_mensaje(type){
//    debugger;
    /*var message = '<div class="alert alert-danger alert-dismissible" role="alert">';
    message += 'Ocurrio un problema con el procesamiento de la información, por favor intentelo nuevamente';
    message += '</div>'*/

    var type = type || ''
    if (type !== ''){
        var $div_data = $('#div_'+type);
        var $div_loading = $('#div_loading_'+type);
        var $div_message = $('#div_message_'+type)
    }
    else{
        var $div_data = $('#div_informacion');
        var $div_loading = $('#div_loading');
        var $div_message = $('#div_error');

    }

    $div_loading.hide();
    $div_data.hide();
    //$div_message.html(message);
    $div_message.show();

}

function desactivar_espera(type){
//    debugger;
    var type = type || ''
    if (type !== '') {
        var $div_data = $('#div_'+type);
        var $div_loading = $('#div_loading_'+type);
        var $div_message = $('#div_message_'+type);
        var $resize_plot = $('#resize_plot'+type);
    }
    else{
        var $div_data = $('#div_informacion');
        var $div_loading = $('#div_loading');
        var $div_message = $('#div_error');
        var $resize_plot = $('#resize_plot');

    }
    $div_loading.hide();
    $div_data.show();
    $div_message.hide();
    $resize_plot.show();
    $("#div_informacion").show();
}
