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
    months: ['1月', '2月', '3月', '4月', '5月', '6月'],
    selectedMonth: '月份',
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
    console.log("avatarUrl:",this.data.avatarUrl);
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
  }

});
