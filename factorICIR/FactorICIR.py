
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

class FactorICIR:
    """FactorICIR
    This class is used to calculate the IC,IR and ICIR of the factor.
    """
    def __init__(self,
                 num:int,
                 datelist:list,
                 path:str,
                 dic_data:dict,
                 factor:str):
        """
        :parameter
        :param num: The num of months of ICIR.
        :param datelist:The date list.
        :param path:The path of the close data stores.
        :param dic_data:A dictionary whose key is timestamp and value is dataframe whose index is stock id and columns are factor
                        ,here the factor has been neutralized.
        :param factor:The factor you want to calculate.
        """
        self.num=num
        self.datelist=datelist
        self.path=path
        self.dic_data=dic_data
        self.factor=factor

    def getIC(self)->pd.DataFrame:
        """
        计算得到每个月的IC。
        :return: A dataframe whose index is date and columns are IC.
        """
        dic_close={}
        for stock_id in self.dic_data[self.datelist[0]].index:
            data=pd.read_excel(self.path+stock_id+'.xlsx',index_col=0)
            data=data.resample('M').last()
            data['nextMonthReturn']=data['close'].pct_change().shift(-1)
            dic_close[stock_id]=data

        df_IC=pd.DataFrame()
        for date in self.datelist[:-1]:  #除去最后一个月，该月的IC无法计算
            print(date)
            data=self.dic_data[date]
            data=data[[self.factor]]
            for stock_id in data.index:
                data.loc[stock_id,'nextMonthReturn']=dic_close[stock_id].loc[date,'nextMonthReturn']
            data=data.dropna()
            df_IC.loc[date,self.factor+'IC']=pearsonr(data[self.factor],data['nextMonthReturn'])[0]
        return df_IC

    def getICIR(self)->pd.DataFrame:
        """
        计算得到未来num月的ICIR
        :return: A dataframe whose index is date and columns are ICIR.
        """
        df_ICIR=pd.DataFrame()
        df_IC=FactorICIR.getIC(self)
        for i in range(len(df_IC.index)-self.num):
            date=df_IC.index[i]
            data=df_IC.loc[df_IC.index[i]:df_IC.index[i+self.num-1],:]
            df_ICIR.loc[date,self.factor+'next'+str(self.num)+'ICIR']=data[self.factor+'IC'].mean()/data[self.factor+'IC'].std()
            print(df_ICIR)
        return df_ICIR









