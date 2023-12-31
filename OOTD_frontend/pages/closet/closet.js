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
      score:-1,
      dialogShow:true,
      // 长按拖拽
      movingImg: '',
      movingUrl:null,
      hidden: true,
      flag: false,
      x: 0,
      y: 0,
      scrollable: true,
      scrollTop:0,
      replace_clothes:[],
      best_score:0
  },

  onShow: function () {
    // 页面加载时的初始化操作，可以在这里处理数据加载等任务
    // console.log("页面加载完成");
    // console.log("nickname:",this.data.nickname);
    const that = this
    wx.request({
      url: 'http://43.138.127.14:8000/api/closet/get_clothes',
      header: {
        'Content-Type': 'application/json' ,
        'Authorization':app.globalData.jwt
      },
      success:function(res){
        //console.log(res)
        that.setData({
          clothes:res.data.clothes
        })
      }
    })
    wx.request({
      url: 'http://43.138.127.14:8000/api/closet/get_outfit',
      header: {
        'Content-Type': 'application/json' ,
        'Authorization':app.globalData.jwt
      },
      success:function(res){
        //console.log(res.data)
        that.setData({
          outfitItems:res.data.clothes,
          score:res.data.rate
        })
      }
    })
    wx.request({
      method: 'GET',
      url: 'http://43.138.127.14:8000/api/user/weather',
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
    //console.log(url)
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
      console.log(this.data.movingUrl)
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
    that.setData({
      scrollable:true,
      hidden:true
    })
    if(this.data.movingUrl==null)return
    const query = wx.createSelectorQuery().in(that);
    query.select('.outfit').boundingClientRect(rect=>{
      if(x>rect.left && x<rect.right && y>rect.top && y<rect.bottom)
      { 
        // console.log("add")
        // console.log("print:", that.data.movingUrl);
        var new_outfit = that.data.movingUrl;
        var flag=false;
        // 连接后端
        wx.request({
          url: 'http://43.138.127.14:8000/api/closet/add_outfit',
          method:'POST',
          header: {
            'Content-Type': 'application/json' ,
            'Authorization':app.globalData.jwt
          },
          data:{
            "id":that.data.movingUrl.id
          },
          success:function(res){
            //console.log(res)
            that.setData({
              outfitItems:res.data.clothes,
              score:0
            })
          }
        })
        this.setData({
          outfitItems:that.data.outfitItems,
          movingUrl:null
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
      url: 'http://43.138.127.14:8000/api/closet/remove_outfit',
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
          outfitItems:res.data.clothes,
          score:0
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
    const that = this
    wx.showLoading({
      title: '评分中',
    })
    wx.request({
      url: 'http://43.138.127.14:8000/api/closet/score',
      method:'POST',
      header: {
        'Content-Type': 'application/json' ,
        'Authorization':app.globalData.jwt
      },
      success:function(res){
        //console.log(res.data)
        wx.hideLoading()
        if(res.statusCode == 200)
        {
          if(res.data.have_better)
          {
            that.setData({
              dialogShow:false,
              replace_clothes:res.data.replace,
              best_score:res.data.best_score
            })
          }
          that.setData({
            score:res.data.rate
          })
        }
        else
        {
          wx.showModal({
            title: '错误',
            content: '穿搭至少包含1件上衣和1件下装',
          })
        }
        
      },
      fail:function(e){
        wx.hideLoading()
      }
    })
    
  },
  changeOutfit:function(e){
    const that = this
    wx.request({
      url: 'http://43.138.127.14:8000/api/closet/replace',
      method:'POST',
      header: {
        'Content-Type': 'application/json' ,
        'Authorization':app.globalData.jwt
      },
      success:function(res){
        console.log(res.data)
        that.setData({
          outfitItems:res.data.clothes,
          score:res.data.rate
        })
      }
    })
    this.setData({
      dialogShow:true
    })
  },
  cancel:function(e){
    this.setData({
      dialogShow:true
    })
  },
  recommend:function(e){
    const that = this
    wx.showLoading({
      title: '生成中',
    })
    wx.request({
      url: 'http://43.138.127.14:8000/api/closet/generate',
      method:'POST',
      header: {
        'Content-Type': 'application/json' ,
        'Authorization':app.globalData.jwt
      },
      success:function(res){
        //console.log(res.data)
        wx.hideLoading()
        if(res.statusCode==200)
        {
          that.setData({
            outfitItems:res.data.clothes,
            score:res.data.rate
          })
        }
        else
        {
          wx.showModal({
            title: '错误',
            content: '衣柜中当季衣服太少，无法给出搭配推荐',
          })
        }
      },
      fail:function(e){
        wx.hideLoading()
      }
    })
  }
})