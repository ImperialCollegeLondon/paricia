var plot_orig_width = 0;
var plot_adjusted = true;
var gid = 0;

btn_adjust_plot = "<button id='resize_plot' class='btn btn-success btn-xs' onclick='resizePlot()'> &gt Un pixel por dato &lt </button>";

function plot_adjust(){
    var window_width = $("#imagemodal").width();
    Plotly.relayout(gid, {width: window_width });
    $("#" + gid).css("width", "");
    plot_adjusted = true;
    $('#resize_plot').html("&gt Un pixel por dato &lt");
}

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

function getDate(element) {
    var date;
    try {
        date = $.datepicker.parseDate(dateFormat, element.value);
    } catch( error ) {
        date = null;
    }
    return date;
}

function activar_espera(){
    $('#div_loading').css('visibility', 'visible');
//    $("#div_informacion").hide();
}

function desactivar_espera(){
    $('#div_loading').css('visibility', 'hidden');
//    $("#div_informacion").show();
}

function accion_click(e){
    var valido = $("#form_consultas")[0].checkValidity();
    if (!valido) {
        $("#grafico").append("<label>Ingrese los campos requeridos: Frecuencia, Variable.</label>");
        $("#imagemodal").modal('show');
        return;
    }

    estacion_id = e.closest("tr").id;
    $("#id_estacion_id").val(estacion_id);
    var accion = e.name;
    $("input[name=accion]").val(accion);

    if (accion == "grafico"){

        $.ajax({
            url: url_accion_click(),
            data: $("#form_consultas").serialize(),
            type:'POST',
            beforeSend: function () {
                activar_espera();
            },
            success: function (data) {
                $("#grafico").html(btn_adjust_plot + data);
                $("#imagemodal").modal('show');
                gid = $('.plotly-graph-div,.js-plotly-plot').attr('id');
                plot_orig_width = $("#" + gid).width();
                desactivar_espera();
                plot_adjust();
            },
            error: function () {
                $("#div_error").show();
                desactivar_espera();
            }

        });
    }else{
        $(".form").submit();
    }

};



function cargar_cuencas(sitio){
    activar_espera();
    if (sitio == undefined){sitio = ""}
    $("#id_cuenca").prop( "disabled", true );
    $("#id_cuenca").find('option').remove().end()
    $("#id_cuenca").append('<option value selected>---------</option>');
    $.ajax({
        url: '/ajax/reportes_cuencas/',
        data: {
        'sitio_id': sitio
        },
        dataType: 'json',
        success: function (data) {
            $.each(data, function(index, value) {
                $("#id_cuenca").append('<option value="' + index + '">' + value + '</option>');
            });
            window.mostrar_label_dentro_de_select();
            $("#id_cuenca").prop( "disabled", false );
            desactivar_espera();
        }
    });


}


function cargar_estaciones(){
    $('#div_tabla').hide();
    activar_espera();
    sitio = "";
    cuenca = "";
    variable = "";
    estacion_tipo = "";

    filtro_id = $('input:radio[name=filtro]:checked').val();
    variable = $("#id_variable").val();
    switch(filtro_id){
        case 'sitio_cuenca':
            sitio = $("#id_sitio").val();
            cuenca = $("#id_cuenca").val();
            break;
    }

    estacion_tipo=$("input[name=estacion_tipo_id]").val();

    $.ajax({
        url: '/ajax/estacion_consulta/',
        data: {
            'variable_id': variable,
            'sitio_id': sitio,
            'cuenca_id': cuenca,
            'estacion_tipo_id': estacion_tipo,
        },
        dataType: 'json',
        success: function (data) {
            $('table').DataTable().clear();
            $('table').DataTable().destroy();
            $(".table tbody tr").remove().end();

            $.each(data.estaciones, function(index, value) {
                $(".table tbody").append("<tr id=" + index + "><td>" + value + "</td><td>" + botones + "</td></tr>");
            });

            actualizar_tabla("table");

            if (data.imagen == ""){
                $("#div_mapa").hide();
            }else{
                $("#div_mapa").show();
                $("#mapa").attr("src", data.imagen);
            }

            desactivar_espera();
        }
    });


}


