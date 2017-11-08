var player = null;
var active = null;
var tracks = null;

function createPlyr() {
  var plyrElement = document.querySelector('.plyr');
  var playlist = document.querySelector('.playlist');
  plyr.setup(plyrElement);
  player = plyrElement.plyr;
  tracks = playlist.querySelectorAll('.playlist--list li');

  for (var i = 0; i < tracks.length; i++) {
    tracks[i].onclick = changeChannel;
  }

  if (tracks.length > 0)
    setSource(getId(tracks[0]));

  plyrElement.addEventListener('ended', nextSong);
}

function changeChannel(e) {
  setSource(getId(e.target), true);
}

function getId(el) {
  return Number(el.getAttribute('data-id'));
}

function setSource(selected, play) {
  if (active !== selected) {
    active = selected;

    for (var i = 0; i < tracks.length; i++) {
      if (Number(tracks[i].getAttribute('data-id')) === selected) {
        var track = tracks[i];
        var title = track.getAttribute('data-title');
        var trackId = track.getAttribute('data-track-id');

        var audioLink = track.getAttribute('data-audio');
        if (audioLink == null) {
          $.getJSON("/audio_info/" + trackId, function(data) {
            if (!data.has_error) {
              var link = decodeLink(data.result.link);
              track.setAttribute('data-audio', link);
              track.className = 'active';

              playAudio(link, title, play);
            }
          });
        }
        else {
          playAudio(audioLink, title, play);
        }
      } else {
        tracks[i].className = '';
      }
    }
  }
}

function playAudio(link, title, play) {
  var sourceAudio = [{ src: link, type: 'audio/mp3' }];

  player.source({ type: 'audio', title: title, sources: sourceAudio });

  if (play) {
    player.play();
  } else {
    player.togglePlay();
  }
}

function nextSong(e) {
  var next = active + 1;
  if (next < tracks.length) {
    setSource(getId(tracks[next]), true);
  }
}