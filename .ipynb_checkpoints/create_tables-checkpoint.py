import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drop all of the tables
    
    Parameters: 
    cur: redshift cursor
    conn: redshift connection 
  
    Returns: 
    None
    
    """
        
    # Execute sql queries to drop all existing tables
    print("Dropping all existing tables...")
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Create all of the tables
    
    Parameters: 
    cur: redshift cursor
    conn: redshift connection 
  
    Returns: 
    None
    
    """
    
    # Execute sql queries to create all tables
    print("Creating all tables...")
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Main function
    
    Parameters: 
    None
  
    Returns: 
    None
    
    """
    
    # Load redshift and s3 configurations
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    # Connect to redshift
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    # Drop all existing tables
    drop_tables(cur, conn)
    
    # Create tables
    create_tables(cur, conn)

    # Close redshift connection
    conn.close()


if __name__ == "__main__":
    main()