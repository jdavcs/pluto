package pluto;

import java.io.*;
import java.lang.StringBuilder;
import java.sql.*;
import java.util.*;
import org.xml.sax.*;
import org.apache.tika.parser.AutoDetectParser;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.sax.*;
import org.apache.tika.io.*;
import org.apache.tika.exception.TikaException;

/*
 * Required arguments: 
 * 1) input_path to directory with files OR to file with paths
 * 2) output_path to directory for extracted text files
 * 3) flag: 1 (process files) or 2 (process paths)
 * 4) batch number 
 * 5) path to file for logging Tika errors
 */
public class TikaExtractor
{
    private int batch;
    private Database db;
    private int textPropertyId;
    private Hashtable<String, Integer> properties;
    private HashSet<String> errorText;
    private HashSet<String> errorPath;
    private HashSet<Integer> pids;
    
    private static final int PROCESS_FILES = 1;
    private static final int PROCESS_PATHS = 2;
    private static final String DELIMITER = "[[pluto-delim]]";

    private ConfigReader config;

    /* required 6 parameters: see code below */
    public static void main(String[] args) throws SQLException
    {
        String pathIn = args[0]; 
        String pathOut = args[1];
        int flag = Integer.parseInt(args[2]);
        int batch = Integer.parseInt(args[3]);
        String errorPathPath = args[4];
        String configPath = args[5];

        if (flag == PROCESS_FILES && !pathIn.endsWith("/")) pathIn += "/";
        if (!pathOut.endsWith("/")) pathOut += "/";
        
        try {
            TikaExtractor te = new TikaExtractor(batch, configPath);
            te.run(flag, pathIn, pathOut, errorPathPath); 
        }
        catch (SQLException e) { 
            System.err.println("ERROR-1: " + e.getMessage()); } 
    }
    
    public TikaExtractor(int batch, String configPath) 
    {
        config = new ConfigReader(configPath);

        this.batch = batch;
        db = new Database(configPath);
        properties = new Hashtable<String, Integer>();
        errorText = new HashSet<String>();
        errorPath = new HashSet<String>();
        pids = new HashSet<Integer>();
    }

    public void run(int flag, String pathIn, String pathOut, String errorPathPath) throws SQLException
    {
        db.open();
        loadProperties();

        int proptypeIdFile = Integer.parseInt(config.get(ConfigProperties.PROPERTYTYPE_ID_FILE)); 
        String extrTextPropName = config.get(ConfigProperties.EXTRACTED_TEXT_PROPERTY_NAME); 
        textPropertyId = db.getPropertyId(proptypeIdFile, extrTextPropName);
                
        File dirOut = new File(pathOut);

        if (flag == PROCESS_FILES)
            processFiles(pathIn, dirOut);
        else
            processPaths(pathIn, dirOut);

        processErrors(errorText, getErrorTextPath());
        processErrors(errorPath, errorPathPath);
        
        db.commit();
        db.close();
    }

    private void processFiles(String pathIn, File dirOut) throws SQLException
    {
        File dir = new File(pathIn);
        int counter = 0;
        for (File f : dir.listFiles())         
            processFile(f, dirOut, ++counter);

        db.commit(); //commit the remainder
    }

    private void processPaths(String pathIn, File dirOut) throws SQLException
    {
        BufferedReader r = null;
        try {
            r = new BufferedReader(new FileReader(pathIn));
            int counter = 0;
            String line;
            while ((line = r.readLine()) != null)            
                processFile(new File(line), dirOut, ++counter);            
        } 
        catch (FileNotFoundException e) {
                System.err.println("ERROR-2 [" + pathIn + "] " + e.getMessage());            
        }
        catch (IOException e) {
                System.err.println("ERROR-3 [" + pathIn + "] " + e.getMessage());            
        }
        finally {
                try { r.close(); }
                catch (IOException e) { System.err.println("ERROR-4 [" + pathIn + "] " + e.getMessage()); }
        }
        db.commit(); //commit the remainder
    }

