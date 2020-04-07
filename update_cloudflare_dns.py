#!/usr/bin/python3
#filename: update_cloudflare_dns.py

import requests
import json

auth_key = "#cloudflare_auth_key#"
auth_email = "#cloudflare_auth_email#"
zone_id = "#cloudflare_zone_id#"
record_type = "A"
record_name = "a.example.com"

def getDnsRecordId():
    url = "https://api.cloudflare.com/client/v4/zones/" + zone_id + "/dns_records"
    method = "GET"

    headers = {
        'X-Auth-Key': auth_key,
        'X-Auth-Email': auth_email,
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
        'X-Auth-Key': auth_key,
        'X-Auth-Email': auth_email,
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

def getIp():
    try:
        r = requests.get("http://ip.cip.cc") # OR http://ifconfig.me/ip
        return r.text.rstrip('\n')
    except:
        pass

ip = getIp()
if ip:
    print("ip:" + ip)
    record_id, record_ip = getDnsRecordId()
    if record_id and ip != record_ip:
        print("record_id:" + record_id)
        result = updateDnsRecord(record_id, ip)
        if result:
            print("update dns record success:", json.dumps(result, indent=1))
        else:
            print("update dns record faild")
    else:
        if ip == record_ip:
            print("ip has not changed")
        else:
            print("get ip faild")
else:
    print("get dns record_id faild")
