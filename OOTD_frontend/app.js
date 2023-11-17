// app.js
App({
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        wx.request({
          url: 'http://127.0.0.1:8000/api/user/login/',
          method: 'PATCH',
          data: {
            code : res.code
          },
          success:function(res){
            // 如果请求成功
            if(res.statusCode === 200){
              console.log('后端返回: ',res.data);
              // TODO
              // 处理后端返回的数据
              const isNewUser = res.data.new;
              this.globalData.isNewUser = isNewUser;
              const jwt = res.data.jwt;
              this.globalData.jwt = jwt;
              const nickname = res.data.nickname;
              this.globalData.nickname = nickname;
              const age = res.data.age;
              this.globalData.age = age;
              const addr = res.data.addr;
              this.globalData.addr = adde;
              const gender = res.data.gender;
              this.globalData.gender = gender;
              const phone = res.data.phone;
              this.globalData.phone = phone;
              const intro = res.data.intro;
              this.globalData.intro = intro;
              const avatarUrl = res.data.avatarUrl;
              this.globalData.avatarUrl = avatarUrl;
              const updated = res.data.updated;
              this.globalData.updated = updated;
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
