
import pandas as pd
import numpy as np
import datetime
from scipy.stats.mstats import winsorize

class FactorDispersion:
    """FactorDispersion
    It's used to read the factor's data and then send them to the strategy just like Wind as a data vendor.
    """
    def __init__(self,
                 sector_list:list,
                 date_list:list,
                 factor:str,
                 stock_pool:pd.DataFrame,
                 path:str):
        """
        :parameter
        :param sector_list:A list includes the sector name.
        :param date_list:A list of the datetime.
        :param stock_pool:A dataframe whose index is a range and columns are ['stock_id','company_name','所属wind行业指数代码','所属wind行业名称']
        :param path:The path of the factor data stores.
        """
        self.sector_list=sector_list
        self.date_list=date_list
        self.factor=factor
        self.stock_pool=stock_pool
        self.path=path

    def dataPreprocessor(self)->dict:
        """
        提前对数据进行整理，将数据分行业整理。
        :return: A distionary whose key is sector name and value is another dictionary whose key is datetime and value is
                 a dataframe whose index is the factor and columns are the company,and it stores the value of factor.
        """

        dic_sector={}
        for sector in self.sector_list:
            sector_stock=self.stock_pool[self.stock_pool["申万行业"]==sector] #找到属于该行业的部分
            dic_sector[sector]={}
            for date in self.date_list:
                dic_sector[sector][date]=pd.DataFrame(index=[self.factor])

        for sector in self.sector_list:
            sector_stock=self.stock_pool[self.stock_pool["申万行业"]==sector] #找到属于该行业的部分
            for i in sector_stock.index:  #找到该行业中的所有股票
                stock_id=sector_stock.loc[i,'stock_id']
                factor_data=pd.read_excel(self.path+stock_id+".xlsx",index_col=0) #读取该股票的因子信息
                for date in self.date_list:
                    dic_sector[sector][date].loc[self.factor,stock_id]=factor_data.loc[date,self.factor].T
        return dic_sector

    def getSectorFactorDiff(self)->dict:
        """
        计算出各行业的因子离散度，并按日期整合到一起。
        :return: A dictionary whose key is sector and value is a dataframe whose index is datetime and columns are the factors
                 and in the dataframe it's the diff of the 0.75 quntile and 0.25 quntile.
        """
        dic_sector=FactorDispersion.dataPreprocessor(self)
        dic_factor_diff={}
        for sector in dic_sector.keys():
            dic_factor_diff[sector]=pd.DataFrame()

        for sector in dic_sector.keys():
            for date in dic_sector[sector].keys():
                data=dic_sector[sector][date]
                df=data.T[[self.factor]].dropna()
                diff=df[self.factor].quantile(q=0.9) - df[self.factor].quantile(q=0.1)
                dic_factor_diff[sector].loc[date,self.factor]=diff
        return dic_factor_diff

    def getFactorDispersion(self)->pd.DataFrame:
        """
        将各行业的的因子离散度进行加总，得到整体的因子离散度。
        :parameter
        :return: A dataframe whose index is the datetime and columns are the factors and it's the factor dispersion.
        """
        # dic_standard=FactorDispersion.getSectorFactorDiffStandardization(self,n)
        dic=FactorDispersion.getSectorFactorDiff(self)
        data=pd.DataFrame(index=self.date_list,columns=[self.factor])
        data=data.fillna(value=0)
        for sector in dic.keys():
            data+=dic[sector]
        data=data/len(dic.keys())
        return data

    def getDispersionDetrend(self,data:pd.DataFrame):
        """
        :param data: 即getFactorDispersion得到的data。
        :return:
        """
        data[self.factor] = (data[self.factor] - data[self.factor].shift(4)) / data[self.factor].shift(4)
        return data

    def getFactorDispersionStandard(self,n:int,data:pd.DataFrame):
        """
        将汇总得到的因子离散度进行标准化，进而可以与其他因子进行比较。
        :param data:getDispersionDetrend得到的data
        :param n: The number of months you will use to do the standardization.
        :return: A dataframe whose index is datetime and columns are factor.
        """
        data=(data-data.rolling(n).mean()) / data.rolling(n).std()
        return data
























