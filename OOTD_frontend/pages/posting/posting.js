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
  deleteImage:function(e){
    const index = e.currentTarget.dataset.id;
    this.data.images.splice(index,1);
    this.setData({
      images:this.data.images
    })
  }
})