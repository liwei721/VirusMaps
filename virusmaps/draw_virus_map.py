"""
    @author: xuanke
    @time: 2020/2/16
    @function: 生成一个中国疫情地图
"""
import requests
import json
from pyecharts.charts import Map
from pyecharts import options as opts


def get_virus_data():
    """
    获取疫情数据
    :return:
    """
    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"}
    response = requests.get(url, headers=headers)
    response_data = json.loads(response.json()["data"])
    china_virus_list = response_data["areaTree"][0]["children"]
    china_virus_dict = {}
    for province_virus_data in china_virus_list:
        china_virus_dict[province_virus_data["name"]] = province_virus_data["total"]["confirm"]

    # 拼接地图中间的标题
    virus_map_title = "数据更新时间:{} 当前确诊人数:{} 疑似人数:{} 死亡人数:{} 治愈人数:{}".format(response_data["lastUpdateTime"],
                                                                           response_data["areaTree"][0]["total"]["confirm"],
                                                                           response_data["areaTree"][0]["total"]["suspect"],
                                                                           response_data["areaTree"][0]["total"]["dead"],
                                                                           response_data["areaTree"][0]["total"]["heal"],)
    return china_virus_dict, virus_map_title


def draw_virus_map(virus_data, virus_title):
    """
    绘制疫情地图
    :param virus_title:
    :param virus_data:
    :return:
    """
    virus_map = Map()
    virus_data_list = []
    """
     A = [1,2,3]
     B = [4,5,6]
     zip(A, B)
     (1,4),(2,5),(3,6)
    """
    virus_zip = zip(virus_data.keys(), virus_data.values())
    for z in virus_zip:
        print(z)
        virus_data_list.append(z)

    virus_map.add(virus_title, virus_data_list, "china")
    virus_map.set_global_opts(title_opts=opts.TitleOpts("中国疫情地图"),
                              visualmap_opts=opts.VisualMapOpts(split_number=6,is_piecewise=True,
                                                                pieces=[{"min": 1, "max": 9, "label": "1-9人",
                                                                         "color": "#ffefd7"},
                                                                        {"min": 10, "max": 99, "label": "10-99人",
                                                                         "color": "#ffd2a0"},
                                                                        {"min": 100, "max": 499, "label": "100-499人",
                                                                         "color": "#fe8664"},
                                                                        {"min": 500, "max": 999, "label": "500-999人",
                                                                         "color": "#e64b47"},
                                                                        {"min": 1000, "max": 9999,
                                                                         "label": "1000-9999人", "color": "#c91014"},
                                                                        {"min": 10000, "label": "10000人及以上",
                                                                         "color": "#9c0a0d"}]),
                              tooltip_opts=opts.TooltipOpts(formatter="{b}:{c}"))
    virus_map.render(path="疫情地图.html")


if __name__ == '__main__':
    china_virus_data = get_virus_data()
    draw_virus_map(china_virus_data[0], china_virus_data[1])
