Page({
  data: {
      category: ["上衣","下装","连衣裙","外套","帽子","鞋子"],
      clothes: [
        ["短袖1","短袖2","卫衣1","卫衣2","长袖1","长袖2","长袖3","长袖4","长袖5","长袖6","长袖7","长袖8","长袖9","长袖10","长袖11","长袖12"],
        ["牛仔裤","运动裤","短裙",]
      ],
      outfitItems: [
        {"name":"搭配1","category":1},
        {"name":"搭配2","category":2},
        {"name":"搭配3","category":3},
        {"name":"搭配4","category":4},],
      curIndex: 0, // 选中的类别
      weatherChar: "晴",
      weatherCode:100,
      temprature:15,
      score:0,
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
  onLoad: function() {
      // 加载的使用进行网络访问，把需要的数据设置到data数据对象
      var that = this        
      wx.request({
          url: '',
          method: 'GET',
          data: {},
          header: {
              'Accept': 'application/json'
          },
          success: function(res) {
              console.log(res)
              that.setData({
                  navLeftItems: res.data,
                  navRightItems: res.data
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
  _longtap: function(e){
    const img = e.currentTarget.dataset.img;
    const url = e.currentTarget.dataset.url;
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
        var new_outfit = {'name':this.data.movingUrl,'category':this.data.curIndex};
        var flag=false;
        for(var i=0;i<this.data.outfitItems.length;i++)
        {
          if(this.data.outfitItems[i].category == new_outfit.category)
          {
            // 相同类别进行替换
            this.data.outfitItems[i] = new_outfit;
            flag=true;
            break;
          }
        }
        if(!flag)
          this.data.outfitItems.push(new_outfit);
        this.setData({
          outfitItems:this.data.outfitItems
        })
        //console.log(new_outfit);
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
    const index = e.currentTarget.dataset.id;
    this.data.outfitItems.splice(index,1);
    this.setData({
      outfitItems:this.data.outfitItems
    })
  }
})