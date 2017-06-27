$(document).ready(function () {

  fetchStats()
})

function fetchStats() {
  var urlStats = '/api/stats';

  $.ajax({
    method: 'GET',
    url: urlStats,
    success: function (stats, textStatus, xhr) {
      if (xhr.status === 200) {
        statsToChart(stats)
      } else {
        console.error('Stats could not be fetched')
      }
    },
    error: function () {
      console.error('Stats could not be fetched')
    }
  })
}

function statsToChart(stats) {
  var labels = []
  var maxAllowed = 0
  var datasets = []
  var dataset = {
    label: 'Usage in MB',
    backgroundColor: '#16a085',
    data: []
  }
  datasets.push(dataset)

  for (var i = 0; i < stats.length; i++) {
    var containerStats = stats[i]

    labels.push(containerStats.container_name)
    dataset.data.push(containerStats.mem_usage)
    maxAllowed = containerStats.mem_limit
  }

  var ctx = document.getElementById('chart')
  var chart = new Chart(ctx, {
    type: 'bar',
    data: {
      'labels': labels,
      datasets: datasets
    },
    options: {
      tooltips: {
        intersect: false,
        callbacks: {
          label: function(tooltipItem) {
            return tooltipItem.yLabel +  ' MB'
          }
        }
      }
    }
  })
}
