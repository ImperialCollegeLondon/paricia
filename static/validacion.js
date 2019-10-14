function alarma_fecha(){
    errores = 0
    normales = 0
    saltos = 0
    $(".seleccionado > .fecha").each(function(){
        if ($(this).hasClass('error') ){
            errores = errores + 1;
        }else if ($(this).hasClass('normal') ){
            normales = normales + 1;
        }else{
            saltos = saltos + 1;
        }
    });
    $("#btn_fec_error").html("Error <br/>"+errores);
    $("#btn_fec_normal").html("Normal <br/>"+normales);
    $("#btn_fec_salto").html("Salto <br/>"+saltos);
};

function alarma_validacion(){
    no_validados = 0
    validados = 0
    cambios = 0
    $(".seleccionado > .validacion").each(function(){
        if ($(this).hasClass('validado') ){
            validados = validados + 1
        }else if ($(this).hasClass('no-validado')){
            no_validados = no_validados + 1;
        }else if ($(this).hasClass('cambio')){
            cambios = cambios +1;
        }
    });
    $("#btn_val_nuevo").html("No Val. <br/>"+no_validados);
    $("#btn_val_ya_validado").html("Val. <br/>"+validados);
    $("#btn_val_cambio").html("Cambio <br/>"+cambios);
};

function alarma_medicion(){
    lim_sup = parseFloat($("input[name='lim_sup']").val());
    lim_inf = parseFloat($("input[name='lim_inf']").val());
    errores = 0
    normales = 0
    $(".seleccionado > .valor").each(function(){
        valor = parseFloat($(this).html().trim());
        if ( valor < lim_inf || valor > lim_sup ){
            $(this).removeClass("normal").addClass("error");
            errores = errores + 1
        }else{
            $(this).removeClass("error").addClass("normal");
            normales = normales + 1;
        }
    });
    $("#btn_med_error").html("Error <br/>"+errores);
    $("#btn_med_normal").html("Normal <br/>"+normales);
};

function alarma_variacion(){
    var_sos = parseFloat($("input[name='orig_variacion_sos']").val());
    var_err = parseFloat($("input[name='orig_variacion_err']").val());
    errores = 0
    sospechosos = 0
    normales = 0
    $(".seleccionado > .var_con").each(function(){
        variacion = parseFloat($(this).html().trim());
        if ( variacion < var_sos ){
            $(this).addClass("normal");
            normales = normales + 1;
        }else if ( variacion < var_err ){
            $(this).addClass("sospechoso");
            sospechosos = sospechosos +1;
        }else if ( variacion >= var_err ){
            $(this).addClass("error");
            errores = errores +1 ;
        }

    });
    $("#btn_var_normal").html("Norm. <br/>"+normales);
    $("#btn_var_sospechoso").html("Sosp. <br/>"+sospechosos);
    $("#btn_var_error").html("Error <br/>"+errores);
};


function alarma_valores_atipicos(){
    errores = 0
    normales = 0
    $(".seleccionado > .stddev").each(function(){
        if ( $(this).hasClass('error') ){
            errores = errores +1;
        }else{
            normales = normales +1;
        }
    });
    $("#btn_dev_error").html("Extr. <br/>" + errores);
    $("#btn_dev_normal").html("Normal <br/>" + normales);
};

menu0_err_fechahora = "<div class='dropdown open' id='habilitar_fecha'><span data-toggle='dropdown' aria-expanded='true'></span><ul class='dropdown-menu'><li><p onclick='habilitar_esta_fecha(this)'>Habilitar esta fecha</p></li></ul></div>";
menu0_fechahora = "<div class='dropdown open' id='anular_fecha0'><span data-toggle='dropdown' aria-expanded='true'></span><ul class='dropdown-menu'><li><p onclick='anular_esta_fecha(this)'>Anular esta fecha</p></li><li><p onclick='anular_desde_aqui(this)'>Anular desde aquí</p></li></ul></div>";
menu0 = false;
menu1_fechahora = "<div class='dropdown open' id='anular_fecha1'><span data-toggle='dropdown' aria-expanded='true'></span><ul class='dropdown-menu'><li><p onclick='anular_hasta_aca(this)'>Anular hasta aquí</p></li><li><p onclick='anular_cancelar(this)'>Cancelar</p></li></ul></div>";
id_fila = null;


function habilitar_esta_fecha(e){
    $(e).parent().parent().parent().parent().removeClass('error').addClass('normal');
    $("#habilitar_fecha").remove();
    alarma_fecha();
}



function anular_esta_fecha(e){
    $(e).parent().parent().parent().parent().removeClass('normal').addClass('error');
    $("#anular_fecha0").remove();
    alarma_fecha();
}

function anular_desde_aqui(e){
    id_fila=$(e).parent().parent().parent().parent().parent().get(0).id;
    menu0 = true;
    $("#anular_fecha0").remove();
}

