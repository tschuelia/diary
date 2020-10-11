function initMap() {
    var diary_loc = JSON.parse(document.getElementById('diary_loc').textContent);
    var locs = JSON.parse(document.getElementById('locations').textContent);
    var labels = JSON.parse(document.getElementById('labels').textContent);
    var urls = JSON.parse(document.getElementById('urls').textContent);

    var map = new google.maps.Map(
        document.getElementById('map')
    );

    var marker;
    if (diary_loc) {
        var pos = new google.maps.LatLng(diary_loc[1], diary_loc[0]);
        marker = new google.maps.Marker({
            position: pos,
            map: map,
        });
        map.setCenter(pos);
        map.setZoom(10);
    }

    if (locs.length > 0 && labels.length > 0) {
        var latlngbounds = new google.maps.LatLngBounds();

        for (var i = 0; i < locs.length; i++) {
            var pos = new google.maps.LatLng(locs[i][1], locs[i][0]);
            latlngbounds.extend(pos);
            marker = new google.maps.Marker({
                position: pos,
                label: { text: labels[i], color: "blue" },
                map: map,
                icon: {
                    url: "http://maps.google.com/mapfiles/ms/icons/orange.png"
                },
                url: urls[i]
            });
            google.maps.event.addListener(marker, 'click', function () {
                window.location.href = this.url;
            });
        };
        map.fitBounds(latlngbounds);
    }
}

