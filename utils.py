

import models
from datetime import datetime


#Just some global varbs. 
favicon_path = '/static/img/favicon.ico'
companyType = ['Public', 'Private', 'Nonprofit']
companyFunction = ['Consumer Research and/or Marketing', 'Consumer Services', 'Data Management and Analysis', 'Financial/Investment Services', 'Information for Consumers']
criticalDataTypes = ['Federal Open Data', 'State Open Data', 'City/Local Open Data', 'Private/Proprietary Data Sources']
revenueSource = ['Advertising', 'Data Management and Analytic Services', 'Database Licensing', 'Lead Generation To Other Businesses', 'Philanthropy', 'Software Licensing', 'Subscriptions', 'User Fees for Web or Mobile Access']
sectors = ['Agriculture', 'Arts, Entertainment and Recreation' 'Crime', 'Education', 'Energy', 'Environmental', 'Finance', 'Geospatial data/mapping', 'Health and Healthcare', 'Housing/Real Estate', 'Manufacturing', 'Nutrition', 'Scientific Research', 'Social Assistance', 'Trade', 'Transportation', 'Telecom', 'Weather']
datatypes = ['Federal Open Data', 'State Open Data', 'City/Local Open Data']
categories = ['Business & Legal Services', 'Data/Technology', 'Education', 'Energy', 'Environment & Weather', 'Finance & Investment', 'Food & Agriculture', 'Geospatial/Mapping', 'Governance', 'Healthcare', 'Housing/Real Estate', 'Insurance', 'Lifestyle & Consumer', 'Research & Consulting', 'Scientific Research', 'Transportation']
states ={ "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KA": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming", "PR": "Puerto Rico"}
stateListAbbrev = [ "", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KA", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "PR"]
stateList = ["(Select State)", "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming", "Puerto Rico"]

class Validators(object):
	def check_for_duplicates(self, companyName):
		#check if companyName exists:
		try: 
			c = models.Company2.objects.get(prettyName=re.sub(r'([^\s\w])+', '', companyName).replace(" ", "-").title())
			response = { "error": "This company has already been submitted. Email opendata500@thegovlab.org for questions." }
		except:
			response = 'true'
		return response


class StatsGenerator(object):
    def get_total_companies(self):
        return models.Stats.objects().first().totalCompanies
    
    def get_total_companies_web(self):
        return models.Stats.objects().first().totalCompaniesWeb
    
    def get_total_companies_surveys(self):
        return models.Stats.objects().first().totalCompaniesSurvey

    def update_totals_companies(self):
        s = models.Stats.objects().first()
        s.totalCompanies = models.Company2.objects().count()
        s.totalCompaniesWeb = models.Company2.objects(submittedThroughWebsite = True).count()
        s.totalCompaniesSurvey = models.Company2.objects(submittedSurvey = True).count()
    
    def increase_individual_state_count(self, state):
        stats = models.Stats.object().first()
        for s in stats.states:
            if s.name == state:
                s.count = s.count + 1
        stats.save()

    def update_all_state_counts(self):
        stats = models.Stats.objects().first()
        companies  = models.Company2.objects(display=True)
        stateCount = []
        for c in companies:
            stateCount.append(c.state)
        stats.states = []
        for i in range(1, 53):
            s = models.States(
                name = stateList[i],
                abbrev = stateListAbbrev[i],
                count = stateCount.count(stateListAbbrev[i]))
            stats.states.append(s)
        stats.save()

    def refresh_stats(self):
        stats = models.Stats.objects().first()
        stats.totalCompanies = models.Company2.objects().count()
        stats.totalCompaniesWeb = models.Company2.objects(submittedThroughWebsite = True).count()
        stats.totalCompaniesSurvey = models.Company2.objects(submittedSurvey = True).count()
        companies  = models.Company2.objects(display=True)
        stateCount = []
        for c in companies:
            stateCount.append(c.state)
        stats.states = []
        for i in range(1, 53):
            s = models.States(
                name = stateList[i],
                abbrev = stateListAbbrev[i],
                count = stateCount.count(stateListAbbrev[i]))
            stats.states.append(s)
        stats.lastUpdate = datetime.now()
        stats.save()


class FileGenerator(object):
    def generate_company_json(self):
        #------COMPANIES JSON---------
        companies = models.Company2.objects(display=True)
        companiesJSON = []
        for c in companies:
            agencies = []
            for a in c.agencies:
                datasets_agency = []
                for d in a.datasets:
                    if c == d.usedBy:
                        ds = {
                            "datasetName":d.datasetName,
                            "datasetURL":d.datasetURL,
                            "rating":d.rating
                        }
                        datasets_agency.append(ds)
                subagencies = []
                for s in a.subagencies:
                    if c in s.usedBy:
                        datasets_subagency = []
                        for d in s.datasets:
                            if c == d.usedBy:
                                ds = {
                                    "datasetName":d.datasetName,
                                    "datasetURL":d.datasetURL,
                                    "rating":d.rating
                                }
                                datasets_subagency.append(ds)
                        sub = {
                            "name":s.name,
                            "abbrev":s.abbrev,
                            "url":s.url,
                            "datasets":datasets_subagency
                        }
                        subagencies.append(sub)
                ag = {
                    "name": a.name,
                    "abbrev":a.abbrev,
                    "prettyName":a.prettyName,
                    "url": a.url,
                    "type":a.dataType,
                    "datasets":datasets_agency,
                    "subagencies":subagencies
                }
                agencies.append(ag)
            company = {
                "company_name_id": c.prettyName,
                "companyName": c.companyName,
                "url": c.url,
                "city": c.city,
                "state": c.state,
                "zipCode": c.zipCode,
                "ceoFirstName": c.ceo.firstName,
                "ceoLastName": c.ceo.lastName,
                "yearFounded": c.yearFounded,
                "fte": c.fte,
                "companyType": c.companyType,
                "companyCategory": c.companyCategory,
                "revenueSource": c.revenueSource,
                "description": c.description,
                "descriptionShort": c.descriptionShort,
                "agencies":agencies,
                "subagencies":subagencies
            }
            companiesJSON.append(company)
        with open(os.path.join(os.path.dirname(__file__), 'static') + '/OD500_Companies.json', 'w') as outfile:
            json.dump(companiesJSON, outfile)
    def generate_agency_json(self):
        #--------------JSON OF AGENCIES------------
        agencies = models.Agency.objects(source="dataGov")
        agenciesJSON = []
        for a in agencies:
            #--------DATASETS AT AGENCY LEVEL------
            datasets_agency = []
            for d in a.datasets:
                ds = {
                    "datasetName":d.datasetName,
                    "datasetURL":d.datasetURL,
                    "rating":d.rating,
                    "usedBy":d.usedBy.prettyName
                }
                datasets_agency.append(ds)
            #--------SUBAGENCIES------
            subagencies = []
            for s in a.subagencies:
                datasets_subagency = []
                for d in s.datasets:
                    logging.info(d.datasetName)
                    ds = {
                        "datasetName":d.datasetName,
                        "datasetURL":d.datasetURL,
                        "rating":d.rating,
                        "usedBy": d.usedBy.prettyName
                    }
                    datasets_subagency.append(ds)
                usedBy = []
                for u in s.usedBy:
                    usedBy.append(u.prettyName)
                sub = {
                    "name":s.name,
                    "abbrev":s.abbrev,
                    "url":s.url,
                    "datasets":datasets_subagency,
                    "usedBy":usedBy
                }
                subagencies.append(sub)
            #--------SUBAGENCIES------
            usedBy = []
            for u in a.usedBy:
                usedBy.append(u.prettyName)
            ag = {
                "name": a.name,
                "abbrev":a.abbrev,
                "prettyName":a.prettyName,
                "url": a.url,
                "type":a.dataType,
                "datasets":datasets_agency,
                "subagencies":subagencies,
                "usedBy":usedBy
            }
            agenciesJSON.append(ag)
        with open(os.path.join(os.path.dirname(__file__), 'static') + '/OD500_Agencies.json', 'w') as outfile:
            json.dump(agenciesJSON, outfile)

    def generate_company_csv(self):
        #---CSV OF ALL COMPANIES----
        companies = models.Company2.objects(display=True)
        csvwriter = csv.writer(open(os.path.join(os.path.dirname(__file__), 'static') + "/OD500_companies.csv", "w"))
        csvwriter.writerow([
            'company_name_id',
            'CompanyName',
            'url',
            'city',
            'state',
            'zipCode',
            'ceoFirstName',
            'ceoLastName',
            'yearFounded',
            'fte',
            'companyType',
            'companyCategory',
            'revenueSource',
            'description',
            'descriptionShort',
            'financialInfo'
            ])
        for c in companies:
            newrow = [
                c.prettyName,
                c.companyName,
                c.url,
                c.city,
                c.state,
                c.zipCode,
                c.ceo.firstName,
                c.ceo.lastName,
                c.yearFounded,
                c.fte,
                c.companyType,
                c.companyCategory,
                ', '.join(c.revenueSource),
                c.description,
                c.descriptionShort,
                c.financialInfo,
            ]
            for i in range(len(newrow)):  # For every value in our newrow
                if hasattr(newrow[i], 'encode'):
                    newrow[i] = newrow[i].encode('utf8')
            csvwriter.writerow(newrow)