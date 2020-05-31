import mysql.connector
import requests
import re
from bs4 import BeautifulSoup
from sklearn import tree

#function for Grabing data from website and save to mysql database
def grab_from_site_and_savemysql(n):

    list_rgn = list()
    list_yb = list()
    list_sqrm = list()
    list_prc = list()

    for i in range(1, n):
        url = 'https://shabesh.com/search/' + str(i) + "خرید-فروش/املاک/ایران/"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        rgns = soup.find_all('h2', attrs={'class': 'announce-desc medium-sans pb-2'})  # و متراژ پیدا کردن مناطق
        for rgn_m in rgns:
            rg = re.findall(r'در\s(.*)\،', rgn_m.text)
            list_rgn.extend(rg)
            m = re.findall(r"آپارتمان\s(\d+)", rgn_m.text)
            if len(m)==0:
                list_sqrm.extend('0')
            else:
                list_sqrm.extend(m)

        built_years_meter = soup.find_all('li')  # پیدا کردن سال ساخت
        for bym in built_years_meter:
            yb = re.findall(r'ساخت(\s\d{4})', bym.text)
            if len(yb) != 0:
                list_yb.extend(yb)

        all_price = soup.find_all('span', attrs={'class': 'rent pb-2'})
        for prc in all_price:
            cost = re.findall(r'\d*\,*\d+\,*\d+\,*\d+', prc.text)
            list_prc.extend(cost)

    list_rgn.reverse()
    print(list_yb)
    print(list_rgn)
    print(list_sqrm)
    print(list_prc)
    print(len(list_yb), len(list_rgn), len(list_sqrm), len(list_prc))  # functio

    for i in range(0, len(list_yb)):
        cnx = mysql.connector.connect(user='root', password='apolo11',
                                      host='127.0.0.1',
                                      database='project_advance')
        cursor = cnx.cursor()
        cursor.execute('INSERT INTO project VALUES(\'%s\',\'%i\',\'%i\',\'%s\')' % (
            list_rgn[i], int(list_yb[i]), int(list_sqrm[i]), list_prc[i]))
        cnx.commit()
        cnx.close()


cnx = mysql.connector.connect(user='ehsan', password='apolo11',
                                  host='127.0.0.1',
                                  database='project_advance')
cursor=cnx.cursor()
query = 'SELECT * FROM project'
cursor.execute(query)
list_data=list()

for data in cursor:
    list_data.append(data)
Y = list()
X=list()

for i in range(0,len(list_data)):
    X.append(list_data[i][0:3])
    Y.append(list_data[i][3])

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)