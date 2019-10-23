import os
import exifread
import re
import json
import requests
from coord_convert.transform import wgs2gcj

from scr import html

def latitude_and_longitude_convert_to_decimal_system(*arg):
    """
    经纬度转为小数, param arg:
    :return: 十进制小数
    """
    return float(arg[0]) + ((float(arg[2])/ 60 + (float(arg[1].split('/')[0]) / float(arg[1].split('/')[-1]) )) / 60)

def find_GPS_image(pic_path):
    GPS = {}
    date = ''
    with open(pic_path, 'rb') as f:
        tags = exifread.process_file(f)
        for tag, value in tags.items():
            if re.match('GPS GPSLatitudeRef', tag):
                GPS['GPSLatitudeRef'] = str(value)
            elif re.match('GPS GPSLongitudeRef', tag):
                GPS['GPSLongitudeRef'] = str(value)
            elif re.match('GPS GPSAltitudeRef', tag):
                GPS['GPSAltitudeRef'] = str(value)
            elif re.match('GPS GPSLatitude', tag):
                try:
                    match_result = re.match('\[(\w*),(\w*),(\w.*)/(\w.*)\]', str(value)).groups()
                    GPS['GPSLatitude'] = int(match_result[0]), int(match_result[1]), int(match_result[2])
                except:
                    deg, min, sec = [x.replace(' ', '') for x in str(value)[1:-1].split(',')]
                    GPS['GPSLatitude'] = latitude_and_longitude_convert_to_decimal_system(deg, min, sec)
            elif re.match('GPS GPSLongitude', tag):
                try:
                    match_result = re.match('\[(\w*),(\w*),(\w.*)/(\w.*)\]', str(value)).groups()
                    GPS['GPSLongitude'] = int(match_result[0]), int(match_result[1]), int(match_result[2])
                except:
                    deg, min, sec = [x.replace(' ', '') for x in str(value)[1:-1].split(',')]
                    GPS['GPSLongitude'] = latitude_and_longitude_convert_to_decimal_system(deg, min, sec)
            elif re.match('GPS GPSAltitude', tag):
                GPS['GPSAltitude'] = str(value)
            elif re.match('.*Date.*', tag):
                date = str(value)
    return {'GPS_information': GPS, 'date_information': date}

def find_address_from_GPS(GPS):
    """
    使用Geocoding API把经纬度坐标转换为结构化地址。
    :param GPS:
    :return:
    """
    secret_key = 'zbLsuDDL4CS2U0M4KezOZZbGUY9iWtVf'
    # secret_key = 'CNzed0LQ2W5PW2l0MQb9OFhfSjj9AfB'
    secret_key = 'W4OlhqOeAApYO7ND06mCrGXU6jYzbGYf'
    secret_key = 'FHTnGWf8sHpGAkvGvH0LNz4DaHisoMBt'
    secret_key = '20ad830c09ac8241c085063b1f6d67ec'#GAODE
    if not GPS['GPS_information']:
        return '该照片无GPS信息'
    lat, lng = GPS['GPS_information']['GPSLatitude'], GPS['GPS_information']['GPSLongitude']
    # https://restapi.amap.com/v3/geocode/regeo?parameters
    baidu_map_api = "https://restapi.amap.com/v3/geocode/regeo?key={0}&location={2},{1}&poitype=&radius=1000&extensions=base&batch=false&roadlevel=0".format(
        secret_key, lat, lng)
    # baidu_map_api = "https://api.map.baidu.com/geocoder/v2/?ak={0}&callback=renderReverse&location={1},{2}s&output=json&pois=0".format(
    #     secret_key, lat, lng)
    print(baidu_map_api)
    response = requests.get(baidu_map_api)
    # print('Response',response)
    content = response.text.replace("renderReverse&&renderReverse(", "")[:-1]
    # print(content)
    baidu_map_address = json.loads(content)
    formatted_address = baidu_map_address["regeocode"]["formatted_address"]
    province = baidu_map_address["regeocode"]["addressComponent"]["province"]
    city = baidu_map_address["regeocode"]["addressComponent"]["city"]
    district = baidu_map_address["regeocode"]["addressComponent"]["district"]
    return formatted_address,province,city,district

def getPEF():
    print("Get pic fileName")
    path = os.getcwd()  # 文件夹目录
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    print(files)
    # print(type(files))
    PEFList = []
    for name in files:
        if (".PEF" in name):
            PEFList.append(name)
            # print(name)
        # while("PEF" not in name):
        #     pass

    # print(PEFList)
    return PEFList