function filtro_todas_estaciones(){
    $("#div_mapa").hide();
    $("#id_sitio").val($("#id_sitio option:first").val());
    $("#id_sitio").prop( "disabled", true );
    $("#id_cuenca").find('option').remove().end();
    $("#id_cuenca").append('<option value selected>---------</option>');
    $("#id_cuenca").prop( "disabled", true );
    $(".sitio-cuenca").css("display", "none");
    cargar_estaciones();
}

function filtro_sitio_cuenca(){
    $(".table tbody tr").remove().end();
    $("#div_mapa").hide();
    $("#id_sitio").prop( "disabled", false );
    cargar_cuencas();
    $(".sitio-cuenca").css("display", "block");
    cargar_estaciones();
}


function consultar_profundidades(){
    $("#id_profundidad").prop( "disabled", true );
    $("#id_profundidad").find('option').remove().end()
    $("#id_profundidad").append('<option value selected>---------</option>');

    $.ajax({
        url: '/ajax/validacion/profundidades/',
        data: {
            'variable_id': $("#id_variable").val()
        },
        dataType: 'json',
        beforeSend: function () {
            activar_espera();
        },
        success: function (data) {
            $.each(data, function(index, value) {
                $("#id_profundidad").append('<option value="' + index + '">' + value + '</option>');
            });
            $("#id_profundidad").prop( "disabled", false );
            desactivar_espera();

        },
        error: function () {
            $("#div_error").show();
            desactivar_espera();
        }
    });

}


function actualizar_tabla(e){
    table = $(e).DataTable({
        language: window.DATATABLES_LANGUAGE,
        scrollY: '50vh',
        scrollCollapse: true,
        paging: false,
        "dom": '<"small"f>rt',
        columnDefs: [
            { "targets": 0, "searchable": true },
            { "targets": 1, "searchable": false  },
        ],
    });

    $('#div_tabla').show();
    table.columns.adjust().draw();

}

function iniciar_datepicker(e){
    $(e).datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "yy-mm-dd",
        showButtonPanel: true,
        onClose: function(dateText, inst) {
            if ( $("#id_frecuencia").val() === "mensual" ){
                var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
                var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
                $(e).datepicker('setDate', new Date(year, month, 1));
            }
        },
        yearRange: '2000:'+(new Date).getFullYear()
    }).focus(function () {
        $("#ui-datepicker-div").position({ my: "center top", at: "center bottom", of: $(e)});
        if ( $("#id_frecuencia").val() == "mensual" ){
            $(".ui-datepicker-calendar").hide();
        } else {
            $(".ui-datepicker-calendar").show();
        }
    });
}

function clean_modal(){
    mapa_fullsize = false;
    $("#mapa_grande").attr("src", "" );
    $("#imagemodal label").remove();
    $("#grafico").empty();
}

var mapa_fullsize = false;

$(document).ready(function() {
    if($("#imagemodal label").length){
        $("#imagemodal").modal('show');
    }

    filtro_todas_estaciones();

    $("#id_filtro").change(function () {
        filtro_id = $('input:radio[name=filtro]:checked').val();
        switch(filtro_id){
            case 'sitio_cuenca':
                filtro_sitio_cuenca();
                break;
            default:
                filtro_todas_estaciones();
        }
    });

    $("#id_variable").change(function () {
        cargar_estaciones();
    });

    $("#id_sitio").change(function () {
        sitio = $(this).val();
        cargar_cuencas(sitio);
        cargar_estaciones();
    });

    $("#id_cuenca").change(function () {
        cargar_estaciones();
    });

    $("#div_mapa .open").on("click", function(){
        var src_img = $("#mapa").attr("src");
        $("#mapa_grande").css("height", "100%");
        $("#mapa_grande").attr("src", src_img );
    });

    $("#imagemodal .close").on("click", function(){
        clean_modal();
    });

    $(document).keyup(function(e) {
        if (e.key === "Escape") {
            clean_modal();
        }
    });

    $("#mapa_grande").on("dblclick", function(){
        if (mapa_fullsize == false){
            $("#mapa_grande").css("height", "auto");
            mapa_fullsize = true;
        }else{
            $("#mapa_grande").css("height", "100%");
            mapa_fullsize = false;
        }
    });

    $("#respuesta").on("click", function(){
        $(".texto").empty();
        $("#respuesta").hide();
    });

/*
    $('.form-group').each(function() {
        window.activar_tooltip($(this));
    });
*/

    desactivar_espera();
});