// personalCenter.js
import * as echarts from '../../ec-canvas/echarts';
const app = getApp()

if (!app) {
  // 如果在测试环境下，手动模拟 getApp
  global.getApp = function() {
    return {};
  };
}

Page({
   //下拉框选择月份
   data: {
    ecLine: {},
    ecPie: {},
    avatarUrl:"",
    nickname:"",
    gender:"",
    age:"",
    addr:"",
    likes:"",
    following:"",
    posts:"",
    followers:"",
    period: ['最近一周', '最近两周', '最近一月'],
    selectedMonthIndex: 0,
    selectedMonth: '最近一周',
    scrolltop: 0,
    dates:[],
    scores:[],
    clothes_list:[],
    count_list:[],
  },
  getWeeklyRatings: function(){
    var that = this
    wx.request({
      url: 'http://127.0.0.1:8000/api/closet/get_score', // 替换为实际的API地址和用户ID
      method: 'GET',
      header: {
        'Content-Type': 'application/json' ,
        'Authorization':app.globalData.jwt
      },
      data:{
        index:that.data.selectedMonthIndex 
      },
      success: (res) => {
        if (res.statusCode === 200){
          this.setData({
            dates:res.data.dates,
            scores: res.data.ratings,
          })
        }
      },
      fail: (error) => {
        console.error('Failed to fetch ratings data:', error);
      }
    });
  },
  getFavoriteClothes:function(){
    var that = this
    wx.request({
      url: 'http://127.0.0.1:8000/api/closet/get_favorite_clothes',
      method: 'GET',
      header: {
        'Content-Type': 'application/json' ,
        'Authorization':app.globalData.jwt
      },
      data:{
        index:that.data.selectedMonthIndex 
      },
      success: (res) => {
        if (res.statusCode === 200){
          this.setData({
            clothes_list:res.data.clothes_list,
            count_list:res.data.count_list,
          })
        }
      },
      fail: (error) => {
        console.error('Failed to fetch clothes data:', error);
      }
    });
  },
  OnReady(){

  },
  // 页面加载时执行的函数
  onLoad: function () {
    // 页面加载时的初始化操作，可以在这里处理数据加载等任务
    //console.log("页面加载完成");
    //console.log("nickname:",this.data.nickname);
    wx.request({
      method: 'GET',
      url: 'http://127.0.0.1:8000/api/user/user',
      header: {
        'Authorization': app.globalData.jwt, // 添加 JWT Token
      },
      success: (res) => {
        if (res.statusCode === 200) {
          // 更新页面数据，显示用户信息
          this.setData({
            avatarUrl: res.data.avatarUrl,
            nickname:res.data.nickname,
            phone:res.data.phone,
            addr:res.data.addr,
            age:res.data.age,
            gender:res.data.gender,
            avatarUrl:res.data.avatarUrl,
            likes:res.data.likes,
            following:res.data.following,
            posts:res.data.posts,
            followers:res.data.followers,
          });
        } else {
          // 处理请求失败的情况
          console.error('Failed to get user info:', res.data);
        }
      },
      fail: (err) => {
        // 处理请求失败的情况
        console.error('Failed to request user info:', err);
      }
    });
    // console.log("avatarUrl:",this.data.avatarUrl);
    this.getWeeklyRatings();
    this.getFavoriteClothes();
    this.setData({
      'ecLine.onInit': this.initChart,
      'ecPie.onInit': this.initPieChart, // 添加饼状图的初始化方法
    });
  },
  initChart: function (canvas, width, height, dpr) {
    const LineChart = echarts.init(canvas, null, {
      width: width,
      height: height,
      devicePixelRatio: dpr // new
    });
    canvas.setChart(LineChart);
    LineChart.setOption(getLineOption(this.data.dates,this.data.scores));
    return LineChart;
  },
  initPieChart: function (canvas, width, height, dpr) {
    const PieChart = echarts.init(canvas, null, {
      width: width,
      height: height,
      devicePixelRatio: dpr // new
    });
    canvas.setChart(PieChart);
    PieChart.setOption(getPieOption(this.data.clothes_list,this.data.count_list));
    return PieChart;
  },
  onPageScroll: function (event){
    // 处理滚动事件，更新Canvas绘图位置
    const scrollTop = event.scrollTop;
    this.setData({
      scrolltop: scrollTop,
    });
  },
  onHide: function() {
    // 在页面离开时清理数据
    this.setData({
      // 重置数据为初始状态
      avatarUrl:"",
      nickname:"",
      gender:"",
      age:"",
      addr:"",
      likes:"",
      following:"",
      posts:"",
      followers:"",
    });
    //console.log("缓存已清理");
  },
  onShow: function () {
    // 页面加载时的初始化操作，可以在这里处理数据加载等任务
    //console.log("页面加载完成");
    //console.log("nickname:",this.data.nickname);
    wx.request({
      method: 'GET',
      url: 'http://127.0.0.1:8000/api/user/user',
      header: {
        'Authorization': app.globalData.jwt, // 添加 JWT Token
      },
      success: (res) => {
        if (res.statusCode === 200) {
          // 更新页面数据，显示用户信息
          this.setData({
            avatarUrl: res.data.avatarUrl,
            nickname: res.data.nickname,
            phone: res.data.phone,
            addr: res.data.addr,
            age: res.data.age,
            gender: res.data.gender,
            likes: res.data.likes,
            following: res.data.following,
            posts: res.data.posts,
            followers: res.data.followers,
          }, () => {
            console.log('页面数据已更新');
          });
        } else {
          // 处理请求失败的情况
          console.error('Failed to request user info:', res.data);
        }
      },
      fail: (err) => {
        // 处理请求失败的情况
        console.error('Failed to request user info:', err);
      },
    });
    this.getWeeklyRatings();
    this.getFavoriteClothes();
  },
  onPickerChange: function (e) {
    const selectedMonthIndex = e.detail && e.detail.value; // 添加安全性检查
    if (selectedMonthIndex !== undefined) {
      const selectedMonth = this.data.period[selectedMonthIndex];
      this.setData({
        selectedMonth: selectedMonth,
        selectedMonthIndex: selectedMonthIndex
      });
      this.getWeeklyRatings();
      this.getFavoriteClothes();
    } else {
      console.error("Invalid picker event:", e);
    }
  },
  
  editProfile:function(e){
    wx.navigateTo({
      url: '/pages/informationEditor/informationEditor',
    })
  },

});


function getLineOption(dates,scores){
  const option = {
    xAxis: {
      type: 'category', 
      data: dates,
    },
    yAxis: {
      type: 'value', 
    },
    series: [{
      data: scores,
      type: 'line',
      smooth:false,
    }]
  };
  
  return option;
};

function getPieOption(clothes_list,count_list){
  var option = {
    series: [{
      label: {
        normal: {
          fontSize: 18
        }
      },
      type: 'pie',
      center: ['50%', '50%'],
      radius: ['20%', '40%'],
      data: clothes_list.map((clothes, index) => ({
        value: count_list[index],
        name: clothes,
      })),
    }]
  };
  
  return option;
};
