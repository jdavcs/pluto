<?php
namespace WebControl;

abstract class BaseControl
{
    protected $config;

    function __construct()
    {
        $this->config = parse_ini_file('../config.ini');
    }
}
