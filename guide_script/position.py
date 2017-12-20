#coding:utf-8
import re
import urllib2
from bs4 import  BeautifulSoup
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class MFW:

    def __init__(self,city):
        self.siteURL = 'url'
        self.city = country
        # self.cityDict = {'曼谷': '11045_518', '清迈': '15284_179', '普吉岛': '11047_858', '苏梅': '14210_686', '芭堤雅': '11046_940'}

        # self.id = self.cityDict[self.city]
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
        self.headers = { 'User-Agent' :self.user_agent}

    #获得景点链接
    def getSightHref(self,pageid):
        url = "/search/s.php?q="+self.city+"&p=" +str(pageid)+ "&t=poi&kt=1"
        page = self.getDetailPage(url)
        soup = BeautifulSoup(page,'html.parser')
        SightHref = []
        SightLists =  soup.find(name="div",attrs={'data-category':'poi'}).ul
        SightHrefList = SightLists.find_all("h3")
        for SightHrefs in SightHrefList:
            SightWebsite = SightHrefs.a['href']
            SightHrefShort = str(SightWebsite).replace('http://www.mafengwo.cn','')
            SightHref.append(SightHrefShort)
        return SightHref

    #获得景点名称
    def getSightName(self,pageid):
        url = "/search/s.php?q="+self.city+"&p=" +str(pageid)+ "&t=poi&kt=1"
        page = self.getDetailPage(url)
        soup = BeautifulSoup(page,'html.parser')
        sightName = []
        sightLists =  soup.find(name="div",attrs={'data-category':'poi'}).ul
        SightHrefList = sightLists.find_all("h3")
        for SightHrefs in SightHrefList:
            SightWebsite = SightHrefs.a['href']
            SightHrefShort = str(SightWebsite).replace('http://www.mafengwo.cn','')
            SightHref.append(SightHrefShort)
        return sightName

    #获得下级WEB页面HTML
    def getDetailPage(self,detailURL):
        try:
            shopURL = self.siteURL + detailURL
            response = urllib2.urlopen(shopURL)
            detailPage = response.read()
            detailPageCode = re.sub(r'<br[ ]?/?>', '\n', detailPage)
            return detailPageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None

   #获得页面HTML
    def getPage(self):
        try:
            url = self.siteURL+"/baike/"+str(self.id)+".html"
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            page = response.read()
            pageCode = re.sub(r'<br[ ]?/?>', '\n', page)
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None

    # 交通（traffic）如何到达
    def getSightInfo(self,page):
        
        itemName=['名字' , '概况' , '电话' , '地址' , '网址', '门票' , '开放时间' ,'交通']
        sightInfoList = ['' for x in range(0, len(itemName))]
        soup = BeautifulSoup(page, 'html.parser')
        
        # 名字
        nameAttr = soup.find("div", class_="title")
        sightInfoList[0] = nameAttr.h1.string

        # 位置
        position = soup.find('div',class_='mod mod-location')
        lab_posi = position.find('div',class_='mhd')
        sightInfoList[3] = lab_posi.p.string
       
        # 简介
        detail = soup.find("div", class_="mod mod-detail")
        if detail != None:
            sightInfoList[1] = detail.find('div',class_='summary').string.strip()
        else :
            sightInfoList[1] = '暂无简介'
        
        # 电话
        lab_tel = detail.find('li',class_='tel')
        if lab_tel == None:
            sightInfoList[2] = ''
        else:
            sightInfoList[2] = lab_tel.find('div',class_='content').string.strip()

        # 网址
        lab_site = detail.find('li',class_='item-site')
        if lab_site == None:
            sightInfoList[4] ='没有网址'
        else :
            sightInfoList[4] = lab_site.find('div',class_='content').a['href']

        # 路线
        lab_traffic = detail.find_all('dl')
        if lab_traffic == None:
            sightInfoList[7] = ''
        else :
            # 取出所有标签的名字。对比我们预设好的名字，如果一致的话，就把他写进去
           for tag in lab_traffic:
                tag1 = self.textUtil(tag,'dt')
                if tag1 == itemName[7]:
                    sightInfoList[7] = self.textUtil(tag,'dd')
                elif tag1 == itemName[6]:
                    sightInfoList[6] = self.textUtil(tag,'dd')
                elif tag1 == itemName[5]:
                    if self.isEmpty(tag,'div'):
                         sightInfoList[5] = '暂无信息'
                    else:
                         sightInfoList[5] = self.textUtil(tag,'div')
            
        return sightInfoList
                
    
    # 对象找不到的尴尬
    def textUtil(self,obj,name):
        if self.isEmpty(obj,name):
            return '暂无信息'
        return obj.find(name).string.strip()

    # 对象为空判断
    def isEmpty(self,obj,name):
        if obj is None or obj.find(name) is None:
            return True
        return False

    #判断是否存在信息列表
    def hasAttr(self,page,list):
        soup = BeautifulSoup(page, 'html.parser')
        col = soup.find("div", class_="col-main").find("div", class_="bd")
        str_col = str(col)
        if list in str_col:
            return True
        else:
            return False


    #抓取景点信息
    def saveSight(self):
        f = open(r'pos.txt','w')
        sightHrefList = self.getSightHref(2)
        print len(sightHrefList)
        for sightHref in sightHrefList:
            try:
                page = self.getDetailPage(sightHref)

                dict = {}.fromkeys(('sightName','brief','telephone','location', 'website', 'ticket', 'openTime','traffic'))
                
                infos = self.getSightInfo(page)
                dict['sightName'] = infos[0]
                dict['brief'] = infos[1]
                dict['telephone'] = infos[2]
                dict['location'] = infos[3]
                dict['website'] = infos[4]
                dict['ticket'] = infos[5]
                dict['openTime'] = infos[6]
                dict['traffic'] = infos[7]

                f.write(json.dumps(dict,indent=1).decode("unicode_escape")+'\n')
                # print json.dumps(dict,indent=1).decode("unicode_escape")
                # print '==============='

            except AttributeError,e:
                continue
            
        f.close
        

country = '德国'
mfw = MFW(country)
mfw.saveSight()


