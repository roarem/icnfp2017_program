import csv
import datetime as dt
from operator import itemgetter


def sort_contributions(filename='inputfiles/contributions.csv'):
    has_key = lambda a, d: any(a in k for k in d)

    with open(filename,'r') as cont_file, open('inputfiles/registrations.csv','r') as regs:
        dates = list(range(17,30))
        cont_reader = csv.reader(cont_file,delimiter=',',quotechar='"')
        headers = next(cont_reader)
        session_mat = []
        sessions = {} 
        count = 0
        out_csv = []
        csv_writers = []
        order_file = open('sorted/sessions/order','w+')

        for row in cont_reader:
            session_mat.append(row)
            if has_key(row[6],sessions):
                continue

            else:
                sessions[row[6]] = count 
                out_csv.append(open('sorted/sessions/session_'+format(count,'02d'),'w+'))
                order_file.write('{:02d}#{}\n'.format(count,row[6]))
                csv_writers.append(csv.writer(out_csv[count],delimiter=',',\
                                   quotechar='"',quoting=csv.QUOTE_MINIMAL))
                count += 1

        order_file.close()
        date_sorted_mat = sorted(session_mat,key=itemgetter(3)) 
        regs = regs.readlines()
        #plenary_csv = open('plenary.csv','w+')
        #csv_writer = csv.writer(plenary_csv,delimiter=',',\
        #                        quotechar='"',quoting=csv.QUOTE_MINIMAL)

        for row in date_sorted_mat:
            if row[3] and row[6]:
                day,clock,length    = check_duration(row[4],row[3][:16])
                speaker             = row[8] 
                #with open('inputfiles/registrations.csv','r') as regs:
                for line in regs:
                    temp_line = line.strip().split(',')
                    name = temp_line[1]
                    if name==speaker:
                        affiliation = temp_line[4]
                        break
                title               = row[1]
                session             = row[6]

                csv_line = [day,clock,speaker,length,title,affiliation]

                csv_writers[sessions[session]].writerow(csv_line)
                #csv_writer.writerow(csv_line)

        for out in out_csv:
            out.close()

        #plenary_csv.close()

def check_duration(dur,time):
    dur = dur.split()

    if dur[1]=='minutes' or 'hour' in dur[1]:
        minutes = int(dur[0]) if dur[1]=='minutes' else 0
        hours   = int(dur[0]) if dur[1] in 'hour' else 0
    else:
        hours   = int(dur[0].replace('h',''))
        minutes = int(dur[1].replace('m',''))
    
    start   = dt.datetime.strptime(time,'%Y-%m-%d %H:%M')
    dura    = dt.timedelta(hours=hours,minutes=minutes)
    length  = str((dura-dt.timedelta(minutes=5)))[2:4]+'+5'
    day     = start.strftime('%d')
    stop    = start+dura
    clock   = start.strftime('%H.%M')+' - '+stop.strftime('%H.%M')

    return day,clock,length

if __name__=='__main__':
    sort_contributions()

