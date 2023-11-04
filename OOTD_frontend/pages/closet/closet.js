Page({
  data: {
      navLeftItems: ["上衣","裤子","连衣裙","外套","半身裙","帽子","鞋子"],
      navRightItems: [
        ["短袖1","短袖2","卫衣1","卫衣2","长袖1","长袖2","长袖3","长袖4","长袖5","长袖6","长袖7","长袖8","长袖9","长袖10","长袖11","长袖12"],
        ["牛仔裤","运动裤","短裙",]
      ],
      outfitItems: ["搭配1","搭配2","搭配3","搭配4","搭配5"],
      curIndex: 0,
      weatherChar: "晴",
      weatherCode:100,
      temprature:15,
      score:0
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
  }

})