function anular_hasta_aca(e){
    id_fila_fin=$(e).parent().parent().parent().parent().parent().get(0).id;

    idIni = parseInt(id_fila);
    idFin = parseInt(id_fila_fin);

    if (idIni > idFin) {
        idTemp = idIni;
        idIni = idFin;
        idFin = idTemp;
    }
    for(i = idIni ;i <= idFin ; i++){
        $("#"+i).children('.fecha').removeClass('normal').addClass('error');
    }
    menu0 = false;
    id_fila = null;
    $("#anular_fecha1").remove();
    alarma_fecha();
}


function anular_cancelar(e){
    menu0 = false;
    id_fila = null;
    $("#anular_fecha1").remove();
    alarma_fecha();
}


function validacion_cancelar_valor(element){
    var celda = $(element).closest("td");
    var valor_original = celda.find("input[name='validacion_original']").val();
    celda.text(valor_original);
}


function validacion_aceptar_valor(element){
    celda = $(element).closest("td");
    valor_nuevo_str = celda.find("input[name='validacion_nuevo']").val();
    valor_original_str = celda.find("input[name='validacion_original']").val();
    valor_nuevo = Number(valor_nuevo_str);
    if (isNaN(valor_nuevo)){
        validacion_cancelar_valor(element);
        return;
    }
    valor_original = Number(valor_original_str);
    if (valor_nuevo == valor_original){
        validacion_cancelar_valor(element);
        return;
    }
    celda.text(valor_nuevo);
    celda.removeClass("cambio").removeClass("validado").removeClass("no-validado").addClass("cambio");
    alarma_validacion();
    row_id = celda.closest("tr").attr("id");
    $("#comentario_content").find("input[name='row_id']").val(row_id);
    $("#comentario_overlay, #comentario_content").addClass("active");
    $("#id_comentario_dialog").dialog();
}



function validacion_enviar(){
    // Eliminando posibles menúes de anulación/masivo
    $("#anular_fecha0").remove();
    $("#anular_fecha1").remove();
    $("#habilitar_fecha").remove();

    $("#mensaje_overlay").addClass("active");
    $("#gif_loading").show();

    // Inicia iteración de fechas
    cambios = [];

    $(".seleccionado > .fecha").each(function(){
        fila = $(this).parent();
        fecha = $(this).text().trim();
        if ($(this).hasClass('error')){
            valor = null;
        }else{
            valor = $(fila).children('.validacion').text().trim();
            if (valor == ""){valor = null;}
        }
        comentario = null;
        if ($(fila).children('.validacion').hasClass('cambio')){
            comentario = $(fila).children('.comentario').text().trim();
            if (comentario == "") {comentario = null}
        }
        cambios.push({fecha: fecha, valor: valor, comentario: comentario});
    });


    if (cambios.length == 0){
        $("#mensaje_overlay, #mensaje_content").addClass("active");
        $("#mensaje_content").css("background", "rgba(210, 210, 210, 0.8)");
        $("#mensaje_texto").text("Sin cambios.");
        return;
    }

    token = $("input[name='csrfmiddlewaretoken']").val();
    estacion_id = $("input[name='orig_estacion_id']").val();
    variable_id = $("input[name='orig_variable_id']").val();
    fecha_inicio = $("input[name='orig_fecha_inicio']").val();
    fecha_fin = $("input[name='orig_fecha_fin']").val();
    comentario_general = $("textarea[name='comentario_general']").val();

    $.ajax({
        url: '/ajax/validacion_enviar/',
        data: {
            'csrfmiddlewaretoken': token,
            'estacion_id': estacion_id,
            'variable_id': variable_id,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'comentario_general' : comentario_general,
            'cambios': JSON.stringify(cambios)
        },
        type:'POST',
        success: function (data) {
            $("#gif_loading").hide();
            if (data.resultado){
                $("#mensaje_overlay, #mensaje_content").addClass("active");
                $("#mensaje_content").css("background", "rgba(127, 255, 127, 0.8)");
                $("#mensaje_texto").text("Validación exitosa");
            }else{
                $("#mensaje_overlay, #mensaje_content").addClass("active");
                $("#mensaje_content").css("background", "rgba(255, 127, 127, 0.8)");
                $("#mensaje_texto").text("Error en validación");
                error_validacion = true
            }
        },
        error: function () {
            $("#gif_loading").hide();
            $("#mensaje_overlay, #mensaje_content").addClass("active");
            $("#mensaje_content").css("background", "rgba(255, 127, 127, 0.8)");
            $("#mensaje_texto").text("Error: Validación no fue generada");

            alert("Soy un error en la validacion pero no se cual ")
            error_validacion = true;
        }
    });
}



