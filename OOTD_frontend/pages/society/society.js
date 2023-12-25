const app = getApp()
Page({
  data:{
    post:[],
    left:[],
    right:[],
    menu_item:["全部","我的","收藏"],
    curIndex:0
  },
  // 把post列表拆分成两列瀑布流
  splitPost:function(post){
    var left=[],right=[]
    for(let i=0;i<post.length;i++)
    {
      if(i%2===0)
        left.push(post[i])
      else
        right.push(post[i])
    }
    this.setData({
      left:left,
      right:right
    })
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
        console.log(res.data)
        that.splitPost(res.data.posts)
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
  },
  changeMenu:function(e){
    const index = parseInt(e.currentTarget.dataset.index)
    const url_name = ['all','created','favorite']
    const that = this
    wx.request({
      url: 'http://127.0.0.1:8000/api/posting/user_posts/'+url_name[index], 
      method: 'GET',
      header: {
        'content-type': 'application/json',
        'Authorization': app.globalData.jwt
      },
      success: function(res) {
        console.log(res.data.posts)
        that.splitPost(res.data.posts) 
        that.setData({
          post:res.data.posts
        })
      }
    });
    this.setData({
      curIndex: index
  })
  }
})