function initMap() {
    var diary_loc = JSON.parse(document.getElementById('diary_loc').textContent);
    var locs = JSON.parse(document.getElementById('locations').textContent);

    var map = new google.maps.Map(
        document.getElementById('map')
    );

    var marker;
    if (diary_loc) {
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(diary_loc[1], diary_loc[0]),
            map: map,
        });
    }

    if (locs) {
        var latlngbounds = new google.maps.LatLngBounds();

        for (var i = 0; i < locs.length; i++) {
            var pos = new google.maps.LatLng(locs[i][1], locs[i][0]);
            latlngbounds.extend(pos);
            marker = new google.maps.Marker({
                position: pos,
                map: map,
                icon: {
                    url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
                }
            });
        };
        map.fitBounds(latlngbounds);
    }

}
