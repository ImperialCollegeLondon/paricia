function actualizar_lista(enlace){
  $("#btn_filtrar").attr('disabled',true);
  $.ajax({
    url: enlace,
    data: $("#form_consulta").serialize(),
    type:'POST',
    beforeSend: function () {
      $("#div_informacion").hide();
      $("#div_loading").show();
      $("#div_error").hide();
    },
    success: function (data) {
      $("#div_informacion").show();
      $("#div_informacion").html(data)
      $("#div_loading").hide();
      $("#div_error").hide();
      $("#btn_filtrar").removeAttr('disabled');
    },
    error: function () {
      $("#div_loading").hide();
      $("#div_error").show();
      $("#btn_filtrar").removeAttr('disabled');
    }
  });
}
function guardar_registro(){
    $.ajax({
        url:$("#form_save").attr('action'),
        type:'POST',
        data: $("#form_save").serialize(),
        beforeSend: function () {
            $("#div_edit").dialog( "close" );
            $("#div_edit").html('')
            activar_espera();
        },
        success: function (data) {
            actualizar_lista();
        },
        error: function (request, status, error) {
            $("#div_informacion").hide();
            $("#div_loading").hide();
            mostrar_errores(request)
            $("#div_error").show();
            cerrar_cuadro_dialogo();
          //$("#btn_procesar").removeAttr('disabled');

        }
    });
}
function mostrar_errores(request){
    var obj = jQuery.parseJSON(request.responseText);
    $("#div_message_error").html('');
    for (var i in obj) {
        $("#div_message_error").append(obj[i][0]+'<br>');
    }
}

function eliminar_registro(){
    $.ajax({
        url:$("#form_delete").attr('action'),
        type:'POST',
        data: $("#form_delete").serialize(),
        beforeSend: function () {
            $( "#div_delete" ).dialog( "close" );
            $( "#div_delete" ).html('');
            activar_espera();
        },
        success: function (data) {
            actualizar_lista();
        }
    });

}
function abrir_cuadro_dialogo(div,enlace){
    $("#div_error").hide();
    var object="#"+div;
    $.ajax({
        url: enlace,
        type:'GET',
        beforeSend: function () {
            $("#div_loading").show();
            $("#div_informacion").hide();
        },
        success: function (data) {
            $(object).html(data);
            $(object).dialog( "open" );
            desactivar_espera()
        },
        error: function () {
            $("#div_loading").hide();
            $("#div_error").show();
        }
    });
    //$(object).dialog( "open" );
}
function cerrar_cuadro_dialogo(){
    var isOpen = $( "#div_edit" ).dialog( "isOpen" );
    console.log(isOpen)
    if (isOpen) {
        $( "#div_edit" ).dialog( "close" );
    }
    isOpen = $( "#div_create" ).dialog( "isOpen" );
    console.log(isOpen)
    if (isOpen) {
        $( "#div_create" ).dialog( "close" );
    }
    isOpen = $( "#div_delete" ).dialog( "isOpen" );
    console.log(isOpen)
    if (isOpen) {
        $( "#div_delete" ).dialog( "close" );
    }
}
function activar_espera(){
  $("#div_loading").show();
  $("#div_informacion").hide();
}
function desactivar_espera(){
  $("#div_loading").hide();
  $("#div_informacion").show();
}


function actualizar_informacion(){
  $.ajax({
    url: $("#link_consulta").attr('href'),
    type:'GET',
    beforeSend: function () {
      $("#div_informacion").hide();
      $("#div_loading").show();
      $("#div_error").hide();
    },
    success: function (data) {
      $("#div_informacion").show();
      $("#div_informacion").html(data)
      $("#div_loading").hide();
      $("#div_error").hide();

    },
    error: function () {
      $("#div_loading").hide();
      $("#div_error").show();
      $("#div_delete").dialog("open");
    }
  });

}

$(document).ready(function() {

  $("#form_consulta").submit(function(event){
    //actualizar_lista($("#form_consulta").attr('action'));
    event.preventDefault();
  });
});