const app = getApp()
Page({
  data:{
    id:0,
    post:{},
    comment:[],
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
  getTime:function(timestr){
    const sendTime = new Date(timestr).getTime()
    const now = Date.now()
    const diff = now-sendTime
    const minute = 60 * 1000;
    const hour = 60 * minute;
    const day = 24 * hour;
    const week = 7 * day;
    const month = 30 * day;
    const year = 365 * day;

    if (diff < minute) {
      return '刚刚';
    } else if (diff < hour) {
      return Math.floor(diff / minute) + '分钟前';
    } else if (diff < day) {
      return Math.floor(diff / hour) + '小时前';
    } else if (diff < week) {
      return Math.floor(diff / day) + '天前';
    } else if (diff < month) {
      return Math.floor(diff / week) + '周前';
    } else if (diff < year) {
      return Math.floor(diff / month) + '月前';
    } else {
      return Math.floor(diff / year) + '年前';
    }
  },
  onShow:function(e){
    const that = this
    wx.request({
      url: `http://43.138.127.14:8000/api/posting/post_detail/id=${that.data.id}`, 
      method: 'GET',
      header: {
        'Authorization': app.globalData.jwt,
        'Content-Type':'application/x-www-form-urlencoded',
      },
      success: function(res) {
        console.log(res.data); 
        var post = res.data.post
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
        post.create_time = that.getTime(post.create_time)
        var comment = res.data.comments
        for(let i = 0;i<comment.length;i++)
          comment[i].create_time = that.getTime(comment[i].create_time)
        console.log(comment)
        that.setData({
          post:post,
          comment:comment,
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
      url: `http://43.138.127.14:8000/api/posting/like_post/${that.data.id}/`, 
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
      url: `http://43.138.127.14:8000/api/posting/favorite_post/${that.data.id}/`, 
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
      url: `http://43.138.127.14:8000/api/posting/comment_post/${that.data.id}/`, 
      method: 'POST',
      header: {
        'Authorization': app.globalData.jwt,
        'Content-Type':'application/x-www-form-urlencoded',
      },
      data:formData,
      success: function(res) {
        console.log(res.data.comment); 
        if(res.statusCode==200)
        {
          wx.showModal({
            title: '评论发送成功',
            content: '发送评论:'+formData.content,
          })
          res.data.comment.create_time = that.getTime(res.data.comment.create_time)
          that.data.comment.push(res.data.comment)
          that.setData({
            comment:that.data.comment
          })
        }
      }
    });
  }
})