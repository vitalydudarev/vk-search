function setView(jData) {
  var pData = JSON.parse(jData);

  $("#weather").attr('data', JSON.stringify(pData))
  $("#weather a" ).text(pData.result.condition.temp + '° ' + pData.result.condition.text);

  $("#weather").popover({ html: true, animation: true, trigger: "click", placement: 'auto' })
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