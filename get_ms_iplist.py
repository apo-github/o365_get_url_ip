# endpoints: https://endpoints.office.com/endpoints/worldwide?clientrequestid=b10c5ed1-bad1-445f-b386-b919946339a7 (csv, jsonのみ対応)
# ref: https://www.centurysys.co.jp/dns-intercept/o365_address.xml

# 処理の流れ
# foreach
    # id
    # key
        # has urls?
            # get
        # has ips?
            # get

import requests
import xml.etree.ElementTree as ET

# requre
endpoints = 'https://endpoints.office.com/endpoints/worldwide?clientrequestid=b10c5ed1-bad1-445f-b386-b919946339a7'
o365_rss = 'https://endpoints.office.com/version/worldwide?allversions=true&format=rss&clientrequestid=b10c5ed1-bad1-445f-b386-b919946339a7'
endpoints_data = requests.get(endpoints).json() #load json
# print(endpoints_data) #debug

# tmp
address_list_ip4 = []
address_list_ip6 = []
url_list = []
# return
json_data = {}
xml_data = ''

def json_to_xml(json_data):
    # get lastBuildDate from RSS info
    rss_data = requests.get(o365_rss).text
    last_build_date = ""
    for channel in ET.fromstring(rss_data).findall('channel'):
        last_build_date = channel.find("lastBuildDate").text
    #ipv4
    root = ET.Element('products')
    root.set('updated',last_build_date)
    elem1 = ET.SubElement(root, 'product')
    elem1.set('name','o365')
    elem2 = ET.SubElement(elem1, 'addresslist')
    elem2.set('type','IPv4')
    for _data in json_data["ipv4"]: 
        elem3 = ET.SubElement(elem2, 'address')
        elem3.text = _data
    # ipv6
    elem2 = ET.SubElement(elem1, 'addresslist')
    elem2.set('type','IPv6')
    for _data in json_data["ipv6"]:
        elem3 = ET.SubElement(elem2, 'address')
        elem3.text = _data
    #urls
    elem2 = ET.SubElement(elem1, 'addresslist')
    elem2.set('type','URL')
    for _data in json_data["urls"]:
        elem3 = ET.SubElement(elem2, 'address')
        elem3.text = _data
    return ET.dump(root)

def get_json_data():
    for i, obj in enumerate(endpoints_data):
        urls = obj.get('urls')
        ips = obj.get('ips')
            
        if ips != None:
            for ip in ips:
                # ipv4
                if '.' in ip:
                    address_list_ip4.append(ip) 
                else:
                # ipv6
                    address_list_ip6.append(ip) 
        if urls != None:
            url_list.extend(urls)
    json_data['ipv4'] = address_list_ip4
    json_data['ipv6'] = address_list_ip6
    json_data['urls'] = url_list
    return json_data

def get_xml_data():
    json_data = get_json_data()
    return json_to_xml(json_data)


if __name__ == '__main__':
    # Json
    # print(get_json_data())

    # Xml (フォーマットはrefに準拠)
    get_xml_data()




