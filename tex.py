import csv,os
from operator import itemgetter
import datetime as dt

PLEN_OUT_PATH       = 'program/sessions/'
MAIN_OUT_FILE       = 'program/main/main.tex'   
INPUT_PATH          = 'sorted/sessions/'

class Program:
    def __init__(self):
        self.day_sess = {}
        for date in range(17,30):
            self.day_sess[date] = {}

    def sessions(self):
    

        break_dict = self.break_dict_creator()
        social_dict= self.social_dict_creator()
            
        session_files = []
        for (dirpath, dirnames, filenames) in os.walk(INPUT_PATH):
            session_files.extend(filenames)
            break
        session_files.sort()
    
        sessions_nam = {}
        sessions_num = {}

        with open(INPUT_PATH+session_files[0],'r') as order:
            for line in order:
                line = line.strip().split('#')
                sessions_nam[line[0]] = line[1]
                sessions_num[line[1]] = line[0]

        for date in range(17,30):
            #if date==27:
            #    self.day_sess[date]['Round Table'] = [[date,'19.00 - 20.30',\
            #                                           '"Round Table on High Energy Physics after the LHC"',\
            #                                           '','']

            for fi in session_files[1:]:
                self.day_sess[date][sessions_nam[fi[-2:]]] = []
                with open(INPUT_PATH+fi,'r') as f:
                    datareader = csv.reader(f,delimiter=',',quotechar='"')
                    for i,row in enumerate(datareader):
                        date_sess = row[0]
                        if date_sess!=str(date):
                            break
                        else:
                            self.day_sess[date][sessions_nam[fi[-2:]]].append(row)
                if i>0:

                    day = str(date)
                    for key in break_dict[day]:
                        try:
                            speaker = break_dict[day][key][3]
                            length  = str(break_dict[day][key][2])
                            clock   = break_dict[day][key][0].strftime('%H.%M')+\
                                      ' - '+\
                                      break_dict[day][key][1].strftime('%H.%M')
                            
                            self.day_sess[date][sessions_nam[fi[-2:]]].append([day,clock,speaker,length,'',''])
                        except:
                            pass

             
            self.day_sess[date]['social'] = []
            for social in social_dict[date]:
                self.day_sess[date]['social'].append([str(date)]+social) 

        for key,value in self.day_sess.items():
            for key2,value2 in value.items():
                val = sorted(value2,key=itemgetter(1)) 
                if val:
                    if key2=='social':
                        tablestart      ='\\begin{longtable}{p{3cm}p{10cm}p{4cm}}\n\\vspace{1cm}\n'
                        A=open(PLEN_OUT_PATH+str(key)+'0_social.tex','w+')
                        A.write(tablestart)
                        for v in val:
                            date_sess = key
                            clock     = v[1]
                            title     = v[2]
                            length    = v[3]

                            h = length.split('h')[0]
                            m = length.split('h')[1][:-1]
                            talkrow = clock+' & {\\bf '+title+'} & \\hfill '
                            titlerow= h+' h '+str(int(m))+' min\\\ \n\\vspace{1cm}\n'

                            A.write(talkrow+titlerow)

                    else:
                        A=open(PLEN_OUT_PATH+str(key)+'_'+sessions_num[key2]+".tex",'w+')
                        tablestart ='\\begin{longtable}{p{3cm}p{13cm}}\n'
                        A.write(tablestart)
                        A.write('&\\hfill {\\bf Convenor '+'INSERT CHAIRMEN'+' }\\\ \n')
                        for v in val:
                            date_sess = v[0]
                            clock     = v[1]
                            speaker   = v[2]
                            length    = v[3]
                            title     = v[4].replace('_','\\_').replace('^','\\^')
                            affili    = v[5]

                            speaker = " ".join(item[0].upper()+item[1:] for item in speaker.lower().split())

                            if 'Coffee' in speaker or 'Lunch' in speaker or 'Dinner' in speaker:
                                talkrow     = clock+' & '+'{\\bf '+speaker+'} \\hfill '
                                titlerow    = length+' \\\ \n & \\\ \n'+' & \\\ \n'

                            else:
                                talkrow = clock+' & '+speaker+' ('+affili+')\\\ \n'
                                titlerow= length+' min. & {\\it '+title+'}\\\ \n'+\
                                          ' & \\\ \n'

                            A.write(talkrow+titlerow) 
                    tablestop ='\\end{longtable}\n\n'
                    A.write(tablestop)
                    A.close()
                        
    def main_tex(self):
    
        main = open(MAIN_OUT_FILE,'w+')
        with open(PLEN_OUT_PATH+'order','r') as order:
            order_dict  = {}
            for line in order:
                temp_line = line.strip().split('#')
                order_dict[temp_line[0]] = temp_line[1]

        main.write('\\input{program/main/preamble.tex}\n'+\
              '\\begin{document}\n'+\
              '\\tableofcontents\n\\clearpage\n')
      
        session_files = []
        for (dirpath, dirnames, filenames) in os.walk(PLEN_OUT_PATH):
            session_files.extend(filenames)
            break

        session_files.sort()
    
        section     = '\\section{{}}' 
        subsection  = '\\subsection{{{}}}\n'
        old_date = '16'
        print(session_files)
        for fi in session_files:
            if fi=='order':
                continue
            elif 'social' in fi:
                session = 'Social events'
            else:
                session = order_dict[fi[-6:-4]]
            date = fi[:2]
            if date != old_date:
                main.write(section.format(date)+'\n')
                old_date=date
    
            main.write(subsection.format(session))
            main.write('\\input{\\PlenaryPath/'+fi+'}\n')
            main.write('\\clearpage\n\n')
           
        main.write('\\end{document}\n')
        main.close()
    
    def break_dict_creator(self):
        break_dict = {}
    
        with open('inputfiles/breaks.csv','r') as breaks:
            h = breaks.readline().strip().split(',')
            for line in breaks:
                temp_line = line.strip().replace(' ','').split(',')
                day = temp_line[0]
                break_dict[day] = {}
                
                for i,he in enumerate(h[1::3]):

                    try:
                        length = str(self.create_datetime(day,temp_line[i*3+3])-\
                                     self.create_datetime(day,temp_line[i*3+2]))

                        length = dt.datetime.strptime(length,'%H:%M:%S')
                        length = length.strftime('%H:%M')
                        if length[:2]=='00':
                            length=length[3:]+' min'
                        else:
                            length = length[1:2]+' h '+length[3:]+' min'

                        break_dict[day][he] = [self.create_datetime(day,temp_line[i*3+2]),\
                                               self.create_datetime(day,temp_line[i*3+3]),\
                                               length,\
                                               temp_line[i*3+1]]
                    except Exception as e:
                        break_dict[day][he] = []
        return break_dict
        
    def social_dict_creator(self):
        social_dict = {}
        for day in range(17,30):
            social_dict[day] = []

        with open('inputfiles/social.csv','r') as socials:
            social_reader = csv.reader(socials,delimiter=',',quotechar='"')
            headers = next(social_reader)
            for line in social_reader:
                day = line[0]
                social_dict[int(day)].append(line[1:])
        return social_dict 

    def create_datetime(self,day,time):
        return dt.datetime.strptime('2017-08-'+day+'-'+time,'%Y-%m-%d-%H.%M')

if __name__=='__main__':
  writer = Program()
  writer.sessions()
  writer.main_tex()
