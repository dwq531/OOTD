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
          url: 'http://127.0.0.1:8000/api/user/login',
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
    userInfo: null
  }
})
