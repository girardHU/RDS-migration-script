import logging, json
from pymysql import cursors, connect

if __name__ == '__main__':
    # Configure logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    log_file = './data_migration.log'
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info('Migration started')

    with open('tables.json') as f:
        tables = json.load(f)

    # Database connection details
    source_db_config = {
        'db': 'mydatabase1',
        'user': 'user1',
        'password': 'password1',
        'host': 'localhost',
        'port': 33061
    }

    destination_db_config = {
        'db': 'mydatabase2',
        'user': 'user2',
        'password': 'password2',
        'host': 'localhost',
        'port': 33062
    }

    # Connect to the source and destination databases
    source_conn = connect(**source_db_config, cursorclass=cursors.DictCursor)
    dest_conn = connect(**destination_db_config, cursorclass=cursors.DictCursor)
    source_cursor = source_conn.cursor()
    dest_cursor = dest_conn.cursor()

    for table in tables:
        try:
            logger.info(f"Current table : {table}")
            # Copy data from source to destination
            source_cursor.execute(f"SELECT * FROM `{table}`")
            rows = source_cursor.fetchall()

            if rows:
                # Get column names except for the auto-incrementing ID
                columns = list(rows[0].keys())
                if 'ID' in columns:
                    columns.remove('ID')

                # Generate the insert query excluding the ID
                placeholders = ', '.join('%s' for _ in columns)
                column_names = ', '.join(columns)
                insert_query = f"INSERT IGNORE INTO `{table}` ({column_names}) VALUES ({placeholders})"

                # Prepare data for insertion (excluding the ID)
                data_to_insert = [tuple(row[col] for col in columns) for row in rows]
                nb_rows_affected = dest_cursor.executemany(insert_query, data_to_insert)
                dest_conn.commit()
                logger.info(f"Operation affected {nb_rows_affected} rows")

        except Exception as e:
            # Handle exceptions
            logger.error(f"Error processing table {table}: {e}")
            source_conn.rollback()
            dest_conn.rollback()

    # Close connections
    source_cursor.close()
    source_conn.close()
    dest_cursor.close()
    dest_conn.close()

    logger.info("Script concluded properly")
