// informationEditor.js
const app = getApp()
Page({
  data:{
    url:'',
    index:'',
    chosenCategory:"请选择",
    category: ["男","女","其他"],
    imgPath:'',
    userInfo:{}
  },
  // 页面加载时执行的函数
  onLoad: function (options) {
    this.getUserInfo();
    this.setData({
      url:options.url,
      index:options.url,
    })
  },
  pickerChange: function(e) {
    this.setData({
      chosenCategory:this.data.category[e.detail.value]
    })
  },
  getUserInfo: function () {
    // 在这里调用后端 API 获取用户信息
    wx.request({
      method: 'GET',
      url: 'https://127.0.0.1:8000/api/user/user',
      header: {
        'Authorization': 'jwt ' + wx.getStorageSync('jwt'), // 添加 JWT Token
      },
      success: (res) => {
        if (res.statusCode === 200) {
          // 更新页面数据，显示用户信息
          this.setData({
            userInfo: res.data,
          });
        } else {
          // 处理请求失败的情况
          console.error('Failed to get user info:', res.data);
        }
      },
      fail: (err) => {
        // 处理请求失败的情况
        console.error('Failed to request user info:', err);
      }
    });
  },
  uploadImg: function(e) {
    // 将 this 存储在 that 变量中，以确保在回调函数中能够访问到正确的上下文
    const that=this;
     // 调用小程序的 chooseMedia 方法，让用户选择媒体文件（这里设置只能选择图片）
    wx.chooseMedia({
      count:1,// 允许选择的文件数量，设置为 1
      mediaType:['image'],// 允许选择的媒体文件类型，设置为图片
      sourceType:['album','camera'],// 允许选择的来源，设置为相册和相机
      sizeType:['original','compressed'],// 允许选择的图片尺寸类型，设置为原图和压缩图
      camera:'back',// 当 sourceType 包含 camera 时，指定使用后置摄像头
      success(res){
        // chooseMedia 成功后的回调函数
        // 通过 setData 更新数据，将选择的图片路径存储在 imgPath 变量中
        that.setData({
          imgPath:res.tempFiles[0].tempFilePath
        })
      }
    })
  },
});
