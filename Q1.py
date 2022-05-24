import requests
import sqlite3
import xmltodict
import json

'''
KNS_Bill - Implements a function which reads all the data from the table "KNS_Bill" from the Knesset interface,
        and writes the data to the table of sqlite I created. 
'''

def null_check(value):
    if type(value) is not str:
        try:
            value['@m:null']
        except:
            val = value['#text']
            if val == '@null':
                return None
            else:
                return val
    else:
        return value


if __name__ == '__main__':
    ans_list = []
    # Gets the data from the URL & converts the xml to dict
    response = requests.get('https://knesset.gov.il/Odata/ParliamentInfo.svc/KNS_Bill()')
    xml_response = xmltodict.parse(response.text)
    #res_dict = json.dumps(xml_response)

    for values in xml_response['feed']['entry']:
        temp_bill = ()
        content_properties = values['content']['m:properties']
        BillID = null_check(content_properties['d:BillID'])
        KnessetNum = null_check(content_properties['d:KnessetNum'])
        Name = null_check(content_properties['d:Name'])
        SubTypeID = null_check(content_properties['d:SubTypeID'])
        SubTypeDesc = null_check(content_properties['d:SubTypeDesc'])
        PrivateNumber = null_check(content_properties['d:PrivateNumber'])
        CommitteeID = null_check(content_properties['d:CommitteeID'])
        StatusID = null_check(content_properties['d:StatusID'])
        Number = null_check(content_properties['d:Number'])
        PostponementReasonID = null_check(content_properties['d:KnessetNum'])
        PostponementReasonDesc = null_check(content_properties['d:PostponementReasonDesc'])
        PublicationDate = null_check(content_properties['d:PublicationDate'])
        MagazineNumber = null_check(content_properties['d:MagazineNumber'])
        PageNumber = null_check(content_properties['d:PageNumber'])
        IsContinuationBill = null_check(content_properties['d:IsContinuationBill'])
        SummaryLaw = null_check(content_properties['d:SummaryLaw'])
        PublicationSeriesID = null_check(content_properties['d:PublicationSeriesID'])
        PublicationSeriesDesc = null_check(content_properties['d:PublicationSeriesDesc'])
        PublicationSeriesFirstCall = null_check(content_properties['d:PublicationSeriesFirstCall'])
        #PublicationSeriesFirstCallDesc = content['d:KnessetNum']['#text']
        LastUpdatedDate = null_check(content_properties['d:LastUpdatedDate'])
        temp_bill = (BillID, KnessetNum, Name, SubTypeID, SubTypeDesc, PrivateNumber, CommitteeID, StatusID,
                     Number, PostponementReasonID, PostponementReasonDesc, PublicationDate, MagazineNumber, PageNumber,
                     IsContinuationBill, SummaryLaw, PublicationSeriesID, PublicationSeriesDesc,
                     PublicationSeriesFirstCall, LastUpdatedDate)
        ans_list.append(temp_bill)
    # Create the database
    db = sqlite3.connect('my_database.db')
    # Get a cursor
    cursor = db.cursor()
    # Create the tabels
    cursor.execute('''
                CREATE TABLE KNS_Bill(BillID INTEGER PRIMARY KEY, KnessetNum INTEGER, Name VARCHAR(255), SubTypeID INTEGER,
                 SubTypeDesc VARCHAR(125), PrivateNumber INTEGER, CommitteeID INTEGER, StatusID INTEGER, Number INTEGER,
                  PostponementReasonID INTEGER, PostponementReasonDesc VARCHAR(125), PublicationDate DATETIME2,
                  MagazineNumber INTEGER, PageNumber INTEGER, IsContinuationBill BIT, SummaryLaw VARCHAR,
                  PublicationSeriesID INTEGER, PublicationSeriesDesc VARCHAR(125), PublicationSeriesFirstCallID INTEGER
                  , LastUpdatedDate DATETIME2)
                  ''')

    cursor.executemany(''' INSERT INTO KNS_Bill(BillID, KnessetNum, Name, SubTypeID, SubTypeDesc, PrivateNumber,
    CommitteeID, StatusID, Number, PostponementReasonID, PostponementReasonDesc, PublicationDate, MagazineNumber, 
    PageNumber, IsContinuationBill, SummaryLaw, PublicationSeriesID, PublicationSeriesDesc, 
    PublicationSeriesFirstCallID, LastUpdatedDate)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', ans_list)


    # select all the data from the cursor and print it
    cursor.execute(''' SELECT * FROM KNS_Bill''')
    for row in cursor:
        print(row)
    print("Many bills inserted")
    db.commit()