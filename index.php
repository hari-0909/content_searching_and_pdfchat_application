<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF Text Search & Download</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f7f7f7;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1, h2 {
            margin-top: 0;
            text-align: center;
        }
        form {
            text-align: center;
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 10px;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #4caf50;
            color: #fff;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .search-results {
            margin-top: 20px;
        }
        .search-results ul {
            list-style: none;
            padding: 0;
        }
        .search-results li {
            margin-bottom: 10px;
        }
        .download-btn {
            margin-top: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>PDF Text Search & Download</h1>
        <form method="POST" action="">
            <label for="searchText">Enter text to search:</label>
            <input type="text" id="searchText" name="searchText" required>
            <button type="submit">Search</button>
        </form>
        <?php
        if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['searchText'])) {
            $searchText = $_POST['searchText'];
            $folder = "contents";
            function searchPDFs($searchText, $folder) {
                $searchResults = [];
                $shell = new COM("Shell.Application");
                $searchFolder = $shell->Namespace($folder);
                if ($searchFolder === null) {
                    echo "Error: Failed to access the search folder.";
                    return $searchResults;
                }
                $items = $searchFolder->Items();
                foreach ($items as $item) {
                    $filename = $item->Path;
                    $searchTextEscaped = escapeshellarg($searchText);
                    $filenameEscaped = escapeshellarg($filename);
                    $pythonExecutable = "C:\\Users\\inspi\\AppData\\Local\\Programs\\Python\\Python310\\python.exe"; 
                    $pythonScript = "search.py";
                    $command = "$pythonExecutable $pythonScript $filenameEscaped $searchTextEscaped";
                    $output = shell_exec($command);
                    if ($output === null) {
                        echo "Error: Failed to execute Python script.";
                        continue;
                    }
                    $result = json_decode($output, true);
                    if (json_last_error() !== JSON_ERROR_NONE) {
                        echo "Error: Failed to parse Python script output. JSON error: " . json_last_error_msg();
                        continue;
                    }
                    if ($result === true) {
                        $searchResults[] = $filename;
                    }
                }
                return $searchResults;
            }
            $searchResults = searchPDFs($searchText, $folder);
            if (!empty($searchResults)) {
        ?>
        <div class="search-results">
            <h2>Search Results</h2>
            <form id="resultsForm" method="POST" action="">
                <ul>
                    <?php foreach ($searchResults as $result) : ?>
                        <li>
                            <label>
                                <input type="checkbox" name="files[]" value="<?= htmlspecialchars($result) ?>">
                                <?= htmlspecialchars(basename($result)) ?>
                            </label>
                        </li>
                    <?php endforeach; ?>
                </ul>
                <div class="download-btn">
                    <button type="submit" name="storeFiles">redirect to chat app</button>
                </div>
            </form>
        </div>
        <?php } else { ?>
            <p>No results found for '<?= htmlspecialchars($searchText) ?>'.</p>
        <?php }
            }
            if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['storeFiles']) && isset($_POST['files'])) {
                $selectedFiles = $_POST['files'];
                $tempFilePath = 'temp\selected_files.txt';
                if (!is_dir(dirname($tempFilePath))){
                    mkdir(dirname($tempFilePath),0777,true);
                }
                file_put_contents($tempFilePath, implode(PHP_EOL, $selectedFiles));
                header('Location: http://localhost:8501');
                exit();
            }
        ?>
    </div>
</body>
</html>