<?php

class Db
{
    private $db;
    
    function __construct() {}

    function open()
    {
        $config = parse_ini_file('../config.ini');

        $host = $config['host'];
        $user = $config['username'];
        $pass = $config['password'];
        $dbname = $config['dbname'];

        $this->db = new PDO("mysql:host=$host;dbname=$dbname", $user, $pass, array(PDO::ATTR_PERSISTENT => true));
        $this->db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    }

    function close()
    {
        $this->db = null;
    }

    function execute($text, $is_sproc, $params=null)
    {
        $this->exec_helper($text, $is_sproc, $params);
    }

    function get_scalar($text, $is_sproc, $params=null)
    {
        $stmt = $this->exec_helper($text, $is_sproc, $params);
        return $stmt->fetchColumn(); 
    }
    
    function get_record($text, $is_sproc, $params=null)
    {   
        $stmt = $this->exec_helper($text, $is_sproc, $params);
        return $stmt->fetch();
    }
    
    function get_records($text, $is_sproc, $params=null)
    { 
        $stmt = $this->exec_helper($text, $is_sproc, $params);
        return $stmt->fetchAll();
    }

    private function exec_helper($text, $is_sproc, $params)
    {
        if ($is_sproc)
            return $this->exec_sp($text, $params);
        else
            return $this->exec_sql($text, $params);
    }

    private function exec_sql($sql, $params)
    {
        $stmt = $this->db->prepare($sql);

        if ($params != null)
        {
            if (!is_array($params))
                $params = array("0" => $params);
        
            for($i=0; $i<count($params); $i++)
                $stmt->bindParam($i+1, $params[$i]);
        }

        try { $stmt->execute(); }
        catch (Exception $e)
        {
            echo "<div style='padding:7px; border:1px red solid;'>$e</div>";
        }

        return $stmt;
    }

    private function exec_sp($sp, $params)    
    {
        if ($params != null)
        {
            if (!is_array($params))
                $params = array("0" => $params);

            $ph = ""; //placeholder
            foreach($params as $p)
                $ph .= "?, ";
            $ph = substr($ph, 0, strlen($ph)-2);

            $stmt = $this->db->prepare("CALL " . $sp . "($ph)");
        
            for($i=0; $i<count($params); $i++)
                $stmt->bindParam($i+1, $params[$i]);
        }
        else
            $stmt = $this->db->prepare("CALL " . $sp . "()");

        try { $stmt->execute(); }
        catch (Exception $e)
        {
            echo "<div style='padding:7px; border:1px red solid;'>$e</div>";
        }

        return $stmt;
    }
}

