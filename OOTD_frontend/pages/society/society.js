const app = getApp()
Page({
  data:{
    post:[]
  },
  onLoad: function(e) {
    const that = this
    // Send a request to the backend to retrieve the post list
    wx.request({
      url: 'http://127.0.0.1:8000/api/posting/user_posts/created', 
      method: 'GET',
      header: {
        'content-type': 'application/json',
        'Authorization': app.globalData.jwt
      },
      success: function(res) {
        console.log(res.data.posts); 
        that.setData({
          post:res.data.posts
        })
      }
    });
  }
})