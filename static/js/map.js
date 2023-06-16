$(document).ready(function() {
    // Add active class to the first table link by default
    $(".filters a:first").addClass("active");
    // Fetch table data when a table link is clicked
    $(".filters a").click(function(e) {
        e.preventDefault();
        $(".filters a").removeClass("active");
        $(this).addClass("active");
        var table = $(this).attr("href").substring(1);
        fetchMapData(table);
    });
    // Fetch table data for the initial table
    var initialTable = $(".filters a:first").attr("href").substring(1);
    fetchMapData(initialTable);
    // Display Map
    var map = L.map('map', { attributionControl: false }).setView([51.505, -0.09], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        //attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
        maxZoom: 18,
    }).addTo(map);
});

function fetchMapData(table) {
    $.ajax({
        url: "/map_data",
        data: { table: table },
        success: function (data) { updateMap(data); },
        error: function (xhr, status, error) { console.error("Error fetching map data:", error); }
    });
}

function updateMap(data) {
    // Clear the map
    map.eachLayer(function (layer) {
        if (layer !== map) {
            map.removeLayer(layer);
        }
    });
    // Loop through the data and display player count and players on the map
    data.forEach(function (countryData) {
        var country = countryData.country;
        var count = countryData["2020"].count;
        var players = countryData["2020"].players;
        var latitude = parseFloat(countryData.latitude);
        var longitude = parseFloat(countryData.longitude);
        // Use the Leaflet library to display the count on the map as markers or any other desired representation
        // For example, you can use L.marker to add a marker at the country's location and display the count as a popup
        // Replace latitude and longitude with the actual coordinates of the country
        var marker = L.marker([latitude, longitude]).addTo(map);
        marker.bindPopup("Players: " + count);
        // Add hover functionality to display a list of players when hovering over a country
        marker.on("mouseover", function (e) {
            var playerList = "";
            players.forEach(function (player) {
                playerList += "<li>" + player + "</li>";
            });
            var popupContent = "<ul>" + playerList + "</ul>";
            marker.bindPopup(popupContent).openPopup();
        });
        marker.on("mouseout", function (e) {
            marker.bindPopup("Players: " + count);
        });
    });
}