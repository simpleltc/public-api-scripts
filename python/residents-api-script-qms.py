import csv, urllib2, base64, json, datetime, sys, time
from config import username, password, provider_uids, quarter_name, api_key, qm_cms_ids, base_url
# Residents Quality Measure Endpoint

filename = 'resident_qms'
filename += datetime.datetime.now().strftime("-%Y-%m-%d_%H-%M-%S")
filename += '.csv'

with open(filename, 'wb') as csvfile:
    fieldnames = [
        'resident_name',
        'qm_cms_id',
        'provider_uid',
        'gender',
        'denominator',
        'numerator',
        'birthday',
        'excluded',
        'resident_uid'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    index = 0
    for qm_cms_id in qm_cms_ids:
            for provider_uid in provider_uids:
                request_url = base_url
                request_url += '/Analytics/QualityMeasures/residents/?'
                request_url += 'provider_uid=%s&'%(provider_uid)
                index += 1
                request_url += 'quarter_name=%s&'%(quarter_name)
                request_url += 'qm_cms_id=%s'%(qm_cms_id)
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
                for resident in response_data:
                    writer.writerow({
                        'resident_name': resident['resident_name'],
                        'qm_cms_id': qm_cms_id,
                        'provider_uid': resident['provider_uid'],
                        'gender': resident['gender'],
                        'denominator': resident['denominator'],
                        'numerator': resident['numerator'],
                        'birthday': resident['birthday'],
                        'excluded': resident['excluded'],
                        'resident_uid': resident['resident_uid']
                    })
