
$(document).ready(function() {
  $( "#div_new" ).dialog({
    autoOpen: false,
    width:400,
    height:400
  });
  $( "#div_update" ).dialog({
    autoOpen: false,
    width:400,
    height:400
  });
  $( "#div_delete" ).dialog({
    autoOpen: false,
    width:400,
    height:400
  });
  $("#link_new").click(function(){
      $("#div_new").dialog("open");
      return false;
  });
  $("#btn_guardar").click(function(){
    $.ajax({
      url: $("#form_new").attr('action'),
      data: $("#form_new").serialize(),
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
        $("#div_new").dialog("close");
      },
      error: function () {
        $("#div_loading").hide();
        $("#div_error").show();
        $("#btn_filtrar").removeAttr('disabled');
        $("#div_new").dialog("close");
      }
    });
    return false;
  });
  //modificar un registro
  $(".link_update").on('click',function(){
    $.ajax({
      url: $(this).attr('href'),
      type:'GET',
      beforeSend: function () {
        $("#div_informacion").hide();
        $("#div_loading").show();
        $("#div_error").hide();
      },
      success: function (data) {
        $("#div_informacion").show();
        $("#div_update").html(data)
        $("#div_loading").hide();
        $("#div_error").hide();
        $("#div_update").dialog("open");
      },
      error: function () {
        $("#div_loading").hide();
        $("#div_error").show();
        $("#div_update").dialog("open");
      }
    });
    return false;
  });

  //eliminar un registro
  $(".link_delete").on('click',function(){
    $.ajax({
      url: $(this).attr('href'),
      type:'GET',

      beforeSend: function () {
        $("#div_informacion").hide();
        $("#div_loading").show();
        $("#div_error").hide();
      },
      success: function (data) {
        $("#div_informacion").show();
        $("#div_delete").html(data)
        $("#div_loading").hide();
        $("#div_error").hide();
        $("#div_delete").dialog("open");
      },
      error: function () {
        $("#div_loading").hide();
        $("#div_error").show();
        $("#div_delete").dialog("open");
      }
    });
    return false;
  });
  $("#btn_graficar").click(function(){
    $(this).attr('disabled',true);
    $.ajax({
      url: '/reportes/consultas/',
      data: $("#form_busqueda").serialize(),
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
    })
    /*.done(function( data, textStatus, jqXHR ) {

         $("#div_informacion").show();
         Plotly.newPlot('div_informacion', data.data,data.layout);
         $("#btn_graficar").removeAttr('disabled');

        $("#div_loading").hide();

        $("#div_error").hide();
    })*/;
  });


});
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

