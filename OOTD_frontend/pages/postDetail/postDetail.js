const app = getApp()
Page({
  data:{
    id:0,
    post:{
      "title":"标题",
      "content":"内容111111",
      "user":{"nickname":"dwq","avatarUrl":"/static/default/noimage.png"},
      "create_time":"2023-5-31",
      "rate":90,
      "weather":"晴",
      "images":[{
        "create_time": "2023-12-16T07:18:10.629618Z",
        "description": "",
        "id": 1,
        "image": "/media/post_images/4IntEXqP2IBH1baebcfc930de208e19e650eed453fc3.jpg"},
        {
          "create_time": "2023-12-16T07:18:10.629618Z",
          "description": "",
          "id": 1,
          "image": "/media/post_images/4IntEXqP2IBH1baebcfc930de208e19e650eed453fc3.jpg"}]
    },
    comment:[{
      "user":{"nickname":"dwq","avatarUrl":"/static/default/noimage.png"},
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
  }
})