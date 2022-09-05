"""
什么值得买自动签到脚本
使用github actions 定时执行
@author : stark
"""
import requests,os
from sys import argv

import config
from utils.serverchan_push import push_to_wechat

class SMZDM_Bot(object):
    def __init__(self):
        self.session = requests.Session()
        # 添加 headers
        self.session.headers = config.DEFAULT_HEADERS

    def __json_check(self, msg):
        """
        对请求 盖乐世社区 返回的数据进行进行检查
        1.判断是否 json 形式
        """
        try:
            result = msg.json()
            print(result)
            return True
        except Exception as e:
            print(f'Error : {e}')            
            return False

    def load_cookie_str(self, cookies):
        """
        起一个什么值得买的，带cookie的session
        cookie 为浏览器复制来的字符串
        :param cookie: 登录过的社区网站 cookie
        """
        self.session.headers['acw_tc=2760821416623821425133377e3d81662f17975f137c9f5e7323fc2567c2c2; __ckguid=l5Wr8hJ7SukAvFxr32fR3; device_id=213070643316623821425242940152243188f0a03d456f96480eba2d74; homepage_sug=d; r_sort_type=score; _zdmA.vid=*; sajssdk_2015_cross_new_user=1; Hm_lvt_9b7ac3d38f30fe89ff0b8a0546904e58=1662382147; footer_floating_layer=0; ad_date=5; ad_json_feed={}; _uab_collina=166238215068701117207109; sensorsdata2015jssdkcross={"distinct_id":"1830db27dda8c-0dadf2a0b75d1c-26021d51-1327104-1830db27ddc3e","first_id":"","props":{"$latest_traffic_source_type":"直接流量","$latest_search_keyword":"未取到值_直接打开","$latest_referrer":""},"$device_id":"1830db27dda8c-0dadf2a0b75d1c-26021d51-1327104-1830db27ddc3e"}; sess=BA-1F6yE9lIw16Z9UJ/SD5qr57BypM8sgdiQ0zv3m0LV6uu3LMpgFNBIi351lIR9svnI7ZQ74lowfYfL1ebw8NjcWm5FGxzlG3d3zgQWehqHOFZJ39/aSVEp+BX; user=user:1791217803|1791217803; smzdm_id=1791217803; _zdmA.uid=ZDMA.HJ1R2rLpi.1662382188.2419200; Hm_lpvt_9b7ac3d38f30fe89ff0b8a0546904e58=1662382188; bannerCounter=[{"number":0,"surplus":1},{"number":0,"surplus":1},{"number":0,"surplus":1},{"number":0,"surplus":1},{"number":2,"surplus":1},{"number":0,"surplus":1}]; amvid=535c90496478b699efd434e26529208b; _zdmA.time=1662382471116.0.https://www.smzdm.com/; ssxmod_itna=Yq0EqAxRx+haGHYKmxj2tDu77e0=8NiqFrQDl2DWqeiODUxn4iaDTxowiDDqoVGalDhbAI3Ln7xPxdYiE0DfNLzRqpXwDU4i80nQD4xYD44GTDt4DTD34DYDixib0DivdDjxGPynXw5tDm4GWCwKDi4D+Cq=DmqG0DDtDiwdDKqGgCdrU8nPdLTwe10=DjqTD/8PWg26YT1azBdrr17iWiqGyRPGu0up/G2bDCotVRkibz3xYlEDYFrPrYixeBroem7DzW0+aY08sIDwo4ff3mD1zDD3KBh4s7iD; ssxmod_itna2=Yq0EqAxRx+haGHYKmxj2tDu77e0=8NiqF3D61+QQ0D0H4DQDLe/auQlEBbqn4wOgS=qAiee=S0prpYxfAAIxuDWTa7FUgMTQ86nWPqjO8I2uQ4h2YTPk0GXvrZq2GlAxHzidmqFNY8Bo0OYGQ8Qm0/A+tHQw3zffj8C2+gtuP4jfiH+b=znnR/UrRSjlKqX2Qle8tj/+uGGQoBKG5sA+dQVh3qgpbfAEtc0PTK/10GvOr8eKK=aLt=QuxhK02A70j/ii0Oi3juBC4hQu0UPbbzFgYhzhldF9pBaY32nAtsf3YGA+hvfHrzDIlhK++/FqTehWj+4Vr9zxUmmNjn27RDrAhGbrneFD+Olrn7+Ii7slxoL7eoKaQoV8W2QbdP7jI2Hi+VAmjmvmSap/KIUhY=Tz7wtT0l8phDEI/5k/xs7+RK4jF4Ceb1GcL8pP=+Y=4c+AtZAtMTzAmOvSp3kLFMj7nOXW1zLP68snoFvg5Y07d+VmOzUIOO2oD07jxDLxD2+hDD=='] = cookies    

    def checkin(self):
        """
        签到函数
        """
        url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        msg = self.session.get(url)
        if self.__json_check(msg):
            return msg.json()
        return msg.content




if __name__ == '__main__':
    sb = SMZDM_Bot()
    # sb.load_cookie_str(config.TEST_COOKIE)
    cookies = os.environ["COOKIES"]
    sb.load_cookie_str(cookies)
    res = sb.checkin()
    print(res)
    SERVERCHAN_SECRETKEY = os.environ["SERVERCHAN_SECRETKEY"]
    print('sc_key: ', SERVERCHAN_SECRETKEY)
    if isinstance(SERVERCHAN_SECRETKEY,str) and len(SERVERCHAN_SECRETKEY)>0:
        print('检测到 SCKEY， 准备推送')
        push_to_wechat(text = '什么值得买每日签到',
                        desp = str(res),
                        secretKey = SERVERCHAN_SECRETKEY)
    print('代码完毕')
