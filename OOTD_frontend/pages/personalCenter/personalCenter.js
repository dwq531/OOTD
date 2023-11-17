// personalCenter.js

Page({
  
  // 页面加载时执行的函数
  onLoad: function () {
    // 页面加载时的初始化操作，可以在这里处理数据加载等任务
    //console.log("页面加载完成");
  },

  //下拉框选择月份
  data: {
    months: ['1月', '2月', '3月', '4月', '5月', '6月'],
    selectedMonth: '月份',
  },

  onPickerChange: function (e) {
    const selectedMonthIndex = e.detail.value;
    const selectedMonth = this.data.months[selectedMonthIndex];
    this.setData({
      selectedMonth: selectedMonth
    });
  },

});
