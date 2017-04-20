import socket  
import struct  
import codecs  
import time  
import ip2locate
import chardet

''''' global constants 
'''  
LINES = []  
  
''''' transform the ip string to int 
'''  
def ip_str_to_int(ip):  
    return socket.ntohl(struct.unpack("I", socket.inet_aton(str(ip)))[0])  
  
''''' remove the invalid space 
'''  
def remove_invalid_space(line):  
    return line.split()  
  
''''' check is china 
'''  
def is_china(location):  
    if is_municipality_or_province(location) or is_autonomous_region(location) or is_special_administrative_region(location):  
        return True  
    else:  
        return False  
  
''''' check is municipality 
'''  
def is_municipality_or_province(location):  
    if '市' in location or '省' in location or '中国' in location:  
        return True  
    else:  
        return False  
  
''''' check is autonomous region 
'''  
def is_autonomous_region(location):  
    if '内蒙古' in location or '宁夏' in location or '新疆' in location or '西藏' in location or '广西' in location:  
        return True  
    else:  
        return False  
  
''''' check is special administrative region 
'''  
def is_special_administrative_region(location):  
    if '香港' in location or '澳门' in location:  
        return True  
    else:  
        return False  
  
''''' convert location to country, province, city 
'''  
def convert_location(location):  
    if is_china(location):  
        # process china  
        if '中国' in location:  
            country = '中国'  
            province = ''  
            city = ''  
        else:  
            country = '中国'  
            if '澳门' in location:  
                province = '澳门'  
                city = '澳门'  
            elif '香港' in location:  
                province = '香港'  
                city = '香港'  
            elif is_autonomous_region(location):  
                if '内蒙古' in location:  
                    length = 3  
                else:  
                    length = 2  
                province = location[:length]  
                index = location.find('市')  
                if index != -1:  
                    city = location[length:index]  
                else:  
                    city = ''  
            elif '省' in location:  
                index_province = location.find('省')  
                province = location[:index_province]  
                index_city = location.find('市')  
                if index_city != -1:  
                    city = location[index_province+1:index_city]  
                else:  
                    city = ''  
            else:  
                index_city = location.find('市')  
                province = location[:index_city]  
                index_region = location.find('区')  
                if index_region != -1:  
                    city = location[index_city+1:index_region+1]  
                else:  
                    city = ''                  
    else:  
        # process foreign country  
        country = location  
        province = ''  
        city = ''  
    if '大学' in location:  
        # special process  
        country = '中国'  
        province = location  
        city = ''  
    return country + ',' + province + ',' + city  
      
''''' format one line 
'''  
def format_one_line(line):  
    begin = ip_str_to_int(line[0])  
    end = ip_str_to_int(line[1])  
    if len(line) == 6:  
        net = line[-3] + line[-2] + line[-1]  
    elif len(line) == 5:  
        net = line[-2] + line[-1]  
    else:  
        net = line[-1]  
    location = convert_location(line[2])  
    convert_line = str(begin) + ',' + str(end) + ',' + location + ',' + net + '\n'  
  
    global LINES  
    LINES.append(convert_line)  
  
''''' write to csv file 
'''  
def write_to_csv_file(lines):  
    try:  
        file = open('ip.csv', 'a', encoding = 'raw-unicode-escape')  
        file.writelines(lines)  
    except FileNotFoundError:  
        print('file not found')  
    finally:  
        if 'file' in locals():  
            file.close()  
      
''''' format the ip file to which we want 
'''  
def format_ip_file(path):  
    try:  
        file = open(path)  
        for line in file:  
            # main logic of format  
            format_one_line(remove_invalid_space(line))  
    except FileNotFoundError:  
        print('file not found')  
    finally:  
        if 'file' in locals():  
            file.close()  
  
'''''
'''
def write2csvfile():  
  print('start format')  
  format_ip_file('ip_tmp.txt')  
  print('end format')  
  print('start write')  
  write_to_csv_file(LINES)  
  print('end write', end = '')  

'''''
load data infile './ip.csv'
into table 'ip'
fields terminated by ',' optionally enclosed by '' escaped by ''
lines terminated by '\r\n';
'''
def convertIp2Locate(str):
  return ip_str_to_int(str)

  




if __name__=='__main__':
  addr=[]
  count=0
  with open('./src_ip.txt','r') as f:
    src_ips=f.readlines()
    for src_ip in src_ips:
      ip=convertIp2Locate(src_ip)
      with codecs.open('./ip.csv','r','gbk') as g:
        baseips=g.readlines()
        for baseip in baseips:
          final_ip2s=baseip.split(',')
          if (int(final_ip2s[0]))<int(ip)<(int(final_ip2s[1])):
            addr.append(src_ip+","+baseip)
  with codecs.open('./output_ip_addr.txt','w','gbk') as h:
    [h.write(addr[int(i)]) for i in range(0,len(addr))]
        
      


      
      
  