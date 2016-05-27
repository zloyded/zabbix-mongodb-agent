#!/usr/bin/env python

# -*- coding: utf-8 -*-

import socket, os, os.path, sys, time, subprocess, re
import simplejson as json

class MongoMonit():

  """docstring for ClassName"""

  def __init__(self):
    self.socket_file = '/var/run/mongo-monitor.sock'
    self.re_moncred = re.compile(r"^(MongoDB).*\n")
    self.re_connect = re.compile(r"(connecting to).*\n")

  def run(self):
    serverStats = self.getSysTable()
    tables = self.getCollections()
    res = {
      'collections': tables,
      'serverStats': serverStats
    }
    print json.dumps(res, sort_keys=True,  indent=2, separators=(',', ': '))

  """ get mongoStats """
  def getSysTable(self):
    data = subprocess.Popen(['mongo', '--eval', 'JSON.stringify(db.serverStatus())'], stdout=subprocess.PIPE).stdout.read()
    m = re.sub(self.re_moncred, '', data)
    d = re.sub(self.re_connect, '', m)
    return json.loads(d) 
    

  def getCollections(self):
    data = subprocess.Popen(['mongo', '--eval', 'JSON.stringify(db.getCollectionInfos())'], stdout=subprocess.PIPE).stdout.read()
    m = re.sub(self.re_moncred, '', data)
    d = re.sub(self.re_connect, '', m)
    return json.loads(d)
    


if __name__ == "__main__":
  MongoMonit().run()
  