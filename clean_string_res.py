#!/usr/bin/python  
# -*- coding=utf-8 -*-  
from lxml import etree
import os,sys,io
import re
dirList=[]
def delXmlNode(file,nodeType,arrName,arrValue,outfile):
	isUpdate=False
	tree = etree.parse(file)
	for element in tree.iter():
		if element.tag==nodeType and element.get(arrName)==arrValue:
			print("%s - %s" % (element.tag, element.get(arrName)))
			element.getparent().remove(element)
			isUpdate=True
	if isUpdate:
		if not outfile or outfile=="" or outfile ==None:
			outfile=file
		fileHandler = open(outfile, "wb")
		tree.write(fileHandler, encoding="utf-8", xml_declaration=True, pretty_print=True)
		fileHandler.close()
	

def loopDirect4Values(rootdir):
    global dirList
    list = os.listdir(rootdir) 
    for i in range(0,len(list)):
        path = os.path.join(rootdir,list[i])
        if os.path.isdir(path):
            if  checkValuesDir(path):
                dirList.append(path)
            loopDirect4Values(path)

def loopFile4Values(rootdir,nodeType,arrName,arrValue,outfile):
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
 
    for i in range(0,len(list)):
        path = os.path.join(rootdir,list[i])
        if os.path.isfile(path) and checkXML(path):
            print path
            try:
                delXmlNode(path,nodeType,arrName,arrValue,outfile)
            except Exception as e:
                print e
            else:
                pass
            finally:
                pass
def checkXML(filepath):
    result = False
    if filepath.lower().endswith('xml')  and os.path.isfile(filepath):
        result = True
    return result
def checkValuesDir(dir):
    return checkDirWithName(dir,'values')


def checkDirWithName(dir,name):
    
    if name not in dir or 'bulid' in dir:
        return False
    p = re.compile(r'\\|/')
    dirContents=p.split(dir.strip())
    size=0
    if dirContents!=None:
        size=len(dirContents)
    if size>0:
        pattern = re.compile(r'values-?[0-9|a-z|A-Z]*',re.UNICODE|re.VERBOSE|re.I)
        return pattern.match(dirContents[size-1])!=None
def app():
    nodeType="string-array"
    arrName="name"
    arrValue="exit_dialog_choices"
    outfile=""
    dir= 'E:\\py_work\\res'
    if os.path.exists(dir):
    	print u'工作路径: %s' %(dir)
    else:
    	print u'工作路径:%s不存在' %(dir)
    	return
    loopDirect4Values(dir)
    for filepath in dirList:
        loopFile4Values(filepath,nodeType,arrName,arrValue,outfile)
if __name__ == '__main__':
    app()