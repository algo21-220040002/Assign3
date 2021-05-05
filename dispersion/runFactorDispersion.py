
import pandas as pd
import numpy as np
import pickle
from dispersion.FactorDispersion import FactorDispersion
import warnings
warnings.filterwarnings("ignore")

def save_obj(path:str,obj:dict, name:str):
    """
    :parameter
    :param obj:The dictionary.
    :param name:The name of the dictionary you want to store.
    """
    with open(path+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(path:str,
             name:str):
    """
    :parameter
    :param name:The name of dictionary.
    :return: The dictionary.
    """
    with open(path+ name + '.pkl', 'rb') as f:
        return pickle.load(f)
class runFactorDispersion:
    def __init__(self,
                 stock_pool:pd.DataFrame,
                 datelist:list,
                 factor:str,
                 path:str):
        """
        :parameter
        :param stock_pool:A dataframe that includes the stock id.
        :param datelist: The datelist.
        :param factor: The factor.
        :param path:The path that the price data stores.
        """
        self.stock_pool=stock_pool
        self.sector_list=list(set(stock_pool['申万行业']))
        self.datelist=datelist
        self.factor=factor
        self.path=path

    def run(self):
        """
        计算因子离散度并将数据保存
        """
        factor_dispersion = FactorDispersion(self.sector_list, self.datelist, self.factor, self.stock_pool, self.path)
        data1 = factor_dispersion.getFactorDispersion()
        data1.to_excel(r'./因子//' + self.factor + '//' + self.factor + '因子离散度.xlsx')
        data2 = factor_dispersion.getDispersionDetrend(data1)
        data2.to_excel(r'./因子//' + self.factor + '//' + self.factor + '因子离散度_detrend.xlsx')