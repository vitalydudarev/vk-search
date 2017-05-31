function setView(jData) {
  var pData = JSON.parse(jData);
  if (pData.has_error) {
    $("#weather a").text("Weather unavailable");
  }
  else {
    $("#weather").attr('data', JSON.stringify(pData))
    $("#weather").text(pData.result.condition.temp + '° ' + pData.result.condition.text);

    $("#weather").popover({ html: true, animation: true, trigger: "hover", placement: 'auto' })
      .on("show.bs.popover", function () {
        var _this = this;
        var data = $('#weather').attr('data');

        var body = "";
        var jsoned = JSON.parse(data)

        var tbody = $('<tbody/>');
        var table = $('<div/>').attr('class', 'table-responsive')
          .append($('<table/>').attr('class', 'table table-bordered')
            .append(tbody));

        $.each(jsoned.result.forecast, function (index, item) {
          var td1 = $('<td/>').text(item.day + ", " + item.date);
          var td2 = $('<td/>').text(item.high + "° " + item.low + "°");
          var td3 = $('<td/>').text(item.text);

          tbody.append($('<tr/>').append(td1, td2, td3));
        });

        $('#weather').attr('data-content', table.html())
      });
  }
}