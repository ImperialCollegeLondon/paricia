var plot_orig_width = 0;
var plot_adjusted = true;
var gid = 0;

function plot_adjust(){
    var window_width = $("#div_informacion").width();
    Plotly.relayout(gid, {width: window_width });
    $("#" + gid).css("width", "");
    plot_adjusted = true;
    $('#resize_plot').html("&gt Un pixel por dato &lt");
}
var dateFormat = "yy-mm-dd";

function plot_orig(){
    Plotly.relayout(gid, {width: plot_orig_width });
    $("#" + gid).css("width", plot_orig_width + "px");
    plot_adjusted = false;
    $('#resize_plot').html("&gt Ajustar a pantalla &lt");
}

function resizePlot(){
    if (plot_adjusted){
        plot_orig();
    }else{
        plot_adjust();
    }
}

tr_ini = '<tr>';
tr_fin = '</tr>';
var datos_json = {};
var data_fecha = [];
var data_valor = [];
var data_maximo = [];
var data_minimo = [];
//var num_dias = 0;
var num_datos = 0;

var indicadores_crudos = {
    num_fecha: 0,
    num_valor: 0,
    num_maximo: 0,
    num_minimo:0,
    num_stddev: 0,
    num_datos:0
}

var indicadores_diarios = {
    num_fecha: 0,
    num_porcentaje: 0,
    num_valor: 0,
    num_maximo: 0,
    num_minimo: 0,
    num_dias: 0
}

var num_fecha = 0;

// Valores de prueba
// M5077 TAI 2015-07-28, valores de -74
// M5025 TAI 2008-05-02, serie de datos faltantes


function mostrar_label_dentro_de_select(){
    //// Elemento SELECT muestre label dentro de su caja
     $('select.use-placeholder').each(function(){
         var op0 = $(this).children('option:first-child');
         if (op0.is(':selected')) {
             op0.css( "display", "none" );
             $(this).addClass('placeholder');
             var label_text = $(this).parent('div').children('label').text();
             op0.text(label_text);
         }
     });
 
     //// Elemento SELECT oculte o muestre selección nula
     $('select.use-placeholder').change(function() {
         var op0 = $(this).children('option:first-child');
         if (op0.is(':selected')) {
             op0.css( "display", "none" );
             $(this).addClass('placeholder');
             var label_text = $(this).parent('div').children('label').text();
             op0.text(label_text);
         } else {
             op0.css( "display", "" );
             $(this).removeClass('placeholder');
             op0.text("---------");
         }
     });
 }
