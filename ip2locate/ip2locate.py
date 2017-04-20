import urllib.parse  
import urllib.request  
import codecs
import re
import chardet
import traceback  
''''' global constants 
'''  
START = ''  
END = ''  
LOCATION = ''  
NET = ''  
LINES = []  
  
''''' remove the invalid space 
'''  
def remove_invalid_space(line):  
    return line.split()  
  
''''' format one line 
'''  
def format_one_line(line):  
#    print(line)
    if len(line) == 6:  
        net = line[-3] + line[-2] + line[-1]  
    elif len(line) == 5:  
        net = line[-2] + line[-1]  
    else:  
        net = line[-1]  
    line_format = [line[0], line[1] , line[2], net]  
    return line_format  
  
''''' merge 
'''  
def line_merge(line): 
    if line is None:
        return None    
    location = line[2]  
    net = line[3]  
      
    line_format = [line[0], line[1], location, net]  
    global LOCATION  
    global NET  
    global START  
    global END  
    if is_same_line(LOCATION, location):  
        line_format_over_write = START + ' ' + str(line_format[1]) + ' ' + LOCATION + ' ' + NET  
        over_write_array(line_format_over_write)  
    else:  
        write_to_array(str(line_format[0]) + ' ' + str(line_format[1]) + ' ' + str(line_format[2]) + ' ' + str(line_format[3]))  
        START = line[0]  
        END = line[1]  
        LOCATION = location  
        NET = net  
  
''''' write to the global param 
'''  
def write_to_array(line):  
    global LINES  
    LINES.append(line)  
    
  
''''' over write to the global param 
'''  
def over_write_array(line):  
    global LINES  
    del LINES[-1]  
    LINES.append(line)  
  
''''' is the same line 
'''  
def is_same_line(last_location, current_location):  
    if last_location == current_location:  
        return True  
    else:  
        last_location_cut = cut_the_location(last_location)  
        current_location_cut = cut_the_location(current_location)  
        if last_location_cut == current_location_cut:  
            return True  
        else:  
            return False  
  
''''' cut the location 
'''  
def cut_the_location(location):  
    index_city = location.find('市')  
    if index_city != -1:  
        return location[0:index_city+1]  
    else:  
        return location  
  
''''' write to tmp file 
'''  
def write_to_tmp_file(lines):  
    try:  
        file = open('ip_tmp.txt', 'a')  
        for line in lines:  
            file.write(line + '\n')  
    except FileNotFoundError:  
        print('file not found')  
    finally:  
        if 'file' in locals():  
            file.close()  
          
def format_ip_file(path):  
    count=0
    try:  
        #file = codecs.open(path,'r','utf8')  
        file = open(path) 
        for line in file.readlines():
          if len(line)==1:
            return None
          count+=1
            # main logic  
          try:
            line_merge(format_one_line(remove_invalid_space(line)))
          except:
            print(line)
            print(len(line))
            print(line)
            print(count)
            traceback.print_exc()
    except FileNotFoundError:  
        print('file not found')  
    finally:  
        if 'file' in locals():  
            file.close()  
if __name__=='__main__':  
    print('start format')  
    format_ip_file('./data/temp/database.txt')  
    print('end format')  
    print('start write')  
    write_to_tmp_file(LINES)  
    print('end write', end = '')  