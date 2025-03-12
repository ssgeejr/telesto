import sys, csv, getopt, mysql.connector
from datetime import datetime
from Saturn import Gravity

class Parser:
    def __init__(self):
        self.db_connection = None
        self.db_cursor = None
        self.file_path = None
        self.total_records = 0

    def connect_to_db(self):
        try:
            gravity = Gravity('.telesto')
            self.db_connection = mysql.connector.connect(
                host=gravity.getServer(),
                user=gravity.getUsername(),
                password=gravity.getPassword(),
                database=gravity.getDB()
            )
            self.db_cursor = self.db_connection.cursor()

        except mysql.connector.Error as err:
            print("Error connecting to MySQL:", err)
            exit(1)

    def parseToDisbledFile(self):
        try:
            self.connect_to_db()  # Ensure database connection is established

            print(f'Parsing file {self.filename}')

            with open(self.filename, mode='r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)  # Read the header row

                # Map CSV column names to expected database columns
                name_idx = headers.index("DisplayName")
                email_idx = headers.index("UserPrincipalName")
                department_idx = headers.index("Department")
                lastlogin_idx = headers.index("LastLoginDateTime")
                lastlogindays_idx = headers.index("DaysSinceLastLogin")

                insert_query = """
                    INSERT INTO disable (name, email, department, lastlogin, lastlogindays) 
                    VALUES (%s, %s, %s, %s, %s)
                """

                for row in reader:
                    try:
                        name = row[name_idx].strip()
                        email = row[email_idx].strip()
                        department = row[department_idx].strip()

                        # Convert LastLoginDateTime to DATE format
                        lastlogin_str = row[lastlogin_idx].strip()
                        lastlogin = datetime.strptime(lastlogin_str,
                                                      "%Y-%m-%d %H:%M:%S").date() if lastlogin_str else None

                        # Convert DaysSinceLastLogin to an integer
                        lastlogindays = int(row[lastlogindays_idx].strip()) if row[
                            lastlogindays_idx].strip().isdigit() else None

                        self.db_cursor.execute(insert_query, (name, email, department, lastlogin, lastlogindays))

                    except (ValueError, IndexError) as e:
                        print(f"Skipping row due to error: {e}")

            self.db_connection.commit()
            print("Data insertion completed successfully.")

        except FileNotFoundError as e:
            raise FileNotFoundError(f"File Error: {e}")
        except PermissionError as e:
            raise PermissionError(f"File Permission Error: {e}")
        except mysql.connector.Error as e:
            raise mysql.connector.Error(f"Database Error: {e}")
        except Exception as e:
            raise Exception(f"Unexpected Error: {e}")
        finally:
            if self.db_connection and self.db_connection.is_connected():
                self.db_cursor.close()
                self.db_connection.close()

    def process(self, argv):

        try:
            opts, args = getopt.getopt(argv, "f:k:hx")
        except getopt.GetoptError as e:
            print('>>>> ERROR: %s' % str(e))
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('Telesto.py -h Help Message  #This help message')
                print('Telesto.py -f {nmap file}   #The NMAP file to parse')
                print('Telesto.py -x               #DO not insert records ... just print the results')
                sys.exit()
            elif opt in "-x":
                self.parseOnly = True
            elif opt in "-f":
                self.filename = arg

        if not self.filename:
            print('Missing filename ...')
            print('python Telesto.py -f myfile.csv')
            sys.exit(-1)

        self.parseToDisbledFile()


if __name__ == '__main__':
    Parser().process(sys.argv[1:])
