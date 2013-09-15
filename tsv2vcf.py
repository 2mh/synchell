#!/usr/bin/env python3
# h2m@access.uzh.ch

DATA_DIR = ''
TSV_FILE = 'Adressdatenbank_Final_fixed.csv'
DEF_ENC = 'UTF-8'

# Basic class
class Vcf():
    def __init__(self, version='2.1'):
        self.begin='BEGIN:VCARD' + '\n'
        self.version='VERSION:'+version +'\n'
        self.end='END:VCARD' + '\n'
                
    def __str__(self):
        s = self.begin
        s += self.version
        s += self.end
        
        return s + '\n'

class TbVcf(Vcf):
    def __init__(
                self, 
                version='2.1', 
                encoding='UTF-8',
                tsv_line=None,
                tsv_mapper=None
                ):
        Vcf.__init__(self, version=version)

        self.charset = ';CHARSET='+encoding+':'
        self.fields_used = set()
        self.tsv_line = tsv_line
        self.tsv_mapper = tsv_mapper
        
        self.n = self._append_charset('N')
        self.fn = self._append_charset('FN')
        self.org = self._append_charset('ORG')
        self.nickname = self._append_charset('NICKNAME')
        self.adr_work = self._append_charset('ADR;WORK;POSTAL') + ';'
        self.adr_home = self._append_charset('ADR;HOME;POSTAL') + ';'
        self.tel_work = 'TEL;WORK;VOICE:'
        self.tel_home = 'TEL;HOME;VOICE:'
        self.tel_cell = 'TEL;CELL;VOICE:'
        self.tel_fax = 'TEL;FAX:'
        self.tel_pager = 'TEL;PAGER:'
        self.email_1 = 'EMAIL;PREF;INTERNET:'
        self.email_2 = 'EMAIL;INTERNET:'
        ''' Not used
        self.email_3 = 'EMAIL;INTERNET:'
        self.email_4 = 'EMAIL;INTERNET:'
        self.email_5 = 'EMAIL;INTERNET:'
        self.email_6 = 'EMAIL;INTERNET:'
        '''
        self.url_home = 'URL;HOME:'
        self.url_work = 'URL;WORK:'
        self.title = self._append_charset('TITLE')
        self.categories = self._append_charset('CATEGORIES')
        self.x_spouse = self._append_charset('X-SPOUSE') # w/o charset?
        self.bday = 'BDAY:'
        self.x_anniversary = 'X-ANNIVERSARY:' # Wedding date ...
        self.note = self._append_charset('NOTE')
        
        self.set_vals()

    def _construct_val(self, field, tsv_line, tsv_indices, delim=';'):
        
        s = ''
        
        idx = 0
        for tsv_idx in tsv_indices:
            data_found = tsv_line[tsv_idx]
            s += data_found
            idx += 1
            if len(tsv_indices) != idx:
                s += delim
            if len(data_found) > 0:
                self.fields_used.add(field)
                
        return s + '\n'

    def set_vals(self, tsv_line=None, tsv_mapper=None):
        
        if tsv_line is None:
            tsv_line = self.tsv_line
        if tsv_mapper is None:
            tsv_mapper = self.tsv_mapper
 
        self.n += self._construct_val('n', 
                                    tsv_line, tsv_mapper.n_idx())
        self.fn += self._construct_val('fn', 
                                    tsv_line, tsv_mapper.fn_idx())
        self.org += self._construct_val('org', 
                                    tsv_line, tsv_mapper.org_idx())
        self.nickname += \
            self._construct_val('nickname', 
                                tsv_line, tsv_mapper.nickname_idx())
        self.adr_work += \
            self._construct_val('adr_work', 
                                tsv_line, tsv_mapper.adr_work_idx())
        self.adr_home += \
            self._construct_val('adr_home', 
                                tsv_line, tsv_mapper.adr_home_idx())
        self.tel_work += \
            self._construct_val('tel_work',
                                tsv_line, tsv_mapper.tel_work_idx())
        self.tel_home += \
            self._construct_val('tel_home',
                                tsv_line, tsv_mapper.tel_home_idx())
        self.tel_cell += \
            self._construct_val('tel_cell', 
                                tsv_line, tsv_mapper.tel_cell_idx())
        self.tel_fax += \
            self._construct_val('tel_fax', 
                                tsv_line, tsv_mapper.tel_fax_idx())
        self.tel_pager += \
            self._construct_val('tel_pager', 
                                tsv_line, tsv_mapper.tel_pager_idx())
        self.email_1 += \
            self._construct_val('email_1', 
                                tsv_line, tsv_mapper.email_1_idx())
        self.email_2 += \
            self._construct_val('email_2', 
                                tsv_line, tsv_mapper.email_2_idx())
        ''' Not used
        self.email_3 += ''
        self.email_4 += ''
        self.email_5 += ''
        self.email_6 += ''
        '''
        self.url_home += \
            self._construct_val('url_home', 
                                tsv_line, tsv_mapper.url_home_idx())
        self.url_work += \
            self._construct_val('url_work',
                                tsv_line, tsv_mapper.url_work_idx())
        self.title += \
            self._construct_val('title', 
                                tsv_line, tsv_mapper.title_idx())
        self.categories += \
            self._construct_val('categories', 
                                tsv_line, tsv_mapper.categories_idx())
        self.x_spouse += \
            self._construct_val('x_spouse', 
                                tsv_line, tsv_mapper.x_spouse_idx())
        self.bday += \
            self._construct_val('bday',
                                tsv_line, 
                                tsv_mapper.bday_idx(),
                                delim='-')
        self.x_anniversary += \
            self._construct_val('x_anniversary',
                                tsv_line, 
                                tsv_mapper.x_anniversary_idx(),
                                delim='-')
        self.note += \
            self._construct_val('note',
                                tsv_line, tsv_mapper.note_idx ()) 
        
        
    def _append_charset(self, field):
        return field+self.charset        
        
    def __str__(self):
        s = self.begin
        s += self.version
        if 'n' in self.fields_used: s += self.n
        if 'fn' in self.fields_used: s += self.fn
        if 'org' in self.fields_used: s += self.org
        if 'nickname' in self.fields_used: s += self.nickname
        if 'adr_work' in self.fields_used: s += self.adr_work
        if 'adr_home' in self.fields_used: s += self.adr_home
        if 'tel_work' in self.fields_used: s += self.tel_work
        if 'tel_home' in self.fields_used: s += self.tel_home
        if 'tel_cell' in self.fields_used: s += self.tel_cell
        if 'tel_fax' in self.fields_used: s += self.tel_fax
        if 'tel_pager' in self.fields_used: s += self.tel_pager
        if 'email_1' in self.fields_used: s += self.email_1
        if 'email_2' in self.fields_used: s += self.email_2
        ''' XXX: Not used
        s += self.email_3
        s += self.email_4
        s += self.email_5
        s += self.email_6
        '''
        if 'url_home' in self.fields_used: s += self.url_home
        if 'url_work' in self.fields_used: s += self.url_work
        if 'title' in self.fields_used: s += self.title
        if 'categories' in self.fields_used: s += self.categories
        if 'x_spouse' in self.fields_used: s += self.x_spouse
        if 'bday' in self.fields_used: s += self.bday
        if 'x_anniversary' in self.fields_used: s += self.x_anniversary
        if 'note' in self.fields_used: s += self.note
        s += self.end
        
        return s + '\n'

