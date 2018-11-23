import csv
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="!@)59380",
  database="footballStats"
)

with open('data/dlstats_2015_2017.csv', newline='') as csvfile:
	header = {}
	spamreader = csv.reader(csvfile, delimiter=',')
	for i,row in enumerate(spamreader):
		# create header dictionary with col num as values
		for y,col in enumerate(row):
			if i == 0:
				header[col] = y
		
		if i == 0:
			print(row)
			continue

		mycursor = mydb.cursor()
		name = row[header['Name']]
		sql = "SELECT id FROM players WHERE firstname = %s AND lastname = %s"
		val = name.replace(',','').rsplit(' ',1)

		#print(val)
		if ',' in name:
			mycursor.execute(sql, [val[1], val[0]])
		else:
			mycursor.execute(sql, val)

		# myresult = (player_id,)
		myresult = mycursor.fetchone()
		player_id = -1
		if myresult != None:
			player_id = myresult[0]
		# if the player doesn't exist in database, add player
		if myresult == None or len(myresult) == 0:
			mycursor = mydb.cursor()

			sql = "INSERT INTO players (firstname, lastname) VALUES (%s, %s)"
			
			if ',' in name:
				mycursor.execute(sql, [val[1], val[0]])
			else:
				mycursor.execute(sql, val)

			mydb.commit()
			player_id = mycursor.lastrowid


		mycursor = mydb.cursor()
		print(row)
		row_with_zeros = []
		for g, col in enumerate(row):
			if col == '':
				row_with_zeros.append(0)
			elif g > 2:
				row_with_zeros.append(int(col))
			else:
				row_with_zeros.append(col)
		print(row_with_zeros)
		sql = "INSERT INTO player_year_stats (player_id, pos, team, year, games_played, rush, rush_yards, rush_td, target, catch, catch_yards, catch_td, pass, complete, pass_yards, pass_td, interceptions, fumbles) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
		mycursor.execute(sql, [player_id]+row_with_zeros[1:])

		mydb.commit()

		