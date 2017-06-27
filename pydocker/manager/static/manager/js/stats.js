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
        createMemoryChart(stats)
      } else {
        console.error('Stats could not be fetched')
      }
    },
    error: function () {
      console.error('Stats could not be fetched')
    }
  })
}

function createMemoryChart(stats) {
  var maxAllowed = 0
  var labels = []
  var dataSets = []

  // Create data set with mem usage per container
  var memData = []
  for (var i = 0; i < stats.length; i++) {
    var containerStats = stats[i]

    labels.push(containerStats.container_name)
    memData.push(containerStats.mem_usage)
    maxAllowed = containerStats.mem_limit
  }

  // Add mem usage data set to chart data sets
  dataSets.push({
    label: 'Memory usage (MB)',
    backgroundColor: '#16A085',
    data: memData
  })

  // Draw chart
  var ctx = document.getElementById('chart-mem')
  var chart = new Chart(ctx, {
    type: 'bar',
    data: {
      'labels': labels,
      'datasets': dataSets
    },
    options: {
      tooltips: {
        callbacks: {
          label: function(tooltipItem) {
            return tooltipItem.yLabel + ' MB'
          }
        }
      }
    }
  })

  // Show chart
  var $chartCanvas = $('#chart-mem');
  $chartCanvas.parent()
    .parent()
    .find('.chart-loading-container')
    .addClass('hidden')
  $chartCanvas.parent().removeClass('hidden')
}
