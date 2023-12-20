const app = getApp()
Page({
  data:{
    weatherCode:100,
    weatherChar:"晴",
    temprature:18,
    score:98,
    outfitItems: [
      {"name":"搭配1","category":1},
      {"name":"搭配2","category":2},
      {"name":"搭配3","category":3},
      {"name":"搭配4","category":4},],
    images:[
      "/static/default/noimage.png",
      "/static/default/noimage.png",
      "/static/default/noimage.png",
      "/static/default/noimage.png"
    ],
  },
  addImage:function(e){
    const that=this
    wx.chooseMedia({
      count:9-that.data.images.length,
      mediaType:['image'],
      sourceType:['album','camera'],
      sizeType:['original','compressed'],
      camera:'back',
      success(res){
        for(let i=0;i<res.tempFiles.length;i++)
          that.data.images.push(res.tempFiles[i].tempFilePath)
        that.setData({
          images:that.data.images
        })
      }
    })
  },
  onShow: function () {
    // 页面加载时的初始化操作，可以在这里处理数据加载等任务
    // console.log("页面加载完成");
    // console.log("nickname:",this.data.nickname);
    wx.request({
      method: 'GET',
      url: 'http://127.0.0.1:8000/api/user/weather',
      header: {
        'Authorization': app.globalData.jwt, // 添加 JWT Token
      },
      success: (res) => {
        if (res.statusCode === 200) {
          // 更新页面数据，显示用户信息
          this.setData({
            weatherChar: res.data.text,
            weatherCode: res.data.icon,
            temprature: res.data.temperature,
          }, () => {
            console.log('页面数据已更新');
          });
        } else {
          // 处理请求失败的情况
          console.error('Failed to request weather:', res.data);
        }
      },
      fail: (err) => {
        // 处理请求失败的情况
        console.error('Failed to request weather:', err);
      },
    });
  },
  deleteImage:function(e){
    const index = e.currentTarget.dataset.id;
    this.data.images.splice(index,1);
    this.setData({
      images:this.data.images
    })
  }
})