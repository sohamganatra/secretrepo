(function($){
  $(function(){

    $('.button-collapse').sideNav();

  }); // end of document ready
})(jQuery); // end of jQuery name space

$(document).ready(function() {
  $('select').material_select();
});

$('.datepicker').pickadate({
  selectMonths: true, // Creates a dropdown to control month
  selectYears: 15, // Creates a dropdown of 15 years to control year
  format: 'yyyy-mm-dd'
});

$("#filter").hide();

var hidden = true;

$("#filter-button").click(function() {
  if (hidden) {
    $("#filter").show();
  } else {
    $("#filter").hide();
  }
  hidden = !hidden;
});
