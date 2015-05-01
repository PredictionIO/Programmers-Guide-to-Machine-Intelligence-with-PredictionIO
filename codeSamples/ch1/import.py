import predictionio
DELIMITER = ","

def import_events(client, filename):
	count = 0
	with open(filename) as f:
		for line in f:
			data = line.rstrip('\r\n').split(DELIMITER)	
			client.create_event(
        		event="rate",
        		entity_type="user",
        		entity_id=data[0],
        		target_entity_type="item",
        		target_entity_id=data[1],
        		properties= { "rating" : float(data[2]) }
        	)   
			count += 1
  	
  	print "%s events are imported." % count

client = predictionio.EventClient(
    access_key='sG0Eqo2URu5YNIQ1B4ppF1gWx79LoHGPjHGcMQ7zW6070FAA1c1rLA762cya6p5e',
    url='http://localhost:7070',
    threads=5,
    qsize=500)
import_events(client, 'music.csv')
