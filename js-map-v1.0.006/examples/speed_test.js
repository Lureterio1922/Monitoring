function $(element) {
  return document.getElementById(element);
}

var speedTest = {};

speedTest.servers = null;
speedTest.map = null;
speedTest.markerClusterer = null;
speedTest.markers = [];
speedTest.infoWindow = null;

speedTest.init = function() {
  var latlng = new google.maps.LatLng(39.91, 116.38);
  var options = {
    'zoom': 2,
    'minZoom':2,
    'center': latlng,
    'disableDefaultUI': true,
    'mapTypeId': google.maps.MapTypeId.ROADMAP
  };

  speedTest.map = new google.maps.Map($('map'), options);
  speedTest.servers = data.servers;
  
  var useGmm = $('usegmm');
  google.maps.event.addDomListener(useGmm, 'click', speedTest.change);
  
  var numMarkers = $('nummarkers');
  google.maps.event.addDomListener(numMarkers, 'change', speedTest.change);

  speedTest.infoWindow = new google.maps.InfoWindow({maxWidth: 200});

  speedTest.showMarkers();
  speedTest.ImportSearchLib()
};

speedTest.showMarkers = function() {
  speedTest.markers = [];

  // включение кластеризации
  var type = 1;
  if ($('usegmm').checked) {
    type = 0;
  }
  if (speedTest.markerClusterer) {
    speedTest.markerClusterer.clearMarkers();
  }

  var panel = $('markerlist');

  for (var i = 0; i < speedTest.servers.length; i++) {
    var titleText = speedTest.servers[i].title;
    if (titleText === '') {titleText = 'No title';}
    var statusText = speedTest.servers[i].status_text;
    if (statusText === '') {statusText = 'No status';}
    var statusColor = speedTest.servers[i].status_color;
    if (statusColor === '') {statusColor = '#808080';}
    var markerColor = speedTest.servers[i].marker_color.replace("#", "");
    if (markerColor === '') {markerColor = '808080';}
    
    var item = document.createElement('tr');
    var status = document.createElement('td');
    var title = document.createElement('td');

    // 1 колонка - статус
    status.className = "status";
    status.innerHTML = `<span class="label" style="background-color:${statusColor}">${statusText}</span>`
 
    // 2 колонка - название
    title.href = '#';
    title.className =  'title';
    title.innerHTML = titleText;

    item.appendChild(status);
    item.appendChild(title);
    panel.appendChild(item);


    var latLng = new google.maps.LatLng(speedTest.servers[i].latitude, speedTest.servers[i].longitude);
    
    var imageUrl  = `http://chart.apis.google.com/chart?cht=mm&chs=24x32&chco=FFFFFF,${markerColor},000000&ext=.png`
    
    var markerImage = new google.maps.MarkerImage(imageUrl,
        new google.maps.Size(24, 32));

    var marker = new google.maps.Marker({
      'position': latLng,
      'icon': markerImage
    });

    var fn = speedTest.markerClickFunction(speedTest.servers[i], latLng, statusColor, statusText);
      google.maps.event.addListener(marker, 'click', fn);
      google.maps.event.addDomListener(title, 'click', fn);
      speedTest.markers.push(marker);
  }

  window.setTimeout(speedTest.time, 0);
};

speedTest.markerClickFunction = function(server, latlng) {
  return function(e) {
    e.cancelBubble = true;
    e.returnValue = false;
    if (e.stopPropagation) {
      e.stopPropagation();
      e.preventDefault();
    }
    var infoHtml = 
    `<div class="info">
      <h3> ${server.title}</h3>
      <div class="status">
        <span class="label" style="background-color:${server.status_color}">
        ${server.status_text}
        </span>
      </div>
      <div class="info-body">
        <div target="_blank">
          <div class="description">
          Lorem Ipsum is simply dummy text of the printing 
          
          </div>
        </a>
      </div>
      <div href="LOGO.png" target="_blank">
      </div><br/>
      Ссылка: <a href="#" target="_blank">TODO</a>
    </div>`;

    speedTest.infoWindow.setContent(infoHtml);
    speedTest.infoWindow.setPosition(latlng);
    speedTest.infoWindow.open(speedTest.map);
  };
};

speedTest.clear = function() {
  $('timetaken').innerHTML = 'cleaning...';
  for (var i = 0, marker; marker = speedTest.markers[i]; i++) {
    marker.setMap(null);
  }
};

speedTest.change = function() {
  speedTest.clear();
  speedTest.showMarkers();
};

speedTest.time = function() {
  $('timetaken').innerHTML = 'timing...';
  var start = new Date();
  if ($('usegmm').checked) {
    speedTest.markerClusterer = new MarkerClusterer(speedTest.map, speedTest.markers, {imagePath: '../images/m'});
  } else {
    for (var i = 0, marker; marker = speedTest.markers[i]; i++) {
      marker.setMap(speedTest.map);
    }
  }
  var end = new Date();
  $('timetaken').innerHTML = end - start;
};

speedTest.ImportSearchLib = function() {
  // Create the search box and link it to the UI element.
  var input = /** @type {HTMLInputElement} */(
   $('pac-input'));
  speedTest.map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  var searchBox = new google.maps.places.SearchBox(
    /** @type {HTMLInputElement} */(input));

  // [START region_getplaces]
  // Listen for the event fired when the user selects an item from the
  // pick list. Retrieve the matching places for that item.
  google.maps.event.addListener(searchBox, 'places_changed', function() {
    var places = searchBox.getPlaces();
    if (places.length == 0) {
      return;
    }
    // For each place, get the icon, place name, and location.
    // markers = [];
    var bounds = new google.maps.LatLngBounds();
    for (var i = 0, place; place = places[i]; i++) {
      // Create a marker for each place.
      // position: place.geometry.location
      bounds.extend(place.geometry.location);
    }

    speedTest.map.fitBounds(bounds);
  });
  // [END region_getplaces]

  // Bias the SearchBox results towards places that are within the bounds of the
  // current map's viewport.
  google.maps.event.addListener(speedTest.map, 'bounds_changed', function() {
    var bounds = speedTest.map.getBounds();
    searchBox.setBounds(bounds);
  });
}       