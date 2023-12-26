// index.js
// 获取应用实例
const app = getApp()

Page({
  data: {
    // motto: '点击头像立即登录',
    userInfo: {},
    hasUserInfo: !app.globalData.isNewUser,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    canIUseGetUserProfile: false,
    // canIUseOpenData: wx.canIUse('open-data.type.userAvatarUrl') && wx.canIUse('open-data.type.userNickName') // 如需尝试获取用户信息可改为false
    canIUseOpenData: false,
  },
  // 事件处理函数
  bindViewTap() {
    wx.switchTab({
      url: '/pages/closet/closet'
    })
  },
  onLoad() {
    if (wx.getUserProfile) {
      this.setData({
        canIUseGetUserProfile: true,
        // 更新 hasUserInfo 的值为全局数据中的 isNewUser
        hasUserInfo: !app.globalData.isNewUser,
      })
    }
  },
  getUserProfile(e) {
    if(!app.globalData.login)
    {
      return;
    }
    else if( app.globalData.isNewUser)
    {// 推荐使用wx.getUserProfile获取用户信息，开发者每次通过该接口获取用户个人信息均需用户确认，开发者妥善保管用户快速填写的头像昵称，避免重复弹窗
      wx.getUserProfile({
        desc: '展示用户信息', // 声明获取用户个人信息后的用途，后续会展示在弹窗中，请谨慎填写
        success: (res) => {
          app.globalData.nickname = res.userInfo.nickName
          app.globalData.avatarUrl = res.userInfo.avatarUrl
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true,
            canIUseOpenData: wx.canIUse('open-data.type.userAvatarUrl') && wx.canIUse('open-data.type.userNickName'),
          })
          wx.request({
            url: 'http://43.138.127.14:8000/api/user/edit_info',
            method: 'PATCH',
            header: {
              'Authorization':app.globalData.jwt,
              'Content-Type': 'application/json' // 设置请求头为JSON格式
            },
            data: {
              'avatarUrl' : app.globalData.avatarUrl,
              'nickname':app.globalData.nickname
            },
            success:(res)=>{
              app.globalData.avatarUrl = res.data.avatarUrl
            }
          })
          wx.switchTab({
            url: '/pages/closet/closet'
          })
        }
      })
    }
    else
    {
      wx.switchTab({
        url: '/pages/closet/closet'
      })
    }
  },
  getUserInfo(e) {
    // 不推荐使用getUserInfo获取用户信息，预计自2021年4月13日起，getUserInfo将不再弹出弹窗，并直接返回匿名的用户个人信息
    console.log(e)
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true,
      canIUseOpenData: wx.canIUse('open-data.type.userAvatarUrl') && wx.canIUse('open-data.type.userNickName'),
    })
    wx.navigateTo({
      url: '../logs/logs'
    })
  }
})
