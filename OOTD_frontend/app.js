// app.js
App({
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    const that = this;

    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        wx.request({
          url: 'http://127.0.0.1:8000/api/user/login',
          method: 'PATCH',
          header: {
            'Content-Type': 'application/json' // 设置请求头为JSON格式
          },
          data: {
            code : res.code
          },
          success:function(res){
            // 如果请求成功
            if(res.statusCode === 200){
              //console.log('后端返回: ',res.data);
              // TODO
              // 处理后端返回的数据
              const isNewUser = res.data.new;
              that.globalData.isNewUser = isNewUser;
              const jwt = res.data.jwt;
              that.globalData.jwt = jwt;
              const nickname = res.data.nickname;
              that.globalData.nickname = nickname;
              const age = res.data.age;
              that.globalData.age = age;
              const addr = res.data.addr;
              that.globalData.addr = addr;
              const gender = res.data.gender;
              that.globalData.gender = gender;
              const phone = res.data.phone;
              that.globalData.phone = phone;
              const intro = res.data.intro;
              that.globalData.intro = intro;
              const avatarUrl = res.data.avatarUrl;
              that.globalData.avatarUrl = avatarUrl;
              const updated = res.data.updated;
              that.globalData.updated = updated;
              that.globalData.login = true;
            }
            else{
              console.error('请求失败，错误状态码：', res.statusCode);
            }
          },
          fail:function(res){
            // 如果请求失败
            console.error('请求失败，无法连接到后端服务器');
          },
        })
      }
    })
  },
  globalData: {
    login:false,
    userInfo: null,
    isNewUser: true,
    jwt: null,
    nickname: null,
    age: null,
    addr: null,
    gender: null,
    phone: null,
    intro: null,
    avatarUrl: null,
    updated: null,
  }
})
