#! /usr/bin/python
#
# Nagios plugin for ASMONIA
# Written by Niels Fallenbeck <niels.fallenbeck@aisec.fraunhofer.de>
# Last modified: 2012-12-30
# 
# Usage: ./asmonia.py
#
# Description
# This plugin returns the state of the opensips SIP server
#
# Output
# Depending on the threshold it will return the appropriate state of 
# server. It will provide information about the current utilization
# and will exit with a code corresponding to its state.
# O OK
# 1 WARNING
# 2 CRITICAL
# 3 UNKNOWN
# 
# Notes:
# There are some standard thresholds defined which will be used if
# no thresholds will be defined during the script's call
#
# Examples:
# Check for logged in users and return warning state at 10 and
# critical state at 50:
#	asmonia -M users -w 10 -c 50
'''
@author: Niels Fallenbeck <niels.fallenbeck@aisec.fraunhofer.de>
@copyright: (c) 2012-2013
'''

## Configuration
import sys
import os
import optparse
from subprocess import PIPE
from subprocess import Popen


class OpenSipsModule:
	name = "OpenSipsModule"
	version = '0.1'
	# opensipsctl = '/usr/local/bin/opensips/sbin/opensipsctl' # production
	opensipsctl = './opensipsctl_dummy' # opensipsctl dummy for testing purposes

	# default settings
	threshold_warning = 2
	threshold_critical = 5
	exitstatus = 3 #OpenSipsModuleStates.UNKNOWN
	test = False
	metric = "all"


	def parse_options(self):
		from optparse import OptionParser
		parser = OptionParser()
		parser.add_option("-v", "--version", action="store_true", dest="show_version", default=False, help="print version and exit")
		parser.add_option("-t", "--test", action="store_true", dest="test_config", default=False, help="test if configuration is working")
		parser.add_option("-M", "--metric", dest="metric", default="all", help="metric to show")
		parser.add_option("-x", "--exitstatus", dest="state", help="exit with this state")
		parser.add_option("-w", "--warning", dest="threshold_warning", help="set threshold for warning state")
		parser.add_option("-c", "--critical", dest="threshold_critical", help="set threshold for critical state")
		(self.options, args) = parser.parse_args()


	def print_version(self):
		print '%s %s' % (self.name, self.version)


	def check_config(self):
		# check if specified binary can be used
		print 'check system environment...'
		print '  binary used as configured in script: %s' % self.opensipsctl
		try:
   			with open(self.opensipsctl) as f: 
				p = Popen('%s 1 2 all' % self.opensipsctl, stdout=PIPE, stderr=PIPE, shell=True)
				output, errors = p.communicate()
				if p.returncode:
					print 'Error: %s' % errors
					exit(2)
				else:
					print '  opensipsctl binary found.'
		except IOError as e:
   			print 'Error: %s' % e
   			exit(1)


   	def get_metric(self):
   		print "The metric (%s) happens here!" % self.metric


	def __init__(self):
		self.parse_options()

		if self.options.show_version:
			self.print_version()
		elif self.options.test_config:
			self.print_version()
			self.check_config()
		else:
			self.get_metric()

		sys.exit(OpenSipsModuleStates.OK)



class OpenSipsModuleStates:
	OK = 0
	WARNING = 1
	CRITICAL = 2
	UNKNOWN = 3


if __name__ == '__main__':
	OpenSipsModule()