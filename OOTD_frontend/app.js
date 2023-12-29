// app.js
App({
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    const that = this;

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
