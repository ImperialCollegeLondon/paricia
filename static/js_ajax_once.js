
$(document).ready(function() {
    $( "#div_new" ).dialog({
        autoOpen: false,
        width:400,
        height:400
    });
    $("#link_new").click(function(){
        $("#div_new").dialog("open");
        return false;
    });
    //crear registro
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
        document.getElementById("form_new").reset();
        return false;
    });

    $("#id_estacion").autocomplete({
        source: "/estacion/search",
        minLength: 2,
        select: function (event, ui) { //item selected
            AutoCompleteSelectHandler(event, ui)
        },
    });

    function AutoCompleteSelectHandler(event, ui)
    {
        var selectedObj = ui.item;
    }



});