class TbVcfCollection():
    def __init__(self, vcard=None):
        self.vcards = list()
        
        if vcard is not None:
            self.vcards.append(vcard)
            
    def __str__(self):
        s = ''
        for vcard in self.vcards:
            s += str(vcard)
            
        return s

class Tb2VcsMapper():
    
    def __init__(self, field_idx_to_name, encoding='UTF-8'):
        self.field_idx_to_name = field_idx_to_name
        
    def n_idx(self):
        return [ 
                self.field_idx_to_name['Last Name'],
                self.field_idx_to_name['First Name']
                ]
        
    def fn_idx(self):
        return [
                self.field_idx_to_name['Display Name']
                ]
    
    def org_idx(self):
        return [
                self.field_idx_to_name['Organization'],
                self.field_idx_to_name['Department']
                ]
 
    def nickname_idx(self):
        return [
                self.field_idx_to_name['Nickname']
                ]               
 
    def adr_work_idx(self):
        return [
                self.field_idx_to_name['Work Address'],
                self.field_idx_to_name['Work Address 2'],
                self.field_idx_to_name['Work City'],
                self.field_idx_to_name['Work State'],
                self.field_idx_to_name['Work ZipCode'],
                self.field_idx_to_name['Work Country']
                ]   
    
    def adr_home_idx(self):
        return [
                self.field_idx_to_name['Home Address'],
                self.field_idx_to_name['Home Address 2'],
                self.field_idx_to_name['Home City'],
                self.field_idx_to_name['Home State'],
                self.field_idx_to_name['Home ZipCode'],
                self.field_idx_to_name['Home Country']
                ]

    def tel_work_idx(self):
        return [
                self.field_idx_to_name['Work Phone']
                ]

    def tel_home_idx(self):
        return [
                self.field_idx_to_name['Home Phone']
                ]

    def tel_cell_idx(self):
        return [
                self.field_idx_to_name['Mobile Number']
                ]

    def tel_fax_idx(self):
        return [
                self.field_idx_to_name['Fax Number']
                ]

    def tel_pager_idx(self):
        return [
                self.field_idx_to_name['Pager Number']
                ]
                
    def email_1_idx(self):
        return [
                self.field_idx_to_name['Primary Email']
                ]
                
    def email_2_idx(self):
        return [
                self.field_idx_to_name['Secondary Email']
                ]
    
    # XXX: TBD
    def email_3_idx(self):
        return [
                None
                ]
    
    # XXX: TBD
    def email_4_idx(self):
        return [
                None
                ]
                
    # XXX: TBD
    def email_5_idx(self):
        return [
                None
                ]
    
    # XXX: TBD
    def email_6_idx(self):
        return [
                None
                ]

    def url_home_idx(self):
        return [
                self.field_idx_to_name['Web Page 2']
                ]
                
    def url_work_idx(self):
        return [
                self.field_idx_to_name['Web Page 1']
                ]

    def title_idx(self):
        return [
                self.field_idx_to_name['Job Title']
                ]

    # XXX: TBC (DE <-> EN)
    def categories_idx(self):
        return [
                self.field_idx_to_name['Kategorie']
                ]

    # XXX: TBC (DE <-> EN)
    def x_spouse_idx(self):
        return [
                self.field_idx_to_name['Partner']
                ]

    def bday_idx(self):
        return [
                self.field_idx_to_name['Birth Year'],
                self.field_idx_to_name['Birth Month'],
                self.field_idx_to_name['Birth Day']
                ]
    
    # XXX: TBC (DE <-> EN)            
    def x_anniversary_idx(self):
        return [
                self.field_idx_to_name['Hochzeitsjahr'],
                self.field_idx_to_name['Hochzeitsmonat'],
                self.field_idx_to_name['Hochzeitstag']
                ]
        
    def note_idx(self):
        return [
                self.field_idx_to_name['Notes']
                ]

def main():
    field_idx_to_name = dict()
    idx = 0

    f = open(DATA_DIR + TSV_FILE, 'r')
    for field_name in f.readline().split('\t'): # First line
        field_idx_to_name[field_name] = idx
        idx += 1
    
    tb2vcs_mapper = Tb2VcsMapper(field_idx_to_name)

    tb_vcf_collection = TbVcfCollection()
    cnt = 1
    for line in f.readlines():
        tb_vcf = TbVcf(
                        tsv_line=line.split('\t'),
                        tsv_mapper=tb2vcs_mapper
                        )
        tb_vcf_collection.vcards.append(tb_vcf)
        ''' Test
        print cnt, len(line.split('\t'))
        cnt += 1
        print(line.split('\t')[tb2vcs_mapper.tel_cell_idx()[0]])
        '''

    f.close()

    print(tb_vcf_collection)

if  __name__ =='__main__':
    main()
