import csv,os

PLEN_OUT_PATH       = 'program/sessions/'
MAIN_OUT_FILE       = 'program/main/main.tex'   
INPUT_PATH          = 'sorted/sessions/'

class Program:

    def sessions(self):
    
        old_date        = '17'
        tablestart      ='\\begin{longtable}{p{3cm}p{13cm}}\n'
        tablestop       ='\\end{longtable}\n\n'
    
        session_files = []
        for (dirpath, dirnames, filenames) in os.walk(INPUT_PATH):
            session_files.extend(filenames)
            break
        session_files.sort()
    
        sessions = {}
        with open(INPUT_PATH+session_files[0],'r') as order:
            for line in order:
                line = line.strip().split('#')
                sessions[line[1]] = line[0]
    
        for date in range(17,30):
            for fi in session_files[1:]:

                f=open(INPUT_PATH+fi,'r')
                datareader = csv.reader(f,delimiter=',',quotechar='"')
                for i,row in enumerate(datareader):
                    date_sess = row[0]
                    clock     = row[1]
                    speaker   = row[2]
                    length    = row[3]
                    title     = row[4].replace('_','\\_').replace('^','\\^')
                    affili    = row[5]

                    speaker = " ".join(item[0].upper()+item[1:] for item in speaker.lower().split())
                    if date_sess!=str(date):
                        break

                    if i==0:
                        A=open(PLEN_OUT_PATH+str(date)+'_'+fi[-2:]+".tex",'w+')
                        A.write(tablestart)
                        A.write('&\\hfill {\\bf Convenor '+'INSERT CHAIRMEN'+' }\\\ \n')

                    talkrow = clock+' & '+speaker+' ('+affili+')\\\ \n'
                    titlerow= length+' min. & {\\it '+title+'}\\\ \n'+\
                              ' & \\\ \n'
    
                    A.write(talkrow+titlerow) 
                      
                    #if 0:#'Coffee' in speaker:#last_name:
                        #pass
                        #try:
                        #   chairman = next(chairmen)[2]
                        #except:
                        #    chairman = ''
                        #talkrow  = clock+' & '+'{\\bf Coffee} \\hfill '+\
                        #           '{\\bf Convenor '+chairman+' }\\\ \n'
                        #titlerow = ' & \\\ \n'
    
                try:
                    A.write(tablestop)
                    A.close() 
                except:
                    continue
                f.close()
                        
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
    
        section     = '\\section{' 
        subsection  = '\\subsection{{{}}}\n'
        old_date = '16'
        for fi in session_files[:-1]:
            date = fi[:2]
            if date != old_date:
                main.write(section+str(date)+'. August}\n')
                old_date=date

            session = order_dict[fi[-6:-4]]
            main.write(subsection.format(session))
            main.write('\\input{\\PlenaryPath/'+fi+'}\n')
            main.write('\\clearpage\n\n')
           
        main.write('\\end{document}\n')
        main.close()
    
        
if __name__=='__main__':
  writer = Program()
  writer.sessions()
  writer.main_tex()
