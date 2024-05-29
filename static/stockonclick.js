$(document).ready(function() {
    $('.stock').on('click', function() {
      var stock = $(this).text();
      window.location.href = '/stock/' + stock;
    });
});