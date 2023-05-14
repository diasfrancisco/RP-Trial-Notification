import requests
import json
import re

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
            self.authors = authors
            self.org = org
            self.summary = summary
            self.start_date = start_date
            self.primary_date = primary_date
            self.end_date = end_date
        
        def __str__(self) -> str:
            return f'A trial, ID: {self.id}, by {self.authors} on {self.title}'
        
    def fetch_data(self):
        payload = requests.get(self.base_url + self.search_ext)
        
        with open('clinical_trails.json', 'w') as f:
            json.dump(payload.json(), f)
            
    def get_ids(self):
        with open('clinical_trails.json', 'r') as f:
            trials_data = json.load(f)
            
            self.studies = trials_data['FullStudiesResponse']['FullStudies']
            
            ids = [study['Study']['ProtocolSection']['IdentificationModule']['NCTId'] for study in self.studies]
            for id in ids:
                self.check_records(id)
            
    def check_records(self, id):
        db = DatabaseStorage()
        db_ids = db.query_ids()
        
        if id not in db_ids:
            trial = self.create_records(id)
            
        db.insert_data()
        # add trial to db
            
    def create_records(self, id):
        for study in self.studies:
            if study['Study']['ProtocolSection']['IdentificationModule']['NCTId'] == id:
                try:
                    title = study['Study']['ProtocolSection']['IdentificationModule']['OfficialTitle']
                except:
                    title = 'Not available'
                    
                try:
                    authors_section = study['Study']['ProtocolSection']['ContactsLocationsModule']
                    authors = [v for k, v in self.recursive_keys(authors_section) if 'Name' in k]
                    if not authors:
                        authors.append('Not available')
                except:
                    authors = ['Not available']
                    
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
                except:
                    start_date = 'Not available'
                    
                try:
                    primary_date = study['Study']['ProtocolSection']['StatusModule']['PrimaryCompletionDateStruct']['PrimaryCompletionDate']
                except:
                    primary_date = 'Not available'
                    
                try:
                    end_date = study['Study']['ProtocolSection']['StatusModule']['CompletionDateStruct']['CompletionDate']
                except:
                    end_date = 'Not available'
        
                trial = self.TrialData(id, title, authors, org, summary, start_date, primary_date, end_date)
                return trial
            else:
                print('ID not available')
                
    def recursive_keys(self, authors_section):
        for k, v in authors_section.items():
            if type(v) is dict:
                yield (k, v)
                yield from self.recursive_keys(v)
            elif type(v) is list:
                for i in v:
                    yield from self.recursive_keys(i)
            else:
                yield (k, v)

def main():
    search_db = ClinicalTrialsRP()
    # search_db.fetch_data()
    search_db.get_ids()

if __name__ == '__main__':
    main()