
import pandas as pd
import numpy as np
import pickle
from dispersion.FactorDispersion import FactorDispersion
from factorICIR.FactorICIR import FactorICIR

def load_obj(path:str,
             name:str):
    """
    :parameter
    :param name:The name of dictionary.
    :return: The dictionary.
    """
    with open(path+ name + '.pkl', 'rb') as f:
        return pickle.load(f)

class runFactorICIR:
    def __init__(self,
                 factor:str,
                 datelist:list,
                 path:str,
                 dic_data:dict,
                 num:int):
        """
        :parameter
        :param factor:The factor.
        :param datelist:The datelist.
        :param path:The path of the price data stores.
        :param dic_data:The data of the neutralized factor.
        :param num: The number of months you want to calculate the ICIR.
        """
        self.factor=factor
        self.datelist=datelist
        self.path=path
        self.dic_data=dic_data
        self.num=num

    def run(self):
        """
        计算因子未来几个月的ICIR，并将数据保存
        """
        factorICIR = FactorICIR(self.num, self.datelist, self.path, self.dic_data, self.factor)
        data2 = factorICIR.getICIR()
        data2.to_excel(r'./因子//' + self.factor + '//' + self.factor + '未来'+str(self.num)+'个月ICIR.xlsx')
