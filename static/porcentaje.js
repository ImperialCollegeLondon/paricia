function numero_valores(){
    errores = 0
    normales = 0
    $("tr > td").each(function(){
        if ($(this).hasClass('error') ){
            errores = errores + 1;
        }else{
            normales = normales + 1;
        }
    });
    $("#btn_valor_error").html("Error <br/>"+errores);
    $("#btn_valor_normal").html("Normal <br/>"+normales);
};
$(document).ready(function() {
    numero_valores();

    $("#btn_valor_next").click(function(){
        $(".valor.error").first().closest("tr").get(0).scrollIntoView();
    });

});