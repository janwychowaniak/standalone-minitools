#!/usr/bin/python




import datetime


import threading
import signal
import time


import termios, sys, os
TERMIOS = termios


def getkey():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
    new[6][TERMIOS.VMIN] = 1
    new[6][TERMIOS.VTIME] = 0
    termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
    c = None
    try:
        c = os.read(fd, 1)
    finally:
        termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
    return c



#~ def printhelp():
	#~ print ' Z	+10m'
	#~ print ' X	+30m'
	#~ print ' C	start/stop'
	#~ print ''


def rwrite(arg):
	sys.stdout.write('\r%s' % arg)
	sys.stdout.flush()



def zerolead(arg):
	arg = str(arg)
	return arg.zfill(2)


#~ def enum(**enums):
	#~ return type('Enum', (), enums)



class Datetime:
	def __init__(self, h, m, s):
		self.start_moment = datetime.datetime(2000,1,1,h,m,s)

	def get_time(self):
		return '%s:%s:%s' % (zerolead(self.start_moment.hour), zerolead(self.start_moment.minute), zerolead(self.start_moment.second))
	
	def add5(self):
		self.start_moment += datetime.timedelta(minutes=5)

	def add30(self):
		self.start_moment += datetime.timedelta(minutes=30)

	def sub1s(self):
		self.start_moment -= datetime.timedelta(seconds=1)

	def add1s(self):	# debug
		self.start_moment += datetime.timedelta(seconds=1)

	def is_expired(self):
		return self.start_moment.hour == 0 and self.start_moment.minute == 0 and self.start_moment.second == 0



class Timer(threading.Thread):
	
	def __init__(self, _timerdatetime):
		threading.Thread.__init__(self)
		self._stop           = threading.Event()
		self.timerdatetime   = _timerdatetime
		self.paused			 = False

		#~ self.daemon = True
		#~ self.start()

	def toggle_state():
		self.paused = not self.paused

	def disp_time(self):
		remtime = self.timerdatetime.get_time()
		rwrite('['+remtime+']')

	def get_time(self):
		return self.timerdatetime.get_time()
		

	def run(self):
		while not self.stopped():# and not self.timerdatetime.is_expired():
			time.sleep(1)
			if not self.paused:
				self.timerdatetime.add1s()
			self.disp_time()


	def stop(self):
		self._stop.set()

	def stopped(self):
		return self._stop.isSet()





#~ Appmode = enum(SETTING=1, RUNNING=2)





if __name__ == '__main__':
	
	
#	if len(sys.argv) < 1:
#		print 'Usage:'
#		print '  ' + sys.argv[0]
#		print
#		sys.exit(1)

	appname = sys.argv[0]
	remtime_s = '00:00:00'
	
	remtime_s_elems = remtime_s.split(':')

	remaining_time = Datetime(int(remtime_s_elems[0]), int(remtime_s_elems[1]), int(remtime_s_elems[2]))
	
	print 
	rwrite('['+remaining_time.get_time()+']')

	# create timer, feed it with the remaining time object
	timer = Timer(remaining_time)
	timer.start()

	
	# signal handler
	def signal_handler(signal, frame):
		print 
		print 'Ctrl+C!'
		print 
		print appname + ' -> ' + timer.get_time()
		timer.stop()
		timer.join()
		sys.exit(2)

	signal.signal(signal.SIGINT, signal_handler)


	# waits
	while timer.is_alive():
		time.sleep(1)


	# ending credits
	print
	print 'timer ended at', time.strftime('%l:%M%p')
	print
