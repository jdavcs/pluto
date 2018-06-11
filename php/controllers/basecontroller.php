<?php
namespace Controller;

abstract class BaseController
{
    const RESET_ID = "_reset";
    const ACTION_EDIT = 1;
    const ACTION_DELETE = 2;
        
    protected $config;

    private $view;
    private $data_array;    //passed to the view
    private $state_array;   //form field names/values

    function __construct($view)
    {
        session_start();

        $this->config = parse_ini_file('../config.ini');
        $this->view = $view; 
        $this->data_array = array();
        $this->state_array = array();

        $this->check_reset();
        $this->load_state();
        $this->process_events();

        $html = "\n<form name='" . $this->config['form_id'] ."' id='" . $this->config['form_id'] . "' action='" . $_SERVER['REQUEST_URI'] . "' method='post'>";
        $this->set('form_html', $html);
    }
    
    function __destruct()
    {
        $VIEW = $this->config['app_root'] . "/views/" . $this->view . ".php";
        extract($this->data_array);
        require $this->config['app_root'] . "/views/tmpl/tmpl.php";
    }

    protected function set($key, $val)
    {
        $this->data_array[$key] = $val;
    }   

    protected function get_state($key)
    {
        if (array_key_exists($key, $this->state_array))
            return $this->state_array[$key];
        else
            return "";
    }

    private function check_reset()
    {
        if(isset($_POST[self::RESET_ID]))
            header('Location: ' . $_SERVER['REQUEST_URI']);        
    }

    private function load_state()
    {
        if($_SERVER['REQUEST_METHOD'] == "POST")
        {
            $this->load_state_helper($_POST);
            $this->load_postvalues();
        }
        //always load these
        $this->load_state_helper($_GET, true);
        $this->load_getvalues();
    }

    private function load_state_helper($arr, $is_get=false)
    {
        $keys = array_keys($arr);
        foreach($keys as $key)
        {
            if (!($is_get && $key == "page")) //ignore page key
            {
                $val = trim($arr[$key]);
                if ($val != "")
                    $this->state_array[$key] = $val;
            }
        }
    }

    protected function process_events() {}
    
    protected function load_postvalues() {}
    
    protected function load_getvalues() {}
}
