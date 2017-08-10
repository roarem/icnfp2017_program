#from os import walk
import csv,os

PLEN_OUT_PATH      = '../program/plenary/'
PARA_OUT_PATH      = '../program/parallel/'
POST_OUT_PATH      = '../program/poster/'
PLEN_IN_FILE       = '../inputfiles/plenary.csv'
PARA_IN_FILE       = '../inputfiles/parallel.csv'
POST_IN_FILE       = '../inputfiles/poster.csv'
PARA_CONV_IN_FILE  = '../inputfiles/convenors_parallel.csv'
PLEN_CONV_IN_FILE  = '../inputfiles/convenors_plenary.csv'

class Program:

  def date_string(self,date):
    if date=='1':
        return 'Week day 1, Month day 1'
    if date=='2':
        return 'Week day 2, Month day 2'
    if date=='3':
        return 'Week day 3, Month day 3'
    if date=='4':
        return 'Week day 4, Month day 4'
    return 'Unresolved'

  def posters(self):
    tablestart      ='\\begin{longtable}{p{0.5cm}p{15cm}}\n'
    tablestop       ='\\end{longtable}\n' 
    f=open("posters.csv",'r')
    datareader = csv.reader(f,delimiter=',',quotechar='"')
    A=open("posters.tex",'w')
    A.write('\\clearpage\n\\begin{center}\n{\\bf \\Large Posters}\n\\end{center}\n')
    A.write(tablestart)
    for i,row in enumerate(datareader):
      last_name = row[0]
      first_name= row[1]
      title     = row[2]
     
      A.write(str(i+1)+'.& '+last_name+', '+first_name+'\\\ \n')
      A.write('& '+title+'\\\ \n \\\ \n ')
    A.write(tablestop)
    A.close()

  def plenary (self):

    old_date        = '1'
    #tablestart      ='\\begin{longtable}[h!]\n\\begin{tabular}{p{3cm}p{13cm}}\n'
    tablestart      ='\\begin{longtable}{p{3cm}p{13cm}}\n'#[h!]\n\\begin{tabular}\n'
    #tablestop       ='\\end{tabular}\n\\end{longtable}\n\n'#+30*'%'+'\n\\hspace*{-10cm}\n' 
    tablestop       ='\\end{longtable}\n\n'#+30*'%'+'\n\\hspace*{-10cm}\n' 

    session_files = []
    for (dirpath, dirnames, filenames) in os.walk('../inputfiles/sessions/'):
        session_files.extend(filenames)
        break
    session_files.sort()

    sessions = {}
    with open('../inputfiles/sessions/'+session_files[0],'r') as order:
        for line in order:
            line = line.strip().split('#')
            sessions[line[1]] = line[0]

    for fi in session_files[1:]:
        #f=open(PLEN_IN_FILE,'r')
        f=open('../inputfiles/sessions/'+fi,'r')
        #g=open(PLEN_CONV_IN_FILE,'r')
        #A=open(PLEN_OUT_PATH+"plenary1.tex",'w')
        A=open(PLEN_OUT_PATH+fi+".tex",'w+')
        
        datareader = csv.reader(f,delimiter=',',quotechar='"')
        #chairmen   = csv.reader(g,delimiter=',',quotechar='"')
        #headers = next(datareader)

        A.write(tablestart)
        A.write('&\\hfill {\\bf Convenor '+'INSERT CHAIRMEN'+' }\\\ \n')
        #A.write('&\\hfill {\\bf Convenor '+next(chairmen)[2] + ' }\\\ \n')

        for row in datareader:
            date      = row[0]
            clock     = row[1]
            speaker   = row[2]
            #last_name   = row[2]
            #first_name  = row[3]
            #stay        = row[4]
            #institute   = row[5]
            length    = row[3]
            title     = row[4]
            
            #if date!=old_date:
            #    A.write(tablestop)
            #    A.close()
            #    A = open(PLEN_OUT_PATH+"plenary"+date+".tex",'w')
            #    A.write(tablestart)
            #    try:
            #        chairman = next(chairmen)[2]
            #    except:
            #        chairman = ''

            #    A.write('&\\hfill {\\bf Convenor '+chairman + ' }\\\ \n')
            #    old_date = date
              
              
            if 0:#'Coffee' in speaker:#last_name:
                pass
                #try:
                #   chairman = next(chairmen)[2]
                #except:
                #    chairman = ''
                #talkrow  = clock+' & '+'{\\bf Coffee} \\hfill '+\
                #           '{\\bf Convenor '+chairman+' }\\\ \n'
                #titlerow = ' & \\\ \n'

            else:
                talkrow = clock+' & '+speaker+'\\\ \n'#last_name.upper()+', '+\
                          #first_name+' ('+institute+')\\\ \n'
                titlerow= length+' min. & {\\it '+title+'}\\\ \n'+\
                          ' & \\\ \n'

                A.write(talkrow+titlerow) 
                
        A.write(tablestop)
        A.close() 
        f.close()
        #g.close()

  def parallel (self):
    old_date        = ''
    old_session     = ''
    chair_line      = '  \\hfill Convenor {}'
    tablestart      ='\\begin{longtable}[h!]\n\\begin{tabular}{p{3cm}p{13cm}}\n'
    tablestop       ='\\end{tabular}\n\\end{longtable}\n\n'+30*'%'+\
                     '\n\\hspace*{-10cm}\n' 
 
    f=open(PARA_IN_FILE,'r')
    g=open(PARA_CONV_IN_FILE,'r')
    A=open(PARA_OUT_PATH+"parallel1.tex",'w')
    
    datareader = csv.reader(f,delimiter=',',quotechar='"')
    chairmen   = csv.reader(g,delimiter=',',quotechar='"')
    headers = next(datareader)
    chaircount = 0
    for row in datareader:
      date        = row[0]
      session     = row[1]
      clock       = row[2]
      last_name   = row[3]
      first_name  = row[4]
      stay        = row[5]
      institute   = row[6]
      length      = row[7]
      title       = row[8]
      
      if session!=old_session:
        if old_session!='':
          A.write(tablestop)
          
        if date!=old_date:
          A.close()
          A = open(PARA_OUT_PATH+"parallel"+date+".tex",'w')
          old_date = date
          
        try:
           chairman = next(chairmen)[2]#chairmen[chaircount]
        except:
            chairman = 'TBA'

        sessionstart = '\\multicolumn{2}{c}{{\\bf Session '+session+\
                        chair_line.format(chairman)+'}}\\\ \n '
        A.write(tablestart+sessionstart)
        old_session = session
        chaircount += 1
        
      talkrow = clock+' & '+last_name.upper()+', '+first_name+' ('+institute+')\\\ \n'
      titlerow= length+' min. & {\\it '+title+'}\\\ \n'+\
                ' & \\\ '
      A.write(talkrow+titlerow) 
    
    A.write(tablestop)
    A.close() 
    f.close()
    g.close()

if __name__=='__main__':
  writer = Program()
  writer.plenary()
  writer.parallel()
  #writer.posters()
