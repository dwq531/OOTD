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
  },
  deleteClothes:function(e){
    wx.showModal({
      title: '删除衣服',
      content: '您确认要删除这件衣服吗？操作不可撤销！',
      complete: (res) => {
        if (res.confirm) {
          // 更新后端数据
          wx.navigateBack({
            delta:1
          })
        }
      }
    })
  },
  saveClothes:function(e){
    // 更新后端
    wx.navigateBack({
      delta:1
    })
  }
})