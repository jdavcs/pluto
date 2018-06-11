package pluto;

import java.io.*;
import java.lang.StringBuilder;
import java.sql.*;
import java.util.*;
import org.apache.tika.*;

public class TikaMTDetector
{
    private Database db;
    private Tika tika;
    private Hashtable<String, Integer> mtypes;
    private Hashtable<String, Integer> mstypes;
    private ConfigReader config;
    
    /* required parameter: path to config.properties */
    public static void main(String[] args) throws SQLException
    {
        String configPath = args[0];
        new TikaMTDetector(configPath).run();
    }
    
    public TikaMTDetector(String configPath)  
    {
        config = new ConfigReader(configPath);
        db = new Database(configPath);
        tika = new Tika();
    }

    public void run() throws SQLException
    {
        db.open();
        loadTypes();
        processResults(db.getFilesByMimetype(-1)); //unknown mimetype files
        
        int octetStreamId = Integer.parseInt(config.get(ConfigProperties.MIMESUBTYPE_ID_OCTETSTREAM));
        processResults(db.getFilesBySubMimetype(octetStreamId)); //octet-stream files
        
        db.commit();
        db.close();
    }

    private void loadTypes()
    {
        mtypes = new Hashtable<String, Integer>();
        mstypes = new Hashtable<String, Integer>();

        try {
            loadHashtable(db.getMimetypes(), mtypes);
            loadHashtable(db.getMimeSubtypes(), mstypes);
        }
        catch (SQLException e) { System.err.println(e.getMessage()); }
    }

    private void loadHashtable(ResultSet rs, Hashtable<String, Integer> ht)
    {
        try {
            while (rs.next())
            {
                int id = rs.getInt(1);
                String name = rs.getString(2);
                ht.put(name, id);
            }
        }
        catch (SQLException e) { System.err.println(e.getMessage()); }
    }

    private void processResults(ResultSet rs) throws SQLException
    {
        int count = 0;
        while (rs.next())
        {
            int itemId       = rs.getInt(1);
            int sourceId     = rs.getInt(2);
            String extension = rs.getString(5); 

            String dirPath = config.get(ConfigProperties.OUTPUT_ROOT) + 
                config.get(ConfigProperties.PROCESSED_FILES_RELPATH);
            String filename = sourceId + "/" + itemId + extension;
            String path = dirPath + filename;

            processFile(itemId, path);

            if (++count % 100 == 0)
            {
                System.out.println("Processing file #" + count);
                db.commit();
            }
        }
    }

    private void processFile(int itemId, String path)
    {
        try {
            File f = new File(path);
            String result = tika.detect(f);

            int p = result.indexOf('/');
            if (p > -1)
            {
                int mtId = -1;
                String mtName  = result.substring(0, p);
                if (mtypes.containsKey(mtName))
                    mtId = mtypes.get(mtName);
                else               
                {
                   System.out.println("found new mt: " + mtName);
                   mtId = db.createMimetype(mtName);
                   db.commit();
                   mtypes.put(mtName, mtId);
                }
            
                int mstId = -1;
                String mstName  = result.substring(p + 1);
                if (mstypes.containsKey(mstName))
                    mstId = mstypes.get(mstName);
                else                
                {
                   System.out.println("found new mst: " + mstName);
                   mstId = db.createMimeSubtype(mstName);
                   db.commit();
                   mstypes.put(mstName, mstId);
                }

                int mtDetectorId = Integer.parseInt(config.get(ConfigProperties.MIMETYPE_DETECTOR_TIKA));

                db.updateFileType(itemId, mtId, mstId, mtDetectorId);
                db.updateDataItemFileType(itemId, mtId, mstId, mtDetectorId, mtName, mstName);
            }

        } catch (IOException e) {
            System.err.println(e.getMessage());
        } catch (SQLException e) {
            System.err.println(e.getMessage());
        }
    }
}
