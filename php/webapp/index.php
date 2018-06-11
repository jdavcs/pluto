<?php

//required for all
require "../lib/db.php";
require "../controllers/basecontroller.php";
require "../webcontrols/basecontrol.php";
require "../models/basemodel.php";

//process GET and get target page
$request = $_SERVER['QUERY_STRING'];

if (empty($request))
    $target = 'home';
else
{
    $parsed = explode('&', $request);
    $arg1 = explode('=', array_shift($parsed));
    $target = $arg1[1]; //page must be first arg

    $data = array();
    foreach ($parsed as $arg)
    {
        list($var , $val) = explode('=' , $arg);
        $data[$var] = $val;
    }
}

//select and launch controller
$root = "../controllers/";

switch($target) 
{
    case 'searchemail':
        require $root . $target . ".php";
        $contr = new Controller\SearchEmail($target);
        break;
    case 'searchfiles':
        require $root . $target . ".php";
        $contr = new Controller\SearchFiles($target);
        break;
    case 'searchall':
        require $root . $target . ".php";
        $contr = new Controller\SearchAll($target);
        break;
    case 'viewitem':
        require $root . $target . ".php";
        $contr = new Controller\ViewItem($target);
        break;
    case 'labels':
        require $root . $target . ".php";
        $contr = new Controller\Labels($target);
        break;
    case 'subsets':
        require $root . $target . ".php";
        $contr = new Controller\Subsets($target);
        break;
    case 'edit_subset':
        require $root . $target . ".php";
        $contr = new Controller\EditSubset($target);
        break;
    case 'sources':
        require $root . $target . ".php";
        $contr = new Controller\Sources($target);
        break;
    case 'redactions':
        require $root . $target . ".php";
        $contr = new Controller\Redactions($target);
        break;
    default:
        require $root . $target . ".php";
        $contr = new Controller\Home($target);
        break;
}

$contr->main();
