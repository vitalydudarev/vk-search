function toTime(sec) {
    var secNum = parseInt(sec, 10); // don't forget the second param
    var hours   = Math.floor(secNum / 3600);
    var minutes = Math.floor((secNum - (hours * 3600)) / 60);
    var seconds = secNum - (hours * 3600) - (minutes * 60);

    if (hours > 0 && minutes < 10) {
        minutes = "0" + minutes;
    }

    if (seconds < 10) {
        seconds = "0" + seconds;
    }

    if (sec < 3600)
        return minutes + ':' + seconds;
    else
        return hours + ':' + minutes + ':' + seconds;
}