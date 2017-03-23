function loadAudio(element, audioControl) {
  element
    .addClass('playing').addClass('active').siblings()
    .removeClass('playing').removeClass('active');

  var trackId = element.attr('track-id');
  var attr = element.attr('data-src');

  if (typeof attr === typeof undefined || attr === false) {
    $.getJSON("/audio_info/" + trackId, function(data) {
      if (!data.has_error) {
        url = decodeLink(data.result.link);
        element.attr('data-src', url);
        audioControl.load(url);
        audioControl.play();
      }
    });
  }
  else {
    audioControl.load(attr);
    audioControl.play();
  }
}

function initPlayer() { 
  // Setup the player to autoplay the next track
  var audioElements = document.getElementsByTagName('audio');
  var audioControl = audiojs.create(audioElements[0], {
    trackEnded: function() {
      var next = $('#search_results a.playing').next()
      if (!next.length) 
        next = $('#search_results a').first();
      loadAudio(next, audioControl);
    }
  });
  
  // Load in the first track
  var first = $('#search_results a').attr('data-src');
  $('#search_results a').first().addClass('playing');
  audioControl.load(first);

  // Load in a track on click
  $('#search_results a').click(function(e) {
    e.preventDefault();
    loadAudio($(this), audioControl);
  });

  // Keyboard shortcuts
  $(document).keydown(function(e) {
    var unicode = e.charCode ? e.charCode : e.keyCode;
       // right arrow
    if (unicode == 39) {
      var next = $('#search_results a.playing').next();
      if (!next.length) next = $('ol li').first();
      next.click();
      // back arrow
    } else if (unicode == 37) {
      var prev = $('#search_results a.playing').prev();
      if (!prev.length) prev = $('ol li').last();
      prev.click();
      // spacebar
    } else if (unicode == 80) {
      audioControl.playPause();
    }
  })
};