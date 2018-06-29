import csv, urllib2, base64, json, datetime, sys, time
from config import username, password, provider_uids, quarter_name, api_key, base_url
# Providers Quality Measure Endpoint

request_url = base_url
request_url += '/Analytics/QualityMeasures/providers/?'

index = 0
for provider_uid in provider_uids:
    request_url += 'provider_uids[%s]=%s&'%(index, provider_uid)
    index += 1

request_url += 'quarter_name=%s'%(quarter_name)

request = urllib2.Request(request_url)
base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)
request.add_header("SLTC-Api-Key", api_key)
response = urllib2.urlopen(request)
response_code = response.getcode()
attempts = 0
while response_code == '429':
    if(attempts == 2):
        sys.exit()
    time.sleep(60)
    response = urllib2.urlopen(request)
    response_code = response.getcode()
    attempts += 1                   
response_data = json.load(response)

filename = 'provider_qms'
filename += datetime.datetime.now().strftime("-%Y-%m-%d_%H-%M-%S")
filename += '.csv'

with open(filename, 'wb') as csvfile:
    fieldnames = [
        'official',
        'provider_uid',
        'provider_name',
        'five_star_score',
        'five_star_rating',
        'composite_score'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    sys.stdout.flush()
    for provider in response_data:
        writer.writerow({
            'official': provider['official'],
            'provider_uid': provider['provider_uid'],
            'provider_name': provider['provider_name'],
            'five_star_score': provider['five_star_score'],
            'five_star_rating': provider['five_star_rating'],
            'composite_score': provider['composite_score']
            })
