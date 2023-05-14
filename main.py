import requests
import json

from data_storage import DatabaseStorage


class ClinicalTrialsRP:
    def __init__(self):
        self.base_url = 'https://clinicaltrials.gov/api/query/full_studies?'
        self.search_ext = 'expr=retinitis+pigmentosa+OR+progressive+pigmentary+retinopathy+OR+rod-cone+dystrophy+OR+RP&min_rnk=1&max_rnk=10&fmt=json'
        self.studies = None
        
    class TrialData:
        def __init__(self, id, title, authors, org, summary, start_date, primary_date, end_date):
            self.id = id
            self.title = title
            self.authors = authors #list
            self.org = org
            self.summary = summary
            self.start_date = start_date
            self.primary_date = primary_date
            self.end_date = end_date
        
        def __str__(self) -> str:
            return f'A trial, ID: {self.id}, by {self.authors} on {self.title}'
        
    def fetch_data(self):
        # Collect the trials data for a particular disease and save as a json file
        payload = requests.get(self.base_url + self.search_ext)
        
        with open('clinical_trails.json', 'w') as f:
            json.dump(payload.json(), f)
            
    def get_ids(self):
        db = DatabaseStorage()
        db.create_table()
        # Read the contents of the json file
        with open('clinical_trails.json', 'r') as f:
            trials_data = json.load(f)
            
            self.studies = trials_data['FullStudiesResponse']['FullStudies']
            
            trials = []
            
            # Grab all the ids and check them against the database
            ids = [study['Study']['ProtocolSection']['IdentificationModule']['NCTId'] for study in self.studies]

            for id in ids:
                trial = self.check_records(id)
                if not None:
                    trials.append(trial)
                    
            if trials:
                for trial in trials:
                    db.insert_data(trial)
            
    def check_records(self, id):
        # Query the database for the ids currently present
        db = DatabaseStorage()
        db_ids = db.query_ids()
        
        # If the id is not present then we create a trial object which holds all the metadata
        if id not in db_ids:
            trial = self.create_records(id)
            return trial
        else:
            return None
            
    def create_records(self, id):
        # Iterate through every study
        for study in self.studies:
            # If the id matches, grab the metadata of that trial and return as a trial object
            if study['Study']['ProtocolSection']['IdentificationModule']['NCTId'] == id:
                try:
                    title = study['Study']['ProtocolSection']['IdentificationModule']['OfficialTitle']
                except:
                    title = 'Not available'
                    
                try:
                    authors_section = study['Study']['ProtocolSection']['ContactsLocationsModule']
                    authors = [v for k, v in self.recursive_keys(authors_section) if 'Name' in k]
                    if not authors:
                        authors = 'Not available'
                    else:
                        authors = ','.join(authors)
                except:
                    authors = 'Not available'
                    
                try:
                    org = study['Study']['ProtocolSection']['IdentificationModule']['Organization']['OrgFullName']
                except:
                    org = 'Not available'
                    
                try:
                    summary = ' '.join(study['Study']['ProtocolSection']['DescriptionModule']['DetailedDescription'].split())
                except:
                    summary = 'Not available'
                    
                try:
                    start_date = study['Study']['ProtocolSection']['StatusModule']['StartDateStruct']['StartDate']
                    start_date = self.convert_date(start_date)
                except:
                    start_date = 'Not available'
                    
                try:
                    primary_date = study['Study']['ProtocolSection']['StatusModule']['PrimaryCompletionDateStruct']['PrimaryCompletionDate']
                    primary_date = self.convert_date(primary_date)
                except:
                    primary_date = 'Not available'
                    
                try:
                    end_date = study['Study']['ProtocolSection']['StatusModule']['CompletionDateStruct']['CompletionDate']
                    end_date = self.convert_date(end_date)
                except:
                    end_date = 'Not available'
        
                trial = self.TrialData(id, title, authors, org, summary, start_date, primary_date, end_date)
                return trial
            else:
                pass
                
    def recursive_keys(self, authors_section):
        # Recursively find all the authors of a trial
        for k, v in authors_section.items():
            if type(v) is dict:
                yield (k, v)
                yield from self.recursive_keys(v)
            elif type(v) is list:
                for i in v:
                    yield from self.recursive_keys(i)
            else:
                yield (k, v)
                
    def convert_date(self, date):
        digits = sum(d.isdigit() for d in date)
        if digits < 5:
            date = date[:-5] + ' 1' + date[-5:]
            return date
        else:
            date = date.replace(',', '')
            return date

def main():
    search_db = ClinicalTrialsRP()
    search_db.fetch_data()
    search_db.get_ids()

if __name__ == '__main__':
    main()