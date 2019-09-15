import zipfile
from utils.logger import Logger

log = Logger("info", name="zip_util")

def unzip(filename, distination, password):
    '''
	parameter:
		filename  需要解压的文件
	'''

    file_zip = zipfile.ZipFile(filename, 'r')
    if len(file_zip.namelist()) <= 1:
        zipchildname = file_zip.namelist()[0]
        log.info('the zipfile [%s] only have one file, the file name is  %s' % (filename, zipchildname))
        try:
            file_zip.extract(zipchildname, path=distination)
        except:
            try:
                log.info('the zipfile [%s] need password to extract, current password is %s' % (filename, password))
                file_zip.extractall(path=distination, pwd=bytes(password, "utf-8"))
            except:
                log.info('error, extract zipfile with password failed,  maybe need change password')
        file_zip.close()
        return zipchildname
    else:
        log.info(' the zipfile [%s]  has %d files ' % (filename, len(file_zip.namelist())))
        try:
            file_zip.extractall(path=distination)
        except:
            try:
                log.info('the zipfile [%s] need password to  extract, current password is %s' % (filename, password))
                file_zip.extractall(path=distination, pwd=bytes(password, "utf-8"))
            except:
                log.info('error , extract zipfile with password failed,  maybe need change password')
        return file_zip.namelist()
