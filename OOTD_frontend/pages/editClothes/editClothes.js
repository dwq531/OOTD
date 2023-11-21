const app = getApp()
Page({
  data:{
    url:'',
    index:'',
    chosenCategory:"请选择",
    category: ["上衣","下装","连衣裙","外套","帽子","鞋子"],
    imgPath:''
  },
  onLoad: function (options) {
    this.setData({
      url:options.url,
      index:options.index
    })
  },
  pickerChange: function(e) {
    this.setData({
      chosenCategory:this.data.category[e.detail.value]
    })
  },
  uploadImg: function(e) {
    const that=this;
    wx.chooseMedia({
      count:1,
      mediaType:['image'],
      sourceType:['album','camera'],
      sizeType:['original','compressed'],
      camera:'back',
      success(res){
        that.setData({
          imgPath:res.tempFiles[0].tempFilePath
        })
      }
    })
  }
})