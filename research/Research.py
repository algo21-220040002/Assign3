
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
from scipy.stats.mstats import winsorize
from scipy.stats import pearsonr
from scipy.stats import spearmanr

class Research:
    def __init__(self,
                 factor:str):
        """
        :param factor: 因子名称
        """
        self.factor=factor


    def drawDispersion(self):
        """
        画出因子离散度的变化
        :return:
        """
        data1=pd.read_excel(r'.\因子\\'+self.factor+'//'+self.factor+'因子离散度.xlsx',index_col=0)
        data2 = pd.read_excel(r'.\因子\\' + self.factor + '//' + self.factor + '因子离散度_detrend.xlsx',index_col=0)
        fig = plt.figure(figsize=[15, 5])
        ax1 = fig.add_subplot(1, 2, 1)
        ax1.plot(data1.index, data1[self.factor], label=self.factor + '因子离散度')
        ax1.set_title(self.factor + '因子离散度')
        ax1.set_xlabel('时间')
        ax1.set_ylabel('离散度')
        ax1.legend()

        ax2 = fig.add_subplot(1, 2, 2)
        ax2.plot(data2.index, data2[self.factor], label=self.factor + 'detrend因子离散度')
        ax2.set_title(self.factor + 'detrend因子离散度')
        ax2.set_xlabel('时间')
        ax2.set_ylabel('detrend离散度')
        ax2.legend()
        plt.show()

    def drawlongshort_dispersion(self):
        """
        分别画出因子多空净值与因子离散度，因子未来12个月ICIR与因子离散度
        :return:
        """
        data = pd.read_excel(r'.\因子\\' + self.factor + "//" + self.factor + '_longshort_5layer.xlsx',index_col=0)
        data_dispersion = pd.read_excel(r'.\因子\\' + self.factor + '//' + self.factor + '因子离散度_detrend.xlsx',index_col=0)
        data = data.join(data_dispersion)
        data1 = data.dropna()
        fig = plt.figure(figsize=[10, 15])
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.plot(data1.index, data1['net value'], c='r', label=self.factor + '多空净值')
        ax1.set_ylabel('多空净值', fontsize=13)
        ax1.set_xlabel('时间', fontsize=13)
        ax1.legend(loc=2)
        ax1.grid()
        ax2 = ax1.twinx()
        ax2.bar(data1.index, data1[self.factor], 20, label='detrend离散度')
        ax2.set_ylabel('detrend离散度', fontsize=13)
        ax2.legend(loc=0)
        plt.title(self.factor + '因子表现与因子离散度')

        data_ICIR = pd.read_excel(r'.\因子\\'+self.factor+'//'+self.factor+'未来12个月ICIR.xlsx',index_col=0)
        data_dispersion = pd.read_excel(r'.\因子\\'+self.factor+'//'+self.factor+'因子离散度_detrend.xlsx',index_col=0)
        df = data_ICIR.join(data_dispersion)
        data2 = df.dropna()
        ax3 = fig.add_subplot(2, 1, 2)
        ax3.plot(data2[self.factor + 'next12ICIR'], c='r', label='未来12月ICIR')
        ax3.set_xlabel('时间', fontsize=13)
        ax3.set_ylabel('未来12个月ICIR', fontsize=13)
        ax3.legend(loc=2)
        ax3.grid()
        ax4 = ax3.twinx()
        ax4.bar(data2.index, data2[self.factor], 20, label='detrend离散度')
        ax4.set_ylabel('detrend离散度', fontsize=13)
        ax4.legend(loc=0)
        plt.title(self.factor + '未来12个月ICIR与因子离散度')
        plt.show()

    def get_scatter(self,num:int):
        """
        画出因子离散度与ICIR的散点图并进行回归
        :param num:用未来多少个月的ICIR
        :return:
        """
        data_dispersion = pd.read_excel(r'.\因子\\' + self.factor + '//' + self.factor + '因子离散度_detrend.xlsx',index_col=0)
        data_ICIR = pd.read_excel(r'.\因子\\' + self.factor + '//' + self.factor + '未来' + str(num) + '个月ICIR.xlsx', index_col=0)
        data = data_dispersion.join(data_ICIR)
        data = data.dropna()

        data[self.factor] = winsorize(data[self.factor], limits=[0.01, 0.01])
        data[self.factor + 'next' + str(num) + 'ICIR'] = winsorize(data[self.factor + 'next' + str(num) + 'ICIR'],
                                                              limits=[0.01, 0.01])
        print('数据个数', len(data))
        corr = pearsonr(data[self.factor], data[self.factor + 'next' + str(num) + 'ICIR'])[0]
        print('相关系数是', corr)
        rank_corr = spearmanr(data[self.factor], data[self.factor + 'next' + str(num) + 'ICIR'])[0]
        print('秩相关系数是', rank_corr)
        plt.figure(figsize=(10, 5))
        plt.scatter(data[self.factor], data[self.factor + 'next' + str(num) + 'ICIR'])
        plt.xlabel(self.factor+'因子离散度')
        plt.ylabel(self.factor+'因子未来'+str(num)+'个月ICIR')
        plt.title(self.factor+'因子未来'+str(num)+'个月ICIR与因子离散度')

        X_set=data[[self.factor]].values
        y_set=data[[self.factor + 'next' + str(num) + 'ICIR']].values
        model_ols = LinearRegression()
        model_ols.fit(X_set, y_set)
        y_pred = model_ols.predict(X_set)
        mse = mean_squared_error(y_set, y_pred)
        rsquare = r2_score(y_set, y_pred)
        print('MSE:' + str(mse) + '\n' + 'R square:' + str(rsquare))
        plt.show()

