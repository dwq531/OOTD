// personalCenter.js
const app = getApp()

Page({
   //下拉框选择月份
   data: {
    avatarUrl:"",
    nickname:"",
    gender:"",
    age:"",
    addr:"",
    likes:"",
    following:"",
    posts:"",
    followers:"",
    period: ['最近一周', '最近一月', '最近一年'],
    selectedMonth: '时间选择',
    canvasWidth: 320,
    canvasHeight: 200,
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
  },
  
  onPickerChange: function (e) {
    const selectedMonthIndex = e.detail.value;
    const selectedMonth = this.data.months[selectedMonthIndex];
    this.setData({
      selectedMonth: selectedMonth
    });
  },
  editProfile:function(e){
    wx.navigateTo({
      url: '/pages/informationEditor/informationEditor',
    })
  },

  getWeeklyRatings: function(){
    wx.request({
      url: 'http://127.0.0.1:8000/api/clothes/ratings', // 替换为实际的API地址和用户ID
      method: 'GET',
      success: (res) => {
        if (res.statusCode === 200){
          // 处理数据，将日期和评分分别提取出来
          const dates = res.data.dates;
          const scores = res.data.ratings;

          // 绘制折线图
          this.drawLineChart(dates, scores);
        }
      },
      fail: (error) => {
        console.error('Failed to fetch ratings data:', error);
      }
    });
  },

  // 绘制折线图
  drawLineChart: function (dates, scores) {
    wx.createSelectorQuery()
    .select('#lineCanvas') // 在 WXML 中填入的 id
    .node(({ node: canvas }) => {
        const ctx = canvas.getContext('2d');
        
        // 设置坐标系原点
        const originX = 30;
        const originY = 180;

        // 计算横坐标和纵坐标的间隔
        const xGap = (this.data.canvasWidth - originX * 2) / (dates.length - 1);
        const yGap = (originY - 20) / (Math.max(...scores) - 0);

        // 绘制横坐标轴
        ctx.moveTo(originX, originY);
        ctx.lineTo(this.data.canvasWidth - originX, originY);
        ctx.stroke();

        // 绘制纵坐标轴
        ctx.moveTo(originX, originY);
        ctx.lineTo(originX, 20);
        ctx.stroke();

        // 绘制折线
        ctx.beginPath();
        ctx.moveTo(originX, originY - (scores[0] - 0) * yGap);
        for (let i = 1; i < dates.length; i++) {
          ctx.lineTo(originX + i * xGap, originY - (scores[i] - 0) * yGap);
        }
        ctx.stroke();
        ctx.closePath();

        // 绘制横坐标刻度
        for (let i = 0; i < dates.length; i++) {
          ctx.fillText(dates[i], originX + i * xGap - 10, originY + 20);
        }

        // 绘制纵坐标刻度
        for (let i = 0; i <= Math.max(...scores); i++) {
          ctx.fillText(i, originX - 25, originY - i * yGap + 5);
        }

        // 执行绘图操作
        ctx.draw();
    })
    .exec()
  },
});
