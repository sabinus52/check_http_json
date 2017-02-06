#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import getopt
import urllib2
import json


###
# Paramètres par défaut
##
hostname = ""
uri = "/"
port = 80
ssl = False


###
# Définition du la fonction usage de la commande
##
def usage():
    print "Usage : %s [hHpiS]" % (sys.argv[0])
    print " -H, --hostname=ADDR : Hostname du serveur à checker"
    print " -p, --port=INTEGER  : Numéro du port (défaut: 80)"
    print " -i, --uri=URI       : URL pour le GET (défaut: /)"
    print " -S, --ssl           : Connection via SSL (port par défaut 443)"
    print " -h, --help          : Affiche cet écran"
    print ""


###
# Parsing des options en paramètre
##
def parseOptions():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hH:i:p:S", ["help", "hostname=", "uri=", "port=", "ssl"])
    except getopt.GetoptError:
        usage()
        sys.exit(3)

    for opt, optarg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(3)
        if opt in ("-H", "--hostname"):
            global hostname
            hostname = optarg
        elif opt in ("-i", "--uri"):
            global uri
            uri = optarg
        elif opt in ("-p", "--port"):
            global port
            try:
                port = int(optarg)
            except ValueError:
                print "UNKNOW : Valeur du port '%s' incorrecte" % (optarg)
                sys.exit(3)
        elif opt in ("-S", "--ssl"):
            global ssl
            ssl = True


###
# Génère l'URL
##
def generateURL(hostname, uri, port, ssl):
    if ssl == True:
        url = "https://"
    else:
        url = "http://"
    url = url + hostname
    if port != 80:
        url = "%s:%s" % (url, port)
    url = url + uri
    return url



###
# Retourne l'objet de la résponse du serveur
##
def getResultURL(url):
    try:
        resultURL = urllib2.urlopen(url).read()
    except urllib2.URLError:
        print "UNKNOW : Impossible d'ouvrir l'url %s" % (url)
        sys.exit(3)

    if sys.version_info[:2] >= (2,5):
        try:
            resultJSON = json.loads(resultURL)
        except ValueError:
            print "UNKNOW: Impossible de décoder le JSON : %s" % resultURL
            sys.exit(3)
    else:
        try:
            resultJSON = json.read(resultURL)
        except json.ReadException:
            print "UNKNOW: Impossible de décoder le JSON : %s" % resultURL
            sys.exit(3)
        
    return resultJSON


###
# Vérifie le retour JSON
##
def checkResult(result):
    if result['code'] == 0:
        print "OK: %s" % (result['msg'])
        sys.exit(0)
    elif result['code'] == 1:
        print "WARNING: %s" % (result['msg'])
        sys.exit(1)
    elif result['code'] == 2:
        print "CRITICAL: %s" % (result['msg'])
        sys.exit(2)
    else:
        print "UNKNOW: %s" % (result['msg'])
        sys.exit(3)


###
# Principal
##
def main():
    parseOptions()
    #print "hostname=%s" % (hostname)
    #print "uri=%s" % (uri)
    url = generateURL(hostname, uri, port, ssl)
    #print url
    resjson = getResultURL(url)
    #print resjson
    checkResult(resjson)


if __name__ == '__main__':
    main()
