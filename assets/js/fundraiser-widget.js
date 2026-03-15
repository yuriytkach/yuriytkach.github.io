/**
 * Fundraiser Widget
 * Displays a circular progress chart with donation data from the fundraiser API.
 *
 * Usage: add a <div class="fundraiser-widget" data-fund-id="FUND_ID"></div>
 * in the page where you want the widget to appear.
 */
(function () {
  const API_BASE = 'https://fundraiser.yuriytkach.com/funds';

  function currSymbol(curr) {
    switch (curr) {
      case 'UAH': return 'грн. ';
      case 'EUR': return '€';
      case 'USD': return '$';
      case 'GBP': return '£';
      default:    return curr + ' ';
    }
  }

  document.querySelectorAll('.fundraiser-widget').forEach(function (widget) {
    var fundId = widget.getAttribute('data-fund-id');
    if (!fundId) return;

    // Build DOM
    var container = document.createElement('div');
    container.className = 'fw-container';

    var chart = document.createElement('div');
    chart.className = 'fw-chart';

    var data = document.createElement('div');
    data.className = 'fw-data';

    var percent = document.createElement('span');
    percent.className = 'fw-percent';

    var raised = document.createElement('span');
    raised.className = 'fw-raised';

    data.appendChild(percent);
    data.appendChild(raised);
    chart.appendChild(data);
    container.appendChild(chart);

    var goal = document.createElement('h2');
    goal.className = 'fw-goal';
    container.appendChild(goal);

    var btn = document.createElement('button');
    btn.className = 'fw-btn';
    btn.innerHTML = '<span>View Donations</span>';
    container.appendChild(btn);

    widget.appendChild(container);

    // Init pie chart
    $(chart).easyPieChart({
      size: 150,
      barColor: '#36e617',
      scaleLength: 0,
      lineWidth: 15,
      trackColor: '#525151',
      lineCap: 'circle',
      animate: 1000
    });

    // Fetch status
    fetch(API_BASE + '/' + fundId + '/status', {
      method: 'GET',
      headers: { 'Accept': 'application/json' }
    })
      .then(function (res) { return res.json(); })
      .then(function (result) {
        var pct = parseInt(result.raised / result.goal * 100);
        var sym = currSymbol(result.currency);
        goal.textContent = sym + result.goal;
        raised.textContent = sym + result.raised;
        percent.textContent = pct + '%';
        $(chart).data('easyPieChart').update(pct);
      })
      .catch(function (e) { console.log(e); });

    // View Donations button
    btn.addEventListener('click', function () {
      fetch(API_BASE + '/' + fundId + '/funders', {
        method: 'GET',
        headers: { 'Accept': 'application/json' }
      })
        .then(function (res) { return res.json(); })
        .then(function (result) {
          var table = document.createElement('table');
          for (var i = 0; i < result.length; i++) {
            var time = dayjs(result[i].fundedAt).format('YYYY-MM-DD HH:mm');
            table.innerHTML += '<tr><td style="text-align:left"><b>'
              + result[i].name
              + '</b></td><td style="width:100px;text-align:right">'
              + result[i].amount + ' ' + result[i].currency
              + '</td><td style="width:160px;text-align:right">'
              + time + '</td></tr>';
          }
          swal({
            title: 'Donations',
            content: table,
            buttons: { confirm: { text: 'OK', className: 'fw-btn-ok' } },
            allowOutsideClick: 'true'
          });
        });
    });
  });
})();
