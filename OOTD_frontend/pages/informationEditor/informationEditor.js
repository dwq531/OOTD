// informationEditor.js
const app = getApp()
Page({
  data:{
    url:"",
    index:"",
    gender:"请选择",//gender
    category: ["男","女"],
    avatarUrl:"",
    nickname:"",
    phone:"",
    addr:"",
    age:"",
    avatarUrl_changed:false,
  },
  // 页面加载时执行的函数
  onLoad: function (options) {
    this.getUserInfo();
    //console.log("phone: "+ this.data.nickname);
    //console.log("nickname:",this.data.nickname);
  },
  pickerChange: function(e) {
    this.setData({
     gender:this.data.category[e.detail.value],
    })
  },
  getUserInfo: function () {
    // 在这里调用后端 API 获取用户信息
    wx.request({
      method: 'GET',
      url: 'http://43.138.127.14:8000/api/user/user',
      header: {
        'Authorization': app.globalData.jwt, // 添加 JWT Token
      },
      success: (res) => {
        if (res.statusCode === 200) {
          // 更新页面数据，显示用户信息
          this.setData({
            avatarUrl:res.data.avatarUrl,
            nickname:res.data.nickname,
            phone:res.data.phone,
            addr:res.data.addr,
            age:res.data.age,
             gender:res.data.gender,
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
          avatarUrl:res.tempFiles[0].tempFilePath,
          avatarUrl_changed:true,
        })
      }
    })
  },
  onNicknameChange: function(e){
    this.setData({
      nickname: e.detail.value,
    });
    //console.log("nickname: ",this.data.nickname);
  },
  onPhoneChange: function(e){
    this.setData({
      phone: e.detail.value,
    });
  },
  onAddrChange: function(e){
    this.setData({
      addr: e.detail.value,
    });
    //console.log("addr: ",this.data.addr);
  },
  onAgeChange: function(e){
    this.setData({
      age: e.detail.value,
    });
  },

  // 保存按钮点击事件处理函数
  saveUserInfo: function () {
    // 获取输入框的值
    const nickname = this.data.nickname;
    const phone = this.data.phone;
    const addr = this.data.addr;
    var avatarUrl = "";
    const age = this.data.age;
  
    // 定义上传头像的 Promise
    const uploadAvatar = new Promise((resolve, reject) => {
      if (this.data.avatarUrl_changed==true) {
        avatarUrl = this.data.avatarUrl;
        wx.uploadFile({
          url: 'http://43.138.127.14:8000/api/user/avatar', // 上传接口地址
          filePath: avatarUrl, // 要上传的文件路径
          name: 'file', // 后端接收文件的字段名
          header: {
            'Content-Type': 'application/json',
            'Authorization': app.globalData.jwt, // 添加 JWT Token
          },
          success: (res) => {
            // 上传成功的处理逻辑
            console.log(res.data);
            resolve();
          },
          fail: (res) => {
            // 上传失败的处理逻辑
            console.error(res);
            reject(res);
          }
        });
      } else {
        // 如果头像没有改变，直接 resolve
        resolve();
      }
    });
  
    // 上传头像完成后，保存用户信息
    uploadAvatar.then(() => {
      // 请求保存用户信息
      return new Promise((resolve, reject) => {
        wx.request({
          method: 'PATCH', // 假设这里是用 POST 请求保存数据
          url: 'http://43.138.127.14:8000/api/user/edit_info',
          header: {
            'Content-Type': 'application/json',
            'Authorization': app.globalData.jwt, // 添加 JWT Token
          },
          data: {
            nickname: nickname,
            phone: phone,
            addr:addr,
            age:age,
          },
          success: (res) => {
            if (res.statusCode === 200) {
              console.log('用户信息保存成功');
              // 这里可以根据后端返回的数据进行相应的处理
              resolve();
            } else {
              console.error('保存用户信息失败:', res.data);
              reject(res);
            }
          },
          fail: (err) => {
            console.error('请求保存用户信息失败:', err);
            reject(err);
          }
        });
      });
    }).then(() => {
      // 保存用户信息完成后，返回上一页
      wx.navigateBack({ delta: 1 });
    }).catch((error) => {
      // 处理错误
      console.error('保存用户信息发生错误:', error);
    });
  },
});
