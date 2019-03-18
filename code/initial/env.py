import os, signal, sys, time, numpy
from acceptor import Acceptor
from leader import Leader
from message import RequestMessage
from process import Process
from replica import Replica
from utils import *
from datetime import datetime

NACCEPTORS = 3
NREPLICAS = 2
NLEADERS = 5
NREQUESTS = 1
NCONFIGS = 1
TOTAL_TIME = 0

class Env:
  def __init__(self):
    self.procs = {}

  def setReplicaCount(self, no_of_replicas):
    self.no_of_replicas = no_of_replicas

  def setRequestCount(self, no_of_requests):
    self.no_of_requests = no_of_requests

  def sendMessage(self, dst, msg):
    if dst in self.procs:
      self.procs[dst].deliver(msg)

  def addProc(self, proc):
    self.procs[proc.id] = proc
    proc.start()

  def removeProc(self, pid):
    del self.procs[pid]

  def run(self):
    self.successful_event = 0
    initialconfig = Config([], [], [])
    self.times = []
    c = 0

    for i in range(self.no_of_replicas):

      pid = "replica %d" % i
      Replica(self, pid, initialconfig)
      initialconfig.replicas.append(pid)
    for i in range(NACCEPTORS):
      pid = "acceptor %d.%d" % (c,i)
      Acceptor(self, pid)
      initialconfig.acceptors.append(pid)
    for i in range(NLEADERS):
      pid = "leader %d.%d" % (c,i)
      Leader(self, pid, initialconfig)
      initialconfig.leaders.append(pid)
    for i in range(self.no_of_requests):
      self.start_time = datetime.now()
      pid = "client %d.%d" % (c,i)
      for r in initialconfig.replicas:
        cmd = Command(pid,0,"operation %d.%d" % (c,i))
        self.sendMessage(r,RequestMessage(pid,cmd))
        time.sleep(1)
      self.end_time = datetime.now()
      self.total_time = self.end_time - self.start_time
    # print(self.times)
      self.times.append(self.total_time.total_seconds())


    for c in range(1, NCONFIGS):
      # Create new configuration
      config = Config(initialconfig.replicas, [], [])
      for i in range(NACCEPTORS):
        pid = "acceptor %d.%d" % (c,i)
        Acceptor(self, pid)
        config.acceptors.append(pid)
      for i in range(NLEADERS):
        pid = "leader %d.%d" % (c,i)
        Leader(self, pid, config)
        config.leaders.append(pid)
      # Send reconfiguration request
      for r in config.replicas:
        pid = "master %d.%d" % (c,i)
        cmd = ReconfigCommand(pid,0,str(config))
        self.sendMessage(r, RequestMessage(pid, cmd))
        time.sleep(1)
      for i in range(WINDOW-1):
        pid = "master %d.%d" % (c,i)
        for r in config.replicas:
          cmd = Command(pid,0,"operation noop")
          self.sendMessage(r, RequestMessage(pid, cmd))
          time.sleep(1)
      for i in range(self.no_of_requests):
        pid = "client %d.%d" % (c,i)
        for r in config.replicas:
          cmd = Command(pid,0,"operation %d.%d"%(c,i))
          self.sendMessage(r, RequestMessage(pid, cmd))
          time.sleep(1)

  def terminate_handler(self, signal, frame):
    self._graceexit()

  def _graceexit(self, exitcode=0):
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(exitcode)

  def get_execution_time(self):
    return numpy.mean(self.times)

  def get_successful_events(self):
      return (self.no_of_requests)

  def get_throughput(self):
      # print(self.times)
      _sd = numpy.std(self.times, dtype=numpy.float64)
      # print(_sd)
      return (self.get_successful_events()/self.get_execution_time()), _sd

def main():
  e = Env()
  e.setRequestCount(2)
  e.setReplicaCount(2)
  e.run()
  # print(e.get_execution_time())
  signal.signal(signal.SIGINT, e.terminate_handler)
  signal.signal(signal.SIGTERM, e.terminate_handler)
  # signal.pause()


if __name__=='__main__':
  main()