$(document).ready(function() {
    /*$( "#id_inicio" ).datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat:"yy-mm-dd",
        yearRange: '2007:'+(new Date).getFullYear()
    });
    $( "#id_inicio" ).on( "change", function() {
        //$( "#id_fin" ).datepicker( "option", "minDate", getDate( this ) );
        $("#div_message_fechas").hide();
    });
    $( "#id_fin" ).datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat:"yy-mm-dd",
        yearRange: '2007:'+(new Date).getFullYear()
    });
    $( "#id_fin" ).on( "change", function() {
       // $( "#id_inicio" ).datepicker( "option", "maxDate", getDate( this ) );
        $("#div_message_fechas").hide();
    });*/
    $("#btn_nuevo_crudo").attr("disabled", true);
    //mostrar_label_dentro_de_select();
    //$("#id_estacion").attr("placeholder", "Estación");
    //console.log($("#id_estacion").attr("placeholder"));
    $('#div_grafico').on('hidden.bs.collapse', function () {
        $("#btn_grafico").text("Mostrar Gráfico");
    });
    $('#div_grafico').on('show.bs.collapse', function () {
        $("#btn_grafico").text("Ocultar Gráfico");
    });



    $("#btn_buscar").click(actualizar_tabla_diario);

    //consultar los periodos de validacion
    $("#btn_periodos_validacion").click(function(){
        $("#btn_periodos_validacion").attr("disabled", true);


    });

    // consultar los limites de la variable
    $("#id_variable").change(function () {
        //var codigo = $('#id_estacion option:selected').text();
        var variable = $(this).val();
        token = $("input[name='csrfmiddlewaretoken']").val();

        $.ajax({
            url: '/variable/limites/',
            dataType: 'json',
            data: {
                'csrfmiddlewaretoken': token,
                'var_id': variable,
            },
            type:'POST',
            success: function (data) {
                $("#id_limite_inferior").val(data.var_minimo);
                $("#id_limite_superior").val(data.var_maximo);
            }
        });

    });




    /*Filtros de la tablas*/
    $("#chk_porcentaje").change(filtrar_diario);
    $("#chk_fecha").change(filtrar_diario);
    $("#chk_numero").change(filtrar_diario);

    $("#chk_fecha_crudo").change(filtrar_crudo);

    $("#chk_valor_crudo").change(filtrar_crudo);
    $("#chk_stddev").change(filtrar_crudo);
    $("#chk_fila").change(filtrar_crudo);

    /*Control de los botones*/

    var $btn_enviar = $('#btn_enviar');
    var $btn_guardar = $('#btn_enviar_crudo');

    var $btn_mostrar = $('#btn_mostrar');
    var $btn_mostrar_crudo = $('#btn_mostrar_crudo');

    var $btn_eliminar = $('#btn_eliminar');
    var $btn_eliminar_crudo = $('#btn_eliminar_crudo');

    var $btn_seleccionar = $('#btn_seleccionar');
    var $btn_seleccionar_crudo = $('#btn_seleccionar_crudo');

    var $btn_desmarcar = $('#btn_desmarcar');
    var $btn_desmarcar_crudo = $('#btn_desmarcar_crudo');

    var $btn_nuevo_promedio = $('#btn_nuevo_promedio');
    var $btn_nuevo_acumulado = $('#btn_nuevo_acumulado');

    var $btn_modificar_promedio = $('#btn_modificar_promedio');
    var $btn_modificar_acumulado = $('#btn_modificar_acumulado');
    var $btn_modificar_agua = $('#btn_modificar_agua');

    var $btn_graficar = $('#btn_grafico');
    var $btn_graficar_crudo = $('#btn_grafico_crudo');

    var $btn_historial = $('#btn_historial');

    var $btn_desvalidar = $('#btn_desvalidar');

    var $table = $('#table_diario');
    ///fondo blnco para la tabal diaria
    //$table.css("background-color","white");

    var $btn_eliminar_valor = $("#btn_eliminar_valor");

    var $btn_nuevo_crudo = $("#btn_nuevo_crudo");


    $btn_enviar.click(guardar_validados);

    $btn_mostrar.click(mostrar);
    $btn_mostrar_crudo.click(mostrar);

    $btn_eliminar.click(eliminar);
    $btn_eliminar_crudo.click(eliminar);

    $btn_seleccionar.click(marcar);
    $btn_desmarcar.click(desmarcar);

    $btn_seleccionar_crudo.click(marcar);
    $btn_desmarcar_crudo.click(desmarcar);

    $btn_nuevo_promedio.click(nuevo_registro);
    $btn_nuevo_acumulado.click(nuevo_registro);


    $btn_modificar_acumulado.click(modificar);
    $btn_modificar_promedio.click(modificar);
    $btn_modificar_agua.click(modificar);

    $btn_guardar.click(guardar_crudos);

    $btn_graficar.click(graficar);
    $btn_graficar_crudo.click(graficar);

    $btn_historial.click(periodos_validacion);

    $btn_eliminar_valor.click(eliminar_crudo)

    $btn_nuevo_crudo.click(abrir_formulario_nuevo);

    $btn_desvalidar.click(desvalidar_datos);


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
                url: '/validacion_v2/',
                data: $("#form_validacion").serialize(),
                type:'POST',
                beforeSend: function () {
                    activar_espera("historial");
                    $("#div_modal_historial").modal("show");
                },
                success: function (data) {
                    //console.log(data);
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
                url: '/validacion_v2/periodos_validacion/',
                data: $("#form_validacion").serialize(),
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

function guardar_validados(event){
    var $table = $('#table_diario');
    var $table_crudo = $('#table_crudo');
    //$table.css("background-color","white");
    token = $("input[name='csrfmiddlewaretoken']").val();
    estacion_id = $("#id_estacion").val();
    variable_id = $("#id_variable").val();
    limite_superior = $("#id_limite_superior").val();
    limite_inferior = $("#id_limite_inferior").val();
    fecha_inicio = $("input[name='inicio']").val();
    fecha_fin = $("input[name='fin']").val();

    //comentario_general = $("textarea[name='comentario_general']").val();
    cambios = JSON.stringify($table.bootstrapTable('getData',{unfiltered:true, includeHiddenRows: true}));


    $.ajax({
        url: '/validacion_v2/guardarvalidados/',
        data: {
            'csrfmiddlewaretoken': token,
            'estacion_id': estacion_id,
            'variable_id': variable_id,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'limite_superior': limite_superior,
            'limite_inferior': limite_inferior,
            //'comentario_general' : comentario_general,
            'cambios': cambios
        },
        type:'POST',
        beforeSend: function () {
            $table.bootstrapTable('showLoading');
            $table_crudo.bootstrapTable('showLoading');
        },
        success: function (data) {
            //console.log(typeof data.resultado)
            if (data.resultado == true){
                $("#div_body_mensaje").html('Datos Guardados')
                $("#div_mensaje_validacion").modal("show");
                $("#resize_plot").hide();
                $("#div_informacion").hide();
                limpiar_filtros('diario');
                limpiar_filtros('crudo');
                $table_crudo.bootstrapTable('removeAll');
                $table.bootstrapTable('removeAll');


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

//eliminar datos validados de la base de datos

function eliminar_validados(event){
    var $table = $('#table_diario');
    var $table_crudo = $('#table_crudo');
    //$table.css("background-color","white");
    token = $("input[name='csrfmiddlewaretoken']").val();
    estacion_id = $("#id_estacion").val();
    variable_id = $("#id_variable").val();
    //comentario_general = $("textarea[name='comentario_general']").val();
    cambios = JSON.stringify($table.bootstrapTable('getData',{unfiltered:true, includeHiddenRows: true}));


    $.ajax({
        url: '/validacion_v2/eliminarvalidados/',
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
            //console.log(typeof data.resultado)
            if (data.resultado == true){
                //$("#div_body_mensaje").html('Datos Guardados')
                //$("#div_mensaje_validacion").modal("show");

                limpiar_filtros('diario');
                limpiar_filtros('crudo');
                //$table_crudo.bootstrapTable('removeAll');
                //$table.bootstrapTable('removeAll');
                actualizar_tabla_diario();


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
    var $table = $('#table_crudo');
    //$table.css("background-color","white");
    token = $("input[name='csrfmiddlewaretoken']").val();
    estacion_id = $("#id_estacion").val();
    variable_id = $("#id_variable").val();
    fecha_inicio = $("input[name='inicio']").val();
    fecha_fin = $("input[name='fin']").val();
    //comentario_general = $("textarea[name='comentario_general']").val();
    cambios = JSON.stringify($table.bootstrapTable('getData',{unfiltered:true}));
    //console.log($table.bootstrapTable('getData',{unfiltered:true, }))
    //detalle_crudos();



    $.ajax({
        url: '/validacion_v2/guardarcrudos/',
        data: {
            'csrfmiddlewaretoken': token,
            'estacion_id': estacion_id,
            'variable_id': variable_id,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            //'comentario_general' : comentario_general,
            'cambios': cambios
        },
        type:'POST',
        beforeSend: function () {
            $table.bootstrapTable('showLoading');
        },
        success: function (data) {
            console.log(typeof data.resultado)
            if (data.resultado == true){
                $("#div_body_mensaje").html('Datos Guardados')
                $("#div_mensaje_validacion").modal("show");
                detalle_crudos();
                modificar_fila();
                limpiar_filtros('crudo');
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
function actualizar_tabla_diario(){
    var $table = $('#table_diario');
    var var_id = $("#id_variable").val();
    var flag_error = false;
    var mensaje = '';
    $("#orig_variable_id").val(var_id);
    $("#div_informacion").html('')
    $("#resize_plot").hide();
    limpiar_filtros('diario');
    limpiar_filtros('crudo');
    //$("#table_crudo").bootstrapTable('removeAll');
    fecha_inicio = $("input[name='inicio']").val();
    fecha_fin = $("input[name='fin']").val();
    if( fecha_inicio == '' || fecha_fin == '')
    {
        $("#div_message_fechas").show("slow");
        $("#div_c").html("");
    }
    else {
        $("#div_message_fechas").hide();
        $("#div_c").html("");
        $.ajax({
            url: $("#form_validacion").attr('action'),
            data: $("#form_validacion").serialize(),
            type:'POST',
            beforeSend: function () {
                //activar_espera();
                $table.bootstrapTable('showLoading');
    
            },
            success: function (data) {            
                $("#btn_buscar").attr("disabled", false);
                for (var key in data){
                    if (key == 'error'){
                        flag_error = true;
                        mensaje = data.error;
                    }
                }
                if (flag_error == false){
                    
                    if (data.grafico === '<div><h1 style="background-color : red">No hay datos</h1></div>'){
                        $("#div_informacion").show("slow");
                        $("#div_informacion").html(data.grafico)
                        $("#resize_plot").hide();
                    }
                    else {
                        $("#div_c").html(data.curva);
                        $("#div_informacion").html(data.grafico)
                        $("#resize_plot").show("slow");
                        $("#div_informacion").show("slow");
                        window.gid = $('.plotly-graph-div,.js-plotly-plot').attr('id');
                        window.plot_orig_width = $("#" + window.gid).width();
                        plot_adjust();
                        habilitar_nuevo();
                    var_id = data.variable[0]['var_id'];
                    variable = data.variable[0];
                    estacion = data.estacion[0];
                    datos_json = data.datos
                    //num_dias = data.indicadores[0]['num_dias'];
                    $table.bootstrapTable('destroy');
                    for (const index in data.indicadores[0]){
                        indicadores_diarios[index]= data.indicadores[0][index];
                    }
                    var columns = get_columns_diario(var_id, data.indicadores[0]);
                    $table.bootstrapTable({
                        columns:columns,
                        data: datos_json,
                        height: 458,
                        showFooter: true,
                        uniqueId: 'id',
                        rowStyle: style_fila
                    });
                    //graficar(data.variable[0], data.estacion[0], data.grafico[0]);
                    //$('#div_grafico').collapse('show')
                    //desactivar_espera();
                    $table.bootstrapTable('hideLoading');
                    $("#table_crudo").bootstrapTable('removeAll');
                    }
                    
    
                }
                else{
                    $table.bootstrapTable('hideLoading');
                    $("#resize_plot").hide();
                    $("#div_body_mensaje").html(mensaje)
                    $("#div_mensaje_validacion").modal("show");
    
                }
    
            },
            error: function () {
                $table.bootstrapTable('hideLoading');
                $("#div_body_mensaje").html('Ocurrio un problema con la validación por favor contacte con el administrador')
                $("#div_mensaje_validacion").modal("show");
                //mostrar_mensaje()
    
            }
        });
    
    }
    
}

// actualizar una fila de la tabla de datos diarios
function modificar_fila(){
    var $table = $('#table_crudo');
    //$table.css("background-color","white");
    var $table_diario = $('#table_diario');

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

    var porcentaje = (sum_datos * 100 / indicadores_crudos['num_datos']).toFixed(2);

    var porcentaje_error = false

    if (var_id == 1){
        porcentaje_error = porcentaje < 80 || porcentaje > 100 ? true : false
    }
    else{
        porcentaje_error = porcentaje < 70 || porcentaje > 100 ? true : false
    }





    if (var_id != 1){
        $table_diario.bootstrapTable('updateByUniqueId', {
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
        $table_diario.bootstrapTable('updateByUniqueId', {
            id: id_diario,
            row: {nivel: avg_nivel, caudal: avg_caudal, validado: true,
                nivel_numero: num_nivel,
                porcentaje: porcentaje, porcentaje_error: porcentaje_error, fecha_numero: num_fecha,
                nivel_error: num_nivel > 0 ? true : false
            }
        });
    }
    else {
        $table_diario.bootstrapTable('updateByUniqueId', {
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
        $table = $("#table_diario");

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
            else if( var_id == 10 || var_id == 11){
                data_nivel.push(item.nivel);
                data_caudal.push(item.caudal);
            }
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
        $table = $("#table_diario");

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
    $(this).attr('disabled',true);
    var name = event.currentTarget.name;
    console.log(name)
    if (name === 'crudo')
        $table = $("#table_crudo");
    else
        $table = $("#table_diario");

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
    $(this).attr('disabled',true);
    var name = event.currentTarget.name;
    console.log(name)
    if (name === 'crudo')
        $table = $("#table_crudo");
    else
        $table = $("#table_diario");

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
    var name = event.currentTarget.name;
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

// Desmarcar filas seleccionadas tabla crudos/diarios
function desmarcar(event){
    var $table = '';
    var name = event.currentTarget.name;
    if (name ==='crudo')
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

    var id_diario = 0;
    var fecha = '';

    var estado = row || false

    if (estado == false ){
        id_diario = $("#orig_id_diario").val();
        fecha = $("#orig_fecha_diario").val();
    }
    else{
        id_diario = row.id;
        fecha = row.fecha;
        $("#orig_id_diario").val(id_diario);
        $("#orig_fecha_diario").val(fecha);
    }

    var var_maximo = $("#id_limite_superior").val();
    var var_minimo = $("#id_limite_inferior").val();


    enlace = '/validacion_v2/lista/' + estacion_id + '/' + variable_id + '/' + fecha + '/' + var_maximo + '/' + var_minimo;

    $.ajax({
        url: enlace,
        type:'GET',
        beforeSend: function () {
            $table.bootstrapTable('showLoading');
        },
        success: function (data) {
            datos_json = data.datos;
            $table.bootstrapTable('destroy');
            for (const index in data.indicadores[0]){
                indicadores_crudos[index] = data.indicadores[0][index];
                $("#span_"+index+"_crudo").text(indicadores_crudos[index]);
            }
            /* this is an example for new snippet extension make by me xD */
            for (const element of datos_json) {
                element["fecha"] = (element['fecha']).replace('T',' ');
            }
            var columns = get_column_validado(variable_id, data.indicadores[0]);
            $table.bootstrapTable({columns:columns, data: datos_json, rowStyle: style_fila})
            //$table.bootstrapTable({columns:columns, data: datos_json})
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
    console.log(row);
    var $table = $('#table_diario');
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
    var $form_modal = $('#modal_eliminar');
    var inputs = $("#form_eliminar").serializeArray();
    $.each(inputs, function(i, field){
        $('input[name="'+field.name+'"]').val(row[field.name]);
    });
    $form_modal.modal("show");
}

//funcion para eliminar una fila de la tabla crudos
function eliminar_crudo(event){
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
function get_columns_diario(var_id){

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

    var fecha = {
        field:'fecha',
        title: 'Fecha',
        cellStyle: style_fecha,
        formatter: format_valor,
        footerFormatter: total_filas,
        //filterControl: 'datepicker'

    };
    var porcentaje = {
        field:'porcentaje',
        title:'Porcentaje ',
        cellStyle: style_porcentaje,
        footerFormatter: footer_promedio,
        //filterControl: 'input'
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
    var n_valor = {
        field:'n_valor',
        title:'Variación Consecutiva',
        cellStyle: style_var_con,
        footerFormatter: footer_variaConse_cont
    };

    columns.push(state);
    columns.push(id);
    columns.push(fecha);
    columns.push(porcentaje);



    if (var_id == 1) {
        var valor = {
            field:'valor',
            title:'Valor ',
            cellStyle: style_valor,
            formatter: format_valor,
            footerFormatter: footer_suma
        };
        columns.push(valor);
        columns.push(n_valor);
    }
    else if ((var_id == 4) || (var_id == 5)){

        var valor = {
            field:'valor',
            title:'Valor ',
            cellStyle: style_valor,
            //formatter: format_valor,
            footerFormatter: footer_promedio
        };

        var maximo = {
            field:'maximo',
            title:'Máximo ',
            visible: false,
            cellStyle: style_valor,
            //formatter: format_valor,
            footerFormatter: footer_promedio
        };

        var minimo= {
            field:'minimo',
            title:'Mínimo ',
            visible: false,
            cellStyle: style_valor,
            //formatter: format_valor,
            footerFormatter: footer_promedio
        }
        var direccion = {
            field:'direccion',
            title:'Direccion',
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
        columns.push(valor);
        columns.push(maximo);
        columns.push(minimo);
        columns.push(direccion);
        columns.push(punto_cardinal);

    }

    else{
        var valor = {
            field:'valor',
            title : 'Valor',
            cellStyle: style_valor,
            formatter: format_valor,
            footerFormatter: footer_promedio
        };
        var maximo = {
            field:'maximo',
            title:'Máximo ',
            cellStyle: style_valor,
            formatter: format_valor,
            footerFormatter: footer_promedio
        };

        var minimo= {
            field:'minimo',
            title:'Mínimo ',
            cellStyle: style_valor,
            formatter: format_valor,
            footerFormatter: footer_promedio
        }
        columns.push(valor);
        columns.push(maximo);
        columns.push(minimo);
        columns.push(n_valor);



    }

    columns.push(accion);

    return columns

}

//generar las columnas para la tabla de datos crudos
function get_column_validado(var_id){
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

    var fecha = {
        field:'fecha',
        title:'Fecha',
        cellStyle: style_fecha,
        footerFormatter: total_datos
    };

    var valor_atipico = {
        field:'',
        title:'Valores Atípicos',
        cellStyle: style_stddev,
        footerFormatter: footer_stddev
    };


    var comentario = {
        field:'comentario',
        title:'Comentario'
    };
    var n_valor = {
        field:'n_valor',
        title:'Variación Consecutiva',
        cellStyle: style_varia_error,
        footerFormatter: footer_variaConse
    };

    var accion = {
        field: 'accion',
        title: 'Acción',
        formatter: operate_table_crudo,
        events: {
           'click .delete_crudo': abrir_form_eliminar,
           'click .update': abrir_formulario

        }
    };

    columns.push(state);
    columns.push(id);
    columns.push(fecha);
    
    if (var_id =='1'){


        var valor = {
            field:'valor',
            title: 'Valor',
            cellStyle: style_error_crudo,
            footerFormatter: footer_suma
        };
        columns.push(valor);

    }
    else if ( (var_id == '4') || ( var_id == '5') ){
        var valor = {
            field:'valor',
            title:'Valor ',
            cellStyle: style_valor,
            //formatter: format_valor,
            footerFormatter: footer_promedio
        };

        var maximo = {
            field:'maximo',
            title: 'Máximo',
            visible: false,
            cellStyle: style_error_crudo,
            footerFormatter: footer_promedio
        };

        var minimo = {
            field:'minimo',
            title: 'Mínimo',
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
            title:'Direccion',
            //cellStyle: style_valor,
            //footerFormatter: footer_promedio
        };
        columns.push(valor);
        columns.push(maximo);
        columns.push(minimo);
        columns.push(direccion);
        columns.push(punto_cardinal);
    }
    else{
        var valor = {
            field:'valor',
            title:'Valor',
            cellStyle: style_error_crudo,
            footerFormatter: footer_promedio
        };

        var maximo = {
            field:'maximo',
            title: 'Máximo',
            cellStyle: style_error_crudo,
            footerFormatter: footer_promedio
        };

        var minimo = {
            field:'minimo',
            title: 'Mínimo',
            cellStyle: style_error_crudo,
            footerFormatter: footer_promedio
        };
        columns.push(valor);
        columns.push(maximo);
        columns.push(minimo);

    }
    columns.push(valor_atipico);
    columns.push(comentario);
    columns.push(n_valor);
    columns.push(accion);
    return columns
}

//Función para generar los iconos de acción de la tabla diario
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

//Función para generar los iconos de acción de la tabla crudos
function operate_table_crudo(value, row, index) {
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
function style_porcentaje(value, row, index) {
    var clase = ''
    if (row.porcentaje_error == true) {
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
function style_fila(row, index){
    if (row.estado == false) {
      clase = 'error'
    }
    /*if (row.seleccionado == false){
        clase = 'no-seleccionado'
    }*/
    else
        clase = ''
    return {classes: clase}
}
function style_valor(value, row, index, field){
    var clase = ''
    field_numero = field+'_numero';
    limite_superior = $('#id_limite_superior').val();
    if (row[field_numero]>0 )
        clase = 'error';
    else
        clase = 'normal';
    return { classes: clase}
}
//Formato para el error de la tabla crudos/diarios
function style_error_crudo(value, row, index, field){
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
    var clase = ''
    if (row.stddev_error === true)
        clase = 'error';
    else
        clase = '';
    return { classes: clase}
}
function style_var_con(value, row, index){
    var clase = ''
    if (row.c_varia_err >= 1)
        clase = 'error';
    else
        clase = '';
    return { classes: clase}
}
function style_varia_error(value, row, index){
    var clase = ''
    if (row.varia_error === true)
        clase = 'error';
    else
        clase = '';
    return { classes: clase}
}

//Formato para el formato de la fecha
function style_fecha(value, row, index){
    var clase = ''
    if (row.fecha_error == 0 || row.fecha_error == 2 || row.fecha_error == 3 || row.fecha_numero > 0)
        clase = 'error';
    else
        clase = '';
    return { classes: clase}

}
//Formato para la fila validada
function style_id(value, row, index){
    var clase = ''
    if (row.validado == true)
        clase = 'validado';
    ///else if (row.estado == false)
       // clase = 'error';
    else if (row.seleccionado == false)
        clase = 'error';
    else
        clase = '';
    return { classes: clase}

}
/*Fomatos de celda para las tablas diario/crudos */
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

function format_punto_cardinal(value, row, index, field){
    puntos_cardinales=['N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO'];

    return puntos_cardinales[parseInt(value-1)]


}

/*Funciones para el footeer de la tabla*/

function footer_id(data){
    var span = '<span class="badge badge-danger">num</span>';
    var num_fecha = data.reduce(function(num, i){
        if (i['estado'] && i['seleccionado']==false)
            return num +1;
        else
            return num;
    }, 0);

    span = span.replace('num',num_fecha.toString());

    return span;

}

// Obtener el promedio de los datos
function footer_promedio(data){
    var field = this.field;
    var field_error = this.field + '_error';


    var span = '<span class="badge badge-danger">num</span>';

    var promedio = 0;
    var suma = data.reduce(function (sum, i) {
        if (i['estado'] && i[field] != null)
            return sum + parseFloat(i[field])
        else
            return sum
    }, 0);
    var num_datos = data.reduce(function (sum, i) {
        if (i['estado'] && i[field] != null)
            return sum + 1
        else
            return sum
    }, 0);

    var num_valor = data.reduce (function (num, i){
        //console.log('field',i[field_error])
        if (i[field_error] && i['estado'])
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
    var fechas = [];
    /*if ((var_id == 4) || (var_id == 5)) {
        console.log(data);
        $.map(data, function(row){
            fechas.push(row.fecha);
        });
        console.log( fechas.unique() );
    }*/

    $.map(data, function(row){
        fechas.push(row.fecha);
    });

    /*var suma = data.reduce(function (sum, i) {
        if (i['estado']){
            return sum + 1
        }
        else{
            return sum
        }

    }, 0);*/

    var suma = fechas.unique().length;

    var num_fecha = data.reduce(function(num, i){
        if ((i['fecha_error']==0) || (i['fecha_error']==2) || (i['fecha_error']==3))
            return num +1;
        else
            return num;
    }, 0);

    span = span.replace('num',num_fecha.toString());

    return suma + ' de ' + indicadores_diarios['num_dias'] + ' días ' + span;
}
//total de datos
function total_datos(data){
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

    return suma + ' de ' + indicadores_crudos['num_datos'] + ' datos ' + span;
}
// valores atípicos
function footer_stddev(data){
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
function footer_variaConse(data){
    var span = '<span class="badge badge-danger">num</span>';
    var num_vcr = data.reduce(function(num, i){
        if (i['stddev_error'] && i['estado'])
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
    var span = '<span class="badge badge-danger">num</span>';
    var num_vc= data.reduce(function(num, i){
        if (i['c_varia_err'] >= 1 )
            return num + 1;
        else
            return num;
    }, 0);

    span = span.replace('num',num_vc);
    return span;
}


/* Filtro de las Tablas */
function filtrar_diario(){
    var fecha = $("#chk_fecha").val();
    var porcentaje = $("#chk_porcentaje").val();
    var numero = $("#chk_numero").val();

    var filtro_fecha = get_filtro_fecha(fecha);
    var filtro_porcentaje = get_filtro_porcentaje(porcentaje);
    var filtro_valor = get_filtro_valor(numero);

    var var_id = $("#id_variable").val();

    if (var_id == 10 || var_id == 11){
        $("#table_diario").bootstrapTable('filterBy', {
        fecha_error: filtro_fecha,
        porcentaje_error: filtro_porcentaje,
        nivel_error: filtro_valor,
        //estado:[true]
    });

    }
    else {
        $("#table_diario").bootstrapTable('filterBy', {
        fecha_error: filtro_fecha,
        porcentaje_error: filtro_porcentaje,
        valor_error: filtro_valor,
        //estado:[true]
    });

    }


}

function get_filtro_fecha(fecha){
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
console.log("Filtrar Crudo ")
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

    if (variable_id == 10 || variable_id == 11){
        $("#table_crudo").bootstrapTable('filterBy', {
            fecha_error: filtro_fecha,
            nivel_error: filtro_valor,
            stddev_error: filtro_stddev,
            estado:filtro_fila
        });
    }
    else{
        console.log("En el else 2269");
        $("#table_crudo").bootstrapTable('filterBy', {
            fecha_error: filtro_fecha,
            valor_error: filtro_valor,
            stddev_error: filtro_stddev,
            n_valor: filtro_varcon,
            estado:filtro_fila
        });

    }
}


function limpiar_filtros(tipo){
    if (tipo == 'crudo'){
        $("#chk_fecha_crudo").prop('selectedIndex',0);
        $("#chk_valor_crudo").prop('selectedIndex',0);
        $("#chk_stddev").prop('selectedIndex',0);
        $("#chk_fila").prop('selectedIndex',0);
        $("#chk_varcon").prop('selectedIndex',0);
        $("#txt_seleccionar_crudo").val('');

    }
    else{
        $("#chk_fecha").prop('selectedIndex',0);
        $("#chk_porcentaje").prop('selectedIndex',0);
        $("#chk_numero").prop('selectedIndex',0);
        $("#txt_seleccionar").val('');
    }



}

function get_valor_error(valor){
    var limite_inferior = Number($("#id_limite_inferior").val());
    var limite_superior = Number($("#id_limite_superior").val());

    var valor_error = false;


    if (Number(valor) > limite_superior || Number(valor) < limite_inferior )
        valor_error = true;
    else
        valor_error = false;

    return valor_error;
}


function habilitar_nuevo(){
    var variable_id = $("#id_variable").val();

    if (variable_id == "1" || variable_id == "10" || variable_id == "11")
        $("#btn_nuevo_crudo").attr("disabled", false);
    else
        $("#btn_nuevo_crudo").attr("disabled", true);


}

function activar_espera(type){

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
