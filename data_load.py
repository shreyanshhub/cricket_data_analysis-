from app import db,Data
import csv

with open('data.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    # Skip the header row
    next(csvreader)
    for row in csvreader:
        # Create a new instance of YourModel for each row in the CSV file
        new_instance = Data(innings=int(row[1]), overs=float(row[2]), ballnumber=int(row[3]), batter=row[4], bowler=row[5], non_striker=row[6], extra_type=row[7], batsman_run=int(row[8]), extras_run=int(row[9]), total_run=int(row[10]), non_boundary=bool(row[11]), is_wicket_delivery=bool(row[12]), player_out=row[13], kind=row[14], fielders_involved=row[15], batting_team=row[16])
        # Add the new instance to the database session
        db.session.add(new_instance)

db.session.commit()
