const app = getApp()
Page({
  data: {
      category: ["上衣","下装","鞋子","包","饰品"],
      clothes: [],
      outfitItems: [],
      curIndex: 0, // 选中的类别
      weatherChar: "晴",
      weatherCode:100,
      temprature:15,
      score:0,
      dialogShow:true,
      // 长按拖拽
      movingImg: '',
      movingUrl:"none",
      hidden: true,
      flag: false,
      x: 0,
      y: 0,
      scrollable: true,
      scrollTop:0,

  },
  onShow:function(e){
    const that = this
    wx.request({
      url: 'http://127.0.0.1:8000/api/closet/get_clothes',
      header: {
        'Content-Type': 'application/json' ,
        'Authorization':app.globalData.jwt
      },
      success:function(res){
        console.log(res)
        that.setData({
          clothes:res.data.clothes
        })
      }
    })
    wx.request({
      url: 'http://127.0.0.1:8000/api/closet/get_outfit',
      header: {
        'Content-Type': 'application/json' ,
        'Authorization':app.globalData.jwt
      },
      success:function(res){
        that.setData({
          outfitItems:res.data.clothes
        })
      }
    })
  },

  //事件处理函数
  switchRightTab: function(e) {
      // 获取item项的id，和数组的下标值
      let id = e.target.dataset.id,
          index = parseInt(e.target.dataset.index);
      // 把点击到的某一项，设为当前index
      this.setData({
          curIndex: index
      })
  },
  longtap: function(e){
    const url = e.currentTarget.dataset.url;
    const img = url.pictureUrl
    console.log(url)
    if(img)
    {
      this.setData({
        movingImg: img,
      })
    }
      this.setData({
        x: e.currentTarget.offsetLeft+90,
        y: e.currentTarget.offsetTop+90-this.data.scrollTop,
        hidden: false,
        flag: true,
        scrollable:false,
        movingUrl:url
      })
  },
  touchs: function(e) {
    this.setData({
      beginIndex: e.currentTarget.dataset.index
    })

  },
  touchm: function(e) {
    if (this.data.flag) {
      const x = e.touches[0].pageX
      const y = e.touches[0].pageY
      this.setData({
        x: x-40,
        y: y-150
      })
    }
  },
  touchend: function(e){
    const that = this
    const x = e.changedTouches[0].pageX
    const y = e.changedTouches[0].pageY
    //console.log(x,y)
    this.setData({
      scrollable:true,
      hidden:true
    })
    const query = wx.createSelectorQuery().in(this);
    query.select('.outfit').boundingClientRect(rect=>{
      if(x>rect.left && x<rect.right && y>rect.top && y<rect.bottom)
      {
        //console.log("add")
        var new_outfit = this.data.movingUrl;
        var flag=false;
        // 连接后端
        wx.request({
          url: 'http://127.0.0.1:8000/api/closet/add_outfit',
          method:'POST',
          header: {
            'Content-Type': 'application/json' ,
            'Authorization':app.globalData.jwt
          },
          data:{
            "id":this.data.movingUrl.id
          },
          success:function(res){
            console.log(res)
            that.setData({
              outfitItems:res.data.clothes
            })
          }
        })
        /*
        for(var i=0;i<this.data.outfitItems.length;i++)
        {
          if(this.data.outfitItems[i].Mtype == new_outfit.Mtype)
          {
            // 相同类别进行替换
            this.data.outfitItems[i] = new_outfit;
            flag=true;
            break;
          }
        }
        if(!flag)
          this.data.outfitItems.push(new_outfit);
        */
        this.setData({
          outfitItems:this.data.outfitItems
        })
        
      }
    }).exec();

  },
  onScrolly: function(e){
    const d = e.detail.scrollTop
    this.setData({
      scrollTop:d
    })
  },
  deleteOutfit:function(e){
    const url = e.currentTarget.dataset.url;
    const that = this
    wx.request({
      url: 'http://127.0.0.1:8000/api/closet/remove_outfit',
      method:'POST',
      header: {
        'Content-Type': 'application/json' ,
        'Authorization':app.globalData.jwt
      },
      data:{
        "id":url.id
      },
      success:function(res){
        that.setData({
          outfitItems:res.data.clothes
        })
      }
    })
  },
  shorttap: function(e) {
    const url = e.currentTarget.dataset.url;
    wx.navigateTo({
      url:"/pages/editClothes/editClothes?url="+JSON.stringify(url)+"&add=0",
    })
  },
  addClothes: function(e){
    wx.navigateTo({
      url:"/pages/editClothes/editClothes?url=0&add=1",
    })
  },
  evaluate:function(e){
    //wx.request
    this.setData({
      dialogShow:false
    })
  },
  changeOutfit:function(e){
    this.setData({
      dialogShow:true
    })
  },
  cancel:function(e){
    this.setData({
      dialogShow:true
    })
  }
})