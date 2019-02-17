<?php

use Slim\Http\Request;
use Slim\Http\Response;

// Routes

$app->get('/', function (Request $request, Response $response, array $args) {
    // Sample log message
    $this->logger->info("Slim-Skeleton '/' route");

    // Render index view
    return $this->renderer->render($response, 'index.html');
});

$app->post("/getBlock", function(Request $request, Response $response, array $args) {

    $param = $request->getParsedBody();
    $data = $param['data'];

    $ch = curl_init();

    curl_setopt($ch, CURLOPT_URL,"http://localhost:5000/getBlockByHeight");
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS,
              "data={$data}");

    // In real life you should use something like:
    // curl_setopt($ch, CURLOPT_POSTFIELDS,
    //          http_build_query(array('postvar1' => 'value1')));

    // Receive server response ...
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $server_output = curl_exec($ch);
    print($server_output);

    curl_close ($ch);

    return ;
});

$app->post("/getBlockHash", function(Request $request, Response $response, array $args) {

    $param = $request->getParsedBody();
    $data = $param['data'];

    $ch = curl_init();

    curl_setopt($ch, CURLOPT_URL,"http://localhost:5000/getBlockByHash");
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS,
              "data={$data}");

    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $server_output = curl_exec($ch);
    print($server_output);

    curl_close ($ch);

    return ;
});
