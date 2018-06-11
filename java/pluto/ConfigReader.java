package pluto; 

import java.io.*;
import java.util.Properties;

public class ConfigReader
{
    private Properties prop;

    /* parameter: path to config.properties */
    public ConfigReader(String path)
    {
        prop = new Properties();
        try {
            prop.load(new FileInputStream(path));
        }    
        catch (FileNotFoundException e) {}
        catch (IOException e) {}
    }

    public String get(String key)    
    {
        return prop.get(key).toString();
    }
}
