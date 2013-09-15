#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# h2m@access.uzh.ch

import vobject as vo

from codecs import open

BASE_DIR = ''
VCF_IN = BASE_DIR + 'Adressdatenbank_Final_Fixed2.vcf'
VCF_OUT = BASE_DIR + 'Adressdatenbank_Final_Fixed2+gender.vcf'
W_FILE = BASE_DIR + 'w_liste.txt'
M_FILE = BASE_DIR + 'm_liste.txt'
DEF_ENC = 'utf-8'

def get_names(gender='f'):
    names = set()
    names_file = W_FILE
    
    if gender == 'm':
        names_file = M_FILE
        
    f = open(names_file, 'r', encoding=DEF_ENC)
    for line in f.readlines():
        names.add(line.strip())
        
    return names

def main():
    end = u'END:VCARD'
    f = open(VCF_IN, 'r', encoding=DEF_ENC)
    
    vcards = [vo.readOne(s+end) for s in f.read().split(end) 
                                if s.rstrip() != u'']
    
    idx = 0                            
    for vcard in vcards:
        try:
            surname = \
                vcard.n.serialize().split(':')[-1].strip().split(';')[1]
        except:
            pass
        print idx, surname
        idx += 1
        if surname in get_names():
            print 'yes: W'
        if surname in get_names(gender='m'):
            print 'yes: M'

if  __name__ =='__main__':
    main()
