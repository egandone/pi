import os
import glob
import ftplib
import sys
import re
import urllib2
import datetime
import traceback
import login

found_images = []
found_directories = []
def ftp_walk(ftp):    
    global found_images
    dirs = ftp.nlst()
    for item in (path for path in dirs if path not in ('.', '..')):
        try:
            ftp.cwd(item)
            try:
                ftp_walk(ftp)
            finally:
                ftp.cwd('..')
        except Exception, e:
            matched_filename = re.search('[jJ][Pp][Gg]$|[pP][nN][gG]$|[Mm][Pp]4$', item)
            if  (matched_filename != None):
                found_images.append(os.path.join(ftp.pwd(), item.strip()))

def internet_on():
    try:
        response=urllib2.urlopen('http://google.ca',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False
        
def check_files(path, remote_dir):
	global found_images
	try:
		if (internet_on()):
			session = ftplib.FTP('ftp.stgeorgestoronto.ca', login.username, login.password)
			session.cwd(remote_dir)
			print 'pwd = ' + session.pwd()
			found_images = []
			ftp_walk(session)
			print 'list count = ' + str(len(found_images))
			if (len(found_images) > 0) :
				existing_files = glob.glob(os.path.join(path, '*.[Jj][Pp][Gg]'))
				existing_files.extend(glob.glob(os.path.join(path, '*.[Pp][Nn][Gg]')))
				existing_files.extend(glob.glob(os.path.join(path, '*.[Mm][Pp]4')))
				for existing_file in existing_files:
					print 'Deleting ' + existing_file
					os.remove(existing_file)
				for new_file in found_images:
					raw_filename = os.path.split(new_file)[-1]
					new_path = os.path.join(path, raw_filename)
					print 'Downloading/creating ' + new_path + ' from ' + new_file
					session.retrbinary('RETR ' + new_file, open(new_path, 'wb').write)
			session.close()
	except:
		traceback.print_exc()
		e = sys.exc_info()[0]
		print 'Exception connecting to ftp.  Update ignored ' + str(e)

if __name__ == "__main__":
    path = './s'
    now = datetime.datetime.now()
    check_files(path, now.strftime("%Y-%m-%d"))
