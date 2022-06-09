# inoon-bin_to_csv.py
# 실행파일과 같은 폴더에 있는 raw data bin file을 인식해 csv로 변환해줍니다.
# 편의를 위해 bin list를 출력하고 파일의 번호를 골라 csv로 바꿀 수 있게 했습니다.
# bin_to_csv(filename)만을 사용해도 상관없을듯합니다.
import pandas as pd
import json
import requests
import sys
import datetime as dtime
from datetime import datetime
import os


raw_json = {}

# string bin_to_csv(filename)
# 파일 이름을 기반으로 파일에 접근하고 읽습니다. 이후 그 파일의 데이터를 csv 파일 형식으로 변환시켜줍니다.
# 변환이 완료되면 저장한 파일명을 return합니다.
def bin_to_csv(filename):
    type_name = filename[25:27]
    f = open(filename, 'rb')
    #print(filename)
    try:
        raw_json = json.loads(f.read().decode('utf_8'))
    except requests.JSONDecodeError as msg:
        print(F"ERROR : json decode has failed.\n please check the file.")
        sys.exit(0)
    except FileNotFoundError as msg:
        print(F"ERROR : there is no file.\n")
        sys.exit(0)
# file close    

    # 센서 종류와 관계없이 data가 list이므로 
    index_list = list()
    data_list = list()
    time_list = list() # 각각 csv파일의 1열, 2열, 3열에 삽입될 데이터

    start_time = datetime.strptime(raw_json["starttime"],"%Y-%m-%d %H:%M:%S") # 예 : 2022-06-09 09:30:00
    end_time = datetime.strptime(raw_json["endtime"],"%Y-%m-%d %H:%M:%S")

    measure_gap = end_time - start_time 
    measure_time = measure_gap.seconds+1 #통상의 경우 600초
    time_count = 0 # time index 기록용 count
    samplerate = raw_json["count"]//measure_time
    index_list = list(range(1, raw_json["count"]+1))

    for i in range(len(raw_json["data"])): # time쪽 잘 돌아가는지 잘 볼 것
        data_list.append(raw_json["data"][i])
        csv_file_time = datetime.strftime(start_time + dtime.timedelta(seconds = time_count), "%H:%M:%S")
        time_list.append(csv_file_time) 
        if (i+1)%samplerate == 0:
            time_count +=1

    excel_frame = pd.DataFrame({"time":time_list, type_name:data_list}, index = index_list)
    #print(excel_frame)
    excel_frame.to_csv(F"{filename[:len(filename)-4]}.csv", mode = "w")

    return F"{filename[:len(filename)-4]}.csv"

# #### 함수부 끝 ####

file_list = os.listdir(os.getcwd()) # 현재 디렉토리에 있는 파일 리스트를 출력
file_list.sort()
not_bin_list = list()

for file in file_list:
    if file[13:16] == "ae." and (file[25:27] == "AC" or file[25:27] == "DI" or file[25:27] == "TP" or file[25:27] == "TI" or file[25:27] == "DS" or file[25:27] == "SS" or file[25:27] == "EX") and file[len(file)-4:] ==".bin":
        pass
    else:
        not_bin_list.append(file)
1

#print(not_bin_list)
if len(not_bin_list) != 0: # bin파일이 아닌 파일이 존재했다면 리스트에서 제외
    for file in not_bin_list:
        file_list.remove(file)

if len(file_list) == 0:
    print("ERROR : there is no file to convert")
    input("press enter to exit...\n")
    sys.exit(0)

while True:
    print("####bin file list####")
    for i in range(len(file_list)):
        print(F"No.{i+1} : {file_list[i]}")
    print("---------")
    input_number = input("enter the number of file which you want to convert to csv\n")
    try:
        input_number = int(input_number)
    except ValueError:
        print("ERROR : you should enter integer")
        print("please retry")
        print("---------")
        continue

    if input_number >= 1 and input_number <= len(file_list):
        print(F"selected file : {file_list[input_number-1]}")
        selected_file = file_list[input_number-1]
    else:
        print("ERROR : entered number is out of range")
        print("please retry")
        print("---------")
        continue

    #print(selected_file[:len(selected_file)-4]+".csv")

    if selected_file[:len(selected_file)-4]+".csv" in not_bin_list: # 이미 csv파일이 존재하는 경우, 한번 더 묻는다
        print("ALERT : csv file with same name already exists")
        print("file name :", selected_file[:len(selected_file)-4]+".csv")
        answer = input("do you really want to make csv file? {Y, N} \n")

        if answer == "Y" or answer == "y":
            print("YES => continue converting.")
            print("---------")
            break
        elif answer == "N" or answer == "n":
            print("NO => please enter other file number")
            print("---------")
            continue
        else:
            print("unknown input : consider input NO command")
            print("NO => please enter other file number")
            print("---------")
            continue

    else:
        break



print("converting...")
file_name = bin_to_csv(file_list[input_number-1])
print("csv file name : ", file_name)
input("press enter to exit...\n")



