<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Custom Link Example</title>
    <style>
        .custom-link {
            color: #1a73e8; /* Blue color */
            text-decoration: none; /* Remove underline */
            font-weight: bold; /* Make the text bold */
            transition: color 0.3s; /* Smooth color transition on hover */
        }
        .custom-link:hover {
            color: #d93025; /* Red color on hover */
        }
        .custom-link:visited {
            color: #6f6f6f; /* Grey color for visited links */
        }
    </style>
</head>
<body>
    <a href="https://the-odds-api.com" class="custom-link" title="Visit The Odds API">Check out The Odds API!</a>
</body>
</html>
