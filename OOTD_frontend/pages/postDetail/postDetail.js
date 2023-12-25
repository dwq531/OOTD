const app = getApp()
Page({
  data:{
    id:0,
    post:{},
    comment:[{
      "user":{"nickname":"dwq","avatarUrl":"avatars/og4-U6m9DqAf90Ou_Kb9HEkkah-Q_avatar_qGl2VxU.jpg"},
      "content":"你好我好大家好askdjhaks jhdkashkdhaksjdhkashdkajsd hkahsdkjsh",
      "create_time":"2023-5-31"
    },
    {
      "user":{"nickname":"dwq","avatarUrl":"avatars/og4-U6m9DqAf90Ou_Kb9HEkkah-Q_avatar_qGl2VxU.jpg"},
      "content":"你好我好大家好",
      "create_time":"2023-5-31"
    }],
    favorite:[],
    like:[],
    is_liked:0,
    like_num:0,
    is_favorite:0,
    fav_num:0
  },
  onLoad: function (options) {
    this.setData({
      id:options.index
    })
  },
  onShow:function(e){
    const that = this
    wx.request({
      url: `http://127.0.0.1:8000/api/posting/post_detail/id=${that.data.id}`, 
      method: 'GET',
      header: {
        'Authorization': app.globalData.jwt,
        'Content-Type':'application/x-www-form-urlencoded',
      },
      success: function(res) {
        console.log(res.data); 
        const post = res.data.post
        for(let i=0;i<post.likes.length;i++)
        {
          if(post.likes[i]==post.user.id)
          {
            that.data.is_liked=true
            break
          }
        }
        for(let i=0;i<post.favorites.length;i++)
        {
          if(post.favorites[i]==post.user.id)
          {
            that.data.is_favorite=true
            break
          }
        }
        that.setData({
          post:res.data.post,
          comment:res.data.comments,
          like_num:res.data.post.likes.length,
          fav_num:res.data.post.favorites.length,
          is_liked:that.data.is_liked,
          is_favorite:that.data.is_favorite
        })
        
      }
    });
  },
  like: function(e) {
    const that = this;
    wx.request({
      url: `http://127.0.0.1:8000/api/posting/like_post/${that.data.id}/`, 
      method: 'POST',
      header: {
        'Authorization': app.globalData.jwt,
      },
      success: function(res) {
        if(res.statusCode==200)
        {
          if(that.data.is_liked)
            that.data.like_num--
          else
            that.data.like_num++
          that.setData({
            is_liked:!that.data.is_liked,
            like_num:that.data.like_num
          })
        }
        
      }
    });
    
  },
  favorite: function(e) {
    const that = this;
    wx.request({
      url: `http://127.0.0.1:8000/api/posting/favorite_post/${that.data.id}/`, 
      method: 'POST',
      header: {
        'Authorization': app.globalData.jwt,
      },
      success: function(res) {
        if(res.statusCode==200)
        {
          if(that.data.is_favorite)
            that.data.fav_num--
          else
            that.data.fav_num++
          that.setData({
            is_favorite:!that.data.is_favorite,
            fav_num:that.data.fav_num
          })
        }
        
      }
    });
  },
  comment:function(e){
    const that = this
    const formData = e.detail.value
    console.log(formData)
    wx.request({
      url: `http://127.0.0.1:8000/api/posting/comment_post/${that.data.id}/`, 
      method: 'POST',
      header: {
        'Authorization': app.globalData.jwt,
        'Content-Type':'application/x-www-form-urlencoded',
      },
      data:formData,
      success: function(res) {
        console.log(res); 
        if(res.statusCode==201)
        {
          wx.showModal({
            title: '评论发送成功',
            content: '发送评论:'+formData.content,
          })
        }
      }
    });
  }
})