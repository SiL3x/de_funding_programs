import pandas as pd

from datetime import datetime


data = pd.read_json("grs-fbw_programm_test.json", orient='records')

data2 = data.rename(
    columns={
    'VorhabenTitel': 'name',
    'LaufzeitStart': 'start',
    'LaufzeitEnde': 'end',
    'Mittel': 'amount',
    'Thema': 'description',
    'Auftragnehmer': 'partner',
    'KlassifizierungLabel': 'topics'    
    } 
)

data2['other_links'] = ""

for index, row in data2.iterrows():
    links = []
    t1 = data2.at[index, 'start']
    t2 = data2.at[index, 'end']
    data2.at[index, 'start'] = str(datetime.fromtimestamp(int(t1[6:-5])))
    data2.at[index, 'end'] = str(datetime.fromtimestamp(int(t2[6:-5])))
    
    for entry in row['Files']:
        links += ['https://www.grs-fbw.de/Archiv/ArchivSearch/DownloadSingleFile?guid=' + entry['FileGuid']]
        data2.at[index, 'other_links'] = links

data2.drop(
    columns=[
    'VorhabenId',
    'VorhabenNr',
    'KurztitelEng',
    'KurztitelDe',
    'HasAbschlussbericht',
    'Files',
    'MittelLabel',
    'HasMetadata'
    ], inplace=True)

data2[
    ["program_link","runtime","region", "Förderbereich", "keywords", "contact", "eligible","funding_reciever"]
] = ""

data2["managing_organization"] = "Gesellschaft für Anlagen- und Reaktorsicherheit (GRS)"
data2["funding_provider"] = ""

data2.to_csv("grs_data.csv", sep=",", index=False, quotechar="'")
