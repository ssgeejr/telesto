<?php
// Database connection details
$host = "tethys";
$port = "3306";
$dbname = "telesto";
$username = "telesto";
$password = "saturnsboy";

// Create connection
$conn = new mysqli($host, $username, $password, $dbname, $port);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Query to fetch data from the disable table
$sql = "SELECT name, email, deprtment, lastlogin, lastlogindays FROM disable";
$result = $conn->query($sql);

// Start HTML output
echo "<!DOCTYPE html><html><head><title>Users to be Disabled</title>";
echo "<style>";
echo "table { border-collapse: collapse; width: 100%; font-family: monospace; }";
echo "th, td { border: 1px solid black; padding: 8px; text-align: left; }"; // Border on all cells
echo "tr { border: 1px solid black; }"; // Explicit border around each row
echo "th { background-color: #f2f2f2; }";
echo "th:nth-child(1), td:nth-child(1) { width: 400px; }"; // name: 40 chars (~400px)
echo "th:nth-child(2), td:nth-child(2) { width: 500px; }"; // email: 50 chars (~500px)
echo "th:nth-child(3), td:nth-child(3) { width: 350px; }"; // deprtment: 35 chars (~350px)
echo "th:nth-child(4), td:nth-child(4) { width: 180px; }"; // lastlogin: 18 chars (~180px)
echo "th:nth-child(5), td:nth-child(5) { width: 70px; }";  // lastlogindays: 7 chars (~70px)
echo "</style>";
echo "</head><body>";
echo "<h1>Users to be Disabled</h1>";

if ($result->num_rows > 0) {
    // Output table headers
    echo "<table>";
    echo "<tr><th>Name</th><th>E-Mail</th><th>Department</th><th>Last Login</th><th>Days</th></tr>";

    // Output data rows
    while ($row = $result->fetch_assoc()) {
        echo "<tr>";
        echo "<td>" . htmlspecialchars($row["name"]) . "</td>";
        echo "<td>" . htmlspecialchars($row["email"]) . "</td>";
        echo "<td>" . htmlspecialchars($row["deprtment"]) . "</td>";
        echo "<td>" . htmlspecialchars($row["lastlogin"]) . "</td>";
        echo "<td>" . htmlspecialchars($row["lastlogindays"]) . "</td>";
        echo "</tr>";
    }
    echo "</table>";
} else {
    echo "<p>No data found in the disable table.</p>";
}

echo "</body></html>";

// Close connection
$conn->close();
?>