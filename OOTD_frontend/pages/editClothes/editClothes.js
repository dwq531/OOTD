const app = getApp()
Page({
  data:{
    url:'',
    index:'',
    chosenCategory:"上衣",
    chosenDetail:"请选择",
    category: ["上衣","下装","鞋子","包","饰品"],
    detail:["T恤","衬衫","卫衣","毛衣","吊带","POLO衫","连衣裙","风衣","马甲","夹克","皮衣","冲锋衣","防晒衣","羽绒服","正装外套","其他"],
    imgPath:''
  },
  onLoad: function (options) {
    this.setData({
      url:options.url,
      index:options.index
    })
  },
  categoryChange: function(e) {
    const type = this.data.category[e.detail.value]
    if(type == "上衣")
      this.data.detail = ["T恤","衬衫","卫衣","毛衣","吊带","POLO衫","连衣裙","风衣","马甲","夹克","皮衣","冲锋衣","防晒衣","羽绒服","正装外套","其他"]
    else if(type == "下装")
      this.data.detail = ["牛仔裤","裙裤","运动裤","背带裤","休闲裤","棉裤","正装裤","半身裙","其他"]
    else if(type == "鞋子")
      this.data.detail = ["运动鞋","凉鞋","板鞋","帆布鞋","靴子","其他"]
    else if(type == "包")
      this.data.detail = ["手提包","腰包","挎包","背包"]
    else if(type == "饰品")
      this.data.detail = ["项链","帽子","围巾","耳环","头饰"]
    this.setData({
      chosenCategory:type,
      detail:this.data.detail,
      chosenDetail:"请选择"
    })
  },
  detailChange:function(e){
    this.setData({
      chosenDetail:this.data.detail[e.detail.value]
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