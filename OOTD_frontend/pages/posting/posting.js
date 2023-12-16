const app = getApp()
Page({
  data: {
    weatherCode: 100,
    weatherChar: "晴",
    temprature: 18,
    score: 98,
    outfitItems: [
      { "name": "搭配1", "category": 1 },
      { "name": "搭配2", "category": 2 },
      { "name": "搭配3", "category": 3 },
      { "name": "搭配4", "category": 4 },],
    images: [
      "/static/default/noimage.png",
      "/static/default/noimage.png",
      "/static/default/noimage.png",
      "/static/default/noimage.png"
    ],
    title: '',
    content: ''
  },
  addImage: function (e) {
    const that = this
    wx.chooseMedia({
      count: 9 - that.data.images.length,
      mediaType: ['image'],
      sourceType: ['album', 'camera'],
      sizeType: ['original', 'compressed'],
      camera: 'back',
      success(res) {
        for (let i = 0; i < res.tempFiles.length; i++)
          that.data.images.push(res.tempFiles[i].tempFilePath)
        that.setData({
          images: that.data.images
        })
      }
    })
  },
  deleteImage: function (e) {
    const index = e.currentTarget.dataset.id;
    this.data.images.splice(index, 1);
    this.setData({
      images: this.data.images
    })
  },
  titleChange: function (e) {
    this.setData({
      title: e.detail.value
    })
  },
  contentChange: function (e) {
    this.setData({
      content: e.detail.value
    })
  },
  send: function (e) {
    console.log(e.detail.value)
    const formData = e.detail.value;
    wx.request({
      url: 'http://127.0.0.1:8000/api/posting/create_post/',
      method: 'POST',
      header: {
        'Content-Type':'application/x-www-form-urlencoded',
        'Authorization': app.globalData.jwt
      },
      data: formData,
      success: (res) => {
        console.log(res)
        const postId = res.data.id;  // 获取新创建的帖子的ID
        this.data.images.forEach((image, index) => {
          wx.uploadFile({
            filePath: image,
            name: `image`,
            url: `http://127.0.0.1:8000/api/posting/upload_image/${postId}/`,  // 使用新的URL，包含帖子的ID
            header: {
              'Authorization': app.globalData.jwt,
            },
            success: function (res) {
              console.log(res)
            }
          })
        });
      }
    })
  }
})
