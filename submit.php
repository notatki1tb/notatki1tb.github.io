<?php

if (isset($_POST['godzina']) && isset($_POST['tekst'])) {
    $godzina = $_POST['godzina'];
    $tekst = $_POST['tekst'];

    // Połączenie z bazą danych (zmień dane dostępowe)
    $mysqli = new mysqli("localhost", "root", "", "przypomnienia");

    if ($mysqli->connect_error) {
        die("Błąd połączenia z bazą danych: " . $mysqli->connect_error);
    }

    // Wstawienie danych do tabeli jako osobny rekord
    $query = "INSERT INTO wpisy (godzina, tekst) VALUES (?, ?)";
    $stmt = $mysqli->prepare($query);
    $stmt->bind_param("ss", $godzina, $tekst);

    if ($stmt->execute()) {
        echo "Nowy wpis dodany do bazy danych.";

        // Pobierz ostatnio dodany ID rekordu
        $last_insert_id = $mysqli->insert_id;

        // Usuń rekord z bazy danych po dodaniu wiadomości
        $delete_query = "DELETE FROM wpisy WHERE id = ?";
        $delete_stmt = $mysqli->prepare($delete_query);
        $delete_stmt->bind_param("i", $last_insert_id);


        $delete_stmt->close();
    } else {
        echo "Błąd: " . $query . "<br>" . $mysqli->error;
    }

    $stmt->close();
    $mysqli->close();
} else {
    echo "Brak danych wejściowych (godzina lub tekst) w formularzu.";
}

?>
