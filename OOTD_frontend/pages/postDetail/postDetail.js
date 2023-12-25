const app = getApp()
Page({
  data:{
    id:0,
    post:{
      "title":"标题",
      "content":"内容111111asdlaskjdnasdkj naskcnkasncksncksnkjscnkajnsck ascjsjdhajhdshdjas asdasdasd dsad sdas dsd",
      "user":{"nickname":"dwq","avatarUrl":"avatars/og4-U6m9DqAf90Ou_Kb9HEkkah-Q_avatar_qGl2VxU.jpg"},
      "create_time":"2023-5-31",
      "rate":90,
      "weather":"晴",
      "temperature":"10",
      "images":[{
        "create_time": "2023-12-16T07:18:10.629618Z",
        "description": "",
        "id": 1,
        "image": "/media/post_images/3SEC9pXPt8wZd004092524c1e061e22223000959642e.jpg"},
        {
          "create_time": "2023-12-16T07:18:10.629618Z",
          "description": "",
          "id": 1,
          "image": "/media/post_images/61iMgVVBw2NV6e47dd2ac73dbf6bd2f2e17a5691fadd.jpg"}]
    },
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
    is_favorite:0
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
        console.log(res); 
        /*
        that.setData({
          post:res.data.post,
          favorite:res.data.favorite_form,
          comment:res.data.comment_form,
          like:res.data.like_form
        })
        */
      }
    });
  },
  like: function(e) {
    const that = this;
    // ？？？
    wx.request({
      url: `http://127.0.0.1:8000/api/posting/like_post/${that.data.id}/`, 
      method: 'POST',
      header: {
        'Authorization': app.globalData.jwt,
      },
      success: function(res) {
        console.log(res); 
        that.setData({
          is_liked:!that.data.is_liked
        })
      }
    });
    
  },
  favorite: function(e) {
    const that = this;
    wx.request({
      url: `http://127.0.0.1:8000/api/posting/like_post/${that.data.id}/`, 
      method: 'POST',
      header: {
        'Authorization': app.globalData.jwt,
      },
      success: function(res) {
        console.log(res); 
        that.setData({
          is_favorite:!that.data.is_favorite
        })
      }
    });
  },
  comment:function(e){
    const that = this
    const formData = e.detail.value
    console.log(formData)
    wx.request({
      url: `http://127.0.0.1:8000/api/posting/post_detail/id=${that.data.id}/`, 
      method: 'POST',
      header: {
        'Authorization': app.globalData.jwt,
        'Content-Type':'application/x-www-form-urlencoded',
      },
      data:formData,
      success: function(res) {
        console.log(res); 
      }
    });
  }
})