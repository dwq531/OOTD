const app = getApp()
Page({
  data:{
    url:'',
    chosenCategory:"上衣",
    chosenDetail:"T恤",
    category: ["上衣","下装","鞋子","包","饰品"],
    detail:["T恤","衬衫","卫衣","毛衣","吊带","POLO衫","连衣裙","风衣","马甲","夹克","皮衣","冲锋衣","防晒衣","羽绒服","正装外套","其他"],
    imgPath:'',
    imgChange:false,
    name:'未命名衣服',
    add:0,
  },
  onLoad: function (options) {
    var url = JSON.parse(options.url)
    //console.log(url)
    const type = url.Mtype
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
    if(url)
    {
      this.setData({
        url:url,
        name:url.name,
        chosenCategory:url.Mtype,
        chosenDetail:url.Dtype,
        imgPath:"http://43.138.127.14:8000/media/images/"+url.pictureUrl,
        detail:this.data.detail,
      })
    }
    this.setData({
      add:options.add
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
          imgPath:res.tempFiles[0].tempFilePath,
          imgChange:true
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
            method: 'POST',
            url: 'http://43.138.127.14:8000/api/closet/delete_clothes',
            header: {
              'Content-Type': 'application/json' ,
              'Authorization':app.globalData.jwt
            },
            data:{
              'id':that.data.url.id
            },
            success:function(res){
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
    e.detail.value.clothes_main_type = this.data.chosenCategory
    e.detail.value.clothes_detail_type = this.data.chosenDetail
    console.log(e.detail.value)
    if(this.data.imgPath=='')
    {
      wx.showModal({
        title: '参数错误',
        content: '您没有上传衣服图片',
      })
      return
    }
    // 更新后端
    if(this.data.add==1)
    {// 新增衣服
      wx.uploadFile({
        filePath: this.data.imgPath,
        name: 'file',
        url: 'http://43.138.127.14:8000/api/closet/add_clothes',
        header: {
          'Content-Type': 'application/x-www-form-urlencoded' ,
          'Authorization':app.globalData.jwt
        },
        formData:e.detail.value,
        success:function(res){
          wx.navigateBack({
            delta:1,
          })
        }
      })
    }
    else
    {// 编辑衣服
      if(this.data.imgChange)
      {
        wx.uploadFile({
          filePath: that.data.imgPath,
          name: 'file',
          url: `http://43.138.127.14:8000/api/closet/edit_clothes/${that.data.url.id}`,
          header: {
            'Content-Type': 'application/x-www-form-urlencoded' ,
            'Authorization':app.globalData.jwt
          },
          formData:e.detail.value,
          success:function(res){
            console.log(res)
            wx.navigateBack({
              delta:1,
            })
          },
          fail:function(res){
            console.log(res)
          }
        })
      }
      else
      {
        wx.request({
          url:`http://43.138.127.14:8000/api/closet/edit_clothes/${this.data.url.id}`,
          header: {
            'Content-Type': 'application/x-www-form-urlencoded' ,
            'Authorization':app.globalData.jwt
          },
          method:'POST',
          data:e.detail.value,
          success:function(res){
            console.log(res)
            wx.navigateBack({
              delta:1,
            })
          }
        })
      }
    }
    
  },
  nameChange:function(e){
    this.setData({
      name:e.detail.value
    })
  }
})