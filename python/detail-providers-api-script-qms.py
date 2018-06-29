import csv, urllib2, base64, json, datetime, sys, time
from config import username, password, provider_uids, quarter_name, api_key, base_url

# Detail Provider Quality Measure Endpoint

filename = 'provider_qm_detail'
filename += datetime.datetime.now().strftime("-%Y-%m-%d_%H-%M-%S")
filename += '.csv'

with open(filename, 'wb') as csvfile:
        index = 0
        fieldnames = [
            'quarter_name',
            'composite_score',
            'sltc_score',
            'provider_uid',
            'cms_rating',
            'sltc_rating',
            'provider_name',
            'sltc_denominator',
            'sltc_rate',
            'sltc_adj_rate',
            'cms_rate',
            'sltc_summary_score',
            'cms_adj_rate',
            'cms_4q_average',
            'sltc_4q_average',
            'sltc_numerator',
            'qm_cms_id'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for provider_uid in provider_uids:
            request_url = base_url
            request_url += '/Analytics/QualityMeasures/providerdetails/?'
            request_url += 'provider_uid=%s&'%(provider_uid)
            index += 1
            request_url += 'quarter_name=%s&'%(quarter_name)
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
            response_data = response_data[0]
            response_data_qms = response_data['qms']
            for qm in response_data_qms:
                writer.writerow({
                    'quarter_name': response_data['quarter_name'],
                    'composite_score': response_data['composite_score'],
                    'sltc_score': response_data['sltc_score'],
                    'provider_uid': response_data['provider_uid'],
                    'cms_rating': response_data['cms_rating'],
                    'sltc_rating': response_data['sltc_rating'],
                    'provider_name': response_data['provider_name'],
                    'sltc_denominator': response_data_qms[qm]['sltc_denominator'],
                    'sltc_rate': response_data_qms[qm]['sltc_rate'],
                    'sltc_adj_rate': response_data_qms[qm]['sltc_adj_rate'],
                    'cms_rate': response_data_qms[qm]['cms_rate'],
                    'sltc_summary_score': response_data_qms[qm]['sltc_summary_score'],
                    'cms_adj_rate': response_data_qms[qm]['cms_adj_rate'],
                    'cms_4q_average': response_data_qms[qm]['cms_4q_average'],
                    'sltc_4q_average': response_data_qms[qm]['sltc_4q_average'],
                    'sltc_numerator': response_data_qms[qm]['sltc_numerator'],
                    'qm_cms_id': response_data_qms[qm]['qm_cms_id']
                })
