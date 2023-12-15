const app = getApp()
Page({
  data:{
    url:'',
    index:'',
    chosenCategory:"上衣",
    chosenDetail:"T恤",
    category: ["上衣","下装","鞋子","包","饰品"],
    detail:["T恤","衬衫","卫衣","毛衣","吊带","POLO衫","连衣裙","风衣","马甲","夹克","皮衣","冲锋衣","防晒衣","羽绒服","正装外套","其他"],
    imgPath:'',
    name:'未命名衣服'
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
      chosenDetail:this.data.detail[0]
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
    const that=this
    wx.showModal({
      title: '删除衣服',
      content: '您确认要删除这件衣服吗？操作不可撤销！',
      complete: (res) => {
        if (res.confirm) {
          // 更新后端数据
          wx.request({
            url: 'http://127.0.0.1:8000/api/clothes/delete_clothes',
            header: {
              'Content-Type': 'application/json' ,
              'Authorization':app.globalData.jwt
            },
            data:{
              'id':this.data.index
            },
            success:function(res){
              let pages = getCurrentPages()
              let prepage = pages[pages.length - 2]
              let clothesToDelete = prepage.__data__.clothes.findIndex(c => c.id === that.data.index)
              prepage.data.clothes.splice(clothesToDelete,1)
              prepage.setData({
                clothes:prepage.data.clothes
              }) 
              wx.navigateBack({
                delta:1
              })
            }
          })
        }
      }
    })
  },
  saveClothes:function(e){
    const that = this
    if(this.data.imgPath=='')
    {
      wx.showModal({
        title: '参数错误',
        content: '您没有上传衣服图片',
      })
      return
    }
    // 更新后端
    if(this.data.index==-1)
    {
      wx.uploadFile({
        filePath: this.data.imgPath,
        name: 'file',
        url: 'http://127.0.0.1:8000/api/clothes/edit_clothes',
        header: {
          'Content-Type': 'application/json' ,
          'Authorization':app.globalData.jwt
        },
        formData:{
          'name':this.data.name,
          'Mtype':this.data.chosenCategory,  
          'Dtyoe':this.data.chosenDetail,  
        },
        success:function(res){
          let pages = getCurrentPages()
          let prepage = pages[pages.length - 2]
          const data = {
            'id': res.data.id,
            'name':that.data.name,
            'Mtype':that.data.chosenCategory,  
            'Dtyoe':that.data.chosenDetail,
            'pictureUrl':that.data.pictureUrl
          };
          prepage.data.clothes.push(data)
          prepage.setData({
            clothes:prepage.data.clothes
          })
          wx.navigateBack({
            delta:1,
          })
        }
      })
    }
    
  },
  nameChange:function(e){
    this.setData({
      name:e.detail.value
    })
  }
})