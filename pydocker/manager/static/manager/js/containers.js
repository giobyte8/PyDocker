
var refreshGridTimer;

$(document).ready(function () {

  // Set initial progress
  document
    .querySelector('#progress-realtime-timer')
    .addEventListener('mdl-componentupgraded', function() {
      this.MaterialProgress.setProgress(0);
    });

  // Refresh containers grid for first time
  refreshGrid()
})

$(document).on('click', '.btn-container-start', function () {
  var _self = $(this)
  _self.css('display', 'none')

  var url = '/api/containers/start'
  $.ajax({
    method: 'POST',
    url: url,
    data: {
      container_id: _self.attr('container-id')
    },
    success: function () {
      refreshGrid()
      setTimeout(function () {
        refreshGrid()
      }, 2000)
    },
    error: function () {
      console.error('Error occurred')
    }
  })
})

$(document).on('click', '.btn-container-stop', function () {
  var _self = $(this)
  _self.css('display', 'none')

  var url = '/api/containers/stop'
  $.ajax({
    method: 'POST',
    url: url,
    data: {
      container_id: _self.attr('container-id')
    },
    success: function () {
      refreshGrid()
      setTimeout(function () {
        refreshGrid()
      }, 2000)
    },
    error: function () {
      console.error('Error occurred')
    }
  })
})

/** Manage changes on 'realtime' switch */
$(document).on('change', '#switch-realtime', function () {
  if ($(this).is(':checked')) {
    scheduleGridRefresh(5)
  } else {
    stopScheduledGridRefresh()
  }
})

function scheduleGridRefresh(inSeconds) {
  var progress = 100 - inSeconds * 20
  document.querySelector('#progress-realtime-timer').MaterialProgress.setProgress(progress)

  if (inSeconds <= 0) {
    refreshGrid()
    refreshGridTimer = setTimeout(function () {
      scheduleGridRefresh(5)
    }, 100)
  } else {
    inSeconds -= .1
    refreshGridTimer = setTimeout(function () {
      scheduleGridRefresh(inSeconds)
    }, 100)
  }
}

function stopScheduledGridRefresh() {
  if (refreshGridTimer) {
    clearTimeout(refreshGridTimer)
    refreshGridTimer = 0

    document.querySelector('#progress-realtime-timer').MaterialProgress.setProgress(0)
  }
}

/**
 * Downloads through ajax the updated containers grid
 * and renders into view
 */
function refreshGrid() {
  var url = 'containers'
  $.ajax({
    method: 'GET',
    url: url,
    success: function (html) {
      $('#grid-containers').html(html)
    },
    error: function () {
      console.error('Error while refreshing containers grid')
    }
  })
}
