const app = getApp()
Page({
  data:{
    post:[]
  },
  onShow: function(e) {
    const that = this
    // Send a request to the backend to retrieve the post list
    wx.request({
      url: 'http://127.0.0.1:8000/api/posting/user_posts/all', 
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
  },
  showDetail:function(e){
    const index = e.currentTarget.dataset.index;
    wx.navigateTo({
      url:"/pages/postDetail/postDetail?"+"&index="+index,
    })
  }
})