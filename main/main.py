
import pandas as pd
import numpy as np
from factorICIR.runFactorICIR import runFactorICIR
from dispersion.runFactorDispersion import runFactorDispersion
import pickle
from research.Research import Research

def main():
    factor='BP'
    datelist = pd.date_range(start='2005-01-31', end='2021-03-31', freq='M')
    path = r'..\data\close_data\\'

    #计算因子未来几个月的ICIR
    # with open(r'./因子//'+factor+'//'+'dic_neutral_'+factor+'.pkl', 'rb') as f:
    #     dic_data=pickle.load(f)
    # runfactorICIR=runFactorICIR(factor,datelist,path,dic_data,12)
    # runfactorICIR.run()

    #计算因子的离散度
    # path=r'..\data\factor_data\\'
    # stock_pool = pd.read_excel(r'..\data\stock_pool\stock_pool_申万行业.xlsx', index_col=0)[0:616]
    # runfactordispersion=runFactorDispersion(stock_pool,datelist,factor,path)
    # runfactordispersion.run()


    #研究因子离散度与多空净值、未来几个月的ICIR之间的关系
    research=Research(factor)
    research.drawDispersion()
    research.drawlongshort_dispersion()
    research.get_scatter(12)
if __name__=="__main__":

    main()