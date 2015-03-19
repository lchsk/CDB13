import urllib2
import json

class DownloadCoords(object):
    def __init__(self):
        self.path = '../data/battles.csv'
        self.output_file = '../data/coordinates.csv'

        self.links = {}

        with open(self.path) as f:
            for line in f:
                data = line.split(',')
                if data[1] == '"AMERICAN CIVIL WAR"':
                    self.links[data[0]] = data[-5][1:-1]

    def run(self):

        f = open(self.output_file, 'w')

        f.write('"isqno","latitude","longitude"\n')

        for k, v in self.links.iteritems():
            try:
                name = v.split('/')[-1]
                # print name
                # http://dbpedia.org/data/Battle_of_Atlanta.json
                url = 'http://dbpedia.org/data/' + name + '.json'
                url2 = 'http://dbpedia.org/resource/' + name
                url3 = 'http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=DESCRIBE+%3C' + url2 + '%3E&format=text%2Fcsv'

                req = urllib2.Request(url3)
                response = urllib2.urlopen(req)
                the_page = response.read()

                lines = the_page.split()

                latitude = longitude = None

                for line in lines:
                    cols = line.split(',')

                    if len(cols) > 1:
                        if 'pos#lat' in cols[1]:
                            latitude = cols[2]
                        elif 'pos#long' in cols[1]:
                            longitude = cols[2]

                if latitude and longitude:
                    f.write(str(k) + ',' + latitude + ',' + longitude + '\n')


                # j = json.loads(the_page)
                # print j
                # print type(j)

            except urllib2.HTTPError, e:
                print k, url, str(e)

            # return

        f.close()



if __name__ == '__main__':

    dc = DownloadCoords()
    dc.run()
