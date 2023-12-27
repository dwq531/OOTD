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
    const that = this
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        wx.request({
          url: 'http://43.138.127.14:8000/api/user/login',
          method: 'PATCH',
          header: {
            'Content-Type': 'application/json' // 设置请求头为JSON格式
          },
          data: {
            code : res.code
          },
          success:function(res){
            console.log(res)
            // 如果请求成功
            if(res.statusCode === 200){
              console.log('后端返回: ',res.data);
              // TODO
              // 处理后端返回的数据
              const isNewUser = res.data.new;
              app.globalData.isNewUser = isNewUser;
              const jwt = res.data.jwt;
              app.globalData.jwt = jwt;
              const nickname = res.data.nickname;
              app.globalData.nickname = nickname;
              const age = res.data.age;
              app.globalData.age = age;
              const addr = res.data.addr;
              app.globalData.addr = addr;
              const gender = res.data.gender;
              app.globalData.gender = gender;
              const phone = res.data.phone;
              app.globalData.phone = phone;
              const intro = res.data.intro;
              app.globalData.intro = intro;
              const avatarUrl = res.data.avatarUrl;
              app.globalData.avatarUrl = avatarUrl;
              const updated = res.data.updated;
              app.globalData.updated = updated;
              app.globalData.login = true;
              if(!isNewUser)
              {
                 wx.switchTab({
                  url: '/pages/closet/closet'
                })
              }
              else
              {
                that.setData({
                  hasUserInfo:true
                })
              }
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
      },
      fail:function(res){
        console.log(res)
      }
    })
  },
  
})
