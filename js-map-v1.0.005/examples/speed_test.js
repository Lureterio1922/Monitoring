function $(element) {
  return document.getElementById(element);
}

var speedTest = {};

speedTest.pics = null;
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
    'mapId': "a71db9a0115114a1",
    'mapTypeId': google.maps.MapTypeId.ROADMAP
  };

  speedTest.map = new google.maps.Map($('map'), options);
  speedTest.pics = data.photos;
  
  var useGmm = $('usegmm');
  google.maps.event.addDomListener(useGmm, 'click', speedTest.change);
  
  var numMarkers = $('nummarkers');
  google.maps.event.addDomListener(numMarkers, 'change', speedTest.change);

  speedTest.infoWindow = new google.maps.InfoWindow();

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
  var numMarkers = $('nummarkers').value;

  for (var i = 0; i < numMarkers; i++) {
    var titleText = speedTest.pics[i].photo_title;
    if (titleText === '') {
      titleText = 'No title';
    }
    
    // выбор цвета маркера и статуса
    var img_color = "808080"; 
    var status_class_name = "label-gray"
    var status_text= "None"

    switch (speedTest.pics[i].status) {
      case 'Normal':
        img_color = "008CFF"; // синий
        status_class_name = "label-green"
        status_text= "Active"
        break;
      
      case 'MediumLoad':
        img_color = "c5d60d"; // желтый
        status_class_name = "label-yellow"
        status_text= "Medium Load"
        break;

      case 'HighLoad':
      case 'Full':
        img_color = "FF0000"; // красный
        status_class_name = "label-red"
        status_text= "Full"
        break;
    }

    var item = document.createElement('tr');
    var status = document.createElement('td');
    var title = document.createElement('td');

    // 1 колонка - статус
    status.className = "status-tr";
    status.innerHTML = `<span class="label ${status_class_name}">${status_text}</span>`
 
    // 2 колонка - название
    title.href = '#';
    title.className =  'title';
    title.innerHTML = titleText;

    item.appendChild(status);
    item.appendChild(title);
    panel.appendChild(item);


    var latLng = new google.maps.LatLng(speedTest.pics[i].latitude,
        speedTest.pics[i].longitude);
    
    var imageUrl  = `http://chart.apis.google.com/chart?cht=mm&chs=24x32&chco=FFFFFF,${img_color},000000&ext=.png`
    
    var markerImage = new google.maps.MarkerImage(imageUrl,
        new google.maps.Size(24, 32));

    var marker = new google.maps.Marker({
      'position': latLng,
      'icon': markerImage
    });

    var fn = speedTest.markerClickFunction(speedTest.pics[i], latLng, status_class_name, status_text);
      google.maps.event.addListener(marker, 'click', fn);
      google.maps.event.addDomListener(title, 'click', fn);
      speedTest.markers.push(marker);
  }

  window.setTimeout(speedTest.time, 0);
};

speedTest.markerClickFunction = function(pic, latlng, status_class_name, status_text) {
  return function(e) {
    e.cancelBubble = true;
    e.returnValue = false;
    if (e.stopPropagation) {
      e.stopPropagation();
      e.preventDefault();
    }
    var title = pic.photo_title;
    var url = pic.photo_url;
    var fileurl = pic.photo_file_url;

    var infoHtml = 
    `<div class="info">
      <h3> ${title}</h3>
      <div class="status">
        <span class="label ${status_class_name}">
        ${status_text}
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
      Ссылка: <a href="${pic.owner_url}" target="_blank">${pic.owner_name}</a>
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