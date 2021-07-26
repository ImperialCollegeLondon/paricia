
$(document).ready(function() {
    //activar tooltip
    $('[data-toggle="tooltip"]').tooltip()


    // Comparar Variables
    $("#btn_graficar").click(function(){
        $(this).attr('disabled',true);
        $.ajax({
            url: $("#form_consulta").attr('action'),
            data: $("#form_consulta").serialize(),
            type:'POST',
            dataType: 'json',
            beforeSend: function () {
                $("#div_informacion").hide();
                $("#div_loading").show();
                $("#div_error").hide();
            },
            success: function (data) {
                $("#div_informacion").show();
                var count = Object.keys(data.data[0].y).length;
                if (count>0) {
                    Plotly.newPlot('div_informacion', data.data,data.layout);

                }
                else{
                    $("#div_informacion").html('<label>No hay información para los parametros ingresados</label>')
                }
                $("#btn_graficar").removeAttr('disabled');

                $("#div_loading").hide();

                $("#div_error").hide();
            },
            error: function () {
                //$("#div_informacion").hide();
                $("#div_loading").hide();
                $("#div_error").show();
                $("#btn_graficar").removeAttr('disabled');
            }
        });
    });


    $("#btn_consultar").click(function(){
        $(this).attr('disabled',true);
        $.ajax({
            url: $("#form_busqueda").attr('action'),
            data: $("#form_busqueda").serialize(),
            type:'POST',
            dataType: 'json',
            beforeSend: function () {
                $("#div_informacion").hide();
                $("#div_loading").show();
                $("#div_error").hide();
                $("#div_mensaje").hide();
            },
            success: function (data) {

                if (Object.keys(data)=="mensaje"){
                    $("#div_mensaje").html(data.mensaje);
                    $("#div_mensaje").show();
                }
                else{
                    $("#div_informacion").show();
                    var count = Object.keys(data.data[0].y).length;
                    if (count>0) {
                        Plotly.newPlot('div_informacion', data.data,data.layout,{scrollZoom: true});
                    }
                    else{
                        //$("#div_informacion").html('<label>No hay información para los parametros ingresados</label>')
                        $("#div_mensaje").html('<label>No hay información para los parametros ingresados</label>');
                        $("#div_mensaje").show();
                    }

                }

                $("#btn_consultar").removeAttr('disabled');

                $("#div_loading").hide();

                $("#div_error").hide();
            },
            error: function () {
                //$("#div_informacion").hide();
                $("#div_loading").hide();
                $("#div_error").show();
                $("#btn_consultar").removeAttr('disabled');
            }
        });
    });

    //formulario validacion
    $("#btn_filtrar").click(function(){

        //actualizar_lista();
        $(this).attr('disabled',true);
        $.ajax({
            url: '/medicion/filter/',
            data: $("#form_filter").serialize(),
            type:'POST',
            dataType: 'json',
            beforeSend: function () {
                $("#div_informacion").hide();
                $("#div_loading").show();
                $("#div_error").hide();
                $("#div_mensaje").hide();
            },
            success: function (data) {
                if (Object.keys(data)=="mensaje"){
                    $("#div_mensaje").html(data.mensaje);
                    $("#div_mensaje").show();
                }
                else{
                    $("#div_informacion").show();
                    var count = Object.keys(data.data[0].y).length;
                    if (count>0) {
                        Plotly.newPlot('div_informacion', data.data,data.layout, {scrollZoom: true});
                    }
                    else{
                        //$("#div_informacion").html('<label>No hay información para los parametros ingresados</label>')
                        $("#div_mensaje").html('<label>No hay información para los parametros ingresados</label>');
                        $("#div_mensaje").show();
                    }
                }

                $("#btn_filtrar").removeAttr('disabled');

                $("#div_loading").hide();

                $("#div_error").hide();
            },
            error: function () {
                $("#btn_filtrar").removeAttr('disabled');
                $("#div_informacion").hide();
                $("#div_loading").hide();
                $("#div_error").show();
            }
        });

        $.ajax({
            url: '/medicion/datos_validacion/',
            data: $("#form_filter").serialize(),
            type:'POST',
            beforeSend: function () {
                $("#div_lista_datos").hide();
                $("#div_loading_datos").show();
                $("#div_error_datos").hide();
                $("#div_mensaje").hide();
            },
            success: function (data) {
                $("#div_lista_datos").html(data);
                $("#div_lista_datos").show();
                $("#btn_filtrar").removeAttr('disabled');
                $("#div_loading_datos").hide();
                $("#div_error_datos").hide();
                $("#div_mensaje").hide();

            },
            error: function () {

                $("#btn_filtrar").removeAttr('disabled');
                $("#div_lista_datos").hide();
                $("#div_loading_datos").hide();
                $("#div_error_datos").show();
            }
        });
        return false;
    });

    //consultar los periodos de validacion
    $("#btn_periodos_validacion").click(function(){
        //periodos_validacion();
    });


    //Cargar variables por estacion

    $("#id_estacion").change(function () {
        var estacion = $(this).val();
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
        });


    });

    //consulta y guarda la información
    $("#btn_procesar").click(function(){
        $(this).attr('disabled',true);
        $.ajax({
            url: $("#form_procesar").attr('action'),
            data: $("#form_procesar").serialize(),
            type:'POST',
            beforeSend: function () {
                activar_espera("#div_loading","#div_informacion","#div_error")
            },
            success: function (data) {
                $("#div_informacion").html(data)
                $("#btn_procesar").removeAttr('disabled');
                desactivar_espera("#div_loading","#div_informacion","#div_error")
            },
            error: function () {
                mostrar_mensaje("#div_loading","#div_informacion","#div_error")
                $("#btn_procesar").removeAttr('disabled');
            }
        });
    });


    //datepicker con intervalo registringido
    var dateFormat = "yy-mm-dd";
    $( "#id_inicio" ).datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat:"yy-mm-dd",
        yearRange: '2000:'+(new Date).getFullYear()
    });
    $( "#id_inicio" ).on( "change", function() {
        $( "#id_fin" ).datepicker( "option", "minDate", getDate( this ) );
    });
    $( "#id_fin" ).datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat:"yy-mm-dd",
        yearRange: '2000:'+(new Date).getFullYear()
    });
    $( "#id_fin" ).on( "change", function() {
        $( "#id_inicio" ).datepicker( "option", "maxDate", getDate( this ) );
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


    function periodos_validacion(){
        token = $("input[name='csrfmiddlewaretoken']").val();
        estacion_id = $("input[name='orig_estacion_id']").val();
        variable_id = $("input[name='orig_variable_id']").val();

        $.ajax({
            url: '/validacion_v2/periodos_validacion/',
            data: $("#form_filter").serialize(),
            type:'POST',
            beforeSend: function () {
                //$("#div_historial").hide();
                //$("#div_loading_historial").show();
                //$("#div_error_historial").hide();
                activar_espera("historial")
            },
            success: function (data) {
                $("#btn_periodos_validacion").attr("disabled", false);
                $("#div_historial").html(data)


                $("#div_historial").show();
                $("#div_loading_historial").hide();
                $("#div_error_historial").hide();

            },
            error: function () {
                $("#div_historial").hide();
                $("#div_loading_historial").hide();
                $("#div_error_historial").show();

            }
        });
    }




});
