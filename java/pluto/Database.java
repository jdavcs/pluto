package pluto;

import java.sql.*;

public class Database
{
    private Connection conn;
    private ConfigReader config;
    
    public Database(String configPath) 
    {
        config = new ConfigReader(configPath);
    }

    public void open() throws SQLException
    {
        String url = config.get(ConfigProperties.DB_URL);
        String user = config.get(ConfigProperties.DB_USER);
        String password = config.get(ConfigProperties.DB_PASSWORD);
        conn = DriverManager.getConnection(url, user, password);
        conn.setAutoCommit(false);
    }

    public void updateFileType(int itemId, int mtId, int mstId, int detectorId) throws SQLException
    {
        PreparedStatement ps = conn.prepareStatement(
            "UPDATE fileitem SET mimetype_id = ?, mimesubtype_id = ?, mimetypedetector_id = ? WHERE item_id = ?");
        ps.setInt(1, mtId);
        ps.setInt(2, mstId);
        ps.setInt(3, detectorId);
        ps.setInt(4, itemId);
        ps.executeUpdate();
    }
    
    public void updateDataItemFileType(int itemId, int mtId, int mstId, int detectorId, String mtName, String mstName) throws SQLException//this is a hack
    {
        StringBuilder sb = new StringBuilder();
        sb.append("UPDATE data_item SET file_mimetype_id = ?, file_mimesubtype_id = ?, file_mimedetector_id = ?, ");
        sb.append("file_mimetype_name = ?, file_mimesubtype_name = ? WHERE item_id = ?");

        PreparedStatement ps = conn.prepareStatement(sb.toString());
        ps.setInt(1, mtId);
        ps.setInt(2, mstId);
        ps.setInt(3, detectorId);
        ps.setString(4, mtName);
        ps.setString(5, mstName);
        ps.setInt(6, itemId);
        ps.executeUpdate();
    }
    
    public int createMimetype(String name) throws SQLException
    {
        PreparedStatement ps = conn.prepareStatement("INSERT INTO mimetype (name) values(?)", Statement.RETURN_GENERATED_KEYS);
        ps.setString(1, name);
        ps.executeUpdate();
        ResultSet rs = ps.getGeneratedKeys();
        if (rs.next())
            return rs.getInt(1);
        else
            return -1;
    }
    
    public int createMimeSubtype(String name) throws SQLException
    {
        PreparedStatement ps = conn.prepareStatement("INSERT INTO mimesubtype (name) values(?)", Statement.RETURN_GENERATED_KEYS);
        ps.setString(1, name);
        ps.executeUpdate();
        ResultSet rs = ps.getGeneratedKeys();
        if (rs.next())
            return rs.getInt(1);
        else
            return -1;
    }
    
    public int getPropertyId(int propertyTypeId, String name) throws SQLException
    {
        PreparedStatement ps = conn.prepareStatement("SELECT id FROM property WHERE propertytype_id = ? and name = ?");
        ps.setInt(1, propertyTypeId);
        ps.setString(2, name);
        ResultSet rs = ps.executeQuery();
        if (rs.next())
            return rs.getInt(1);
        else
            return -1;
    }

    public int createProperty(int propertyTypeId, String name) throws SQLException
    {
        PreparedStatement ps = conn.prepareStatement(
            "INSERT INTO property (propertytype_id, name) values(?, ?)", Statement.RETURN_GENERATED_KEYS);
        ps.setInt(1, propertyTypeId);
        ps.setString(2, name);
        ps.executeUpdate();
        ResultSet rs = ps.getGeneratedKeys();
        if (rs.next())
            return rs.getInt(1);
        else
            return -1;
    }
    
    public void createItemProperty(int itemId, int propertyId, String value, int batch) throws SQLException
    {
        PreparedStatement ps = conn.prepareStatement("INSERT INTO item_property (item_id, property_id, value, batch) values(?, ?, ?, ?)");
        ps.setInt(1, itemId);
        ps.setInt(2, propertyId);
        ps.setString(3, value);
        ps.setInt(4, batch);
        ps.executeUpdate();
    }

    public void concatItemProperty(int itemId, int propertyId, String value) throws SQLException
    {
        PreparedStatement ps = conn.prepareStatement("UPDATE item_property SET value = concat(value, ?) WHERE item_id = ? AND property_id = ?");
        ps.setString(1, value);
        ps.setInt(2, itemId);
        ps.setInt(3, propertyId);
        ps.executeUpdate();
    }
    
    public ResultSet getMimetypes() throws SQLException
    {
        PreparedStatement ps = conn.prepareStatement("SELECT id, name FROM mimetype");
        return ps.executeQuery();
    }
    
    public ResultSet getMimeSubtypes() throws SQLException
    {
        PreparedStatement ps = conn.prepareStatement("SELECT id, name FROM mimesubtype");
        return ps.executeQuery();
    }

    public ResultSet getProperties(int propertyTypeId) throws SQLException
    {
        PreparedStatement ps = conn.prepareStatement("SELECT id, name FROM property WHERE propertytype_id = ?");
        ps.setInt(1, propertyTypeId);
        return ps.executeQuery();
    }
    
    public ResultSet getFilesByMimetype(int mimetypeId) throws SQLException
    {
        PreparedStatement ps;

        StringBuilder sb = new StringBuilder();
        sb.append("SELECT i.id, i.source_id, fi.mimesubtype_id, fi.filesize, fi.extension FROM item i INNER JOIN fileitem fi ON fi.item_id = i.id ");
        
        if (mimetypeId !=  -1)
        {
            sb.append("AND fi.mimetype_id = ?");
            ps = conn.prepareStatement(sb.toString());
            ps.setInt(1, mimetypeId);
        }
        else
        {
            sb.append("AND fi.mimetype_id IS NULL");
            ps = conn.prepareStatement(sb.toString());
        }
        return ps.executeQuery();
    }
    
    public ResultSet getFilesBySubMimetype(int mimesubtypeId) throws SQLException
    {
        PreparedStatement ps;
        StringBuilder sb = new StringBuilder();
        sb.append("SELECT i.id, i.source_id, fi.mimesubtype_id, fi.filesize, fi.extension FROM item i INNER JOIN fileitem fi ON fi.item_id = i.id ");
        sb.append("AND fi.mimesubtype_id = ?");
        ps = conn.prepareStatement(sb.toString());
        ps.setInt(1, mimesubtypeId);
        return ps.executeQuery();
    }

    public void commit() throws SQLException
    {
        conn.commit();
    }

    public void close() throws SQLException
    {
        conn.close();
    }
}
