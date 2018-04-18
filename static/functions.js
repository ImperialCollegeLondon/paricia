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
