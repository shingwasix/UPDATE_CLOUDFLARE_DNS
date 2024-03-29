#!/usr/bin/python3
#filename: update_cloudflare_dns.py

import requests
import json

token = "#cloudflare_token#"
zone_id = "#cloudflare_zone_id#"
record_type = "A"
record_name = "a.example.com"


def getDnsRecordId():
    url = "https://api.cloudflare.com/client/v4/zones/" + zone_id + "/dns_records"
    method = "GET"

    headers = {
        'Authorization': 'Bearer ' + token,
    }

    try:
        r = requests.request(method, url, headers=headers)
        json = r.json()
        for item in json["result"]:
            if (item["type"] == record_type) and (item["name"] == record_name):
                return (item["id"], item["content"])
    except:
        pass


def updateDnsRecord(id, ip):
    url = "https://api.cloudflare.com/client/v4/zones/" + zone_id + "/dns_records/" + id
    method = "PUT"

    headers = {
        'Authorization': 'Bearer ' + token,
    }

    params = {
        'type': record_type,
        'name': record_name,
        'content': ip
    }

    try:
        r = requests.request(method, url, headers=headers, json=params)
        return r.json()
    except:
        pass


def getIpByService(service):
    try:
        r = requests.get("http://" + service, timeout=3)
        return r.text.rstrip('\n')
    except requests.exceptions.RequestException as e:
        pass
    except:
        pass


def getIp():
    try:
        ipServices = [
            'ip.cip.cc',
            'icanhazip.com',
            'ident.me',
            'whatismyip.akamai.com',
            'myip.dnsomatic.com',
            'ifconfig.me',  # 外网
            'ipinfo.io/ip',  # 外网
        ]

        for service in ipServices:
            ip = getIpByService(service)
            if ip:
                print("get ip:" + ip + " by service:" + service)
                return ip
    except:
        pass


ip = getIp()
if ip:
    record_id, record_ip = getDnsRecordId()
    if record_id and ip != record_ip:
        print("record_id:" + record_id)
        result = updateDnsRecord(record_id, ip)
        if result:
            print("update dns record success:", json.dumps(result, indent=1))
        else:
            print("update dns record failed")
    else:
        if ip == record_ip:
            print("ip has not changed")
        else:
            print("get ip failed")
else:
    print("get dns record_id failed")
