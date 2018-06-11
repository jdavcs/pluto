<?php 
namespace Controller;

class Source
{
    function main($config)
    {
        $app_root = $config['app_root'];
        $view = $app_root . '/views/sources.php';

        $data = array();

        $db = new \Db($config);
        $db->open();
        $data['sources'] = $db->get_sources_p(20, 30);
        $db->close();

        tmpl_display($app_root, $view, $data);
    }
}
