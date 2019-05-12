import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Load raw data from S3 into redshift staging tables
    
    Parameters: 
    cur: redshift cursor
    conn: redshift connection 
  
    Returns: 
    None
    
    """
    
    # Execute SQL queries to load data from S3 into redshift staging tables
    print("Loading data from S3 into redshift staging tables...")
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Insert data from staging into final tables in redshift
    
    Parameters: 
    cur: redshift cursor
    conn: redshift connection 
  
    Returns: 
    None
    
    """

    # Execute SQL queries to insert data from staging into final tables in redshift
    print("Inserting data from staging into final tables...")
    for query in insert_table_queries:
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

    # Connect to redshift cluster
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    # Load data from s3 into redshift staging tables
    load_staging_tables(cur, conn)
    
    # Insert data from staging into final tables in redshift
    insert_tables(cur, conn)

    # Close redshift connection
    conn.close()


if __name__ == "__main__":
    main()