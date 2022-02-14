from github import Github
import gspread,datetime,re,argparse
from oauth2client.service_account import ServiceAccountCredentials

#Github Auth token
token = open("token.txt", "r")
for token_ in token.readlines(): 
    ACCESS_TOKEN = token_  #github token 
g = Github(ACCESS_TOKEN)
datetime_dt = datetime.datetime.today()

def search_github(keywords, day_):
    #time range
    datetime_str = datetime_dt.strftime("%Y-%m-%d")
    delta_day = datetime.timedelta(days=day_)    #defult is past a week
    early_datetime_str = datetime_dt - delta_day
    early_datetime_str_ = early_datetime_str.strftime("%Y-%m-%d")
    #query args
    query = '+'.join(keywords) + ' created:' + early_datetime_str_ + '..' + datetime_str + ' in:readme,description'
    repositories_sum = g.search_repositories(query, sort = 'updated')

    print(f'Found {repositories_sum.totalCount} repo(s)')
    result_ = []
    for repo in repositories_sum:
        #print(repo.__dict__)
        CVE_ = CVE_parser(f'{repo.description}', f'{repo.clone_url}')
        data = f'{repo.clone_url}' + ',' + f'{repo.updated_at}' + ',' + f'{repo.created_at}' + ',' + CVE_
        data = [data_.strip() for data_ in data.split(',')]
        result_.append(data)
    return result_

def CVE_parser(description, url):
    CVE_pattern = re.compile(r'(?i)CVE-\d{4}-\d{4,7}')
    if bool(CVE_pattern.findall(description)) == True:
        CVE = CVE_pattern.findall(description)
        CVE = "".join(CVE)
        return CVE
    else:
        CVE = CVE_pattern.findall(url)
        CVE = "".join(CVE)
        return CVE    

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

def parse_args():
    parser = argparse.ArgumentParser(description="exploit search")
    parser.add_argument("type", choices=["gsheet", "print"],
                        help="print out type")
    parser.add_argument("-d", "--day", type=int, default=1,
                        help="trace back day")
    args = parser.parse_args()
    return vars(args)

def main(keywords):
    args = parse_args()
    if args["type"] == "gsheet":
        repo_data = search_github(keywords, day_=args["day"])
        gsheet(repo_data)
    else:
        repo_data = search_github(keywords, day_=args["day"])
        for i in repo_data:
            print(i, end = ' ')
            print()

if __name__ == '__main__':
    #Keyword for github search, ex:CVE number, exploit name, etc.
    fo = open("keywords.txt", "r")
    for keywords in fo.readlines(): 
        keywords = keywords.strip()       
    keywords = [keyword.strip() for keyword in keywords.split(',')]
    main(keywords)
    