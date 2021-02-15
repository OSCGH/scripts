#! /usr/bin/python3
# -*- coding : utf-8 -*-
#input:python implcc.py obj.h
#output:obj.cpp
#***note: template may not be available***
import sys
import os
import re
def implcc(head):
        src=re.sub('.h$','.cpp',head)
        os.system('rm -f %s' % src)
        os.system('touch %s' % src)
        os.system('echo "#include <%s>" > %s' % (head,src))
        os.system('ctags -f tags --fields=+afmikKlnsStz --sort=no %s' % head)
        os.system('grep kind:function tags>funclist.tmp' )
        os.system('grep -E -o "namespace\:([[:print:]]+)" tags |sort -u -r|sed -e s#namespace:##g > spa.tmp')
        spas = []
        with open('spa.tmp') as f:
                for i in f:
                        line = i.replace('\r','').replace('\n','')
                        spas.append(line)
        with open('funclist.tmp') as f:
                for i in f:
                        retv=obj=spa=func=para=''
                        line=i.replace('\r','').replace('\n','')
                        num=re.sub('.*line:','',line)
                        num=re.sub('\t.*','',num)
                        if('class:' in line):
                                spaobj=re.sub('.*class\:','',line)
                                spaobj=re.sub('\t.*','',spaobj)
                                if('::' in spaobj):
                                        obj=spaobj
                                        for i in spas:
                                                obj=obj.replace('%s::'%i,'')
                                        spa=spaobj.replace('::%s'%obj,'')
                                else:
                                        obj=spaobj
                                obj=obj+'::'
                        elif('struct:' in line):
                                spaobj=re.sub('.*struct\:','',line)
                                spaobj=re.sub('\t.*','',spaobj)
                                if('::' in spaobj):
                                        obj=spaobj
                                        for i in spas:
                                                obj=obj.replace('%s::'%i,'')
                                        spa=spaobj.replace('::%s'%obj,'')
                                else:
                                        obj=spaobj
                                obj=obj+'::'
                        elif('namespace:' in line):
                                spa=re.sub('.*namespace\:','',line)
                                spa=re.sub('\t.*','',spa)
                        if('typeref:typename' in line):
                                retv=re.sub('.*typeref\:typename\:','',line)
                                retv=re.sub('\t.*',' ',retv)
                        func = re.sub('\t.*','',line)
                        para = re.sub('.*signature\:','',line)
                        para = re.sub('=[^,]+,',',',para)
                        para = re.sub('=[^,]+\)',')',para)
                        os.system('echo "namespace %s { %s%s%s%s{} }"'%(spa,retv,obj,func,para))
                        os.system('echo "" >> %s ' % (src))
                        os.system('echo "/* %s line:%s */" >> %s ' % (head,num,src))
                        os.system('echo "namespace %s { %s%s%s%s{} }" >> %s'%(spa,retv,obj,func,para,src))
if __name__ == '__main__':
        if((len(sys.argv) == 2) and (os.path.isfile(sys.argv[1]))):
                implcc(sys.argv[1])
        else:
                print("error:args wrog")
