# project208
# 接口文档
#### 除了登陆授权获取基本信息其他路由带上请求头
Authorization: Bearer
###
## 授权登陆
#### URL：/api/user/token
### POST
```
{
    "code":"CODE"
}
```
#### RETURN
```
{
    "status":-102, //code无效或过期
    "message":"CODE无效！"
}
{
    "status":-101, //缺少code
    "message":"用户登录需要凭证"
}
{
    "status":1,
    "message":"成功！"，
    "data":{
        "token":TOKEN
    }
}

```

## 获取用户基本信息
#### URL /api/user/data
### GET
##### request header 
Authorization: Bearer
### RETURN
```angular2
{
    "status":1,
    "message":"获取成功！",
    "data":{
        "id": 1314  //用户id
        'id': user.id,  //用户id(不是openid)
        'nickname': nickname,  //昵称
        'gender': gender,  // 1为男性，2为女性，0为未知
        'icon_url': icon_url,  // 用户头像URL,具体见微信官方文档
        'registration_time': //注册时间
    }
}
```

## 获取单个题目
#### URL /api/question?id=ID
### GET
##### request header 
Authorization: Bearer
### return
```angular2
{
    "status":1,
    "message":"获取成功！",
    "data":{
        "id": 1,  //题目id
        'subject': what,  // 题目问题
        'option_A': option_A,  // A选项内容
        'option_B': option_B,  // B选项内容
        'option_C': option_C,  // C选项内容
        'option_D': option_D  // D选项内容
        
    }
}
//  缺少id或id部队返回404
```
## 获取有效的题目
#### URL /api/question/valid
### GET
##### request header 
Authorization: Bearer
### return
```angular2

{
    "status":1,
    "message":"获取成功！",
    "data":{
        "total": 5 // 题目总数
        "id":[1,2,3,4,5,] // 列表
        
    }
}
```
## 获取默认（待选择）的留言
#### URL 
### GET /api/question/message
##### request header 
Authorization: Bearer
### return
```angular2

{
    "status":1,
    "message":"获取成功！",
    "data":{
        "total": 3, // 留言总数
        "content":["留言1","留言2","留言3"] // 列表
        
    }
}
```
## 获取我发布的题目
### GET  /api/question/my
##### request header
Authorization: Bearer
### return
```
{
    "status": 1,
    "message": "成功",
    "data": [
        {
            "set_id": 1,  //题组id
            "questions": {
                "1": "B" , //题目id： 设置的答案
                "2": "A"
            },
            "messages": "出题者设置的留言",
            "all_answers": [
                {
                    "answer_man": 1,  //回答者id
                    "answers": {
                        "1": "B", // 题目id, 回答者的答案
                        "2": "B"
                        
                    },
                    "time": "2019-05-11 13:01:06", //回答时间
                    "score": "20" // 分数
                },
                {
                    "answer_man": 2,
                    "answers": {
                        "1": "C"
                    },
                    "time": "2019-05-12 03:16:48",
                    "score": "50"
                }
            ]
        },
        {
            "set_id": 4,
            "questions": {
                "1": "A"
            },
            "messages": "",
            "all_answers": []
        }
    ]
}
```

 ## 出题
 
 ### URL /api/question/my
 ##### request header
Authorization: Bearer
 ### POST 
 ```
 {
    "questions":{
        "1":"B",
        "2":"C"  //题目id： 出题者设置的答案
        ...
    },
    "messages":"出题者设置的留言"
 }

```
### RETURN
```
{
    "status":1,
    "message":"出题成功"
}
```
## 获取我回答的问题
### GET /api/answer/my
##### request header
Authorization: Bearer
### RETURN

```
{
    "status": 1,
    "message": "获取成功",
    "data": [
        {
            "id": 1,  // 回答问题的键
            "user_id": 1,  //出题人id
            "set_id": 1,  // 题组id
            "answers": {
                "1": "B" //答题人的huida
            },
            "messsage": "答题人的留言，如果score超过60就有这一项",
            "create_time": "2019-05-11 13:01:06",
            "score": "80",  
            "real_answer": {
                "1": "A"  //出题人设置的真正答案
            }
        },
        {
            "id": 3,
            "user_id": 2,
            "set_id": 1,
            "answers": {
                "1": "C"
            },
            "messsage": "dsdsads",
            "create_time": "2019-05-12 03:16:48",
            "score": "50",
            "real_answer": {
                "1": "a"
            }
        }
    ]
}

```

## 答题
###　ＵＲＬ　/api/answer/my
##### request header
Authorization: Bearer
### POST
``` 
{
    "set_id":"1"  //题组号
    "answer": {
            "1":"B",  //题目序号：回答的答案
            "2":"A",
            ...
            
    },
    "message":"回答问题的人给出题者的留言"
}
```
### RETURN
```
{
    "status":"1",
    "message":"提交成功"，
    "data":{
        "score":60,
        "message":"出题者的留言，分数高于６０就有此列"
    }
    
}

```