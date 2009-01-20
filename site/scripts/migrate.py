import MySQLdb
import datetime

   # cursor = conn.cursor ()
   # cursor.execute ("SELECT VERSION()")
   # row = cursor.fetchone ()
   # print "server version:", row[0]
   # cursor.close ()
   # conn.close ()

# Old Podiobooks DB
pbconn = MySQLdb.connect (host = "localhost",
                          user = "root",
                          passwd = "password",
                          db = "podiobooks")

# New PB2 DB
pb2conn = MySQLdb.connect (host = "localhost",
                        user = "root",
                        passwd = "password",
                        db = "pb2")

print "Migrating Titles..."
pbcursor = pbconn.cursor()
pbcursor.execute ("SELECT * from book where enabled = 1")
while (1):
	row = pbcursor.fetchone()
	if row == None:
		break
	print "Moving %s ..." % row[1]
	old_id = row[0]
	name = row[1]
	date_created = row[2]
	description = row[5]
	promo = row[8]
	cover = row[10]
	display_on_homepage = row[11]
	explicit = row[13]
	slug = row[14]
	is_complete = row[16]
	AvgAudioQuality = row[26]
	AvgNarration = row[27]
	AvgWriting = row[28]
	AvgOverall = row[29]
	is_adult = 0
	if explicit == 4:
		is_adult = 1
	date_updated = datetime.datetime.now()
	
	pb2cursor = pb2conn.cursor()
	sql = """INSERT INTO main_title (name,date_created,description,cover,display_on_homepage,
						slug,is_complete,avg_audio_quality,avg_narration,avg_writing,avg_overall,old_id, is_adult, date_updated)
	                  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""" 
	pb2cursor.execute(sql,	(name,date_created,description,cover,display_on_homepage,slug,is_complete,AvgAudioQuality,AvgNarration,AvgWriting,AvgOverall,old_id,is_adult, date_updated))
	pb2conn.commit()
	pb2cursor.close()
	
print "Done!"
pbcursor.close()
pbconn.close()
pb2conn.close()
	
	

