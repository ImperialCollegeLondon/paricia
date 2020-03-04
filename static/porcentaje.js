function numero_valores(){

    errores = 0
    normales = 0
    $("tr > td").each(function(){
        if ($(this).hasClass('valor error') ){
            errores = errores + 1;
        }else{
            normales = normales + 1;
        }
    });
    $("#btn_valor_error").html("Error <br/>"+errores);
    $("#btn_valor_normal").html("Normal <br/>"+normales);
};
function numero_porcentaje(){

    errores = 0
    normales = 0
    $("tr > .porcentaje").each(function(){
        if ($(this).hasClass('error') ){
            errores = errores + 1;
        }else{
            normales = normales + 1;
        }
    });
    $("#btn_porcentaje_error").html("Menor a 70% <br/>"+errores);
    $("#btn_porcentaje_normal").html("Mayor a 70% <br/>"+normales);
};

$(document).ready(function() {
    numero_porcentaje();


    $("#chk_porcentaje").on("change", function(){
        filtro = document.getElementById("chk_porcentaje").value;
        table = document.getElementById("tbl_data");
        tr = table.getElementsByTagName("tr");
        for (i = 0; i < tr.length; i++) {
            td = tr[i].getElementsByTagName("td")[1];
            console.log(td)
            if (td) {
                txtValue = td.className;
                console.log(txtValue)

                if (txtValue.indexOf(filtro) > -1) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    });

    $(".link-validacion").click(function(e){
        e.preventDefault();
        enlace = $(this).attr('href')
        $.ajax({
            url: enlace,
            type:'GET',
            beforeSend: function () {
                //$("#div_informacion").hide();
                //$("#div_loading").show();
                //$("#div_error").hide();
            },
            success: function (data) {
              $("#div_datos").show();
              $("#div_datos").html(data)
              //$("#div_loading").hide();
              //$("#div_error").hide();

            },
            error: function () {
              //$("#div_loading").hide();
              //$("#div_error").show();
              //$("#btn_filtrar").removeAttr('disabled');
            }
        });
    });

});