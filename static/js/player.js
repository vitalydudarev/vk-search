
      function initPlayer() { 
        // Setup the player to autoplay the next track
        var a = audiojs.createAll({
          trackEnded: function() {
            var next = $('#search_results a.playing').next()
            if (!next.length) next = $('#search_results a').first();
            next.addClass('playing').siblings().removeClass('playing');
            audio.load(next.attr('data-src'));
            audio.play();
          }
        });
        
        // Load in the first track
        var audio = a[0];
            first = $('#search_results a').attr('data-src');
        $('#search_results a').first().addClass('playing');
        audio.load(first);

        // Load in a track on click
        $('#search_results a').click(function(e) {
          e.preventDefault();
          $(this)
            .addClass('playing').addClass('active').siblings()
            .removeClass('playing').removeClass('active');
          var trackId = $(this).attr('track-id');

          var attr = $(this).attr('data-src');

          if (typeof attr === typeof undefined || attr === false) {
            var elem = $(this);

            $.getJSON("/audio_info/" + trackId, function(data) {
              if (!data.has_errors) {
                url = decodeLink(data.result.link);
                elem.attr('data-src', url);
                audio.load(url);
                audio.play();
              }
            });
          }
          else {
            audio.load(attr);
            audio.play();
          }
        });
        // Keyboard shortcuts
        $(document).keydown(function(e) {
          var unicode = e.charCode ? e.charCode : e.keyCode;
             // right arrow
          if (unicode == 39) {
            var next = $('li.playing').next();
            if (!next.length) next = $('ol li').first();
            next.click();
            // back arrow
          } else if (unicode == 37) {
            var prev = $('li.playing').prev();
            if (!prev.length) prev = $('ol li').last();
            prev.click();
            // spacebar
          } else if (unicode == 32) {
            audio.playPause();
          }
        })
      };