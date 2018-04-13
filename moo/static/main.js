$(document).ready(function(){
  $('#searchbar-icon').click(function(){
    $('#searchbar-input').animate({width: 'toggle'});
    $("#searchbar-icon").toggle();
    $("#searchbar-cross").toggle(500);
  });
  
  $('#searchbar-cross').click(function(){
    $('#searchbar-input').animate({width: 'toggle'});
    $("#searchbar-cross").toggle();
    $("#searchbar-icon").toggle(500);
  });

});

$('.video').click(function(){
  $.ajax({
    type: 'POST',
    contentType: 'application/json; charset=utf-8',
    url: '/download',
    data: JSON.stringify({ urls: [this.value] }),
    dataType: 'json',
  });
  $(this).attr("disabled", true);
});

function submit() {
  document.searchForm.submit();
}