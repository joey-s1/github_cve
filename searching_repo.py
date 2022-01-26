from github import Github
import gspread,datetime,re
from oauth2client.service_account import ServiceAccountCredentials

#Github Auth token
token = open("token.txt", "r")
for token_ in token.readlines(): 
    ACCESS_TOKEN = token_  #github token 
g = Github(ACCESS_TOKEN)
datetime_dt = datetime.datetime.today()

def search_github(keywords):
    #time range
    datetime_str = datetime_dt.strftime("%Y-%m-%d")
    delta_day = datetime.timedelta(days=7)    #defult is past a week
    early_datetime_str = datetime_dt - delta_day
    early_datetime_str_ = early_datetime_str.strftime("%Y-%m-%d")
    #query args
    query = '+'.join(keywords) + ' created:' + early_datetime_str_ + '..' + datetime_str + ' in:readme,description'
    repositories_sum = g.search_repositories(query, sort = 'updated')

    print(f'Found {repositories_sum.totalCount} repo(s)')
    result_ = []
    for repo in repositories_sum:
        #print(repo.__dict__)
        CVE_pattern = re.compile(r'CVE-\d{4}-\d{4,7}')
        CVE = CVE_pattern.findall(f'{repo.description}')
        CVE_ = "".join(CVE)
        data = f'{repo.clone_url}' + ',' + f'{repo.updated_at}' + ',' + f'{repo.created_at}' + ',' + CVE_
        data = [data_.strip() for data_ in data.split(',')]
        result_.append(data)
    return result_

def gsheet(datas):
    #google client OAuth
    scopes = ["https://spreadsheets.google.com/feeds"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scopes) #google sheet credentials
    client = gspread.authorize(credentials) 
    #update github information to google sheet
    sheet = client.open_by_key("1t7HL6ysRiM-r_TxS5sGBg2a0vjlYYXj3pnwih4vBepY") #google sheet key
    datetime_str = datetime_dt.strftime("%Y-%m-%d")
    worksheet = sheet.add_worksheet(title=datetime_str, rows="100", cols="20")
    titles = ("Repositories","Update time", "Create time", "CVE") 
    worksheet.insert_row(titles, 1)
    for data in datas:
        worksheet.append_row(data)

if __name__ == '__main__':
    #Keyword for github search, ex:CVE number, exploit name, etc.
    fo = open("keywords.txt", "r")
    for keywords in fo.readlines(): 
        keywords = keywords.strip()       
    keywords = [keyword.strip() for keyword in keywords.split(',')]
    
    repo_data = search_github(keywords)
    gsheet(repo_data)