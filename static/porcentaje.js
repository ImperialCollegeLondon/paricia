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
    $("#btn_porcentaje_error").html("Error <br/>"+errores);
    $("#btn_porcentaje_normal").html("Normal <br/>"+normales);
};

$(document).ready(function() {
    numero_valores();
    numero_porcentaje();

    $("#btn_valor_next").click(function(){
        $(".valor.error").first().closest("tr").get(0).scrollIntoView();
    });

    $("#chk_valor").on("change", function(){
        filtro = document.getElementById("chk_valor").value;

        table = document.getElementById("tbl_data");
        tr = table.getElementsByTagName("tr");
        for (i = 0; i < tr.length; i++) {
            td = tr[i].getElementsByTagName("td")[1];
            if (td) {
                txtValue = td.className;
                if (txtValue.indexOf(filtro) > -1) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }

        }
    });

    $("#chk_porcentaje").on("change", function(){
        filtro = document.getElementById("chk_porcentaje").value;

        table = document.getElementById("tbl_data");
        tr = table.getElementsByTagName("tr");
        for (i = 0; i < tr.length; i++) {
            td = tr[i].getElementsByTagName("td")[2];
            if (td) {
                txtValue = td.className;
                if (txtValue.indexOf(filtro) > -1) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }

        }
    });

});