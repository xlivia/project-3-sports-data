const Flask = {
    render_template: (template, data) => {
        const templateHTML = document.getElementById(template).innerHTML;
        const renderedHTML = Mustache.render(templateHTML, data);
        document.body.innerHTML = renderedHTML;
    },
    request: {
        args: {
            get: (key, defaultValue) => {
                const urlParams = new URLSearchParams(window.location.search);
                const value = urlParams.get(key);
                return value !== null ? value : defaultValue;
            },
        },
    },
    jsonify: (data) => JSON.stringify(data),
};

async function fetchData(query) {
    const response = await fetch(`/data?query=${encodeURIComponent(query)}`);
    const data = await response.json();
    return data;
}

function loadCSVToDatabase() {
    // Create a SQLAlchemy engine to connect to the database
    const engine = {
        execute: (query) => fetchData(query),
    };

    const csvFiles = ['players_15', 'players_16', 'players_17', 'players_18', 'players_19', 'players_20'];

    for (const file of csvFiles) {
        const tableName = file;
        const query = `SELECT * FROM ${tableName} LIMIT 100`;
        fetchData(query)
            .then((data) => {
                const players = data;
                console.log(`Loaded ${players.length} records from ${tableName}`);
            })
            .catch((error) => {
                console.error(`Failed to load data from ${tableName}`, error);
            });
    }
}

loadCSVToDatabase();

function getPlayerInfo() {
    const selectedPlayer = document.getElementById('player-select').value;
    if (selectedPlayer !== '') {
        const query = `SELECT short_name, age, nationality, club FROM players WHERE short_name = '${selectedPlayer}'`;
        fetchData(query)
            .then((data) => {
                const player = data[0];
                const tableBody = document.getElementById('player-table').getElementsByTagName('tbody')[0];
                tableBody.innerHTML = `
                    <tr>
                        <td>${player.short_name}</td>
                        <td>${player.age}</td>
                        <td>${player.nationality}</td>
                        <td>${player.club}</td>
                    </tr>
                `;
            })
            .catch((error) => {
                console.error('Failed to fetch player data:', error);
            });
    }
}

$(document).ready(function() {
    // Fetch the data for the initial page load
    const query = 'SELECT * FROM players LIMIT 100';
    fetchData(query)
        .then((data) => {
            const players = data;
            const columns = Object.keys(players[0]);
            Flask.render_template('index.html', { players, columns });
        })
        .catch((error) => {
            console.error('Failed to fetch data:', error);
        });
});

/*
$(document).ready(function() {
    // Add active class to the first table link by default
    $(".filters a:first").addClass("active");
    // Fetch table data when a table link is clicked
    $(".filters a").click(function(e) {
        e.preventDefault();
        $(".filters a").removeClass("active");
        $(this).addClass("active");
        var table = $(this).attr("href").substring(1);
        fetchTableData(table);
    });
    // Fetch table data for the initial table
    var initialTable = $(".filters a:first").attr("href").substring(1);
    fetchTableData(initialTable);
});

function fetchTableData(table) {
    $.ajax({
        url: "/data",
        data: { table: table },
        success: function(data) {
            updateTable(data);
        },
        error: function(xhr, status, error) {
            console.error("Error fetching table data:", error);
        }
    });
}

function updateTable(data) {
    var columns = Object.keys(data[0]);
    // Update the table header
    var tableHeader = "<tr>";
    columns.forEach(function(column) {
        tableHeader += "<th>" + column + "</th>";
    });
    tableHeader += "</tr>";
    $("table thead").html(tableHeader);
    // Update the table rows
    var tableRows = "";
    data.forEach(function(row) {
        tableRows += "<tr>";
        columns.forEach(function(column) {
            tableRows += "<td>" + row[column] + "</td>";
        });
        tableRows += "</tr>";
    });
    $("table tbody").html(tableRows);
}
*/