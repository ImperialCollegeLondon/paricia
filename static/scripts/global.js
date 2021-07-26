( function( factory ) {
	if ( typeof define === "function" && define.amd ) {
		define( [ "../widgets/datepicker" ], factory );
	} else {
		factory( jQuery.datepicker );
	}
}( function( datepicker ) {

datepicker.regional.es = {
	closeText: "Cerrar",
	prevText: "&#x3C;Ant",
	nextText: "Sig&#x3E;",
	currentText: "Hoy",
	monthNames: [ "enero","febrero","marzo","abril","mayo","junio",
	"julio","agosto","septiembre","octubre","noviembre","diciembre" ],
	monthNamesShort: [ "ene","feb","mar","abr","may","jun",
	"jul","ago","sep","oct","nov","dic" ],
	dayNames: [ "domingo","lunes","martes","miércoles","jueves","viernes","sábado" ],
	dayNamesShort: [ "dom","lun","mar","mié","jue","vie","sáb" ],
	dayNamesMin: [ "Do","Lu","Ma","Mi","Ju","Vi","Sa" ],
	weekHeader: "Sm",
	dateFormat:"yy-mm-dd",
	firstDay: 1,
	isRTL: false,
	showMonthAfterYear: false,
	yearSuffix: "" };
datepicker.setDefaults( datepicker.regional.es );

return datepicker.regional.es;

} ) );


function iniciar_datepicker_generic(e){
    $(e).datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "yy-mm-dd",
        showButtonPanel: true,
        onClose: function(dateText, inst) {
        },
        yearRange: '2000:'+(new Date).getFullYear()
    }).focus(function () {
        $("#ui-datepicker-div").position({ my: "left top", at: "left bottom", of: $(e)});
    });
}


var DATATABLES_LANGUAGE = {
            "lengthMenu": "Mostrar _MENU_ registros por página",
            "zeroRecords": "No hay registros",
            "info": "Página _PAGE_ de _PAGES_",
            "infoEmpty": "No hay registros",
            "infoFiltered": "(filtrados de _MAX_ registros totales)",
            "search":         "Buscar:",
            "paginate": {
                "first":      "Primero",
                "last":       "Último",
                "next":       "Sig.",
                "previous":   "Ant."
            },
        };


function mostrar_label_dentro_de_select(){
   //// Elemento SELECT muestre label dentro de su caja
    $('select.use-placeholder').each(function(){
        var op0 = $(this).children('option:first-child');
        if (op0.is(':selected')) {
            op0.css( "display", "none" );
            $(this).addClass('placeholder');
            var label_text = $(this).parent('div').children('label').text();
            op0.text(label_text);
        }
    });

    //// Elemento SELECT oculte o muestre selección nula
    $('select.use-placeholder').change(function() {
        var op0 = $(this).children('option:first-child');
        if (op0.is(':selected')) {
            op0.css( "display", "none" );
            $(this).addClass('placeholder');
            var label_text = $(this).parent('div').children('label').text();
            op0.text(label_text);
        } else {
            op0.css( "display", "" );
            $(this).removeClass('placeholder');
            op0.text("---------");
        }
    });
}


function activar_tooltip(e){
    var etiqueta = e.find('label').html();
    e.attr('data-original-title', etiqueta);
    e.tooltip();

    e.on("click", function(){
        $(this).tooltip('hide');
    });
}


$(document).ready(function() {

    //// Desactivar tecla ENTER para enviar formulario
    $("form").keypress(function(e) {
        if (e.which == 13) {
            // Pulsó ENTER
            return false;
        }
    });

    mostrar_label_dentro_de_select();

});


/*
//// Remueve la barra menú cuando se hace scroll hacia abajo. Y la reaparece cuando se sube
var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
  var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    document.getElementById("menu_navbar").style.top = "0";
  } else {
    document.getElementById("menu_navbar").style.top = "-50px";
  }
  prevScrollpos = currentScrollPos;
}
*/

//// muestra globo de texto tooltip cuando una celda no muestra el contenido completo (ver clase td text-overflow)
$(document).on('mouseenter', '.overflowtooltip th, .overflowtooltip td', function() {
    var $this = $(this);
    if(this.offsetWidth < this.scrollWidth ){
        $this.tooltip();
        if( !$this.attr('data-original-title')){
            $this.attr('data-original-title', $this.text());
        }
        $this.tooltip('show');
    }else{
        $this.tooltip('hide');
    }
});

/////
// Para Botones en DataTables

function btn_detalle_html(rel_url){
    btn_html = "<a href='#' onclick='window.dt_ir(this, \"URL\")'><i class='fas fa-eye fa-sm fa-fw'></i></a>";
    return btn_html.replace('URL', rel_url );
}

function btn_editar_html(rel_url){
    btn_html = "<a href='#' onclick='window.dt_ir(this, \"URL\")'><i class='fas fa-pen fa-sm fa-fw'></i></a>";
    return btn_html.replace('URL', rel_url );
}

function btn_eliminar_html(rel_url){
    btn_html = "<a href='#' onclick='window.dt_ir(this, \"URL\")'><i class='fas fa-trash fa-sm fa-fw'></i></a>";
    return btn_html.replace('URL', rel_url );
}

function dt_ir(e, rel_url){
    var dt = $(e).parents('table').DataTable();
    var data = dt.row( $(e).parents('tr') ).data();
    window.location.href = rel_url.replace('0', data[0]);
};


/////////////////////////////////////////////////////////////
///            Datatables