$(document).ready(function() {
    let ls = parseFloat($("input[name='orig_lim_sup']").val());
    let li = parseFloat($("input[name='orig_lim_inf']").val());
    $("input[name='lim_sup']").val(ls)
    $("input[name='lim_inf']").val(li)
    alarma_fecha();
    alarma_validacion();
    alarma_medicion();
    alarma_variacion();
    alarma_valores_atipicos();

    $("#btn_fec_error").click(function(){
        $(".fecha.error").first().closest("tr").get(0).scrollIntoView();
    });

    $("#btn_fec_normal").click(function(){
        $(".fecha.normal").first().closest("tr").get(0).scrollIntoView();
    });

    $("#btn_fec_salto").click(function(){
        $(".fecha.salto").first().closest("tr").get(0).scrollIntoView();
    });

    $("#btn_val_nuevo").click(function(){
        $(".validacion.no-validado").first().closest("tr").get(0).scrollIntoView();
    });
   
    $("#btn_val_ya_validado").click(function(){
        $(".validacion.validado").first().closest("tr").get(0).scrollIntoView();
    });
    
    $("#btn_val_cambio").click(function(){
        $(".validacion.cambio").first().closest("tr").get(0).scrollIntoView();
    });



    $("#btn_med_error").click(function(){
        $(".valor.error").first().closest("tr").get(0).scrollIntoView();
    });

    $("#btn_med_normal").click(function(){
        $(".valor.normal").first().closest("tr").get(0).scrollIntoView();
    });



    $("#btn_var_normal").click(function(){
        $(".var_con.normal").first().closest("tr").get(0).scrollIntoView();
    });

    $("#btn_var_sospechoso").click(function(){
        $(".var_con.sospechoso").first().closest("tr").get(0).scrollIntoView();
    });

    $("#btn_var_error").click(function(){
        $(".var_con.error").first().closest("tr").get(0).scrollIntoView();
    });

    $("#btn_dev_error").click(function(){
        $(".stddev.error").first().closest("tr").get(0).scrollIntoView();
    });

    $("#btn_dev_normal").click(function(){
        $(".stddev.normal").first().closest("tr").get(0).scrollIntoView();
    });


    $('.seleccionado > .fecha').dblclick(function(){
        $("#anular_fecha0").remove();
        $("#anular_fecha1").remove();
        $("#habilitar_fecha").remove();

        if ($(this).hasClass('error')){
            $(this).append(menu0_err_fechahora);
            return;
        }

        if (menu0 == false){
            $(this).append(menu0_fechahora);
        }else{
            $(this).append(menu1_fechahora);
        }
    });



    $('.seleccionado > .validacion').dblclick(function(){
        // Si la fecha tiene error, no permite cambiar valor
        if ($(this).parent().children('.fecha').hasClass('error')){ return;}

        $("input[name='validacion_nuevo']").each(function(){
            var celda = $(this).closest("td");
            var valor_original = celda.find("input[name='validacion_original']").val();
            parent.text(valor_original);
        });

        valor = $(this).text();
        $(this).text("");
        input = '<input type="text" name="validacion_nuevo" value="'+valor+'" size="4">';
        original = '<input type="hidden" name="validacion_original" value="' + valor + '">';
        boton_ok = '<button type="button" class="btn btn-success" onclick="validacion_aceptar_valor(this)"><span class="fas fa-check" style="font-size:10px;"></span></button>';
        boton_no = '<button type="button" class="btn btn-danger" onclick="validacion_cancelar_valor(this)"><span class="fas fa-times" style="font-size:10px;"></span></button>';
        $(this).append(  input + original + boton_ok + boton_no );
        $("input[name='validacion_nuevo']").focus();
    });

    $("#btn_guardar_comentario").click(function(){
        row_id =  $("#comentario_content").find("input[name='row_id']").val();
        comentario = $(this).closest(".dialog").find("textarea[name='nuevo_comentario']").val();
        $('#' + row_id).find('.comentario').text(comentario);
        $('#' + row_id).find('.comentario').addClass('cambio');
        $("#comentario_overlay, #comentario_content").removeClass("active");
        $("#comentario_content").find("input[name='row_id']").val("");
        $(this).closest(".dialog").find("textarea[name='nuevo_comentario']").val("");
        $(this).closest(".dialog").dialog("close");
    });

    $("#btn_sin_comentario").click(function(){
        $("#comentario_overlay, #comentario_content").removeClass("active");
        $("#comentario_content").find("input[name='row_id']").val("");
        $(this).closest(".dialog").find("textarea[name='nuevo_comentario']").val("");
        $(this).closest(".dialog").dialog("close");
    });


    $("#limites_cambiar").click(function(){
        lim_sup = $("input[name='lim_sup']").val();
        lim_inf = $("input[name='lim_inf']").val();
        alarma_medicion();
    });

    $("#limites_reset").click(function(){
        lim_sup = parseFloat($("input[name='orig_lim_sup']").val());
        $("input[name='lim_sup']").val(lim_sup);
        lim_inf = parseFloat($("input[name='orig_lim_inf']").val());
        $("input[name='lim_inf']").val(lim_inf);
        alarma_medicion();
    });

    $("#btn_validacion_enviar").click(function(){
        validacion_enviar();
    });
});
