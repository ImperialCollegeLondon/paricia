

function getDate(element) {
    var date;
    try {
        date = $.datepicker.parseDate(dateFormat, element.value);
    } catch( error ) {
        date = null;
    }
    return date;
}

// Función para controlar la acción de la lista de estaciones
function accion_click(e){
    // obtener el id de la estacion
    estacion_id = e.closest("tr").id;
    // actualizar la caja de texto oculta
    $("#id_estacion").val(estacion_id).trigger("chosen:updated");
    //Saber que boton aplasto por el nombre del mismo
    var accion = e.name;
    $("input[name=accion]").val(accion);
    if (accion == "grafico"){
        $.ajax({
            url: $("#form_consultas").attr('action'),
            data: $("#form_consultas").serialize(),
            type:'POST',
            beforeSend: function () {
                //$("#mensaje_overlay, #mensaje_content").addClass("active");
                $("#modal_grafico").modal("show")
                $("#div_loading_grafico").show();
                $("#div_error_grafico").hide();
            },
            success: function (data) {
                //$("#grafico").html(data)

                $("#grafico").show();
                var count = Object.keys(data.data[0].y).length;
                if (count>0) {
                    Plotly.newPlot('grafico', data.data,data.layout);

                }
                else{
                    $("#grafico").html('<label>No hay información para los parametros ingresados</label>')
                }

                $("#div_loading_grafico").hide();
                $("#div_errorgraf").hide();

            },
            error: function () {
                $("#div_loading_grafico").hide();
                $("#div_error_grafico").show();
            }

        });
    }else{
        $(".form").submit();
    }

};



function cargar_cuencas(sistema){
    if (sistema == undefined){sistema = ""}
    $("#id_cuenca").prop( "disabled", true );
    $("#id_cuenca").find('option').remove().end()
    $("#id_cuenca").append('<option value selected>---------</option>');
    $.ajax({
        url: '/ajax/reportes_cuencas/',
        data: {
        'sistema_id': sistema
        },
        dataType: 'json',
        success: function (data) {
            $.each(data, function(index, value) {
                $("#id_cuenca").append('<option value="' + index + '">' + value + '</option>');
            });
        }
    });
    $("#id_cuenca").prop( "disabled", false );
}


function cargar_estaciones(){
    sistema = "";
    cuenca = "";
    variable = "";
    estacion_tipo = "";

    filtro_id = $('input:radio[name=filtro]:checked').val();
    variable = $("#id_variable").val();
    switch(filtro_id){
        case 'sistema_cuenca':
            sistema = $("#id_sistema").val();
            cuenca = $("#id_cuenca").val();
            break;
    }

    estacion_tipo=$("input[name=estacion_tipo_id]").val();

    $.ajax({
        url: '/ajax/reportes_estaciones/',
        data: {
            'variable_id': variable,
            'sistema_id': sistema,
            'cuenca_id': cuenca,
            'estacion_tipo_id': estacion_tipo,
        },
        dataType: 'json',
        success: function (data) {
            $(".table tbody tr").remove().end();

            $.each(data.estaciones, function(index, value) {
                $(".table tbody").append("<tr id=" + index + "><td>" + value + "</td><td>" + botones + "</td></tr>");
            });


        }
    });

}


function filtro_todas_estaciones(){
    $("#div_mapa").hide();
    $("#id_sistema").val($("#id_sistema option:first").val());
    $("#id_sistema").prop( "disabled", true );
    $("#id_cuenca").find('option').remove().end();
    $("#id_cuenca").append('<option value selected>---------</option>');
    $("#id_cuenca").prop( "disabled", true );
    $(".sistema-cuenca").css("display", "none");
    cargar_estaciones();
}

function filtro_sistema_cuenca(){
    $(".table tbody tr").remove().end();
    $("#div_mapa").hide();
    $("#id_sistema").prop( "disabled", false );
    cargar_cuencas();
    $(".sistema-cuenca").css("display", "block");
    cargar_estaciones();
}


$(document).ready(function() {

    filtro_todas_estaciones();

    $("#id_filtro").change(function () {
        filtro_id = $('input:radio[name=filtro]:checked').val();
        switch(filtro_id){
            case 'sistema_cuenca':
                filtro_sistema_cuenca();
                break;
            default:
                filtro_todas_estaciones();
        }
    });


    $("#id_variable").change(function () {
        cargar_estaciones();
    });


    $("#id_sistema").change(function () {
        sistema = $(this).val();
        cargar_cuencas(sistema);
        cargar_estaciones();
    });


    $("#id_cuenca").change(function () {
        cargar_estaciones();
    });



    /*$(".open").on("click", function(){
        $("#botones").hide();
        var src_img = $("#mapa").attr("src");
        $("#mapa-grande").attr("src", src_img );
        $(".popup-overlay, .popup-content").addClass("active");

    });
    */


   /* $(".close, .popup-overlay").on("click", function(){
        let btclo= $(this).attr('id');
        if(btclo=='clover'){
            $("#botones").show();
            $(".popup-overlay, .popup-content").removeClass("active");
         }
    });*/


    $("#respuesta").on("click", function(){
        $(".texto").empty();
        $("#respuesta").hide();
    });

});