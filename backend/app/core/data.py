import pandas as pd
import sys
from io import StringIO
import MeCab
from functools import lru_cache
from pyecharts.charts import Pie
from pyecharts import options as opts
from pyecharts.globals import CurrentConfig, NotebookType, WarningType

WarningType.ShowWarning = False
df = pd.read_excel('C:\\temp\日本都道府県一覧.xlsx')
JP_CITYS = df['略語'].values.tolist()

mecab = MeCab.Tagger("-Ochasen")


@lru_cache
def get_simple_city_name_by_mycab(city):
    global mecab, JP_CITYS
    city = city.replace('都', '').replace('府', '').replace('県', '')
    content = mecab.parse(city)
    table = pd.read_table(StringIO(content),
                          skipfooter=1,
                          header=None,
                          usecols=[0, 1, 2, 3],
                          engine='python')
    for index, row in table.iterrows():
        # print(row[0])
        if ('地域' in row[3]) and (row[0] in JP_CITYS):
            return row[0]
    return 'その他'


def getPie():
    merchant_data = pd.read_excel('C:\\temp\加盟店情報一覧_ALL_20200615183456.xlsx',
                                  usecols='A,B,C,D,I,J,O,Y,AI',
                                  dtype=str)
    merchant_data['都道府県修正'] = merchant_data['都道府県'].apply(
        get_simple_city_name_by_mycab)

    m_cnt = merchant_data[['都道府県修正', '加盟店ID']].groupby(
        '都道府県修正', as_index=False).count().sort_values(by='加盟店ID')

    c = (Pie().add(
        "", m_cnt[['都道府県修正', '加盟店ID']].values,
        center=["40%", "50%"]).set_global_opts(
            title_opts=opts.TitleOpts(title="都道府県"),
            legend_opts=opts.LegendOpts(
                pos_left="75%", orient="vertical")).set_series_opts(
                    label_opts=opts.LabelOpts(formatter="{b}:{d}%:{c}")))

    return c