
var refreshGridTimer;
var urlStartContainer = '/api/container/start'
var urlStopContainer = '/api/container/stop'

$(document).ready(function () {

  // Refresh containers grid for first time
  refreshGrid()
})

$(document).on('click', '.btn-container-start', function (e) {
  e.preventDefault()
  onToggleContainerStatusClicked($(this), true)
})

$(document).on('click', '.btn-container-stop', function (e) {
  e.preventDefault()
  onToggleContainerStatusClicked($(this), false)
})

/** Manage changes on 'realtime' switch */
$(document).on('change', '#switch-realtime', function () {
  if ($(this).is(':checked')) {
    scheduleGridRefresh(5)
  } else {
    stopScheduledGridRefresh()
  }
})

/**
 * Manages clicks over start/stop container buttons
 * from containers grid
 *
 * @param button JQuery target element
 * @param startContainer Indicates if start or stop container
 */
function onToggleContainerStatusClicked(button, startContainer) {
  var $icon = button.find('span')

  // If currently working, abort operation
  if ($icon.hasClass('fa-cog')) {
    return;
  }

  // Show loading animation
  $icon.removeClass('fa-circle')
  $icon.addClass('fa-spin fa-cog')

  // Retrieve data for api call
  var url = button.attr('href')
  var containerId = button.attr('container-id')

  $.ajax({
    method: 'POST',
    url: url,
    data: {
      container_id: containerId
    },
    success: function (data, textStatus, xhr) {
      if (xhr.status === 204) {

        // Update button mode
        if (startContainer) {
          button.removeClass('btn-container-start')
          button.attr('href', urlStopContainer)
          button.addClass('btn-container-stop')

          // Show start icon
          $icon.removeClass('fa-spin fa-cog color-gray')
          $icon.addClass('fa-circle color-green')
        } else {
          button.removeClass('btn-container-stop')
          button.attr('href', urlStartContainer)
          button.addClass('btn-container-start')

          // Show stop icon
          $icon.removeClass('fa-spin fa-cog color-green')
          $icon.addClass('fa-circle color-gray')
        }
      }
    },
    error: function () {
      console.error('Error occurred')
    }
  })
}

function scheduleGridRefresh(inSeconds) {
  var progress = 100 - inSeconds * 20
  $('#progress-refresh').css('width', progress + '%')

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

    $('#progress-refresh').css('width', '0%')
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
