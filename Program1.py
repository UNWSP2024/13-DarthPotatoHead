#Program Written By: Ainsley Bellamy
#Date Written: 04/29/2025
#Program Title: CitiesDatabase_Display


#Import proper module to create database.
import sqlite3
#I referenced the example source code from page 796 in our textbook.
#I was not sure if I was supposed to completely copy it or not, so I followed
#along and rewrote it into my own file for learning purposes.
def main():
#Connect/create proper database file.
    conn = sqlite3.connect('cities.db')
#Create cursor.
    cur = conn.cursor()
#Call various function to process/add data.
#insertTable() doesn't really need an explanation.
    insertTable(cur)
#insertInfo() runs through the cities list provided in our textbook source code and
#adds it to the new database file's table.
    insertInfo(cur)
#Commit changes.
    conn.commit()
#Now display the new data in the table.
    displayData(cur)
#Finally, close out the file.
    conn.close()

#Self-explanatory.
def insertTable(cur):
    cur.execute('DROP TABLE IF EXISTS Cities')
    cur.execute("""CREATE TABLE Cities (ID INTEGER PRIMARY KEY NOT NULL, CityName TEXT, Population INTEGER)""")

#Now insert the actual info into the rows.
def insertInfo(cur):
    info = [(1, 'Tokyo', 38001000),
                  (2, 'Delhi', 25703168),
                  (3, 'Shanghai', 23740778),
                  (4, 'Sao Paulo', 21066245),
                  (5, 'Mumbai', 21042538),
                  (6, 'Mexico City', 20998543),
                  (7, 'Beijing', 20383994),
                  (8, 'Osaka', 20237645),
                  (9, 'Cairo', 18771769),
                  (10, 'New York', 18593220),
                  (11, 'Dhaka', 17598228),
                  (12, 'Karachi', 16617644),
                  (13, 'Buenos Aires', 15180176),
                  (14, 'Kolkata', 14864919),
                  (15, 'Istanbul', 14163989),
                  (16, 'Chongqing', 13331579),
                  (17, 'Lagos', 13122829),
                  (18, 'Manila', 12946263),
                  (19, 'Rio de Janeiro', 12902306),
                  (20, 'Guangzhou', 12458130)]
#Insert using for-loop.
    for row in info:
        cur.execute('''INSERT INTO Cities (ID, CityName, Population) VALUES (?,?,?)''', (row[0], row[1], row[2]))

#This function neatly displays the data in the terminal.
def displayData(cur):
    cur.execute('SELECT * FROM Cities')
    results = cur.fetchall()
    for row in results:
        print(f'{row[0]:2}{row[1]:^30}{row[2]:10}')

if __name__ == '__main__':
    main()