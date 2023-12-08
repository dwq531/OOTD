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
    title:'',
    content:''
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
  deleteImage:function(e){
    const index = e.currentTarget.dataset.id;
    this.data.images.splice(index,1);
    this.setData({
      images:this.data.images
    })
  },
  titleChange:function(e){
    this.setData({
      title:e.detail.value
    })
  },
  contentChange:function(e){
    this.setData({
      content:e.detail.value
    })
  },
  send:function(e){

    console.log('posting')
    /*
    wx.request({
      url: 'http://127.0.0.1:8000/api/posting/create_post/',
      method:'GET',
      header: {
        'Authorization':app.globalData.jwt,
        'Content-Type': 'application/json' // 设置请求头为JSON格式
      },
      success:function(res){
        console.log(res)
      }
    })
    */

    wx.uploadFile({
      filePath: this.data.images[0],
      name: 'images',
      url: 'http://127.0.0.1:8000/api/posting/create_post/',
      header: {
        'Authorization':app.globalData.jwt,
        'Content-Type': 'application/json' // 设置请求头为JSON格式
      },
      formData:{
        'title':this.data.title,
        'content':this.data.content,
      },
      success:function(res){
        console.log(res)
      }
      
    })
  }
})
