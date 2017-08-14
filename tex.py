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
    
        tablestart      ='\\begin{longtable}{p{3cm}p{13cm}}\n'
        tablestop       ='\\end{longtable}\n\n'

        break_dict = self.break_dict_creator()
            
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

        #day_sess = {17:{},18:{},19:{},20:{},21:{},22:{},23:{},24:{},25:{},26:{},27:{},28:{},29:{}}

        for date in range(17,30):
            #day_sess[date] = {}
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
            
        for key,value in self.day_sess.items():
            for key2,value2 in value.items():
                val = sorted(value2,key=itemgetter(1)) 
                if val:
                    A=open(PLEN_OUT_PATH+str(key)+'_'+sessions_num[key2]+".tex",'w+')
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
                    A.write(tablestop)
                    A.close()

        


        #for date in range(17,30):
        #    for fi in session_files[1:]:

        #        f=open(INPUT_PATH+fi,'r')
        #        datareader = csv.reader(f,delimiter=',',quotechar='"')
        #        for i,row in enumerate(datareader):
        #            date_sess = row[0]
        #            clock     = row[1]
        #            speaker   = row[2]
        #            length    = row[3]
        #            title     = row[4].replace('_','\\_').replace('^','\\^')
        #            affili    = row[5]

        #            speaker = " ".join(item[0].upper()+item[1:] for item in speaker.lower().split())
        #            if date_sess!=str(date):
        #                break

        #            else:

        #                if i==0:
        #                    A=open(PLEN_OUT_PATH+str(date)+'_'+fi[-2:]+".tex",'w+')
        #                    A.write(tablestart)
        #                    A.write('&\\hfill {\\bf Convenor '+'INSERT CHAIRMEN'+' }\\\ \n')
        #                
        #                if 'Coffee' in speaker or 'Lunch' in speaker or 'Dinner' in speaker:
        #                    talkrow     = clock+' & '+'{\\bf '+speaker+'} \\hfill '
        #                    titlerow    = length+' \\\ \n & \\\ \n'+' & \\\ \n'

        #                else:
        #                    talkrow = clock+' & '+speaker+' ('+affili+')\\\ \n'
        #                    titlerow= length+' min. & {\\it '+title+'}\\\ \n'+\
        #                              ' & \\\ \n'
    
        #                A.write(talkrow+titlerow) 
        #              
    
        #        try:
        #            A.write(tablestop)
        #            A.close() 
        #        except:
        #            continue
        #        f.close()
                        
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
        for fi in session_files[:-1]:
            date = fi[:2]
            if date != old_date:
                main.write(section.format(date)+'\n')
                old_date=date
    
            session = order_dict[fi[-6:-4]]
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
        
    def create_datetime(self,day,time):
        return dt.datetime.strptime('2017-08-'+day+'-'+time,'%Y-%m-%d-%H.%M')

if __name__=='__main__':
  writer = Program()
  writer.sessions()
  writer.main_tex()
