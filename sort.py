import csv
import datetime as dt
from operator import itemgetter


def sort_contributions(filename='inputfiles/contributions.csv'):
    has_key = lambda a, d: any(a in k for k in d)

    break_dict = break_dict_creator()

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

        for row in date_sorted_mat:
            if row[3] and row[6]:
                day,clock,length = check_time(row[4],row[3][:16])
                speaker = row[8] 
                for line in regs:
                    temp_line = line.strip().split(',')
                    name = temp_line[1]
                    if name==speaker:
                        affiliation = temp_line[4]
                        break
                title   = row[1]
                session = row[6]

                csv_line = [day,clock,speaker,length,title,affiliation]

                csv_writers[sessions[session]].writerow(csv_line)

                start_time = create_datetime(day,clock[:6].strip())
                stop_time  = create_datetime(day,clock[8:].strip())
                for key in break_dict[day]:
                    try:
                        if stop_time>=break_dict[day][key][0] and stop_time<=break_dict[day][key][1]:
                            speaker = break_dict[day][key][3]
                            length  = str(break_dict[day][key][2])
                            clock   = break_dict[day][key][0].strftime('%H.%M')+\
                                      ' - '+\
                                      break_dict[day][key][1].strftime('%H.%M')

                            csv_line = [day,clock,speaker,length,'','']
                            csv_writers[sessions[session]].writerow(csv_line)
                    except:
                        pass

        for out in out_csv:
            out.close()

def create_datetime(day,time):
    return dt.datetime.strptime('2017-08-'+day+'-'+time,'%Y-%m-%d-%H.%M')

def break_dict_creator():
    break_dict = {}

    with open('inputfiles/breaks.csv','r') as breaks:
        h = breaks.readline().strip().split(',')
        for line in breaks:
            temp_line = line.strip().replace(' ','').split(',')
            day = temp_line[0]
            break_dict[day] = {}
            for i,he in enumerate(h[1::3]):
                try:

                    length = str(create_datetime(day,temp_line[i*3+3])-\
                                 create_datetime(day,temp_line[i*3+2]))
                    length = dt.datetime.strptime(length,'%H:%M:%S')
                    length = length.strftime('%H:%M')
                    if length[:2]=='00':
                        length=length[3:]+' min'
                    else:
                        length = length[1:2]+' h '+length[3:]+' min'
                    break_dict[day][he] = [create_datetime(day,temp_line[i*3+2]),\
                                           create_datetime(day,temp_line[i*3+3]),\
                                           length,\
                                           temp_line[i*3+1]]
                except:
                    break_dict[day][he] = []
    return break_dict

def check_time(dur,time):
    dur = dur.split()

    if dur[1]=='minutes' or 'hour' in dur[1]:
        minutes = int(dur[0]) if dur[1]=='minutes' else 0
        hours   = int(dur[0]) if dur[1] in 'hour' else 0
    else:
        hours   = int(dur[0].replace('h',''))
        minutes = int(dur[1].replace('m',''))
    
    start   = dt.datetime.strptime(time,'%Y-%m-%d %H:%M')+dt.timedelta(hours=3)
    dura    = dt.timedelta(hours=hours,minutes=minutes)
    length  = str((dura-dt.timedelta(minutes=5)))[2:4]+'+5'
    day     = start.strftime('%d')
    stop    = start+dura
    clock   = start.strftime('%H.%M')+' - '+stop.strftime('%H.%M')

    return day,clock,length

if __name__=='__main__':
    sort_contributions()
    #print(break_dict_creator())