    private void processFile(File fileIn, File dirOut, int counter)    
    {
        pids.clear(); //empty stored property set for each file!

        try {
            if (counter % 1000 == 0) //db commit every 1000 files
                db.commit();
        }
        catch (SQLException e) { logProcessingError(1, e.getMessage(), fileIn.toString()); }
                
        String strItemId = fileIn.getName();
        int dot = strItemId.indexOf(".");
        if (dot > -1)
            strItemId = strItemId.substring(0, dot);

        File fileOut = new File(dirOut, strItemId);

        //added this as a safeguard because of doing a second run: delete previously written files!
        if (fileOut.exists())
            fileOut.delete();

        InputStream is = null;
        OutputStream os = null;
        try {
            is = TikaInputStream.get(fileIn);
            os = new FileOutputStream(fileOut);
            Metadata metadata = new Metadata();
            ContentHandler ch = new BodyContentHandler(os);
            AutoDetectParser parser = new AutoDetectParser();
            parser.parse(is, ch, metadata);

            int itemId = Integer.parseInt(strItemId);

            for (String pn : metadata.names())
               processItemProperty(itemId, pn, metadata.get(pn));
        } 
        catch (FileNotFoundException e) { logProcessingError(2, e.getMessage(), fileIn.toString()); }
        catch (IOException e) { logProcessingError(3, e.getMessage(), fileIn.toString()); }
        catch (SAXException e) { logProcessingError(4, e.getMessage(), fileIn.toString()); }
        catch (TikaException e) { logProcessingError(5, e.getMessage(), fileIn.toString()); }
        catch (SQLException e) { logProcessingError(6, e.getMessage(), fileIn.toString()); }
        finally {
            if (is != null)
                try { is.close(); }
                catch (IOException e) { logProcessingError(7, e.getMessage(), fileIn.toString()); }
            if (os != null)
            {
                try { 
                    os.flush();
                    os.close();
                }                   
                catch (IOException e) { logProcessingError(8, e.getMessage(), fileIn.toString()); }
            }
        }
    }

    private void processErrors(HashSet<String> errors, String filePath) //append paths to log file
    {    
        if (errors.size() > 0) // only process if there are errors in the set
        {
            StringBuilder sb = new StringBuilder();
            Iterator it = errors.iterator();
            while (it.hasNext())
                sb.append(it.next() + "\n");

            BufferedWriter w = null;
            try {
                String text = sb.toString();
                w = new BufferedWriter(new FileWriter(filePath, true));
                w.write(text, 0, text.length());
                w.flush();
            }
            catch (IOException e) {
                System.err.println("ERROR-5: " + e.getMessage());
            }
            finally {
                try { w.close(); }
                catch (IOException e) { System.err.println("ERROR-6: " + e.getMessage()); }
            }
        }
    }

    private void logProcessingError(int errorCode, String message, String path)
    {
        errorText.add("PROCESSING-ERROR-" + errorCode + " [" + path + "] " + message);
        if (message.indexOf("Too many open") > -1)
            errorPath.add(path);
    }

    private void loadProperties() throws SQLException
    {
        int proptypeIdFile = Integer.parseInt(config.get(ConfigProperties.PROPERTYTYPE_ID_FILE));
        ResultSet rs = db.getProperties(proptypeIdFile);
        while (rs.next())
        {
            int id = rs.getInt(1);
            String name = rs.getString(2);
            properties.put(name, id);
        }
    }

    private void processItemProperty(int itemId, String name, String value) throws SQLException
    {
        int propertyId = -1;
        if (properties.containsKey(name))        
            propertyId = properties.get(name);        
        else
        {
            int proptypeIdFile = Integer.parseInt(config.get(ConfigProperties.PROPERTYTYPE_ID_FILE)); 
            propertyId = db.createProperty(proptypeIdFile, name);
            properties.put(name, propertyId);
        }

        if (!pids.contains(propertyId))  //this property has not been extratced for this item yet
        {
            pids.add(propertyId);
            db.createItemProperty(itemId, propertyId, value, batch); 
        }
        else    //this property has been extracted for this item: must concatenate
        {
            value = " " + DELIMITER + " " + value;
            db.concatItemProperty(itemId, propertyId, value);
        }
    }

    private String getErrorTextPath()
    {
        String dirPath = config.get(ConfigProperties.OUTPUT_ROOT) + 
                config.get(ConfigProperties.TIKA_LOG_RELPATH);
        String filename = "errors-" + batch + ".log"; 
        return dirPath + filename;
    }
}
