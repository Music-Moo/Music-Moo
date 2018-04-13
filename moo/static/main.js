// Search bar animations
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

// Pressing ENTER to search in search bar
function submit() {
  document.searchForm.submit();
}

// Download button on videos
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

// Download button to download all the playlist
$('.videos').click(function(){
  $.ajax({
    type: 'GET',
    url: '/download/' + this.value,
  });
  $(this).attr("disabled", true);
});