###backup
# def getPEF(path):
#     print("Get pic fileName")
#     # path = os.getcwd()  # 文件夹目录
#     # print(path)
#     files = os.listdir(path)  # 得到文件夹下的所有文件名称
#     print(files)
#     # print(type(files))
#     PEFList = []
#     for name in files:
#         if (".PEF" in name):
#             PEFList.append(name)
#             # print(name)
#         # while("PEF" not in name):
#         #     pass
#
#     # print(PEFList)
#     return PEFList



def getPEF(path):
    print("Get pic fileName")
    # path = os.getcwd()  # 文件夹目录
    # print(path)
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    # print(files)
    # print(type(files))
    PEFList = []

    for name in files:
        if os.path.isdir(path +name):
            # print(path +name)
            PEFList.extend(getPEF(path +name+'/')) #回调函数，对所有子文件夹进行搜索
        elif os.path.isfile(path +name):
            if (".PEF" in name):
                PEFList.append(name)
                # print(name)
            # while("PEF" not in name):
            #     pass
        else:
            print("未知文件 %s",name)

    print(PEFList)
    return PEFList


def getPic(path,format):
    print("Get pic fileName")
    # path = os.getcwd()  # 文件夹目录
    print(path)
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    # print(files)
    # print(type(files))
    PEFList = []

    for name in files:
        if os.path.isdir(path +'/'+name):
            # print(path +name)
            PEFList.extend(getPic(path +'/'+name+'/',format)) #回调函数，对所有子文件夹进行搜索
        elif os.path.isfile(path +'/'+name):
            # print(type(format))
            # print(type(name))
            if (format.lower() in name.lower()):
                PEFList.append(name)
                # print(PEFList)
            # while("PEF" not in name):
            #     pass
        else:
            print("未知文件:%s",name)

    # print(PEFList)
    return PEFList

def getGPSInfo(PEFList):
    print("Get pic GPS info")
    GPSInfo=[]

    for pef in PEFList:
        PEFInfo = []
        GPS_info = find_GPS_image(pic_path=pef)
        # print(GPS_info)
        if(GPS_info['GPS_information']):
            print(GPS_info['GPS_information'])
            PEFInfo.append(GPS_info['GPS_information']['GPSLatitude'])
            PEFInfo.append(GPS_info['GPS_information']['GPSLongitude'])
            PEFInfo.append(GPS_info['GPS_information']['GPSAltitude'])
            GPSInfo.append(PEFInfo)
        else:
            pass
        # print(PEFInfo)

        # print(GPS_info)
        # lat, lon = GPS_info['GPS_information']['GPSLatitude'], GPS_info['GPS_information']['GPSLongitude']
    return GPSInfo

def getGPSInfo(path,PEFList):
    print("Get pic GPS info")
    GPSInfo=[]
    path=path+'/'
    for pef in PEFList:
        PEFInfo = []
        # print(path+pef)
        GPS_info = find_GPS_image(pic_path=path+pef)
        # print(GPS_info)
        if(GPS_info['GPS_information']):
            # print(GPS_info['GPS_information'])
            PEFInfo.append(GPS_info['GPS_information']['GPSLatitude'])
            PEFInfo.append(GPS_info['GPS_information']['GPSLongitude'])
            PEFInfo.append(GPS_info['GPS_information']['GPSAltitude'])
            PEFInfo.append(pef)
            GPSInfo.append(PEFInfo)
        else:
            pass
        # print(PEFInfo)

        # print(GPS_info)
        # lat, lon = GPS_info['GPS_information']['GPSLatitude'], GPS_info['GPS_information']['GPSLongitude']
    return GPSInfo
'''
var markerArr = [
    {title: "名称：广州火车站", point: "113.264531,23.157003"},
    {title: "名称：广州塔（赤岗塔）", point: "113.330934,23.113401"},
    {title: "名称：广州动物园", point: "113.312213,23.147267"},
    {title: "名称：天河公园", point: "113.372867,23.134274"}

];
'''
def buildGPSArry(gpsInfo):
    '''Format is {title: "名称：天河公园", point: "113.94930470452066,2.434274"}'''
    print("trans to arr")
    main='var markerArr = ['
    for gps in gpsInfo:
        lon,lat=wgs2gcj(gps[1],gps[0])


        # info = '{title: "名称：{0}", point: "{1},{2}"},'.format('nill', gps[1], gps[2])
        info='{title: "相片：'+gps[3]+'", point: "'+str(lon)+','+str(lat)+'"},'
        main=main+info
    main=main[:-1]+'];'
    return main
    # print(main)

# st='123'
# print(st.join("hahah"))
# pef=getPEF()
# print(getGPSInfo(pef))
# gps=getGPSInfo(pef)
# print(gps)
# arr=buildGPSArry(gps)
# print(arr)
# html=html.mapsFrame
# html=html.replace("var markerArr = [];",arr)
# print(html)
# print(type(html))

# print(getPEF("/Users/aria/PycharmProjects/PhotoMap/scr/"))