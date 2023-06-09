import pandas as pd
form = []
for year in range(2022, 2024):
    if year == 2022:
        start_month = 1
        end_month = 13  # 包括 1 到 12 月
    else:
        year == 2023
        start_month = 1
        end_month = 4  # 包括 1 到 3 月
    for month in range(start_month,end_month):
        filename = f"C:/Users/eason/Desktop/檔案區/STOCK_DAY_2330_{year}{month:02}.csv"
        data = pd.read_csv(filename,encoding="big5")      #讀取 CSV 檔案
        data = data.reset_index()   #重新設置列索引   原本的列索引會全部變成欄位
        title = data.columns[-1]
        data = data.drop(columns=[title])  #刪除最後的欄位
        data.columns = data.loc[0,:]  #取代欄位名稱
        data = data.drop([0])
        data = data [ data["日期"].apply(lambda x : x.split("/")[0].isdigit())  ] #用邏輯陣列、匿名函式刪除文字
        data = data.drop(["成交金額","漲跌價差","成交筆數"],axis=1)
        data["成交股數"] = data["成交股數"].str.split(",").str.join("").astype(int)  #把字串改int，並且刪除數字中的,
        data[["開盤價","最高價","最低價","收盤價"]] = data[["開盤價","最高價","最低價","收盤價"]].astype(float)
        form.append(data)
sheet = pd.concat(form, ignore_index=True)
sheet.index = sheet['日期']
sheet = sheet.drop( [sheet.columns[0]], axis=1)  # 刪除指定行索引的資料行
import mpl_finance as mpf
import matplotlib.pyplot as plt
import talib
import numpy as np
sma_5 = talib.SMA(np.array(sheet['收盤價']), 5)
sma_20 = talib.SMA(np.array(sheet['收盤價']), 20)
sma_60 = talib.SMA(np.array(sheet['收盤價']), 60)
fig = plt.figure(figsize=(14, 6))
ax1 = fig.add_axes([0.05,0.35,0.9,0.6])
ax2 = fig.add_axes([0.05,0.06,0.9,0.25])
ax1.set_xticks([])
ax1.set_xticklabels([])
mpf.candlestick2_ochl(ax1, sheet['開盤價'], sheet['收盤價'], sheet['最高價'],sheet['最低價'],   #ochl要給左邊四個值
                      width=0.6, colorup='r', colordown='g', alpha=1)   #固定要給的值,因為是股市畫圖用
ax1.plot(sma_5, label='5日均線',alpha=1)
ax1.plot(sma_20, label='20日均線',alpha=1)
ax1.plot(sma_60, label='60日均線',alpha=1)
ax1.legend()
mpf.volume_overlay(ax2, sheet['開盤價'], sheet['收盤價'], sheet['成交股數'], colorup='r', colordown='g', width=0.5, alpha=1)
ax2.set_xticks(range(0, len(sheet.index), 30)) #set_xticks = 想要幾個小牙籤
ax2.set_xticklabels(sheet.index[::30])  #set_xticklabels = 設定小牙籤的label
plt.show()