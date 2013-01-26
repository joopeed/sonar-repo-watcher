#!/usr/bin/python
# coding: utf-8

import popen2,socket, os, sys, re, platform, datetime, time



class Component:
	def __init__(self, name, machine, conf, zipped_path):
        	self.__name = name
		self.__machine = machine
		self.__conf = conf

	def process_name(self):
        	return self.__process_name

	def name(self):
        	return self.__name

	def conf(self):
        	return self.__conf

	def machine(self):
        	return self.__machine

	def execute(remote_command, user, machine_addr, delay=None):
    		process = subprocess.Popen(" ".join(["ssh",
	                                 user +"@" + machine_addr,
                                         remote_command]),
					 shell=True,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT)
   		out, err = process.communicate()
    		return out, err, process.returncode

	def copy_zip(self, user, machine):
        	remote_path = user+"@" + node + ":/tmp/"
        	getdata_cmd = " ".join(["scp", "-r",
        	                        zipped_path,
        	                        remote_path])
		self.__zipped = zipped_path.split(sep)[-1]
        	process = subprocess.Popen(getdata_cmd,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        	out, err = process.communicate()
        	return out, err, process.returncode


    	def mount():
		copy_zip("joopeeds", machine())
		execute("unzip /tmp/"+self.__zipped, "joopeeds", machine())
		execute("rm /tmp/"+self.__zipped, "joopeeds", machine())
		
	def unmount():

	def clear():
	
	def start():

	def stop():






DATA_SERVER = Component("Honeycomb", "honeycomb")
META_SERVER = Component("Queenbee", "queenbee")
CLIENT = Component("Honeybee", "honeybee")















def openconf(file):

	def fn(line):
 	   if line[0] == "#":
 	       line = ""
 	   else:
 	       idx = re.search (r"[^\\]#", line)
 	       if idx != None:
 	           line = line[:idx.start()+1]
 	   # Split non-comment into key and value.
 	   idx = re.search (r"=", line)
 	   if idx == None:
  	      key = line
  	      val = ""
 	   else:
  	      key = line[:idx.start()]
  	      val = line[idx.start()+1:]
  	  val = val.replace ("\\#", "#")
  	  return (key.strip(),val.strip())

        config = {}
        new = open(file).read()
        for i in new.split('\n'):
                if fn(" "+i)[0]!='':
                        config[fn(" "+i)[0]] = fn(" "+i)[1]
        return config

def getsize(source):
	folder_size = 0
	for (path, dirs, files) in os.walk(source):
  		for file in files:
    			filename = os.path.join(path, file)
    			folder_size += os.path.getsize(filename)
	return "%.1fMB" % (folder_size/(1024*1024.0))


def generateheader(text):
	return  '#'*((60-len(text+'  '))/2) +' '+ text+' ' + '#'*((60-len(text+'  '))/2) +'\n'


def main():
	so = platform.system()
	if so == "Linux":
		sep = '/'
	else:
		sep = '\\'

	# this script must be in beefs directory where exists \conf  
	honeybee = openconf('conf'+sep+'honeybee.conf')
	honeycomb = openconf('conf'+sep+'honeycomb.conf')
	source = sys.argv[1] # Type the origem without the last '\'
	if so == "Linux":
		dest = honeybee['mount_directory']
		command = 'cp -r '+source+'/ '+dest+'/\n'
	else: 
		command = 'copy "'+source+'\*.*" "'+dest+'\\" \n'

	queenbee = honeycomb['osdmaster'].split(':')
	if queenbee[0]=="localhost":
		allocation = "Non-Distributed"
	else:
		allocation = "Distributed"
	mode = honeycomb['file_synchronization'] + allocation
	#clear_storage = "rm -r "+honeycomb['contributing_storage.directory']+sep+'*'
	#os.system(clear_storage)
	#clear_metadata = "rm -r "+honeycomb['metadata_directory']+sep+'*'
	#os.system(clear_metadata)

	hostname = socket.gethostname()
	size = getsize(source)
	queenbee = honeycomb['osdmaster'].split(':')

	dt = datetime.datetime.now()
	test = ' Test on '+ platform.system() +' '+ dt.strftime("%d/%m/%Y %H:%M ")
	header = '#'*60 + '\n' + generateheader(test) + generateheader("Hostname of honeycomb: "+hostname) + generateheader("Queenbee on "+queenbee[0]) + generateheader("Mode: "+mode) + generateheader("Workload: "+ size)
	log = open('testlogs'+sep+'test.log.'+dt.strftime("%d-%m-%Y.%Hh%M")+'.log','w')
	log.write(header)
	startepoch = int(time.time())
	popen2.popen2(command)[0].readlines()
	endepoch = int(time.time())
	body =  'Copying from '+source+' to '+dest +'\n' + 'Command executed: '+command + '\n' + 'elapsed: ' + str( endepoch - startepoch )  +'s\n' + '#'*60 + '\n'
	log.write(body)
	log.close()


if __name__ == "__main__":

	if len(sys.argv) != 1:
       	 sys.stderr.write("Usage: python beefstester.py config_file\n")
         sys.exit(-1)

	config_file = sys.argv[1]
	#FIXME
	zipped_path, samples, queenbee, queenbee_conf, honeycomb, honeycomb_conf, honeybee, honeybee_conf = openfile(config_file).values()

	main()


#getStartime = 'date +%s%N\n'
#getEndtime = 'date +%s%N'
