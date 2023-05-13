import requests
import json


class ClinicalTrialsRP:
    def __init__(self):
        self.base_url = 'https://clinicaltrials.gov/api/query/full_studies?'
        self.search_ext = 'expr=retinitis+pigmentosa+OR+progressive+pigmentary+retinopathy+OR+rod-cone+dystrophy+OR+RP&min_rnk=1&max_rnk=10&fmt=json'
        
    def fetch_data(self):
        payload = requests.get(self.base_url + self.search_ext)
        
        with open('clinical_trails.json', 'w') as f:
            json.dump(payload.json(), f)
            
    def get_ids(self):
        with open('clinical_trails.json', 'r') as f:
            trials_data = json.load(f)
            
            studies = trials_data['FullStudiesResponse']['FullStudies']
            
            ids = [study['Study']['ProtocolSection']['IdentificationModule']['NCTId'] for study in studies]
            for id in ids:
                self.check_records(id)
            
    def check_records(self, id):
        # call the db
        # check if trial is in db
        # if it is
        #   then end the process
        # otherwise
        #   create a trial data object to update the db
        #   pass event to kafka topic
        pass
            
    class TrialData:
        def __init__(self, id, title, authors, org, summary, start, primary, end):
            self.id = id
            self.title = title
            self.authors = authors
            self.org = org
            self.summary = summary
            self.start_date = start
            self.primary_date = primary
            self.end_date = end

def main():
    search_db = ClinicalTrialsRP()
    # search_db.fetch_data()
    search_db.get_ids()

if __name__ == '__main__':
    main()